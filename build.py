"""Builds the Kickstart Tech Solutions multi-page site.

Run: python3 build.py
Outputs:
  dist/      full static site for deployment (Cloudflare Pages, any static host)
  preview/   same site, with index.html as a fragment for the Claude Artifact preview
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
PREVIEW = os.path.join(ROOT, "preview")

PHONE = "+1 (770) 289-5440"
EMAIL = "connect@kickstarttechsolutions.com"
BOOK = "https://outlook.office365.com/book/FocusDesignConsultingITServices@focusdesignconsulting.com/"
LINKEDIN = "https://www.linkedin.com/company/focus-design-consulting/"

FONTS = "https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Source+Sans+3:wght@400;600&display=swap"
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 700 700'%3E%3Crect x='72' y='60' width='196' height='588' fill='%23004AAD'/%3E%3Cpolygon points='298,278 435,60 638,60 298,562' fill='%23000'/%3E%3Cpolygon points='370,510 486,337 648,648 436,648' fill='%23000'/%3E%3C/svg%3E"

NAV = [("about.html", "About"), ("services.html", "Services"), ("faq.html", "FAQ")]

SERVICES = {
    "hardware": {
        "file": "hardware.html", "name": "Hardware", "code": "HW",
        "icon": '<rect x="3" y="4" width="18" height="12"/><path d="M8 20h8M12 16v4"/>',
        "short": "Business-grade equipment sourced, configured, and delivered ready to work. We match the gear to the job and your budget, then keep track of it for its whole life.",
        "headline": "The right equipment, set up and ready on day one.",
        "lede": "From a single laptop to a full office refresh, we source business-grade hardware, configure it for your environment, and install it on site. Then we track warranties and lifecycles so nothing catches you off guard.",
        "bullets": ["Laptops and workstations", "Servers and storage", "Printers and peripherals", "Point-of-sale hardware", "Upgrades and repairs", "Asset and warranty tracking"],
        "tags": ["Dell", "HP", "Lenovo", "Imaging & setup"],
        "items": [
            ("Laptops and workstations", "Business-class machines chosen for the work your team does, imaged with your apps and settings so they are ready to use out of the box."),
            ("Servers and storage", "File servers, NAS units, and on-site storage sized for your data today with room to grow."),
            ("Printers and peripherals", "Office printers, scanners, docks, monitors, and conference room gear, installed and connected."),
            ("Point-of-sale hardware", "Terminals, receipt printers, scanners, and cash drawers for retail and service counters."),
            ("Upgrades and repairs", "Memory and storage upgrades, part replacements, and repairs that extend the life of the equipment you already own."),
            ("Asset and warranty tracking", "A living inventory of every device, its warranty, and its replacement date, so you can budget refreshes ahead of time."),
        ],
        "projects": [("Office refresh", "Replace aging PCs on a planned schedule, migrate user files, and recycle old equipment."), ("New hire setup", "Laptops configured and shipped or installed before an employee's first day."), ("Store opening", "POS terminals, back-office PC, and printers installed and tested before doors open.")],
    },
    "networking": {
        "file": "networking.html", "name": "Networking", "code": "NET",
        "icon": '<rect x="9" y="2" width="6" height="5"/><rect x="2" y="17" width="6" height="5"/><rect x="16" y="17" width="6" height="5"/><path d="M12 7v5M5 17v-5h14v5"/>',
        "short": "Fast, reliable networks designed around how your space is actually used. From a single office to multiple locations, we plan it, cable it, and tune it.",
        "headline": "Fast, reliable networks, planned around your space.",
        "lede": "Slow Wi-Fi and dropped calls cost real time. We design, cable, and configure wired and wireless networks that cover every corner of your space and keep up as you add people and devices.",
        "bullets": ["Network design and layout", "Structured cabling", "Switches and PoE", "Wi-Fi surveys and access points", "Voice and data", "IP camera and NVR installs"],
        "tags": ["Cat6 / Cat6A", "PoE+", "Wi-Fi 6", "VoIP"],
        "items": [
            ("Network design and layout", "A plan for your switches, access points, and cabling based on a walkthrough of your space and how people use it."),
            ("Structured cabling", "Clean, labeled Cat6 and Cat6A runs, patch panels, and network racks that are easy to maintain."),
            ("Switches and PoE", "Managed switches that power phones, access points, and cameras over a single cable."),
            ("Wi-Fi surveys and access points", "Coverage surveys and properly placed access points so the signal is strong where your team works."),
            ("Voice and data", "Networks configured to keep VoIP calls clear alongside everyday internet traffic."),
            ("IP camera and NVR installs", "Camera placement, cabling, and recorder setup with remote viewing from your phone."),
        ],
        "projects": [("Office move", "Cabling and Wi-Fi in place before move-in day, with internet service coordinated."), ("Wi-Fi upgrade", "Replace consumer routers with business access points and eliminate dead zones."), ("Multi-site network", "Connect two or more locations so files and systems are shared reliably.")],
    },
    "managed-it": {
        "file": "managed-it.html", "name": "Managed IT & Cloud", "code": "MSP / CSP",
        "icon": '<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.1 9.5 4.3 4.3 0 0 0 7 18z"/>',
        "short": "As your MSP, we monitor and maintain your systems around the clock for a predictable monthly fee. As your CSP, we set up and manage the cloud tools your team uses every day.",
        "headline": "Your IT department, for a fixed monthly fee.",
        "lede": "As your managed service provider (MSP), we monitor, maintain, and support your technology so your team can focus on their work. As your cloud solution provider (CSP), we handle Microsoft 365 and other cloud subscriptions from licensing to setup.",
        "bullets": ["24/7 monitoring and alerts", "Help desk for your staff", "Updates and maintenance", "Backup and recovery", "Microsoft 365 licensing and setup", "Cloud and email migration"],
        "tags": ["MSP", "CSP", "Microsoft 365", "Azure"],
        "items": [
            ("24/7 monitoring and alerts", "We watch your computers, servers, and network around the clock and act on problems before they slow you down."),
            ("Help desk for your staff", "A real person to call or email when something is not working, with remote fixes and on-site visits when needed."),
            ("Updates and maintenance", "Operating system and software updates applied on a schedule that does not interrupt your workday."),
            ("Backup and recovery", "Automatic backups of your important files and systems, tested regularly so a restore works when you need it."),
            ("Microsoft 365 licensing and setup", "The right licenses for each person, plus email, Teams, OneDrive, and SharePoint configured properly."),
            ("Cloud and email migration", "Moving files, mailboxes, and apps to the cloud with a plan that keeps your team working throughout."),
        ],
        "projects": [("Fully managed IT", "One monthly fee covers monitoring, maintenance, and help desk for every user and device."), ("Microsoft 365 rollout", "Licenses, mailboxes, Teams, and shared files set up and moved over in a weekend."), ("Co-managed IT", "We back up your in-house IT person with tools, after-hours coverage, and project help.")],
    },
    "consulting": {
        "file": "consulting.html", "name": "Consultation", "code": "ADVISORY",
        "icon": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
        "short": "Straight answers on what to buy, what to replace, and what to leave alone. We turn your goals and budget into a technology plan you can act on.",
        "headline": "A clear technology plan, in plain English.",
        "lede": "Technology decisions are easier with someone in your corner. We assess what you have, listen to where the business is going, and give you a prioritized plan with real costs and timelines.",
        "bullets": ["IT assessments", "Technology roadmaps", "Budgeting and refresh cycles", "New office and move planning", "Vendor selection", "Project management"],
        "tags": ["Free assessment", "12 to 36 month plans"],
        "items": [
            ("IT assessments", "A walkthrough of your hardware, network, accounts, and software, with a written summary of what is working and what is not."),
            ("Technology roadmaps", "A 12 to 36 month plan that ties technology spending to your business goals."),
            ("Budgeting and refresh cycles", "Predictable replacement schedules so big purchases never come as a surprise."),
            ("New office and move planning", "Cabling, internet, and equipment planned months ahead of a move or build-out."),
            ("Vendor selection", "Help choosing internet providers, phone systems, and software, with no vendor kickbacks steering the advice."),
            ("Project management", "One point of contact who coordinates vendors, schedules, and installs from start to finish."),
        ],
        "projects": [("Annual IT review", "A yearly check-in on your systems, spending, and plans for the year ahead."), ("Growth planning", "Prepare your technology for new hires, a second location, or a new line of business."), ("Software selection", "Compare options for a new system and plan the rollout with your team.")],
    },
}

FAQS = [
    ("What does managed IT cost?", "Managed services are billed at a fixed monthly rate based on the number of users and devices. Hardware and network projects are quoted up front so there are no surprises. Many businesses spend less than they would on an in-house IT hire."),
    ("Can you supply hardware and set it up too?", "Yes. We source business-grade equipment, configure it for your environment, deliver it, and install it on site. Your team gets devices that are ready to use on day one."),
    ("What is the difference between MSP and CSP?", "As a managed service provider (MSP), we take care of your day-to-day IT: monitoring, maintenance, and help desk. As a cloud solution provider (CSP), we handle your cloud subscriptions such as Microsoft 365, including licensing, setup, and billing."),
    ("We are moving offices. Can you help?", "Office moves and new build-outs are some of our favorite projects. We plan the cabling and Wi-Fi before you move in, coordinate internet service, and have every desk working on your first morning."),
    ("Do you work with the equipment we already have?", "Absolutely. We start by assessing what you own, keep what is still serving you well, and plan replacements on a schedule that fits your budget."),
    ("How fast can you respond when something breaks?", "Remote support starts as soon as you reach us, and urgent issues get same-day attention. When hands-on work is needed, our team comes to you."),
    ("Do we have to sign a long contract?", "No. Managed services run month to month after an initial onboarding period, and projects are quoted individually. We would rather earn your business every month."),
    ("What happens during the free IT assessment?", "We review your current hardware, network, and cloud accounts, usually in about an hour on site or remotely. You get a short written summary with our recommendations and no obligation to buy anything."),
    ("Which brands do you work with?", "We commonly work with Dell, HP, Lenovo, Microsoft, Netgear, and Crucial, and we recommend equipment based on your needs rather than a single vendor's catalog."),
    ("When are you available?", "Our office hours are Monday to Friday, 9 AM to 8 PM. Managed clients are monitored around the clock."),
]

K_SYMBOL = ""

BRAND = '''<a class="brand" href="index.html" aria-label="Kickstart Tech Solutions home">
      <img src="assets/kts-logo-web.png" width="900" height="163" alt="Kickstart Tech Solutions">
    </a>'''


def icon(svc):
    return f'<div class="svc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square">{svc["icon"]}</svg></div>'


def header(active):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active or (label == "Services" and active in [s["file"] for s in SERVICES.values()]) else ""
        links.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if active == "contact.html" else ""
    links.append(f'<li><a class="btn btn-primary" href="contact.html"{cur}>Get a quote</a></li>')
    return f'''<header class="site">
  <div class="wrap nav">
    {BRAND}
    <button class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="nav-links">Menu</button>
    <ul class="nav-links" id="nav-links" hidden>
      {"".join(links)}
    </ul>
  </div>
</header>'''


def footer():
    svc_links = "".join(f'<li><a href="{s["file"]}">{s["name"]}</a></li>' for s in SERVICES.values())
    return f'''<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        {BRAND}
        <p>Hardware, networking, managed IT and cloud, and technology consulting for small and mid-sized businesses.</p>
      </div>
      <div><h4>Services</h4><ul>{svc_links}</ul></div>
      <div><h4>Company</h4><ul><li><a href="about.html">About</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Contact</a></li><li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></li></ul></div>
      <div><h4>Reach us</h4><ul><li>{PHONE}</li><li class="wrap-any">{EMAIL}</li><li>Mon to Fri, 9 AM to 8 PM</li></ul></div>
    </div>
    <div class="foot-bottom"><span>© <span id="yr">2026</span> Kickstart Tech Solutions. All rights reserved.</span><span>Hardware · Networking · Managed IT · Consulting</span></div>
  </div>
</footer>'''


def page_hero(eyebrow, title, lede, crumbs=None):
    bc = ""
    if crumbs:
        parts = " <span aria-hidden=\"true\">/</span> ".join(f'<a href="{h}">{l}</a>' if h else f'<span aria-current="page">{l}</span>' for h, l in crumbs)
        bc = f'<nav class="crumbs" aria-label="Breadcrumb">{parts}</nav>'
    return f'''<section class="page-hero">
    <div class="wrap page-hero-inner">
      {bc}
      <p class="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p class="lede">{lede}</p>
    </div>
  </section>'''


def cta_band(title="Ready to get your tech working for you?", text="Book a free IT assessment. We will review what you have and give you a clear, no-obligation plan."):
    return f'''<section class="cta-band">
    <div class="wrap cta-inner">
      <div><h2>{title}</h2><p>{text}</p></div>
      <div class="cta-actions"><a class="btn btn-light" href="contact.html">Book a free assessment</a><span class="cta-phone">or call {PHONE}</span></div>
    </div>
  </section>'''


def svc_card(s, link=True):
    lis = "".join(f"<li>{b}</li>" for b in s["bullets"])
    tags = "".join(f'<span class="tag">{t.replace("&", "&amp;")}</span>' for t in s["tags"])
    more = f'<a class="more" href="{s["file"]}">Explore {s["name"].replace("&", "&amp;")} <span aria-hidden="true">→</span></a>' if link else ""
    return f'''<article class="svc">
          <div class="svc-top">{icon(s)}<h3><a href="{s["file"]}">{s["name"].replace("&", "&amp;")}</a></h3></div>
          <p>{s["short"]}</p>
          <ul>{lis}</ul>
          <div class="tags">{tags}</div>
          {more}
        </article>'''


WHY = [
    ("One partner, start to finish", "Hardware, network, cloud, and support under one roof. One call gets it handled, with no finger-pointing between vendors."),
    ("Predictable costs", "Fixed monthly rates for managed services and clear quotes for projects. You know what you are paying before work begins."),
    ("Proactive, not reactive", "We watch your systems around the clock and fix most problems before your team ever notices them."),
    ("Local and on-site", "A nearby team that can be at your door when something needs hands on hardware, not just a ticket number."),
    ("Built to grow with you", "We design for the business you are becoming, so adding staff, devices, or a new location is simple."),
    ("Plain-English advice", "No jargon and no upselling. We explain the options and recommend what fits your goals."),
]
STEPS = [
    ("Assess", "We walk your site and review your current hardware, network, and accounts to see what is working and what is not."),
    ("Plan", "You get a clear proposal with equipment, timelines, and costs, prioritized by business impact."),
    ("Deploy", "We source, install, and configure everything, scheduled around your hours to keep downtime to a minimum."),
    ("Support", "We monitor, maintain, and answer your team's calls, and review the plan with you as you grow."),
]
INDUSTRIES = [
    ("Retail", "POS terminals, store Wi-Fi, back-office PCs, and multi-location networks."),
    ("Healthcare practices", "Front desk and exam room workstations, printers, and dependable connectivity."),
    ("Professional services", "Laptops, Microsoft 365, file sharing, and remote work for growing teams."),
    ("Education", "Classroom devices, campus Wi-Fi coverage, and lab setups."),
    ("Construction", "Rugged field devices, job site connectivity, and office-to-site access."),
]


def why_band():
    items = "".join(f'<div class="why"><h3>{t}</h3><p>{d}</p></div>' for t, d in WHY)
    return f'''<section class="band" aria-labelledby="why-title">
    <div class="wrap">
      <p class="eyebrow">Why Kickstart</p>
      <h2 id="why-title">Enterprise know-how, sized for small business.</h2>
      <div class="why-grid">{items}</div>
    </div>
  </section>'''


def process(intro=True):
    steps = "".join(f'<li class="step"><span class="step-num">STEP {i}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS, 1))
    return f'''<section class="section" aria-labelledby="process-title">
    <div class="wrap">
      <div class="section-head">
        <div><p class="eyebrow">How we work</p><h2 id="process-title">From first call to fully supported.</h2></div>
        <p>Every engagement follows the same four steps, whether it is one new laptop or a full office build-out.</p>
      </div>
      <ol class="steps">{steps}</ol>
    </div>
  </section>'''


def faq_list(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"


RACK = '''<div class="rack" aria-label="Illustration of a network rack installed by Kickstart Tech Solutions">
        <div class="rack-top"><span>RACK A · 12U</span><span>KTS MANAGED</span></div>
        <div class="unit"><div class="unit-label"><b>CORE SWITCH</b>24 × 1GbE PoE+</div><div class="ports" data-ports="core"></div></div>
        <div class="unit"><div class="unit-label"><b>PATCH PANEL</b>Cat6A · 24 port</div><div class="ports" data-ports="patch"></div></div>
        <div class="unit"><div class="unit-label"><b>ACCESS SWITCH</b>Wi-Fi 6 uplinks</div><div class="ports" data-ports="access"></div></div>
        <div class="unit server"><div class="unit-label"><b>FILE SERVER</b>4-bay storage</div><div class="bays"><div class="bay"><i></i></div><div class="bay"><i></i></div><div class="bay"><i></i></div><div class="bay"><i></i></div></div></div>
        <div class="rack-foot"><span>Uplink <b>10G</b></span><span>Status <b>All systems normal</b></span><span>Backup <b>Verified</b></span></div>
      </div>'''


def home():
    cards = "".join(svc_card(s) for s in SERVICES.values())
    return f'''<section class="hero" aria-labelledby="hero-title">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <p class="eyebrow">Hardware · Networking · Managed IT · Consulting</p>
        <h1 id="hero-title">The tech your business runs on, <em>built right</em> and kept running.</h1>
        <p class="lede">Kickstart Tech Solutions supplies the hardware, builds the network, manages your IT and cloud, and plans what comes next. One partner from the first purchase order to everyday support, for small and mid-sized businesses.</p>
        <div class="hero-ctas">
          <a class="btn btn-primary" href="contact.html">Book a free IT assessment</a>
          <a class="btn btn-ghost" href="services.html">See our services</a>
        </div>
        <div class="pillars"><span>Fixed monthly pricing</span><span>24/7 monitoring</span><span>On-site and remote support</span></div>
      </div>
      {RACK}
    </div>
  </section>

  <section class="section" aria-labelledby="svc-title">
    <div class="wrap">
      <div class="section-head">
        <div><p class="eyebrow">What we do</p><h2 id="svc-title">Four services, one accountable team.</h2></div>
        <p>Most businesses juggle a hardware vendor, a cabling contractor, a cloud reseller, and an IT person on call. We cover all four so nothing falls between the cracks.</p>
      </div>
      <div class="services">{cards}</div>
    </div>
  </section>

  {why_band()}
  {process()}

  <section class="section" style="padding-top:0" aria-labelledby="home-faq">
    <div class="wrap">
      <div class="section-head">
        <div><p class="eyebrow">FAQ</p><h2 id="home-faq">Questions we hear often</h2></div>
        <p>A few quick answers. See the <a href="faq.html">full FAQ</a> for more.</p>
      </div>
      {faq_list(FAQS[:4])}
    </div>
  </section>

  {cta_band()}'''


def about():
    inds = "".join(f"<li><b>{n}</b><span>{d}</span></li>" for n, d in INDUSTRIES)
    return f'''{page_hero("About us", "A technology partner that handles the whole stack.", "Kickstart Tech Solutions helps small and mid-sized businesses buy the right equipment, build dependable networks, and keep everything running. We focus on the hardware, network, and managed services side of IT.", [("index.html", "Home"), (None, "About")])}

  <section class="section" aria-labelledby="story-title">
    <div class="wrap split">
      <div>
        <p class="eyebrow">Who we are</p>
        <h2 id="story-title">Enterprise experience, small business focus.</h2>
      </div>
      <div class="prose">
        <p>Our team brings years of experience running technology for large organizations, combined with first-hand knowledge of what it takes to run a small business. That means we know how to build systems properly, and we know every dollar matters.</p>
        <p>We started Kickstart to give growing businesses one dependable partner for the physical side of IT: the laptops on desks, the cabling in walls, the Wi-Fi in the air, and the cloud accounts everyone logs into. One team plans it, installs it, and supports it.</p>
        <p>Our values are simple. Recommend only what a client needs, explain it in plain English, show up when we say we will, and leave every closet and rack neater than we found it.</p>
      </div>
    </div>
  </section>

  {why_band()}
  {process()}

  <section class="section" style="padding-top:0" aria-label="Industries and brands">
    <div class="wrap split">
      <div>
        <p class="eyebrow">Who we serve</p>
        <h2>Industries we know well</h2>
        <ul class="ind-list">{inds}</ul>
      </div>
      <div>
        <p class="eyebrow">Brands we work with</p>
        <h2>Gear from names you trust</h2>
        <div class="brands"><div>Dell</div><div>HP</div><div>Lenovo</div><div>Microsoft</div><div>Netgear</div><div>Crucial</div></div>
        <p class="brands-note">We recommend equipment based on your needs, not on a single vendor's catalog.</p>
      </div>
    </div>
  </section>

  {cta_band("Let's talk about your technology.", "Tell us where your business is headed and we will show you how technology can help you get there.")}'''


def services_page():
    cards = "".join(svc_card(s) for s in SERVICES.values())
    return f'''{page_hero("Services", "Four services, one accountable team.", "Hardware, networking, managed IT and cloud, and consultation. Use one, or let us handle all four so nothing falls between vendors.", [("index.html", "Home"), (None, "Services")])}

  <section class="section" aria-label="Our services">
    <div class="wrap">
      <div class="services">{cards}</div>
    </div>
  </section>

  {process()}
  {cta_band()}'''


def service_page(key):
    s = SERVICES[key]
    name = s["name"].replace("&", "&amp;")
    items = "".join(f'<div class="detail"><h3>{t}</h3><p>{d}</p></div>' for t, d in s["items"])
    projects = "".join(f'<div class="project"><span class="project-kicker">Typical project</span><h3>{t}</h3><p>{d}</p></div>' for t, d in s["projects"])
    tags = "".join(f'<span class="tag">{t.replace("&", "&amp;")}</span>' for t in s["tags"])
    others = "".join(f'<a class="other" href="{o["file"]}">{icon(o)}<span>{o["name"].replace("&", "&amp;")}</span></a>' for k, o in SERVICES.items() if k != key)
    return f'''{page_hero("Services", s["headline"], s["lede"], [("index.html", "Home"), ("services.html", "Services"), (None, name)])}

  <section class="section" aria-labelledby="inc-title">
    <div class="wrap">
      <div class="section-head">
        <div><p class="eyebrow">{name}</p><h2 id="inc-title">What's included</h2></div>
        <div class="tags head-tags">{tags}</div>
      </div>
      <div class="details">{items}</div>
    </div>
  </section>

  <section class="section alt" aria-labelledby="proj-title">
    <div class="wrap">
      <div class="section-head">
        <div><p class="eyebrow">In practice</p><h2 id="proj-title">How clients use it</h2></div>
        <p>Every project starts with a free assessment and a written quote.</p>
      </div>
      <div class="projects">{projects}</div>
    </div>
  </section>

  <section class="section" aria-labelledby="other-title">
    <div class="wrap">
      <p class="eyebrow">Pairs well with</p>
      <h2 id="other-title" class="h2-sm">Our other services</h2>
      <div class="others">{others}</div>
    </div>
  </section>

  {cta_band(f"Talk to us about {name.lower() if key != 'managed-it' else 'managed IT and cloud'}.")}'''


def faq_page():
    return f'''{page_hero("FAQ", "Questions we hear often", "Straight answers about pricing, services, and how we work. Don't see your question? Send us a note and a real person will reply.", [("index.html", "Home"), (None, "FAQ")])}

  <section class="section" aria-label="Frequently asked questions">
    <div class="wrap">{faq_list(FAQS)}</div>
  </section>

  {cta_band("Still have questions?", "We are happy to talk through your situation. No pressure and no jargon.")}'''


def contact_page():
    return f'''{page_hero("Contact", "Let's get your tech working for you.", "Tell us a little about your business and we will set up a free IT assessment. Expect to hear back within one business day.", [("index.html", "Home"), (None, "Contact")])}

  <section class="section contact" aria-label="Contact details and form">
    <div class="wrap contact-grid">
      <div class="contact-copy">
        <p class="eyebrow">Reach us</p>
        <dl class="reach">
          <div><dt>Phone</dt><dd>{PHONE}</dd></div>
          <div><dt>Email</dt><dd>{EMAIL}</dd></div>
          <div><dt>Book</dt><dd><a href="{BOOK}" target="_blank" rel="noopener">Schedule a free assessment call</a></dd></div>
          <div><dt>Hours</dt><dd>Mon to Fri, 9 AM to 8 PM</dd></div>
        </dl>
      </div>
      <form class="quote" id="quote-form" method="POST" novalidate>
        <input type="hidden" name="_subject" value="New assessment request from the KTS website">
        <input type="hidden" name="_template" value="table">
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="f-company">Business name</label><input id="f-company" name="company" autocomplete="organization" required></div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field full"><label for="f-interest">I'm interested in</label>
          <select id="f-interest" name="interest"><option>Hardware</option><option>Networking</option><option>Managed IT &amp; Cloud</option><option>Consultation</option><option>Not sure yet</option></select>
        </div>
        <div class="field full"><label for="f-msg">How can we help?</label><textarea id="f-msg" name="message" placeholder="For example: we're opening a second location and need Wi-Fi, 10 laptops, and Microsoft 365."></textarea></div>
        <div class="form-foot">
          <button class="btn btn-primary" type="submit">Request my free assessment</button>
          <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
        </div>
      </form>
    </div>
  </section>'''


PAGES = [
    ("index.html", "Kickstart Tech Solutions", "Business hardware, networking, managed IT and cloud services, and technology consulting for small and mid-sized businesses.", home),
    ("about.html", "About | Kickstart Tech Solutions", "Who we are and how Kickstart Tech Solutions works with small and mid-sized businesses.", about),
    ("services.html", "Services | Kickstart Tech Solutions", "Hardware, networking, managed IT and cloud, and technology consultation.", services_page),
    ("faq.html", "FAQ | Kickstart Tech Solutions", "Answers about pricing, services, and how Kickstart Tech Solutions works.", faq_page),
    ("contact.html", "Contact | Kickstart Tech Solutions", "Book a free IT assessment with Kickstart Tech Solutions.", contact_page),
]
for key, s in SERVICES.items():
    PAGES.append((s["file"], f'{s["name"]} | Kickstart Tech Solutions', s["short"], (lambda k: lambda: service_page(k))(key)))


def head_tags(title, desc):
    return f'''<title>{title.replace("&", "&amp;")}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc.replace("&", "&amp;")}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="styles.css">'''


def body(fname, fn):
    return f'''{K_SYMBOL}
{header(fname)}
<main id="top">
  {fn()}
</main>
{footer()}
<script src="site.js"></script>'''


def full_doc(fname, title, desc, fn):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head_tags(title, desc)}
</head>
<body>
{body(fname, fn)}
</body>
</html>
'''


def main():
    css = open(os.path.join(ROOT, "src", "styles.css")).read()
    js = open(os.path.join(ROOT, "src", "site.js")).read()
    for out in (DIST, PREVIEW):
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "styles.css"), "w").write(css)
        open(os.path.join(out, "site.js"), "w").write(js)
        if os.path.isdir(os.path.join(ROOT, "assets")):
            shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(out, "assets"), dirs_exist_ok=True)
    for fname, title, desc, fn in PAGES:
        doc = full_doc(fname, title, desc, fn)
        open(os.path.join(DIST, fname), "w").write(doc)
        if fname == "index.html":
            # The Artifact viewer adds its own document skeleton around the main page
            frag = head_tags(title, desc) + "\n" + body(fname, fn) + "\n"
            open(os.path.join(PREVIEW, fname), "w").write(frag)
        else:
            open(os.path.join(PREVIEW, fname), "w").write(doc)
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
