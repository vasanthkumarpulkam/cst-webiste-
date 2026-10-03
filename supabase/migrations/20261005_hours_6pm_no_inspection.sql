-- Owner corrections: the shop closes at 6 PM, and does not offer state inspections.

create or replace function public.book_appointment(
  p_service text, p_date date, p_time text, p_name text, p_phone text, p_email text,
  p_year int, p_make text, p_model text, p_notes text
) returns table(ref text, start_at timestamptz, end_at timestamptz)
language plpgsql security definer set search_path = ''
as $$
declare
  dur int; mins int; s timestamptz; e timestamptz; r text; today date;
begin
  if p_service not in ('Brake service','Computer diagnostics','Electrical','Oil change','Transmission',
      'A/C and heating','Tires and alignment','Fleet maintenance','Not sure, need it looked at') then
    raise exception 'invalid_service'; end if;
  dur := case when p_service = 'Oil change' then 30 else 60 end;
  if p_time !~ '^\d{2}:\d{2}$' then raise exception 'invalid_time'; end if;
  mins := split_part(p_time, ':', 1)::int * 60 + split_part(p_time, ':', 2)::int;
  if mins % dur <> 0 or mins < 540 or mins + dur > 1080 then raise exception 'invalid_time'; end if;
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

create or replace function public.admin_book(
  p_service text, p_date date, p_time text, p_name text, p_phone text, p_email text,
  p_year int, p_make text, p_model text, p_notes text, p_source text
) returns table(ref text, start_at timestamptz, end_at timestamptz)
language plpgsql security definer set search_path = ''
as $$
declare
  dur int; mins int; s timestamptz; e timestamptz; r text; today date;
begin
  if not public.is_admin() then raise exception 'not_allowed'; end if;
  if p_source not in ('phone','walk-in') then raise exception 'invalid_source'; end if;
  if p_service not in ('Brake service','Computer diagnostics','Electrical','Oil change','Transmission',
      'A/C and heating','Tires and alignment','Fleet maintenance','Not sure, need it looked at') then
    raise exception 'invalid_service'; end if;
  if char_length(btrim(coalesce(p_name,''))) < 2 then raise exception 'invalid_name'; end if;
  if char_length(regexp_replace(coalesce(p_phone,''), '\D', '', 'g')) < 10 then raise exception 'invalid_phone'; end if;
  dur := case when p_service = 'Oil change' then 30 else 60 end;
  if p_time !~ '^\d{2}:\d{2}$' then raise exception 'invalid_time'; end if;
  mins := split_part(p_time, ':', 1)::int * 60 + split_part(p_time, ':', 2)::int;
  if mins % 30 <> 0 or mins < 540 or mins + dur > 1080 then raise exception 'invalid_time'; end if;
  today := (now() at time zone 'America/Chicago')::date;
  if extract(isodow from p_date) > 5 or p_date < today or p_date > today + 120 then raise exception 'invalid_date'; end if;
  s := (p_date + (p_time::time)) at time zone 'America/Chicago';
  e := s + make_interval(mins => dur);
  if exists (select 1 from public.blocks b where tstzrange(b.start_at, b.end_at) && tstzrange(s, e)) then
    raise exception 'slot_taken'; end if;
  r := 'CST-' || to_char(p_date, 'MMDD') || '-' || upper(substr(md5(random()::text || clock_timestamp()::text), 1, 4));
  begin
    insert into public.appointments (ref, service, start_at, end_at, customer_name, phone, email,
        vehicle_year, vehicle_make, vehicle_model, notes, source)
      values (r, p_service, s, e, btrim(p_name), btrim(p_phone), nullif(btrim(coalesce(p_email,'')), ''),
        p_year, btrim(p_make), btrim(p_model), nullif(btrim(coalesce(p_notes,'')), ''), p_source);
  exception when exclusion_violation then raise exception 'slot_taken';
  end;
  return query select r, s, e;
end $$;
revoke all on function public.admin_book(text,date,text,text,text,text,int,text,text,text,text) from public, anon;
grant execute on function public.admin_book(text,date,text,text,text,text,int,text,text,text,text) to authenticated;
