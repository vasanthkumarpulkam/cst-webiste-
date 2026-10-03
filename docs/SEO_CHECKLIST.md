# SEO and AEO checklist

**SEO** = showing up in Google/Bing. **AEO** = being the answer that Google's AI overviews, ChatGPT, Claude, Perplexity, Siri and voice assistants give for "auto repair near me".

## Already done in the code (regenerate with `python3 scripts/build_seo.py https://your-domain.com`)
- Title, description, canonical URL, social share image (`og.png`) and Open Graph / Twitter tags on both pages.
- Structured data (JSON-LD): `AutoRepair` business with address, geo, hours, services and a booking action; `WebSite`; `WebPage`; `FAQPage`. The FAQ in the markup is generated from the same list as the visible FAQ, so they always match.
- 10 answer-first FAQ entries (location, hours, walk-ins, booking, oil change time, services, makes, inspections, price approval, fleet).
- `sitemap.xml`, `robots.txt` (search and AI crawlers allowed, `/admin` blocked), `llms.txt` (plain summary for AI assistants).
- Fast, mobile-first pages, one `h1` per page, real text (not images) for all content, `lang`, click-to-call phone links.
- Deliberately NOT in the structured data: review counts or star ratings (not allowed by your rule, and Google requires a count), founding year, email, prices. Add them only when the owner confirms.

## Must do outside the code (this is where local ranking is won)
1. **Google Business Profile** (biggest factor for "auto repair near me"). Claim and verify it, then make everything match the website exactly: name `CST Automotive`, address `2557 Glenda Ln #1&2, Dallas, TX 75229`, phone `(214) 256-6347`, hours Mon to Fri 9 to 5.
   - Primary category "Auto repair shop". Add secondary ones that are true (for example "Oil change service", "Brake shop", "Auto air conditioning service", "Car inspection station").
   - Add every service, the website link, the booking link (`/booking`), and real photos of the shop, team and work.
   - Post an update or photo every week or two. Answer every review, good or bad, within a day or two.
2. **Reviews.** Ask every happy customer for a Google review, with a short link or QR code at the counter. Never buy or fake reviews. Count and recency matter more than anything else you control.
3. **Same name, address and phone everywhere** (called NAP). Claim or create: Yelp (currently unclaimed with zero reviews), Bing Places, Apple Business Connect, Facebook, Yellow Pages, BBB, RepairPal, Angi, Nextdoor. A mismatch in any of them hurts ranking.
4. **Google Search Console and Bing Webmaster Tools.** Add the site, verify it, submit `sitemap.xml`, and check "Pages" for errors after a week. Without this you cannot see what people searched for.
5. **A real domain** (for example `cstautomotivedallas.com`). Connect it in Vercel, run `python3 scripts/build_seo.py https://thatdomain.com`, push, and set the Vercel `.vercel.app` address to redirect to it. Also use it for email (Resend) and the Google profile website field.
6. **Local links.** Ask for a link from the Dallas-area businesses and groups he already works with (fleet customers, neighbors, chamber of commerce, local sponsorships).

## Next on-site step that moves rankings most: dedicated pages
Google ranks pages, not websites. One home page cannot rank for every search. Add one useful page per search people actually make, each with real content from the owner:
- Services: brake repair, oil change, diagnostics and check-engine light, A/C repair, transmission, state inspection, fleet maintenance (each "… in Dallas, TX").
- Imports: BMW, Mercedes-Benz, Audi, Porsche, Volvo, Honda and Acura repair in Northwest Dallas.
- Each page: what is included, how long it takes, signs you need it, a booking button, and 3 to 5 FAQs. Each needs unique text. Do not copy-paste the same paragraph across pages, which Google treats as thin content.
- Needs from the owner: which services he truly offers, any warranty or free-estimate terms, certifications, and 5 to 10 photos.
Ask for these pages when the owner has confirmed the details.

## How to check it worked
- Paste each page URL into Google's Rich Results Test and the Schema Markup Validator. Both should show the business and the FAQ with no errors.
- Share the link in WhatsApp or iMessage and confirm the preview shows `og.png`.
- Search `site:your-domain.com` after a few days to see it indexed.
- Expect local ranking to move over weeks, not days. Reviews and the Google profile do most of the work.
