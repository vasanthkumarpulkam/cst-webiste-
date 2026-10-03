# CST Automotive website: project handoff

Written for a Claude Code session that has **not** seen the original chat. Everything needed to continue is in this file and in the published artifact. Read this whole file first, then read the artifact (see "Where the work lives").

Last updated: Sat 2026-10-03, artifact version 9.

---

## 1. What this project is

A professional website for **CST Automotive**, an independent auto repair shop in Dallas, TX. The user is a web builder making it for the shop owner. The user will show the owner a finished-looking site first, then correct any wrong details with him afterwards. The user's reputation is on it, so quality and accuracy both matter.

Deliverable is two pages:

1. **Main page** (`index.html`): hero, services, makes, how a visit works, about, Google rating, FAQ, contact, footer.
2. **Booking page** (`booking.html`): a step-by-step appointment scheduler (day, then time, then details, then "Book now").

---

## 2. Where the work lives

- **Published artifact (private, owner is the user):** https://claude.ai/artifact/AG8awKDSh2wYZKByyih19D
- Two published files: `index.html` (the artifact page itself) and `booking.html` (a supporting file).
- To get the source in a new session, use the Artifact tool:
  - `action: "read"`, `url: "https://claude.ai/artifact/AG8awKDSh2wYZKByyih19D"` returns `index.html`.
  - `action: "read"`, same `url`, `path: "booking.html"` returns the booking page.
  - `action: "list"`, `scope: "files"`, same `url` lists published files.
- To change it: edit local copies, then publish with the Artifact tool:
  `file_path: <index.html>`, `url: <artifact url>` (or the same file path as before), `files: {"booking.html": "<path to booking.html>"}`.
  Always pass `booking.html` in `files` when publishing, or keep it unchanged by leaving it out.
- The artifact is private. The user must share it from the page's Share menu before the owner can open it.
- Local working folder in the old session was `/home/claude/cst-automotive/` (not available in a new session).

---

## 3. Business facts, with how reliable each is

| Fact | Value | Source / reliability |
|---|---|---|
| Name | CST Automotive | Certain |
| Address | 2557 Glenda Ln #1&2, Dallas, TX 75229 | Google Maps listing. Yelp says "Ste 1" |
| Phone | (214) 256-6347 | Google Maps, Manta, user notes. Reliable |
| Email | cstautomotive@yahoo.com | From a user-supplied note. **Unverified** |
| Hours | Mon to Fri 9:00 AM to 5:00 PM, Sat and Sun closed | Google Maps and Facebook. **Conflict:** Yelp and Roadtrippers say Saturday 9 AM to 3 PM. Yelp is an unclaimed listing. Ask the owner |
| Walk-ins | Always welcome | **Stated by the user.** Treat as true |
| Opened | 2019 | Manta only. Google reviews dating back about 6 years fit it. **Unverified** |
| Google rating | 4.5 out of 5 | Google Maps, seen directly |
| Google review topics | friendly staff, mechanic, BMW, quality of work, honest mechanic, honest staff | Google Maps topic chips |
| Google Place ID | `ChIJodd8VEEnTIYRuZpToNmA-RI` | Google Places |
| Coordinates | 32.8901701, -96.8917733 | Google Places |
| Facebook | https://www.facebook.com/cstautomotive/ | Search result. Could not be opened (robots.txt) |
| Yelp | Unclaimed, **no reviews at all** | Seen directly on 2026-10-03 |

**Services list (from a directory listing, owner has not confirmed):** brake service; computerized diagnostics; electrical (battery, alternator, starter); oil changes (standard and synthetic); transmission (fluid service and repair); A/C and heating; tires and alignment (sales, mounting, rotation, balancing, alignment); state safety inspections and emissions; fleet maintenance with priority scheduling.

**Makes shown (from the same directory):** Acura, Audi, BMW, Genesis, Honda, Infiniti, Mazda, Mercedes-Benz, Nissan, Porsche, Volvo, Chevrolet, GMC, Lincoln. The user wants the site to say the shop services **all makes and models**, with imports a specialty. Google reviews mention BMW, Mercedes, Bentley, Ferrari and a Mustang.

---

## 4. Decisions and rules from the user (follow these)

1. **Do not put the owner's name anywhere on the website.** (His first name appears in Google reviews. Leave it out.)
2. **Do not show the number of Google reviews.** The site shows only the 4.5 rating and the topic chips, with no counts.
3. **Walk-ins are always welcome.** Say so in the hero, shop info card, About facts, steps, FAQ, hours card and booking pages.
4. **The shop services and repairs all makes and models.** Imports are described as a specialty, not the only focus.
5. **Booking lives on its own page** (`booking.html`). The main page only has a short "Book your visit" block and buttons that link to it.
6. **Booking opens one step at a time:** pick a day, then the times appear, then after picking a time the details form and "Book now" appear.
7. **Show the owner first, correct wrong details afterwards.** So the site must not contain claims we know are false, but unconfirmed items are acceptable as long as they are flagged to the owner.
8. **Real photos only.** Do not use stock or AI-generated images in place of shop photos.
9. **Never invent reviews or testimonials.** Two earlier "Yelp" reviews were removed because they were not on CST's Yelp page (they came from a third-party directory and predate 2019, so they likely belong to a previous business at that address). Do not bring them back.
10. Do not copy Google review text onto the site without the reviewers' or owner's permission. Use the rating and topics, or Google's own review widget.

---

## 5. Current state of the site (version 9)

### Main page sections, in order
Header bar (logo, nav: Services, How it works, Reviews, Contact; phone; Book appointment) then:

1. **Hero:** "Fixed right the first time." Eyebrow "All makes and models · Northwest Dallas". Two buttons (Book appointment to `booking.html`, Call). Chips. A tilted "Shop info" card with live open/closed status in Dallas time, weekly hours, walk-ins row, email, copy-number button. A scrolling strip of makes.
2. **Services:** 9 cards in a 3-column grid, each with a custom line icon.
3. **All makes and models:** tiles for 14 makes plus a note to bring in any make.
4. **How a visit works:** 4 steps (Book or walk in, We diagnose, You approve, We fix it).
5. **About:** "Small shop. Straight answers." with facts (open since 2019, Google rating 4.5/5, walk-ins welcome, Mon to Fri).
6. **Reviews:** large 4.5 with stars, "Rating on Google Maps", topic chips, link to the Google listing.
7. **Book your visit:** short block linking to `booking.html`.
8. **Common questions:** 5 accordion items.
9. **Visit the shop:** address card (Google Maps link), phone and email card (Facebook link), hours card.
10. Footer, plus a fixed **Call / Book appointment bar on phones**.

### Booking page
Compact header (logo, phone, Back to site). Intro mentions walk-ins. A white card with:
- Step 1: calendar (Mon to Fri only, no past days, up to 60 days ahead, Dallas time).
- Step 2: time slots 9 AM to 4 PM, hourly. Hidden until a day is picked.
- Step 3: service dropdown (10 options), year, make, model, name, phone, optional email, optional notes. Hidden until a time is picked. A summary line, a "Book now" button and a note "The shop calls to confirm every appointment."
- On desktop a dashed placeholder "Your details open here" fills the right column until step 3 opens.
- After submit: a confirmation with reference number, full details, and buttons: Email to the shop (mailto), Copy details, Call, Book another.
- "Your requests on this device" list with Remove buttons. Booked slots are marked taken for that browser only.

### Behaviour
- Hero entrance animation, scroll-in reveals, hover transitions. All disabled for `prefers-reduced-motion`.
- Light and dark themes via tokens.
- If a phone link does not start a call (common in the Claude app viewer), a toast shows the number with a Copy button.
- Sticky header fills the app's top safe-area inset so content never shows above it.

---

## 6. Design system

Layout idea: deep oil-blue hero over a faint blueprint grid, with a tilted "repair order" ticket for shop info; hazard-stripe divider; light content sections with square, outlined blocks.

Tokens (light, defined on `:root`; dark values redefined under `prefers-color-scheme: dark` guarded by `:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]`):

```
--bg #EEF1F3   --surface #FFFFFF   --ink #0E1B26   --muted #51616E   --line #CBD3D9
--brand #0F4C75   --signal #F2B705   --signal-ink #1A1400
--hero-bg #0F2C40   --hero-fg #F2F6F8   --hero-muted #A9BDCB   --hero-line #2A4A61
--ok #1E7B4B   --closed #A6372B
dark: --bg #0C141B --surface #14202A --ink #E9EEF2 --muted #93A3AF --line #26343F
      --brand #6FB6E3 --signal #F4B81A --hero-bg #101D27 --ok #5CC58D --closed #EF8A7C
```

Fonts: Barlow Condensed (display, italic 800 for headlines), Barlow (body), JetBrains Mono (numbers, hours, labels), all from Google Fonts with fallback stacks. Gutter `clamp(16px,4vw,48px)`.

---

## 7. Technical rules and traps (learned the hard way)

**Artifact platform**
- External scripts only from cdnjs / jsdelivr / unpkg. Stylesheets only from Google Fonts. **No external images** (they are blocked), so photos must be embedded as `data:` URIs (resize to about 1600 px wide, JPEG, keep total page under 16 MB).
- No `alert/confirm/prompt`, no `window.print`, no real form posts, no downloads started by the page.
- `mailto:` and `tel:` links are unreliable inside the viewer. Always show the email and number as visible text and keep the copy fallbacks.
- `index.html` is wrapped in a skeleton at publish time: write it **without** `<html>/<head>/<body>`, with `<title>` and `<style>` at the top. The skeleton provides `[hidden]{display:none!important}` and a body reset.
- `booking.html` is a **supporting file, served raw**. It must be a full document (doctype, charset, viewport, `<title>`), and it must define its own `[hidden]{display:none!important}` and a body background token. It already does. It also duplicates the main page's style block (stylesheets cannot be shared), so **any style change must be made in both files**.
- Sticky header: use `top: env(safe-area-inset-top,0px)` and the `.bar::before` filler so content does not show in the app's inset.
- Fixed bottom bars add `env(safe-area-inset-bottom,0px)`.
- Page must not scroll horizontally at about 390 px wide. It was checked at 1280 and 390.
- Any change to the booking logic should be re-tested end to end (see section 9).

**Build traps**
- When bulk-editing with regex, never use `.*?` across repeated blocks without a guard. An icon-swap script once deleted 8 of 9 service cards. The services grid was rebuilt from a clean list. Check element counts after edits (`<article>` count should be 9).
- `fieldset` rules with `display:flex` override the UA `hidden` behaviour. Keep the explicit `[hidden]` rule.
- Playwright full-page screenshots show sticky and fixed elements in the middle of the image. That is a capture artifact, not a bug.

---

## 8. Known gaps and risks

1. **No real photos yet.** Owner-posted photos exist on the Google Maps listing (Photos, then "By owner"). They could not be downloaded from the cloud session (image host blocked). Needs the user to save them (or get originals from the owner) and attach them. Plan: resize, embed as data URIs, use one in the hero, one in About, and a small gallery, all with alt text. Only use photos posted by the owner; customer-posted photos belong to customers.
2. **Booking is a demo.** Requests are stored only in the visitor's browser (`localStorage` key `cst-requests`) and reach the shop only if the visitor taps the email button or copies the details. Two visitors can pick the same slot. Do not describe it to the client as live online booking.
3. **Unconfirmed facts** to check with the owner: Saturday hours, services list, makes list, opening year (2019), email address, whether he approves the "you approve the cost before any repair starts" wording in "How a visit works", and the hero line "tell you what it costs".
4. **Saturday hours conflict** between Google/Facebook (closed) and Yelp/Roadtrippers (9 to 3).
5. **Phone links** may not open the dialer inside the Claude app. On a real hosted site they should. Untested on a real iPhone beyond the user's report.
6. **No custom domain, no analytics, no search markup** yet.
7. Newest-first sorting of Google reviews did not clearly apply when checked, so the review topics may not reflect only the latest reviews.

---

## 9. Plan to finish

| Step | Work | Suggested model | Notes |
|---|---|---|---|
| 1 | Walk the owner through the draft and record corrections (hours, services, makes, year, email, name use, wording) | The user | At the meeting |
| 2 | Apply corrections to both pages | Sonnet-class | Edit both files; recheck counts and layout |
| 3 | Add shop photos and, with permission, 3 testimonials | Sonnet-class | Embed as data URIs, add alt text, keep pages light |
| 4 | Real booking: requests saved in a shared database, alert to the shop, no double-booking, simple owner view | Opus-class | Supabase and Make are connected in the user's account. Use the artifact `db` capability or Supabase. Load the `artifact-capabilities` skill first. Never hardcode seeds |
| 5 | Local search markup (`AutoRepair` JSON-LD with address, phone, hours, geo), page description, domain, Vercel deploy, link from Google listing, final phone and laptop check | Sonnet-class, then an Opus-class review | Vercel connector is available |

Reference notes from competitor research: strong auto repair sites show the phone number on every page, an online booking path above the fold, third-party reviews (Google/Yelp), real photos of the shop and team, warranty and certification badges where true, service-specific content, and mobile-first speed. Park Cities Auto Care (Dallas) is a useful benchmark: 4.9 stars, a family-run story, free estimates, and a rideshare perk. Only add badges, warranties or free-estimate claims the owner confirms.

---

## 10. How to test

The previous session used Playwright with the bundled Chromium (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`, do not run `playwright install`).

- Render both pages at 1280x800 and 390x800, light and dark, full-page, and check `document.documentElement.scrollWidth <= clientWidth`.
- To preview `index.html` locally, wrap it in `<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui;background:#fafafa}[hidden]{display:none!important}</style></head><body>` + file + `</body></html>`, because the real skeleton is added at publish time.
- End-to-end booking test (all passed in version 9): open booking page, confirm steps 2 and 3 are hidden; click a day (step 2 appears); click a time (step 3 and the Book now button appear); change the day (step 3 hides, entered values stay); fill the form and click Book now (confirmation with reference appears, slot marked taken); Book another resets to step 1; Remove frees the slot; no console errors.
- Call fallback test: click a `tel:` link with the default prevented, wait about 1 second, confirm the number toast appears.
- Simulate the Claude app's top inset by replacing `env(safe-area-inset-top,0px)` with `120px` in a copy, scroll, and confirm no content shows above the sticky header.

---

## 11. Sources used

- Google Maps listing: https://www.google.com/maps/place/?q=place_id:ChIJodd8VEEnTIYRuZpToNmA-RI
- Yelp (unclaimed, no reviews): https://www.yelp.com/biz/cst-automotive-dallas
- Roadtrippers listing: https://maps.roadtrippers.com/us/dallas-tx/services/cst-automotive
- Manta listing (established 2019): https://www.manta.com/c/mkbjf81/cst-automotive
- Directory listing used for services and makes: https://near-me.auto-repair.shop/ecat/shop/101566
- Facebook page: https://www.facebook.com/cstautomotive/
- Reference: https://freshysites.com/blog/top-auto-repair-websites/ and https://lantern.llc/b/park-cities-auto-care-dallas/book
