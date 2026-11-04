#!/usr/bin/env python3
"""Builds the Quantech Graphics static site into dist/.

Usage:  python3 build.py
Edit links in site.config.json. Edit copy in this file (PAGES section).
Placeholder images are generated into dist/assets/img/*.svg; to use real art,
drop a file with the same name but a .jpg/.png/.webp extension into
src/assets/img/ and it will be used instead.
"""
import json, re, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
CFG = json.loads((ROOT / "site.config.json").read_text())
SOC = {s["key"]: s for s in CFG["socials"]}
E = html.escape
YEAR = 2026

# ------------------------------------------------------------------ images
IMG_SLOTS = {
    # name: (width, height, label)
    "hero-vecter-assault": (1920, 1080, "VECTER ASSAULT · KEY ART OR GAMEPLAY LOOP"),
    "lane-game": (1200, 900, "VECTER ASSAULT"),
    "kit-cqc-stealth": (1600, 900, "CQC STEALTH KIT · ARENA DEMO CAPTURE"),
    "kit-rig-qa-lab": (1600, 900, "RIG QA LAB · HEATMAP SCREENSHOT"),
    "kit-sci-fi-drone": (1600, 900, "SCI-FI DRONE PACK · SWARM RENDER"),
    "kit-body-cam": (1600, 900, "BODY CAM FPS KIT · UNDER CONSTRUCTION"),
    "tool-cqc-arena": (600, 600, "CQC ARENA"),
    "tool-rig-qa": (600, 600, "RIG QA WEB"),
    "va-trailer": (1920, 1080, "TRAILER · VIDEO PLACEHOLDER"),
    "va-shot-1": (1600, 900, "SCREENSHOT 01"),
    "va-shot-2": (1600, 900, "SCREENSHOT 02"),
    "va-shot-3": (1600, 900, "SCREENSHOT 03"),
    "va-shot-4": (1600, 900, "SCREENSHOT 04"),
    "va-shot-5": (1600, 900, "SCREENSHOT 05"),
    "va-shot-6": (1600, 900, "SCREENSHOT 06"),
    "og-default": (1200, 630, "QUANTECH GRAPHICS · SHARE IMAGE"),
}

def placeholder_svg(name, w, h, label):
    construction = "UNDER CONSTRUCTION" in label
    stripes = ""
    if construction:
        stripes = (f'<pattern id="s" width="80" height="80" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                   f'<rect width="40" height="80" fill="#f2a93b" fill-opacity=".09"/></pattern>'
                   f'<rect width="{w}" height="{h}" fill="url(#s)"/>')
    step = max(w, h) // 24
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w, step))
    grid += "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h, step))
    fs = max(18, min(w, h) // 18)
    c = max(28, min(w, h) // 12)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Placeholder: {E(label)}">
<rect width="{w}" height="{h}" fill="#141a20"/>
<g stroke="#2a343e" stroke-width="1">{grid}</g>{stripes}
<g fill="none" stroke="#f2a93b" stroke-width="3" stroke-opacity=".8">
<path d="M{c} {c*2}V{c}H{c*2}"/><path d="M{w-c*2} {c}H{w-c}V{c*2}"/>
<path d="M{c} {h-c*2}V{h-c}H{c*2}"/><path d="M{w-c*2} {h-c}H{w-c}V{h-c*2}"/>
<circle cx="{w/2}" cy="{h/2 - fs*1.2}" r="{fs*1.1}"/><path d="M{w/2-fs*1.8} {h/2-fs*1.2}h{fs*1.2}M{w/2+fs*0.6} {h/2-fs*1.2}h{fs*1.2}"/>
</g>
<text x="{w/2}" y="{h/2 + fs*1.2}" fill="#e6ebef" font-family="JetBrains Mono, Menlo, monospace" font-size="{fs}" font-weight="600" letter-spacing="3" text-anchor="middle">{E(label)}</text>
<text x="{w/2}" y="{h/2 + fs*2.6}" fill="#8d9aa6" font-family="JetBrains Mono, Menlo, monospace" font-size="{fs*0.62:.0f}" letter-spacing="2" text-anchor="middle">PLACEHOLDER · {w}×{h} · {name}</text>
</svg>'''

def img_src(name):
    for ext in (".webp", ".jpg", ".jpeg", ".png", ".gif"):
        if (SRC / "assets" / "img" / (name + ext)).exists():
            return f"assets/img/{name}{ext}"
    return f"assets/img/{name}.svg"

def ph(name):
    return ' class="ph"' if img_src(name).endswith(".svg") else ""

def img(name, alt, cls="r16x9", loading="lazy"):
    return f'<div class="media {cls}"><img{ph(name)} src="{img_src(name)}" alt="{E(alt)}" loading="{loading}"></div>'

# ------------------------------------------------------------------ icons
def icon(key):
    p = SRC / "icons" / f"{key}.svg"
    svg = p.read_text()
    svg = re.sub(r"<title>.*?</title>", "", svg)
    return svg.replace('role="img"', 'aria-hidden="true" focusable="false"')

BRAND_ANIM = '<span class="brand-anim" data-logo-anim><img class="brand-mark" src="assets/brand/mark.svg" alt="" width="44" height="32"></span><img class="brand-word" src="assets/brand/wordmark-2line.svg" alt="Quantech Graphics" width="89" height="24">'
BRAND = '<img class="brand-mark" src="assets/brand/mark.svg" alt="" width="44" height="32"><img class="brand-word" src="assets/brand/wordmark-2line.svg" alt="Quantech Graphics" width="89" height="24">'
LOGO = '''<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><g fill="none" stroke="#f2a93b" stroke-width="2"><path d="M16 2 28 9v14l-12 7-12-7V9z"/><circle cx="16" cy="16" r="5.5"/><path d="M19.5 19.5 24 24"/></g></svg>'''

def social_link(key, cls="social"):
    s = SOC[key]
    if s["url"]:
        return f'<a class="{cls}" href="{E(s["url"])}" target="_blank" rel="noopener">{icon(key)}<span>{E(s["name"])}</span></a>'
    return f'<a class="{cls} soon" href="#" aria-disabled="true" title="Coming soon">{icon(key)}<span>{E(s["name"])}</span><span class="soon-tag">SOON</span></a>'

def ext_or_soon(url, label, cls="btn", soon_label=None):
    if url:
        return f'<a class="{cls}" href="{E(url)}" target="_blank" rel="noopener">{label}</a>'
    return f'<a class="{cls}" href="#" aria-disabled="true" title="Coming soon">{soon_label or label}</a>'

# ------------------------------------------------------------------ chrome
NAV = [
    ("index.html", "Home"),
    ("vecter-assault.html", "Vecter Assault"),
    ("kits.html", "Kits & Tools"),
    ("services.html", "Services"),
]

def header(active):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{E(t)}</a>' for h, t in NAV)
    d, p = SOC["discord"], SOC["patreon"]
    links += (f'<a href="{E(d["url"])}" target="_blank" rel="noopener">Discord</a>' if d["url"]
              else '<a href="#" aria-disabled="true">Discord</a>')
    links += (f'<a href="{E(p["url"])}" target="_blank" rel="noopener">Patreon</a>' if p["url"]
              else '<a href="#" aria-disabled="true" title="Coming soon">Patreon</a>')
    links += f'<a class="nav-cta" href="contact.html"{" aria-current=\"page\"" if active == "contact.html" else ""}>Contact</a>'
    bar = ('<div class="preview-bar">Preview build · placeholder images · not public yet</div>'
           if CFG["preview"] else "")
    return f'''{bar}<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Quantech Graphics home">{BRAND_ANIM}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">MENU</button>
    <nav class="nav" id="site-nav" aria-label="Main">{links}</nav>
  </div>
</header>'''

def footer():
    soc = "".join(
        (f'<li><a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["name"])}</a></li>' if s["url"]
         else f'<li class="soon">{E(s["name"])} · soon</li>') for s in CFG["socials"])
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html" aria-label="Quantech Graphics home">{BRAND}</a>
        <p class="foot-tag">{E(CFG["tagline"])}</p>
        <p class="foot-line">Independent game studio, tools developer and technical art partner. Unreal, Unity, Godot and the web.</p>
      </div>
      <div>
        <h4>Studio</h4>
        <ul>
          <li><a href="vecter-assault.html">Vecter Assault</a></li>
          <li><a href="kits.html">Kits &amp; Tools</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="vecter-assault.html#press">Press kit</a></li>
        </ul>
      </div>
      <div>
        <h4>Developers</h4>
        <ul>
          <li><a href="kit-cqc-stealth.html">CQC Stealth Kit</a></li>
          <li><a href="kit-rig-qa-lab.html">Rig QA Lab</a></li>
          <li><a href="kit-sci-fi-drone.html">Sci-Fi Drone Pack</a></li>
          <li><a href="kit-body-cam.html">Body Cam FPS Kit</a></li>
        </ul>
      </div>
      <div>
        <h4>Follow</h4>
        <ul>{soc}</ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© {YEAR} Quantech Graphics · <a href="mailto:{CFG["email_general"]}">{CFG["email_general"]}</a></span>
      <span><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></span>
    </div>
  </div>
</footer>'''

THEMES = [("ops", "Ops"), ("synapse", "Synapse"), ("chrome", "Chrome")]
FONTS_EXTRA = "https://fonts.googleapis.com/css2?family=Michroma&family=Barlow:wght@400;500;600&family=Share+Tech+Mono&family=Saira+Condensed:wght@600;700;800&family=Saira:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"

def theme_links():
    t = CFG.get("theme", "ops")
    if not CFG.get("theme_switcher"):
        return "" if t == "ops" else f'<link rel="stylesheet" href="{FONTS_EXTRA}">\n<link rel="stylesheet" href="assets/themes/{t}.css">'
    # preview: load all skins, pick one from the switcher (remembered per browser)
    return (f'<link rel="stylesheet" href="{FONTS_EXTRA}">\n'
            + "".join(f'<link rel="stylesheet" href="assets/themes/{k}.css">\n' for k, _ in THEMES if k != "ops")
            + "<script>try{var s=localStorage.getItem('qg-skin');if(s)document.documentElement.setAttribute('data-skin',s)}catch(e){}</script>")

def skin_attr():
    t = CFG.get("theme", "ops")
    return "" if CFG.get("theme_switcher") or t == "ops" else f' data-skin="{t}"'

def switcher():
    if not CFG.get("theme_switcher"):
        return ""
    btns = "".join(f'<button type="button" data-skin-btn="{k}">{E(n)}</button>' for k, n in THEMES)
    return f'<div class="skin-switch" role="group" aria-label="Preview theme"><span>Theme</span>{btns}</div>'

def page(fname, title, desc, body, active=None):
    robots = '<meta name="robots" content="noindex, nofollow">' if CFG["preview"] else ""
    full_title = title if fname == "index.html" else f"{title} · Quantech Graphics"
    url = CFG["site_url"] + ("/" if fname == "index.html" else "/" + fname)
    return f'''<!doctype html>
<html lang="en"{skin_attr()}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(full_title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{CFG["site_url"]}/{img_src("og-default")}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d1115">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="assets/site.css">
{theme_links()}
</head>
<body>
{header(active or fname)}
<main>
{body}
</main>
{footer()}
{switcher()}
<script src="assets/brand/quantech-logo.js"></script>
<script>window.QG_INTRO = "{CFG.get("logo_intro", "first-visit")}";</script>
<script src="assets/site.js"></script>
</body>
</html>
'''

def notify_form(fid, product, button="Notify me"):
    return f'''<form class="inline-form" id="{fid}" data-endpoint="" data-offline-msg="Sign-ups open at launch. For now, email {CFG["email_general"]} and we will add you." data-ok-msg="You are on the list for {E(product)}.">
  <input type="hidden" name="product" value="{E(product)}">
  <input id="{fid}-email" type="email" name="email" placeholder="you@studio.com" aria-label="Email address" required autocomplete="email">
  <button class="btn solid" type="submit">{E(button)}</button>
  <p class="form-msg" aria-live="polite"></p>
</form>'''

# ------------------------------------------------------------------ data
KITS = [
    dict(slug="kit-cqc-stealth", img="kit-cqc-stealth", name="CQC Stealth Kit",
         engines="Unreal 5.6+ · Unity 6 · Web (three.js)",
         badges=[("dev", "In development"), ("ok", "Playable demo")],
         line="Paired stealth takedowns, full-body IK and stealth AI. Grab, choke, disarm, drop.",
         btn="Try the Arena demo", btn_url_key="cqc_demo_url"),
    dict(slug="kit-rig-qa-lab", img="kit-rig-qa-lab", name="Rig QA Lab",
         engines="Unreal · Web viewer (more planned)",
         badges=[("free", "Free web tool"), ("dev", "In development")],
         line="Find bad skin weights before your players do. Heatmaps and scores for rigging and skinning.",
         btn="Get notified", btn_url_key=None),
    dict(slug="kit-sci-fi-drone", img="kit-sci-fi-drone", name="Sci-Fi Drone Pack",
         engines="Unity 6",
         badges=[("dev", "In development")],
         line="Swarms, shields that form around you, sleeper mines that wake on contact. A modular drone AI system for Unity.",
         btn="Get notified", btn_url_key=None),
    dict(slug="kit-body-cam", img="kit-body-cam", name="Body Cam FPS Kit",
         engines="Engines TBC",
         badges=[("off", "Coming soon")],
         line="Raw, real-footage body cam perspective for first-person shooters.",
         btn="Get notified", btn_url_key=None),
]

SERVICES = [
    ("MECH", "Game mechanics development", "Combat, movement, AI and systems in Unreal, Unity, Godot and three.js."),
    ("VFX", "VFX and shader development", "Real-time effects and custom shaders that look great and hold frame rate."),
    ("ASSET", "Game asset development", "Game-ready characters, props and environments, modeled, textured and rigged."),
    ("LEVEL", "Level design", "Playable spaces with flow, cover and pacing, from blockout to final pass."),
    ("TERRA", "Terrain generation and maps", "Procedural and hand-crafted landscapes with Houdini, Gaea and World Creator."),
    ("SIM", "Simulations and 3D software", "Real-time simulations, configurators and custom 3D apps for web and desktop."),
    ("XR", "VR and AR experiences", "Immersive XR for games, training and product showcases."),
]

TOOLSET = ["Unreal Engine", "Unity", "Godot", "three.js", "Blender", "Maya", "Houdini",
           "Substance Painter", "Substance Designer", "World Creator", "Gaea", "Photoshop", "Illustrator"]

def badges(bs):
    return '<div class="badges">' + "".join(f'<span class="badge {c}">{E(t)}</span>' for c, t in bs) + "</div>"

def kit_card(k):
    return f'''<article class="card">
  <a href="{k["slug"]}.html" tabindex="-1" aria-hidden="true">{img(k["img"], k["name"])}</a>
  <div class="card-body">
    <div class="card-meta"><span class="engines">{E(k["engines"])}</span>{badges(k["badges"])}</div>
    <h3><a href="{k["slug"]}.html" style="color:inherit;text-decoration:none">{E(k["name"])}</a></h3>
    <p>{E(k["line"])}</p>
    <a class="btn" href="{k["slug"]}.html">{E(k["btn"])} →</a>
  </div>
</article>'''

def services_grid(with_cta=True):
    tiles = "".join(f'''<div class="service"><span class="code">// {c}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>'''
                    for c, t, d in SERVICES)
    if with_cta:
        tiles += '''<a class="service cta" href="services.html#start"><span class="code">// BRIEF</span><h3>Start a project →</h3><p>Tell us what you are building. We reply within two working days.</p></a>'''
    return f'<div class="services">{tiles}</div>'

def toolset():
    return '<ul class="toolset">' + "".join(f"<li>{E(t)}</li>" for t in TOOLSET) + "</ul>"

def socials_grid():
    return '<div class="socials">' + "".join(social_link(s["key"]) for s in CFG["socials"]) + "</div>"

def join_band():
    return f'''<section class="band" id="join">
  <div class="wrap join">
    <div class="section-head" style="margin:0">
      <span class="readout">Community</span>
      <h2>Join the unit</h2>
      <p>Devlogs, early builds and behind the scenes. Get launch news for Vecter Assault and every kit.</p>
      {notify_form("join-form", "Newsletter", "Sign up")}
    </div>
    {socials_grid()}
  </div>
</section>'''

def discord_btn(cls="btn ghost"):
    return ext_or_soon(SOC["discord"]["url"], "Join the Discord →", cls)

def steam_btn(cls="btn solid"):
    return ext_or_soon(CFG["steam_url"], "Wishlist on Steam →", cls)

# ------------------------------------------------------------------ pages
def rig_qa_btn():
    if CFG["rig_qa_url"]:
        return ext_or_soon(CFG["rig_qa_url"], "Launch Rig QA →")
    return '<a class="btn" href="kit-rig-qa-lab.html#notify">Get notified →</a>'

PAGES = {}

PAGES["index.html"] = ("Quantech Graphics · " + CFG["tagline"].rstrip("."),
    "Quantech Graphics is an independent studio building Vecter Assault, a curved-space multiplayer extraction shooter, plus game dev kits and custom game tech for Unreal, Unity, Godot and the web.",
f'''<section class="hero">
  <div class="hero-media"><img{ph("hero-vecter-assault")} src="{img_src("hero-vecter-assault")}" alt="Vecter Assault key art (placeholder)" loading="eager"></div>
  <div class="hud-corners" aria-hidden="true"></div>
  <div class="wrap">
    <span class="rec">QUANTECH GRAPHICS PRESENTS</span>
    <h1>Vecter<br><span>Assault</span></h1>
    <p class="pitch">A curved-space multiplayer extraction shooter. The battleground wraps 360 degrees around you, so threats come from every angle. Drop in, scavenge, fight, and get out alive.</p>
    <p class="status">Coming soon to Early Access on Steam · PC · Built in Unreal Engine 5</p>
    <div class="btn-row">{steam_btn()}{discord_btn()}</div>
  </div>
</section>

<section class="band">
  <div class="wrap section-head" style="margin:0 auto 40px">
    <span class="readout">Pick your lane</span>
    <h2>{E(CFG["tagline"])}</h2>
    <p class="intro">Quantech Graphics is an independent studio building Vecter Assault, game kits and engine tools for developers, and custom games and simulations for clients across Unreal, Unity, Godot and the web.</p>
  </div>
  <div class="wrap">
    <div class="lanes">
      <a class="lane" href="vecter-assault.html"><span class="idx">THE GAME</span><h3>Vecter Assault</h3><p>In development on Unreal Engine 5.</p><span class="go">See the game →</span></a>
      <a class="lane" href="kits.html"><span class="idx">KITS &amp; TOOLS</span><h3>Gear up your project</h3><p>Production kits and tools for Unreal, Unity and the web.</p><span class="go">Browse kits →</span></a>
      <a class="lane" href="services.html"><span class="idx">SERVICES</span><h3>Hire the squad</h3><p>Mechanics, VFX, worlds and XR, built to ship.</p><span class="go">See services →</span></a>
    </div>
  </div>
</section>

<section class="band alt" id="kits">
  <div class="wrap">
    <div class="section-head">
      <span class="readout">Kits &amp; Tools</span>
      <h2>Gear up your project</h2>
      <p>Production kits and tools for Unreal, Unity and the web.</p>
    </div>
    <div class="cards">{"".join(kit_card(k) for k in KITS)}</div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="readout">Free tools</span>
      <h2>Try it in your browser</h2>
      <p>Play before you buy. No install, no account.</p>
    </div>
    <div class="strip">
      <div class="tool">{img("tool-cqc-arena", "CQC Arena demo", "")}<div class="stack"><span class="badge ok">Playable</span><h3>CQC Arena</h3><p>Run the stealth takedown sandbox in your browser.</p>{ext_or_soon(CFG["cqc_demo_url"], "Play the demo →", "btn", "Demo link coming soon")}</div></div>
      <div class="tool">{img("tool-rig-qa", "Rig QA web viewer", "")}<div class="stack"><span class="badge free">Free</span><h3>Rig QA Web</h3><p>Upload a character, see where the rigging and skinning break.</p>{rig_qa_btn()}</div></div>
    </div>
  </div>
</section>

<section class="band alt" id="services">
  <div class="wrap">
    <div class="section-head">
      <span class="readout">Services</span>
      <h2>Hire the squad</h2>
      <p>The team behind Vecter Assault and our kits, available for your project.</p>
    </div>
    {services_grid()}
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head"><span class="readout">Toolset</span><h2>What we build with</h2></div>
    {toolset()}
  </div>
</section>

{join_band()}''')

PAGES["vecter-assault.html"] = ("Vecter Assault",
    "Vecter Assault is a curved-space multiplayer extraction shooter in development on Unreal Engine 5. Coming soon to Early Access on Steam.",
f'''<section class="hero">
  <div class="hero-media"><img{ph("hero-vecter-assault")} src="{img_src("hero-vecter-assault")}" alt="Vecter Assault key art (placeholder)" loading="eager"></div>
  <div class="hud-corners" aria-hidden="true"></div>
  <div class="wrap">
    <span class="crumbs"><a href="index.html">Home</a> / The game</span>
    <h1>Vecter<br><span>Assault</span></h1>
    <p class="pitch">A curved-space multiplayer extraction shooter. The battleground wraps 360 degrees around you, so threats come from every angle. Drop in, scavenge, fight, and get out alive.</p>
    <p class="status">Coming soon to Early Access on Steam · PC · Built in Unreal Engine 5</p>
    <div class="btn-row">{steam_btn()}{discord_btn()}</div>
  </div>
</section>

<section class="band" id="trailer">
  <div class="wrap">
    <div class="section-head"><span class="readout">Trailer</span><h2>Watch the drop</h2></div>
    {img("va-trailer", "Trailer placeholder")}
    <div class="btn-row" style="margin-top:20px">{ext_or_soon(CFG["trailer_url"], "Watch trailer on YouTube →", "btn", "Trailer coming soon")}</div>
  </div>
</section>

<section class="band alt">
  <div class="wrap">
    <div class="section-head"><span class="readout">The loop</span><h2>Drop. Scavenge. Fight. Extract.</h2></div>
    <ul class="features">
      <li><b>360° battleground</b><span>The map curves around you. High ground, cover and sightlines work in every direction.</span></li>
      <li><b>Drop in</b><span>Deploy into a curved-space battleground alongside other players.</span></li>
      <li><b>Scavenge</b><span>Search the map for gear and supplies, and decide what is worth the risk.</span></li>
      <li><b>Fight</b><span>Engage other players from every angle the curved arena allows.</span></li>
      <li><b>Get out alive</b><span>Reach extraction to keep what you found.</span></li>
      <li><b>Built in UE5</b><span>Developed in Unreal Engine 5 for PC.</span></li>
    </ul>
  </div>
</section>

<section class="band" id="screens">
  <div class="wrap">
    <div class="section-head"><span class="readout">Screenshots</span><h2>From the field</h2></div>
    <div class="shots">{"".join(img(f"va-shot-{i}", f"Vecter Assault screenshot {i} (placeholder)") for i in range(1, 7))}</div>
  </div>
</section>

<section class="band alt" id="roadmap">
  <div class="wrap split">
    <div class="section-head" style="margin:0"><span class="readout">Roadmap</span><h2>Where we are</h2><p>Follow progress on Discord and YouTube.</p></div>
    <ol class="roadmap">
      <li class="now"><b>In development</b><span>Core extraction loop on Unreal Engine 5.</span></li>
      <li><b>Steam page refresh</b><span>Updated store copy, trailer and screenshots.</span></li>
      <li><b>Playtests</b><span>Dates announced on Discord first.</span></li>
      <li><b>Early Access on Steam</b><span>PC. Date to be announced.</span></li>
    </ol>
  </div>
</section>

<section class="band" id="press">
  <div class="wrap split">
    <div class="section-head" style="margin:0"><span class="readout">Press kit</span><h2>For press and creators</h2><p>Logos, key art, screenshots and fact sheet. Press enquiries: <a href="mailto:{CFG["email_press"]}">{CFG["email_press"]}</a></p></div>
    <dl class="specs">
      <dt>Title</dt><dd>Vecter Assault</dd>
      <dt>Developer</dt><dd>Quantech Graphics</dd>
      <dt>Genre</dt><dd>Curved-space multiplayer extraction shooter</dd>
      <dt>Platform</dt><dd>PC (Steam)</dd>
      <dt>Engine</dt><dd>Unreal Engine 5</dd>
      <dt>Release</dt><dd>Coming soon to Early Access</dd>
      <dt>Press kit</dt><dd>Download link coming soon</dd>
    </dl>
  </div>
</section>

{join_band()}''')

PAGES["kits.html"] = ("Kits & Tools",
    "Production kits and tools for Unreal, Unity and the web: CQC Stealth Kit, Rig QA Lab, Sci-Fi Drone Pack and Body Cam FPS Kit.",
f'''<section class="page-head"><div class="wrap">
  <span class="crumbs"><a href="index.html">Home</a> / Kits &amp; Tools</span>
  <h1>Gear up your project</h1>
  <p>Production kits and tools for Unreal, Unity and the web.</p>
</div></section>
<section class="band"><div class="wrap"><div class="cards">{"".join(kit_card(k) for k in KITS)}</div>
<p class="note">// Pricing will be listed when each kit launches.</p></div></section>
{join_band()}''')

def kit_page(fname, k, headline, intro, features, specs, extra=""):
    feats = "".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a, b in features)
    sp = "".join(f"<dt>{E(a)}</dt><dd>{b}</dd>" for a, b in specs)
    PAGES[fname] = (k["name"], k["line"], f'''<section class="page-head"><div class="wrap">
  <span class="crumbs"><a href="index.html">Home</a> / <a href="kits.html">Kits &amp; Tools</a> / {E(k["name"])}</span>
  {badges(k["badges"])}
  <h1>{E(headline)}</h1>
  <p>{E(k["name"])} · {E(k["engines"])}</p>
</div></section>
<section class="band"><div class="wrap split">
  {img(k["img"], k["name"] + " (placeholder)")}
  <div class="prose">
    <span class="readout">Overview</span>
    <p>{E(intro)}</p>
    {extra}
  </div>
</div></section>
<section class="band alt"><div class="wrap">
  <div class="section-head"><span class="readout">Features</span><h2>What is inside</h2></div>
  <ul class="features">{feats}</ul>
</div></section>
<section class="band" id="notify"><div class="wrap split">
  <div class="section-head" style="margin:0"><span class="readout">Status</span><h2>Get launch news</h2><p>Leave your email and we will tell you when {E(k["name"])} is ready.</p>{notify_form(fname.replace(".html","") + "-notify", k["name"])}</div>
  <dl class="specs">{sp}</dl>
</div></section>''', "kits.html")

K = {k["slug"]: k for k in KITS}

kit_page("kit-cqc-stealth.html", K["kit-cqc-stealth"], "Silent. Close. Final.",
    "A stealth close-quarters combat system for action and tactical games. Paired attacker and victim takedowns line up perfectly every time, driven by full-body IK, stealth AI and physics ragdolls.",
    [("17 paired takedowns", "11 stealth and 6 combat moves."),
     ("Full-body IK", "Two-bone and FABRIK solvers keep both characters planted."),
     ("Stealth AI", "Perception, awareness and patrols."),
     ("Physics ragdolls", "Bodies drop with weight."),
     ("Animation Lab", "Scrubber, ghost preview, metrics and export."),
     ("Blender pipeline", "Bring your own animations.")],
    [("Engines", "Unreal Engine 5.6+ plugin · Unity 6 package · browser prototype"),
     ("Status", "In development · playable web demo"),
     ("Price", "Announced at launch")],
    f'<p class="muted">Play it in your browser before you buy.</p><div class="btn-row">{ext_or_soon(CFG["cqc_demo_url"], "Try the Arena demo →", "btn solid", "Demo link coming soon")}</div>')

kit_page("kit-rig-qa-lab.html", K["kit-rig-qa-lab"], "Check your rig.",
    "Upload your character, see exactly where the rigging and skinning break. Free, in your browser, no install. Heatmaps show bad skin weights and problem joints, with a quality score per rig.",
    [("Skin weight heatmaps", "See bad weights at a glance."),
     ("Problem joints", "Flag joints that pinch, collapse or stretch."),
     ("Rig quality score", "One score per rig, so you can track fixes."),
     ("Free web tool", "Runs in your browser. No install."),
     ("Unreal plugin", "The same checks inside Unreal Engine.")],
    [("Platforms", "Web viewer · Unreal (more planned)"),
     ("Status", "In development"),
     ("Price", "Web tool is free")],
    f'<div class="btn-row">{ext_or_soon(CFG["rig_qa_url"], "Launch Rig QA →", "btn solid", "Web tool coming soon")}</div>')

kit_page("kit-sci-fi-drone.html", K["kit-sci-fi-drone"], "Deploy the swarm.",
    "A modular sci-fi drone system for Unity. Build a drone from small modules, give it a behavior, and command one drone or a whole swarm through a single, clean API.",
    [("Swarms", "Flocking AI with spatial-hash hit detection."),
     ("Shield formations", "Drones wrap around a target and repair their own gaps."),
     ("Sector sweep", "Surveillance patterns across a search volume."),
     ("Sleeper mines", "Wake, launch and intercept."),
     ("8 movement styles · 10 attack patterns", "Orbit and Sting, Perimeter Collapse, EMP Cloud, Adhesive Mine and more."),
     ("Weapons", "Bullet, missile, laser and EMP."),
     ("9-state drone AI", "Clear, debuggable behavior states."),
     ("5 editor windows", "Drone Builder, Swarm Designer, Shield Formation, Patrol and Sector Editor, Weapon Preset Editor."),
     ("6 sample scenes", "Drop in and play.")],
    [("Engine", "Unity 6"), ("Status", "In development"), ("Price", "Announced at launch")])

kit_page("kit-body-cam.html", K["kit-body-cam"], "Under construction.",
    "Raw, real-footage body cam perspective for first-person shooters. We are building it now. Sign up to hear first when it is ready.",
    [("In development", "The full feature list is coming soon. Sign up below to hear first.")],
    [("Engines", "TBC"), ("Status", "Coming soon"), ("Price", "Announced at launch")])

PAGES["services.html"] = ("Services",
    "Game development services: mechanics, VFX and shaders, game assets, level design, terrain and maps, simulations and VR/AR, in Unreal, Unity, Godot and three.js.",
f'''<section class="page-head"><div class="wrap">
  <span class="crumbs"><a href="index.html">Home</a> / Services</span>
  <h1>Hire the squad</h1>
  <p>The team behind Vecter Assault and our kits, available for your project. Mechanics, VFX, worlds and XR, built to ship.</p>
</div></section>
<section class="band"><div class="wrap">{services_grid(False)}</div></section>
<section class="band alt"><div class="wrap">
  <div class="section-head"><span class="readout">Toolset</span><h2>What we build with</h2></div>
  {toolset()}
</div></section>
<section class="band" id="start"><div class="wrap split">
  <div class="section-head" style="margin:0"><span class="readout">Start a project</span><h2>Brief us</h2><p>Tell us what you are building, your engine and your timeline. We reply within two working days. Prefer email? <a href="mailto:{CFG["email_general"]}">{CFG["email_general"]}</a></p></div>
  <form class="form" id="project-form" data-endpoint="" data-offline-msg="The form is not connected yet. Email {CFG["email_general"]} for now." data-ok-msg="Brief received. We will reply within two working days.">
    <div class="row">
      <div class="field"><label for="pf-name">Name</label><input id="pf-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="pf-email">Email</label><input id="pf-email" name="email" type="email" required autocomplete="email"></div>
    </div>
    <div class="row">
      <div class="field"><label for="pf-service">Service</label><select id="pf-service" name="service">{"".join(f"<option>{E(t)}</option>" for _, t, _ in SERVICES)}<option>Something else</option></select></div>
      <div class="field"><label for="pf-engine">Engine</label><select id="pf-engine" name="engine"><option>Unreal Engine</option><option>Unity</option><option>Godot</option><option>three.js / Web</option><option>Not sure yet</option></select></div>
    </div>
    <div class="field"><label for="pf-brief">Project brief</label><textarea id="pf-brief" name="brief" required placeholder="What are you building, and what do you need from us?"></textarea></div>
    <div><button class="btn solid" type="submit">Send brief →</button></div>
    <p class="form-msg" aria-live="polite"></p>
  </form>
</div></section>''')

PAGES["contact.html"] = ("Contact",
    "Contact Quantech Graphics for client work, kit support and press.",
f'''<section class="page-head"><div class="wrap">
  <span class="crumbs"><a href="index.html">Home</a> / Contact</span>
  <h1>Contact</h1>
  <p>Client work, kit questions or press. Pick a channel.</p>
</div></section>
<section class="band"><div class="wrap contact-grid">
  <div>
    <div class="contact-line"><span class="readout">General and client enquiries</span><a href="mailto:{CFG["email_general"]}">{CFG["email_general"]}</a></div>
    <div class="contact-line"><span class="readout">Press</span><a href="mailto:{CFG["email_press"]}">{CFG["email_press"]}</a></div>
    <div class="contact-line"><span class="readout">Start a project</span><a href="services.html#start">Send a brief →</a></div>
  </div>
  <div class="prose"><span class="readout">Find us</span>{socials_grid()}</div>
</div></section>''')

LEGAL_NOTE = '<div class="callout"><b>Draft placeholder.</b> This page needs real text before launch.</div>'
PAGES["privacy.html"] = ("Privacy", "Quantech Graphics privacy policy.",
f'''<section class="page-head"><div class="wrap"><span class="crumbs"><a href="index.html">Home</a> / Privacy</span><h1>Privacy</h1></div></section>
<section class="band"><div class="wrap legal">
<h2>What we collect</h2><p>When you sign up for updates or send a brief, we collect the email address and details you give us. We use them only to reply and to send the updates you asked for.</p>
<h2>Cookies and analytics</h2><p>This site does not use cookies or analytics trackers. Fonts are served by Google Fonts, and the site is hosted on GitHub Pages, which may log basic technical data such as IP addresses for security.</p><h2>Your choices</h2><p>You can ask us to delete any details you have sent us at any time.</p>
<h2>Contact</h2><p>Questions: <a href="mailto:{CFG["email_general"]}">{CFG["email_general"]}</a></p></div></section>''')
PAGES["terms.html"] = ("Terms", "Quantech Graphics terms of use.",
f'''<section class="page-head"><div class="wrap"><span class="crumbs"><a href="index.html">Home</a> / Terms</span><h1>Terms</h1></div></section>
<section class="band"><div class="wrap legal">
<h2>Use of this site</h2><p>The content on this site, including text, images and trademarks such as Vecter Assault, belongs to Quantech Graphics unless stated otherwise. You may link to and share our pages, but please do not copy or republish our content without permission.</p><h2>Kits and licenses</h2><p>Each kit will ship with its own license terms, published on its product page at launch.</p><h2>Contact</h2><p>Questions: <a href="mailto:{CFG["email_general"]}">{CFG["email_general"]}</a></p></div></section>''')
PAGES["404.html"] = ("Signal lost", "Page not found.",
'''<section class="page-head"><div class="wrap"><span class="rec">ERROR 404</span><h1>Signal lost</h1><p>That page does not exist. Head back to base.</p><div class="btn-row"><a class="btn solid" href="index.html">Back to home →</a></div></div></section>''')

# ------------------------------------------------------------------ build
def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets" / "img").mkdir(parents=True)
    shutil.copy(SRC / "assets" / "site.css", DIST / "assets" / "site.css")
    shutil.copy(SRC / "assets" / "site.js", DIST / "assets" / "site.js")
    shutil.copytree(SRC / "assets" / "themes", DIST / "assets" / "themes")
    shutil.copytree(SRC / "assets" / "brand", DIST / "assets" / "brand")
    mark = (SRC / "assets" / "brand" / "mark.svg").read_text()
    fav = mark.replace('viewBox="813 377 278 203"', 'viewBox="797 323 310 310"').replace(
        "<title>Quantech Graphics</title>", '<rect x="797" y="323" width="310" height="310" rx="56" fill="#0b1015"/>')
    (DIST / "assets" / "favicon.svg").write_text(fav)
    for name, (w, h, label) in IMG_SLOTS.items():
        src = img_src(name)
        if src.endswith(".svg"):
            (DIST / src).write_text(placeholder_svg(name, w, h, label))
        else:
            shutil.copy(SRC / src, DIST / src)
    for fname, (title, desc, body, *active) in PAGES.items():
        (DIST / fname).write_text(page(fname, title, desc, body, active[0] if active else None))
    robots = "User-agent: *\nDisallow: /\n" if CFG["preview"] else f"User-agent: *\nAllow: /\nSitemap: {CFG['site_url']}/sitemap.xml\n"
    (DIST / "robots.txt").write_text(robots)
    urls = "".join(f"<url><loc>{CFG['site_url']}/{'' if f == 'index.html' else f}</loc></url>"
                   for f in PAGES if f != "404.html")
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (DIST / "CNAME").write_text("quantechgraphics.com\n")
    (DIST / ".nojekyll").write_text("")
    print(f"Built {len(PAGES)} pages into {DIST}")

if __name__ == "__main__":
    build()
