# CST Automotive Website

Static website for CST Automotive (2557 Glenda Ln, Dallas, TX 75229).

- `index.html` — home page
- `booking.html` — appointment booking page
- `docs/HANDOFF.md` — project handoff: business facts, decisions, design system, known gaps and plan
- `admin.html` — shop schedule (sign in, view and cancel appointments, block times)
- `supabase/` — database migration and the `book` edge function
- `docs/BOOKING_SETUP.md` — setup steps for email, SMS, admin logins and hosting
- `docs/SEO_CHECKLIST.md` — what SEO/AEO is already built and the off-site steps that drive ranking
- `scripts/build_seo.py` — regenerates meta, structured data, FAQ, sitemap, robots and llms.txt (run with the real domain once connected)

Imported from the Claude artifact "CST Automotive". No build step: open `index.html` in a browser or serve the folder with any static host (GitHub Pages, Vercel, Netlify).
