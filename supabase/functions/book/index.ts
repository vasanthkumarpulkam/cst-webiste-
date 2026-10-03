// Public booking endpoint: validates, books the slot in the database, then sends
// confirmations. Email (Resend) and SMS (Twilio) are optional and only run when their
// secrets are set; a notification failure never undoes a booking.
//
// Secrets (Supabase dashboard > Edge Functions > Secrets):
//   RESEND_API_KEY      enables email
//   FROM_EMAIL          e.g. "CST Automotive <bookings@yourdomain.com>" (needs a verified domain in Resend)
//   SHOP_EMAIL          where the shop is notified (default cstautomotive@yahoo.com)
//   TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM   enable SMS to the customer
//   SHOP_SMS_TO         optional: shop phone to text on each booking
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY");
const FROM_EMAIL = Deno.env.get("FROM_EMAIL") ?? "CST Automotive <onboarding@resend.dev>";
const SHOP_EMAIL = Deno.env.get("SHOP_EMAIL") ?? "cstautomotive@yahoo.com";
const TWILIO_SID = Deno.env.get("TWILIO_ACCOUNT_SID");
const TWILIO_TOKEN = Deno.env.get("TWILIO_AUTH_TOKEN");
const TWILIO_FROM = Deno.env.get("TWILIO_FROM");
const SHOP_SMS_TO = Deno.env.get("SHOP_SMS_TO");

const SHOP_PHONE = "(214) 256-6347";
const SHOP_ADDRESS = "2557 Glenda Ln #1&2, Dallas, TX 75229";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });

const esc = (s: string) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const ERRORS: Record<string, [number, string]> = {
  slot_taken: [409, "That time was just taken. Please pick another time."],
  too_many: [429, "This phone number already has 3 upcoming appointments. Please call the shop."],
  invalid_service: [400, "Please choose a service."],
  invalid_time: [400, "That time is not available."],
  invalid_date: [400, "The shop is open Monday to Friday. Please pick a weekday within the next 60 days."],
};

const fmtDate = (iso: string) =>
  new Intl.DateTimeFormat("en-US", { timeZone: "America/Chicago", weekday: "long", month: "long", day: "numeric", year: "numeric" }).format(new Date(iso));
const fmtTime = (iso: string) =>
  new Intl.DateTimeFormat("en-US", { timeZone: "America/Chicago", hour: "numeric", minute: "2-digit" }).format(new Date(iso));

async function sendEmail(to: string, subject: string, text: string, html: string): Promise<boolean> {
  if (!RESEND_API_KEY) return false;
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from: FROM_EMAIL, to: [to], subject, text, html }),
    });
    if (!r.ok) console.error("resend", r.status, await r.text());
    return r.ok;
  } catch (e) {
    console.error("resend", e);
    return false;
  }
}

async function sendSms(to: string, body: string): Promise<boolean> {
  if (!TWILIO_SID || !TWILIO_TOKEN || !TWILIO_FROM) return false;
  const digits = to.replace(/\D/g, "");
  const e164 = digits.length === 10 ? `+1${digits}` : digits.length === 11 && digits[0] === "1" ? `+${digits}` : null;
  if (!e164) return false;
  try {
    const r = await fetch(`https://api.twilio.com/2010-04-01/Accounts/${TWILIO_SID}/Messages.json`, {
      method: "POST",
      headers: { Authorization: "Basic " + btoa(`${TWILIO_SID}:${TWILIO_TOKEN}`), "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ To: e164, From: TWILIO_FROM, Body: body }),
    });
    if (!r.ok) console.error("twilio", r.status, await r.text());
    return r.ok;
  } catch (e) {
    console.error("twilio", e);
    return false;
  }
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
  if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);

  let b: Record<string, unknown>;
  try {
    b = await req.json();
  } catch {
    return json({ error: "Invalid request." }, 400);
  }
  const str = (k: string, max: number) => String(b[k] ?? "").trim().slice(0, max);

  // Honeypot: real visitors never fill this hidden field. Pretend success to bots.
  if (str("website", 100)) return json({ ok: true, ref: "CST-0000-XXXX" });

  const service = str("service", 60), date = str("date", 10), time = str("time", 5);
  const name = str("name", 100), phone = str("phone", 20), email = str("email", 200);
  const make = str("make", 50), model = str("model", 50), notes = str("notes", 1000);
  const year = parseInt(str("year", 4), 10);

  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^\d{2}:\d{2}$/.test(time)) return json({ error: "Please pick a day and time." }, 400);
  if (name.length < 2) return json({ error: "Please enter your name." }, 400);
  if (phone.replace(/\D/g, "").length < 10) return json({ error: "Please enter a 10-digit phone number." }, 400);
  if (email && !/^\S+@\S+\.\S+$/.test(email)) return json({ error: "Please check the email address." }, 400);
  if (!year || year < 1950 || year > new Date().getFullYear() + 1) return json({ error: "Please enter the vehicle year." }, 400);
  if (!make || !model) return json({ error: "Please enter the vehicle make and model." }, 400);

  const rpc = await fetch(`${SUPABASE_URL}/rest/v1/rpc/book_appointment`, {
    method: "POST",
    headers: { apikey: SERVICE_KEY, Authorization: `Bearer ${SERVICE_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      p_service: service, p_date: date, p_time: time, p_name: name, p_phone: phone, p_email: email,
      p_year: year, p_make: make, p_model: model, p_notes: notes,
    }),
  });
  const out = await rpc.json().catch(() => null);
  if (!rpc.ok) {
    const known = ERRORS[String(out?.message ?? "")];
    if (known) return json({ error: known[1], code: out.message }, known[0]);
    console.error("book_appointment", rpc.status, JSON.stringify(out));
    return json({ error: "Something went wrong. Please call the shop at " + SHOP_PHONE + "." }, 500);
  }
  const row = Array.isArray(out) ? out[0] : out;
  const when = `${fmtDate(row.start_at)} at ${fmtTime(row.start_at)}`;

  const details = [
    `Reference: ${row.ref}`, `When: ${when}`, `Service: ${service}`, `Vehicle: ${year} ${make} ${model}`,
    `Name: ${name}`, `Phone: ${phone}`, ...(email ? [`Email: ${email}`] : []), ...(notes ? [`Notes: ${notes}`] : []),
  ];
  const rows = details.map((l) => {
    const i = l.indexOf(": ");
    return `<tr><td style="padding:4px 14px 4px 0;color:#51616E">${esc(l.slice(0, i))}</td><td style="padding:4px 0"><b>${esc(l.slice(i + 2))}</b></td></tr>`;
  }).join("");

  const shopMail = sendEmail(
    SHOP_EMAIL,
    `New appointment ${row.ref}: ${service}, ${year} ${make} ${model}`,
    `New appointment booked online\n\n${details.join("\n")}`,
    `<div style="font-family:Arial,sans-serif;color:#0E1B26"><h2>New appointment booked online</h2><table>${rows}</table></div>`,
  );
  const custMail = email
    ? sendEmail(
      email,
      `Your CST Automotive appointment is booked: ${when}`,
      `Hi ${name},\n\nYour appointment is booked.\n\n${details.filter((d) => !d.startsWith("Name:") && !d.startsWith("Phone:") && !d.startsWith("Email:")).join("\n")}\n\nWhere: ${SHOP_ADDRESS}\nQuestions or need to change it? Call ${SHOP_PHONE}. Walk-ins are always welcome.\n\nCST Automotive`,
      `<div style="font-family:Arial,sans-serif;color:#0E1B26"><h2>Your appointment is booked</h2><p>Hi ${esc(name)}, we have you down for <b>${esc(when)}</b>.</p><table>${rows}</table><p>${esc(SHOP_ADDRESS)}<br>Questions or need to change it? Call <a href="tel:+12142566347">${SHOP_PHONE}</a>. Walk-ins are always welcome.</p><p>CST Automotive</p></div>`,
    )
    : Promise.resolve(false);
  const custSms = sendSms(phone, `CST Automotive: you're booked for ${when} (${service}). Ref ${row.ref}. Call ${SHOP_PHONE} to change it.`);
  const shopSms = SHOP_SMS_TO
    ? sendSms(SHOP_SMS_TO, `New booking ${row.ref}: ${service}, ${year} ${make} ${model}, ${when}. ${name} ${phone}`)
    : Promise.resolve(false);

  const [shopEmailSent, customerEmailSent, customerSmsSent] = await Promise.all([shopMail, custMail, custSms, shopSms]);

  return json({
    ok: true, ref: row.ref, when, service, vehicle: `${year} ${make} ${model}`,
    shopEmailSent, customerEmailSent, customerSmsSent,
  });
});
