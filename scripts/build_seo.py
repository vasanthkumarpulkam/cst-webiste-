#!/usr/bin/env python3
"""Regenerates the SEO / AEO parts of the site from one place.

    python3 scripts/build_seo.py https://your-domain.com

Writes: the <head> SEO block in index.html and booking.html, the visible FAQ plus its
FAQPage structured data (kept identical on purpose), sitemap.xml, robots.txt and llms.txt.
Run it again with the new URL when the custom domain is connected.
Only facts already on the site are used. Do not add prices, warranties or review counts here
unless the owner has confirmed them.
"""
import html, json, re, sys, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = (sys.argv[1] if len(sys.argv) > 1 else "https://cst-webiste.vercel.app").rstrip("/")

NAME = "CST Automotive"
PHONE = "+1-214-256-6347"
PHONE_DISPLAY = "(214) 256-6347"
ADDRESS = {"streetAddress": "2557 Glenda Ln #1&2", "addressLocality": "Dallas", "addressRegion": "TX",
           "postalCode": "75229", "addressCountry": "US"}
GEO = (32.8901701, -96.8917733)
MAPS = "https://www.google.com/maps/place/?q=place_id:ChIJodd8VEEnTIYRuZpToNmA-RI"
FACEBOOK = "https://www.facebook.com/cstautomotive/"

TITLE = "Auto Repair in Dallas, TX | CST Automotive"
DESC = ("CST Automotive is an independent auto repair shop in Northwest Dallas, TX. Brakes, diagnostics, "
        "oil changes, transmission, A/C, tires and fleet service on all makes and models. Book online or walk in.")
BOOK_TITLE = "Book an Appointment | CST Automotive, Dallas TX"
BOOK_DESC = ("Book an auto repair appointment at CST Automotive in Dallas, TX. Oil changes take a 30-minute slot, "
             "other services one hour. Pick a day and time online, Monday to Friday.")

SERVICES = [
    ("Brake service", "Brake inspection, pads and rotors, and brake fluid changes."),
    ("Computer diagnostics", "Warning lights read and traced to the actual cause before parts are replaced."),
    ("Electrical", "Battery, alternator and starter testing and replacement."),
    ("Oil changes", "Standard and full synthetic."),
    ("Transmission", "Fluid service and transmission repair."),
    ("A/C and heating", "HVAC diagnosis and air conditioning service."),
    ("Tires and alignment", "Sales, mounting, rotation, balancing and wheel alignment."),
    ("Fleet maintenance", "Maintenance contracts with priority scheduling for business vehicles."),
]

# Answer-first, plain facts. Rendered on the page AND as FAQPage JSON-LD, so they always match.
FAQ = [
    ("Where is CST Automotive located?",
     "CST Automotive is at 2557 Glenda Ln #1&2, Dallas, TX 75229, in Northwest Dallas. Call (214) 256-6347 for directions."),
    ("When is CST Automotive open?",
     "Monday to Friday, 9:00 AM to 6:00 PM. The shop is closed on Saturday and Sunday."),
    ("Do I need an appointment?",
     "No. Walk-ins are always welcome. If you want a time set aside for your car, book online or call (214) 256-6347."),
    ("How do I book an appointment?",
     "Use the online booking page: pick a service, a day and a time, and enter your car and contact details. You see your confirmation straight away, and if you give an email address we send one there too."),
    ("How long does an oil change take?",
     "Oil changes are booked as a 30-minute slot. Other services hold a one-hour slot, and longer repairs are scheduled when the car is diagnosed."),
    ("What services does CST Automotive offer?",
     "Brake service, computer diagnostics, electrical (battery, alternator, starter), oil changes (standard and full synthetic), transmission service and repair, A/C and heating, tires and alignment, and fleet maintenance."),
    ("Which makes and models do you work on?",
     "All makes and models, domestic and import. Imports such as Acura, Audi, BMW, Honda, Mazda, Mercedes-Benz, Nissan, Porsche and Volvo are a specialty."),
    ("Will I know the price before work starts?",
     "Yes. We find the cause first, then give you the price and what it covers. Nothing is repaired until you approve it."),
    ("Do you service business vehicles?",
     "Yes. Fleet maintenance is available with priority scheduling. Call to talk through what your vehicles need."),
]

HOURS = [{"@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}]


def jl(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def head_block(page):
    home = page == "index"
    url = SITE + ("/" if home else "/booking")
    title, desc = (TITLE, DESC) if home else (BOOK_TITLE, BOOK_DESC)
    biz = {"@id": SITE + "/#business"}
    graph = []
    if home:
        graph.append({
            "@type": ["AutoRepair", "LocalBusiness"], "@id": SITE + "/#business", "name": NAME, "url": SITE + "/",
            "telephone": PHONE, "image": SITE + "/og.png", "description": DESC,
            "address": dict(ADDRESS, **{"@type": "PostalAddress"}),
            "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
            "hasMap": MAPS, "openingHoursSpecification": HOURS,
            "areaServed": {"@type": "City", "name": "Dallas", "containedInPlace": {"@type": "State", "name": "Texas"}},
            "knowsAbout": ["Domestic auto repair", "Import auto repair", "Vehicle diagnostics", "Oil changes", "Brake repair", "Fleet maintenance"],
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Auto repair services", "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d}} for n, d in SERVICES]},
            "sameAs": [FACEBOOK, MAPS],
            "potentialAction": {"@type": "ReserveAction", "name": "Book an appointment",
                                "target": {"@type": "EntryPoint", "urlTemplate": SITE + "/booking",
                                           "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]},
                                "result": {"@type": "Reservation", "name": "Auto repair appointment"}},
        })
        graph.append({"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME,
                      "publisher": biz, "inLanguage": "en-US"})
        graph.append({"@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/", "name": title,
                      "description": desc, "isPartOf": {"@id": SITE + "/#website"}, "about": biz, "inLanguage": "en-US"})
        graph.append({"@type": "FAQPage", "@id": SITE + "/#faq", "isPartOf": {"@id": SITE + "/#webpage"},
                      "mainEntity": [{"@type": "Question", "name": q,
                                      "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    else:
        graph.append({"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
                      "isPartOf": {"@id": SITE + "/#website"}, "about": biz, "inLanguage": "en-US"})
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Book an appointment", "item": url}]})
    icon = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E'
            '%3Crect width=%2764%27 height=%2764%27 rx=%2710%27 fill=%27%230F2C40%27/%3E%3Ctext x=%2732%27 y=%2744%27 '
            'font-family=%27Arial Black,Arial%27 font-size=%2726%27 font-weight=%27900%27 text-anchor=%27middle%27 '
            'fill=%27%23F2B705%27%3ECST%3C/text%3E%3C/svg%3E">')
    e = html.escape
    lines = [
        "<!-- seo:start (generated by scripts/build_seo.py) -->",
        f"<title>{e(title)}</title>",
        f'<meta name="description" content="{e(desc)}">',
        f'<link rel="canonical" href="{url}">',
        '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">',
        '<meta name="theme-color" content="#0F2C40">',
        '<meta name="format-detection" content="telephone=yes">',
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:locale" content="en_US">',
        f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{NAME}, auto repair in Dallas, TX. Fixed right the first time.">',
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{SITE}/og.png">',
        icon,
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        jl({"@context": "https://schema.org", "@graph": graph}),
        "<!-- seo:end -->",
    ]
    return "\n".join(lines)


def inject_head(path, page):
    s = path.read_text()
    block = head_block(page)
    if "<!-- seo:start" in s:
        s = re.sub(r"<!-- seo:start.*?<!-- seo:end -->", lambda m: block, s, flags=re.S)
    else:
        a = s.index("<title>")
        b = s.index("<style>", a) if page == "index" else s.index('<link rel="stylesheet"', a)
        s = s[:a] + block + "\n" + s[b:]
    path.write_text(s)


def inject_faq(path):
    s = path.read_text()
    items = []
    for i, (q, a) in enumerate(FAQ):
        op = " open" if i == 0 else ""
        items.append(f"        <details{op}><summary>{html.escape(q, quote=False)}</summary><p>{html.escape(a, quote=False)}</p></details>")
    block = "<!-- faq:start (generated by scripts/build_seo.py) -->\n" + "\n".join(items) + "\n        <!-- faq:end -->"
    if "<!-- faq:start" in s:
        s = re.sub(r"<!-- faq:start.*?<!-- faq:end -->", lambda m: block, s, flags=re.S)
    else:
        m = re.search(r'(<div class="faq">\n)(.*?)(\n      </div>)', s, flags=re.S)
        s = s[:m.start(2)] + "        " + block + s[m.end(2):]
    path.write_text(s)


def write_files():
    today = datetime.date.today().isoformat()
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>{SITE}/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
        f'  <url><loc>{SITE}/booking</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
        '</urlset>\n')
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot",
            "Google-Extended", "Applebot", "Applebot-Extended", "Bingbot", "CCBot"]
    r = ["User-agent: *", "Allow: /", "Disallow: /admin", "Disallow: /admin.html", ""]
    for b in bots:
        r += [f"User-agent: {b}", "Allow: /", "Disallow: /admin", "Disallow: /admin.html", ""]
    r += [f"Sitemap: {SITE}/sitemap.xml", ""]
    (ROOT / "robots.txt").write_text("\n".join(r))
    svc = "\n".join(f"- {n}: {d}" for n, d in SERVICES)
    faq = "\n\n".join(f"**{q}**\n{a}" for q, a in FAQ)
    (ROOT / "llms.txt").write_text(
        f"# {NAME}\n\n> Independent auto repair shop in Northwest Dallas, Texas. Domestic and import vehicles, all makes and models. Walk-ins are always welcome.\n\n"
        f"## Facts\n- Address: 2557 Glenda Ln #1&2, Dallas, TX 75229\n- Phone: {PHONE_DISPLAY}\n- Hours: Monday to Friday, 9:00 AM to 6:00 PM (closed Saturday and Sunday)\n"
        f"- Booking: {SITE}/booking (oil changes use 30-minute slots, other services one hour)\n- Google Maps: {MAPS}\n- Facebook: {FACEBOOK}\n\n"
        f"## Services\n{svc}\n\n## Pages\n- [Home]({SITE}/): services, makes, hours, FAQ, contact\n- [Book an appointment]({SITE}/booking)\n\n## FAQ\n\n{faq}\n")


if __name__ == "__main__":
    inject_head(ROOT / "index.html", "index")
    inject_head(ROOT / "booking.html", "booking")
    inject_faq(ROOT / "index.html")
    write_files()
    print("SEO files built for", SITE)
