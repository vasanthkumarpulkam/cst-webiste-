# Booking system: setup and operations

## How it works
- `booking.html` shows live availability (`get_busy` in Supabase) and books through the `book` edge function.
- Oil changes use **30-minute** slots. Every other service uses **1-hour** slots on the hour. Open Mon to Fri, 9 AM to 5 PM Dallas time, up to 60 days ahead.
- One bay: a booking or block on a moment makes it unavailable to everyone. The database enforces this, so two people can never hold the same time.
- On booking, the function emails the shop and (if an email was given) the customer, and texts the customer when SMS is configured.
- `admin.html` is the shop's schedule: sign in, see upcoming appointments, cancel one, and block off time (lunch, closed days, a parts delivery).

## Supabase project
`cst-automotive` (ref `frxzhjmvoqyjzgdcupkg`, us-east-2). Schema is in `supabase/migrations/`, the function in `supabase/functions/book/`.

## One-time steps you must do
1. **Email.** Create a free account at https://resend.com, make an API key, and add it under Supabase > Edge Functions > Secrets as `RESEND_API_KEY`.
   - Without a verified domain, Resend only delivers to the account owner's own email. To email customers, verify your domain in Resend and add the secret `FROM_EMAIL` (for example `CST Automotive <bookings@yourdomain.com>`).
   - `SHOP_EMAIL` sets where the shop is notified (default `cstautomotive@yahoo.com`).
2. **Admin login.** Supabase > Authentication > Users > Add user (email and password) for each person who will use `admin.html`. Then make sure that email is in the `shop_admins` table (`insert into shop_admins values ('them@example.com');`). Currently listed: `pulkamchintu@gmail.com`.
3. **SMS (optional, later).** Add secrets `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`, and optionally `SHOP_SMS_TO`. US carriers require the sending number to be registered (A2P 10DLC or toll-free verification), which takes days to weeks. Until the secrets exist, SMS is skipped.
4. **Host the site** (Vercel, Netlify or GitHub Pages) from this folder. `vercel.json` sets security headers and clean URLs.

## Things to know
- Cancelling in the admin page frees the time but does not notify the customer. Call them.
- Service lengths live in `book_appointment` (SQL), in `dur()` in `booking.html`, and in the edge function's service list. Change all three together.
- The anon key in the pages is public by design. Customer data is only readable by signed-in admins.
