-- Appointments, shop-blocked times, admin list, and the functions the website uses.
-- One bay: only one confirmed appointment or block can occupy any moment.

create table public.appointments (
  id uuid primary key default gen_random_uuid(),
  ref text not null unique,
  service text not null,
  start_at timestamptz not null,
  end_at timestamptz not null,
  customer_name text not null check (char_length(customer_name) between 2 and 100),
  phone text not null check (char_length(phone) between 10 and 20),
  email text check (email is null or char_length(email) <= 200),
  vehicle_year int not null check (vehicle_year between 1950 and 2100),
  vehicle_make text not null check (char_length(vehicle_make) between 1 and 50),
  vehicle_model text not null check (char_length(vehicle_model) between 1 and 50),
  notes text check (notes is null or char_length(notes) <= 1000),
  status text not null default 'confirmed' check (status in ('confirmed','cancelled')),
  created_at timestamptz not null default now(),
  check (end_at > start_at),
  constraint appointments_no_overlap
    exclude using gist (tstzrange(start_at, end_at) with &&) where (status = 'confirmed')
);

create table public.blocks (
  id uuid primary key default gen_random_uuid(),
  start_at timestamptz not null,
  end_at timestamptz not null,
  reason text check (reason is null or char_length(reason) <= 200),
  created_at timestamptz not null default now(),
  check (end_at > start_at)
);

create table public.shop_admins (email text primary key);

alter table public.appointments enable row level security;
alter table public.blocks enable row level security;
alter table public.shop_admins enable row level security;

revoke all on public.appointments, public.blocks, public.shop_admins from anon, authenticated;

create function public.is_admin() returns boolean
language sql stable security definer set search_path = ''
as $$ select exists (select 1 from public.shop_admins where lower(email) = lower(coalesce(auth.jwt() ->> 'email', ''))) $$;
revoke all on function public.is_admin() from public, anon;
grant execute on function public.is_admin() to authenticated;

grant select, update on public.appointments to authenticated;
grant select, insert, update, delete on public.blocks to authenticated;

create policy admin_read_appointments on public.appointments for select to authenticated using (public.is_admin());
create policy admin_update_appointments on public.appointments for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy admin_all_blocks on public.blocks for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- Public: which minutes of each day (shop time) are taken. No customer data.
create function public.get_busy(p_from date, p_to date)
returns table(day date, start_min int, end_min int)
language sql stable security definer set search_path = ''
as $$
  with iv as (
    select (start_at at time zone 'America/Chicago') s, (end_at at time zone 'America/Chicago') e
      from public.appointments where status = 'confirmed' and end_at > now() - interval '1 day'
    union all
    select (start_at at time zone 'America/Chicago'), (end_at at time zone 'America/Chicago')
      from public.blocks where end_at > now() - interval '1 day'
  )
  select d::date,
         greatest(0, floor(extract(epoch from (greatest(iv.s, d) - d)) / 60))::int,
         least(1440, ceil(extract(epoch from (least(iv.e, d + interval '1 day') - d)) / 60))::int
    from iv,
         lateral generate_series(date_trunc('day', iv.s), date_trunc('day', iv.e - interval '1 second'), interval '1 day') d
   where p_to - p_from <= 90 and d::date between p_from and p_to
$$;
revoke all on function public.get_busy(date, date) from public;
grant execute on function public.get_busy(date, date) to anon, authenticated;

-- Called only by the booking edge function (service role). Validates everything server-side.
create function public.book_appointment(
  p_service text, p_date date, p_time text, p_name text, p_phone text, p_email text,
  p_year int, p_make text, p_model text, p_notes text
) returns table(ref text, start_at timestamptz, end_at timestamptz)
language plpgsql security definer set search_path = ''
as $$
declare
  dur int; mins int; s timestamptz; e timestamptz; r text; today date;
begin
  if p_service not in ('Brake service','Computer diagnostics','Electrical','Oil change','Transmission',
      'A/C and heating','Tires and alignment','Inspection','Fleet maintenance','Not sure, need it looked at') then
    raise exception 'invalid_service'; end if;
  dur := case when p_service = 'Oil change' then 30 else 60 end;
  if p_time !~ '^\d{2}:\d{2}$' then raise exception 'invalid_time'; end if;
  mins := split_part(p_time, ':', 1)::int * 60 + split_part(p_time, ':', 2)::int;
  if mins % dur <> 0 or mins < 540 or mins + dur > 1020 then raise exception 'invalid_time'; end if;
  today := (now() at time zone 'America/Chicago')::date;
  if extract(isodow from p_date) > 5 or p_date < today or p_date > today + 60 then raise exception 'invalid_date'; end if;
  s := (p_date + (p_time::time)) at time zone 'America/Chicago';
  e := s + make_interval(mins => dur);
  if s <= now() then raise exception 'invalid_time'; end if;
  if exists (select 1 from public.blocks b where tstzrange(b.start_at, b.end_at) && tstzrange(s, e)) then
    raise exception 'slot_taken'; end if;
  if (select count(*) from public.appointments a
       where a.status = 'confirmed' and a.end_at > now()
         and regexp_replace(a.phone, '\D', '', 'g') = regexp_replace(p_phone, '\D', '', 'g')) >= 3 then
    raise exception 'too_many'; end if;
  r := 'CST-' || to_char(p_date, 'MMDD') || '-' || upper(substr(md5(random()::text || clock_timestamp()::text), 1, 4));
  begin
    insert into public.appointments (ref, service, start_at, end_at, customer_name, phone, email,
        vehicle_year, vehicle_make, vehicle_model, notes)
      values (r, p_service, s, e, btrim(p_name), btrim(p_phone), nullif(btrim(coalesce(p_email,'')), ''),
        p_year, btrim(p_make), btrim(p_model), nullif(btrim(coalesce(p_notes,'')), ''));
  exception when exclusion_violation then raise exception 'slot_taken';
  end;
  return query select r, s, e;
end $$;
revoke all on function public.book_appointment(text,date,text,text,text,text,int,text,text,text) from public, anon, authenticated;
grant execute on function public.book_appointment(text,date,text,text,text,text,int,text,text,text) to service_role;

-- Add the first admin (change this email). More admins: insert more rows.
insert into public.shop_admins (email) values ('pulkamchintu@gmail.com');

-- Shop blocks time in its own (Dallas) clock: a date plus start/end time, or a whole day.
create function public.add_block(p_date date, p_from time, p_to time, p_reason text)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare s timestamptz; e timestamptz; new_id uuid;
begin
  if not public.is_admin() then raise exception 'not_allowed'; end if;
  if p_to <= p_from then raise exception 'invalid_range'; end if;
  s := (p_date + p_from) at time zone 'America/Chicago';
  e := (p_date + p_to) at time zone 'America/Chicago';
  insert into public.blocks (start_at, end_at, reason) values (s, e, nullif(btrim(coalesce(p_reason,'')), ''))
    returning id into new_id;
  return new_id;
end $$;
revoke all on function public.add_block(date, time, time, text) from public, anon;
grant execute on function public.add_block(date, time, time, text) to authenticated;
