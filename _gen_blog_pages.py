# -*- coding: utf-8 -*-
"""Generate SEO cheat blog pages for every catalog product."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"c:\Users\ii\articles")
PRODUCTS = json.loads((ROOT / "_gen_products.json").read_text(encoding="utf-8"))
OUT = ROOT / "blogs"

# Genre hints for tighter, non-generic copy (still cheat-keyword focused)
GENRE = {
    "escape-from-tarkov": "raid",
    "rust": "survival",
    "dayz": "survival",
    "pubg": "br",
    "battlefield-6": "fps",
    "call-of-duty-black-ops-7": "fps",
    "call-of-duty-black-ops-6": "fps",
    "valorant": "tactical",
    "cs2": "tactical",
    "counter-strike-2": "tactical",
    "fortnite": "br",
    "apex-legends": "br",
    "warzone": "br",
    "rainbow-six-siege": "tactical",
    "destiny-2": "looter",
    "warframe": "looter",
    "gta-5": "open",
    "gta-online": "open",
    "roblox": "sandbox",
    "minecraft": "sandbox",
    "ark": "survival",
    "scum": "survival",
    "hunt-showdown": "tactical",
    "dead-by-daylight": "asymmetric",
}

TICK = (
    '<svg class="tick" viewBox="0 0 20 20" aria-hidden="true">'
    '<path fill="currentColor" d="M7.7 14.3 3.4 10l1.4-1.4 2.9 2.9 7-7L16.1 6l-8.4 8.3z"/>'
    "</svg>"
)
CROSS = (
    '<svg class="cross" viewBox="0 0 20 20" aria-hidden="true">'
    '<path fill="currentColor" d="M5.3 4 4 5.3 8.7 10 4 14.7 5.3 16 10 11.3 14.7 16 16 14.7 11.3 10 16 5.3 14.7 4 10 8.7 5.3 4z"/>'
    "</svg>"
)


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def kw_name(name: str) -> str:
    return f"{name} cheats"


def meta_title(name: str) -> str:
    # Primary keyword first; keep under ~60 chars when possible
    base = f"{name} Cheats"
    if len(base) <= 42:
        return f"{base} | Aimbot, ESP & Spoofer"
    if len(base) <= 52:
        return f"{base} | Aimbot & ESP"
    return f"{base} | Buy Undetected"


def meta_desc(name: str, genre: str) -> str:
    hooks = {
        "raid": f"Buy {name} cheats with loot ESP, player ESP, aimbot and HWID spoofer. Undetected builds, instant delivery, 24/7 support.",
        "survival": f"Get {name} cheats: ESP, aimbot, no recoil and spoofer tools. Instant delivery after purchase. Built for long sessions.",
        "br": f"{name} cheats with aimbot, ESP/wallhack and spoofer. Compare features, pick a plan, get instant access.",
        "fps": f"Shop {name} cheats — aimbot, ESP, triggerbot and HWID spoofer. Undetected options with instant delivery.",
        "tactical": f"{name} cheats focused on ESP, aimbot and stream-proof overlays. Instant delivery, clear feature comparison.",
        "looter": f"{name} cheats: ESP for loot and players, aim assist and spoofer. Instant delivery after checkout.",
        "open": f"Buy {name} cheats with ESP, aimbot, money tools and spoofer where available. Instant delivery.",
        "sandbox": f"{name} cheats and scripts — ESP, aim helpers and quality-of-life tools. Instant delivery.",
        "asymmetric": f"{name} cheats with ESP, aura reads and aim assist. Instant delivery and active updates.",
    }
    d = hooks.get(genre, f"Buy {name} cheats with aimbot, ESP and spoofer. Instant delivery, feature comparison, and support.")
    return d[:158]


def lead(name: str, genre: str) -> str:
    lines = {
        "raid": f"{name} cheats are built for extraction play: see players, loot and extracts before you push. This page covers aimbot, ESP and spoofer options you can buy now.",
        "survival": f"If you run {name}, cheats that show people and loot through walls cut the grind. Below is a straight feature comparison for aimbot, ESP and spoofer builds.",
        "br": f"{name} cheats stack aimbot and ESP so fights start on your terms. Compare plans, then buy with instant delivery.",
        "fps": f"{name} cheats center on aimbot tracking, ESP boxes and a HWID spoofer when you need a clean load. Features and status are listed below.",
        "tactical": f"{name} is round-based and information-heavy. These cheats prioritize ESP and controlled aimbot — not loud public paste junk.",
        "looter": f"{name} cheats help you find targets and rare drops faster with ESP, then finish fights with aim assist.",
        "open": f"{name} cheats focus on ESP, combat helpers and account safety tools like a spoofer where the build includes one.",
        "sandbox": f"{name} cheats and helpers here are keyed to ESP and aim tools players actually search for — not filler blog text.",
        "asymmetric": f"{name} cheats lean on ESP and aura-style reads so you know where pressure is coming from.",
    }
    return lines.get(
        genre,
        f"{name} cheats on this page are keyworded to what buyers search for: aimbot, ESP, wallhack and spoofer — with a clear comparison before you buy.",
    )


def bullets(name: str) -> list[str]:
    return [
        f"Aimbot for {name} with FOV, smooth and bone options on supported builds",
        f"ESP / wallhack for players, bots and key world objects in {name}",
        f"HWID spoofer pairing on select {name} cheats after hardware risk",
        f"Instant delivery — license details after payment clears",
        f"Active updates when {name} patches break older cheats",
    ]


def faq(name: str) -> list[tuple[str, str]]:
    return [
        (
            f"Are {name} cheats undetected?",
            f"Status changes after every {name} patch. We list the current status on the product and update builds when detection hits. Always read the latest note before you inject or load.",
        ),
        (
            f"What do {name} cheats include?",
            f"Most packs combine aimbot, ESP (player and/or loot) and optional extras like no recoil, triggerbot or a HWID spoofer. The comparison table on this page shows what each tier covers.",
        ),
        (
            f"How fast is delivery for {name} cheats?",
            "Delivery is instant after payment. You get load instructions and license access without waiting on a ticket queue.",
        ),
        (
            f"Can I use a spoofer with {name} cheats?",
            f"Yes on builds that ship a built-in spoofer or list Gouda/HWID support. If you already have a hardware ban on {name}, use a spoofer before the first launch.",
        ),
    ]


def related(products: list[dict], current: str, n: int = 6) -> list[dict]:
    others = [p for p in products if p["slug"] != current]
    # stable pseudo-shuffle by slug hash
    others = sorted(others, key=lambda p: (hash(p["slug"] + current) & 0xFFFF))
    return others[:n]


def page_html(p: dict, all_products: list[dict]) -> str:
    name = p["name"]
    slug = p["slug"]
    img = p["img"]
    gif = p.get("gif") or ""
    genre = GENRE.get(slug, "fps")
    title = meta_title(name)
    desc = meta_desc(name, genre)
    canonical = f"https://example.com/blogs/{slug}"  # relative-friendly; use path in link
    path_canon = f"/blogs/{slug}"
    hero_src = gif or img
    media = (
        f'<img class="hero-img" src="{esc(img)}" alt="{esc(name)} cheats" width="381" height="434" '
        f'loading="eager" decoding="async"'
        + (f' data-gif="{esc(gif)}"' if gif else "")
        + "/>"
    )
    if gif:
        media = (
            f'<img class="hero-img" src="{esc(img)}" data-img="{esc(img)}" data-gif="{esc(gif)}" '
            f'alt="{esc(name)} cheats gameplay" width="381" height="434" loading="eager"/>'
        )

    feat_rows = [
        ("Aimbot", True, True, False),
        ("ESP / Wallhack", True, True, True),
        ("Triggerbot", True, False, False),
        ("No recoil / weapon helpers", True, True, False),
        ("HWID Spoofer", True, False, False),
        ("Stream-proof mode", True, False, False),
        ("Instant delivery", True, True, True),
        ("24/7 support", True, True, False),
    ]

    def cell(ok: bool) -> str:
        return f'<td class="{"yes" if ok else "no"}">{TICK if ok else CROSS}</td>'

    rows_html = "\n".join(
        f"<tr><th scope=\"row\">{esc(label)}</th>{cell(a)}{cell(b)}{cell(c)}</tr>"
        for label, a, b, c in feat_rows
    )

    bullet_html = "".join(f"<li>{TICK}<span>{esc(b)}</span></li>" for b in bullets(name))
    faq_html = "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq(name)
    )
    rel = related(all_products, slug)
    rel_html = "".join(
        f'<a class="rel" href="/blogs/{esc(r["slug"])}">'
        f'<img src="{esc(r["img"])}" alt="{esc(r["name"])} cheats" loading="lazy" width="120" height="137"/>'
        f"<span>{esc(r['name'])} Cheats</span></a>"
        for r in rel
    )

    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": f"{name} Cheats",
        "description": desc,
        "image": img,
        "brand": {"@type": "Brand", "name": "Cheat Catalog"},
        "category": "Game Cheats",
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "priceCurrency": "USD",
            "url": path_canon,
        },
    }
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq(name)
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}"/>
  <meta name="robots" content="index,follow,max-image-preview:large"/>
  <meta name="keywords" content="{esc(name)} cheats, {esc(name)} aimbot, {esc(name)} ESP, {esc(name)} wallhack, {esc(name)} spoofer, buy {esc(name)} cheats, undetected {esc(name)} cheats"/>
  <link rel="canonical" href="{esc(path_canon)}"/>
  <meta property="og:type" content="product"/>
  <meta property="og:title" content="{esc(title)}"/>
  <meta property="og:description" content="{esc(desc)}"/>
  <meta property="og:url" content="{esc(path_canon)}"/>
  <meta property="og:image" content="{esc(img)}"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{esc(title)}"/>
  <meta name="twitter:description" content="{esc(desc)}"/>
  <meta name="twitter:image" content="{esc(img)}"/>
  <link rel="icon" href="/favicon.ico"/>
  <link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&display=swap" rel="stylesheet"/>
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
  <style>
    :root {{
      --bg:#090819; --card:#12102a; --line:rgba(255,255,255,.10);
      --text:#E2E8FF; --muted:#ABB0C7; --accent:#8B5CF6; --ok:#34d399; --bad:#f87171;
    }}
    * {{ box-sizing:border-box; }}
    html {{ scrollbar-width:thin; scrollbar-color:#8B5CF6 #1a1535; }}
    body {{
      margin:0; font-family:Onest,system-ui,sans-serif; color:var(--text);
      background:linear-gradient(180deg,#100e2b 0%, var(--bg) 40%);
      line-height:1.55;
    }}
    a {{ color:#c4b5fd; text-decoration:none; }}
    a:hover {{ color:#fff; }}
    .top {{
      position:sticky; top:0; z-index:20; display:flex; align-items:center; justify-content:space-between;
      gap:1rem; padding:.85rem 1.25rem; background:rgba(9,8,25,.92); border-bottom:1px solid var(--line);
      backdrop-filter:blur(8px);
    }}
    .top nav {{ display:flex; gap:1.1rem; font-size:.9rem; font-weight:600; }}
    .top img {{ display:block; width:36px; height:36px; }}
    .wrap {{ width:min(1080px, calc(100% - 2rem)); margin:0 auto; padding:2rem 0 4rem; }}
    .crumb {{ color:var(--muted); font-size:.85rem; margin-bottom:1.25rem; }}
    .hero {{
      display:grid; grid-template-columns: minmax(200px,280px) 1fr; gap:1.75rem; align-items:start;
      margin-bottom:2rem;
    }}
    .hero-media {{
      aspect-ratio:381/434; border-radius:1.1rem; overflow:hidden; border:1px solid var(--line);
      background:#100e28; box-shadow:0 12px 30px rgba(0,0,0,.38);
    }}
    .hero-img {{ width:100%; height:100%; object-fit:cover; display:block; }}
    h1 {{
      margin:0 0 .6rem; font-size:clamp(1.7rem, 3vw, 2.35rem); line-height:1.15; font-weight:700;
      background:linear-gradient(90deg,#5D88FF,#8560FF); -webkit-background-clip:text; background-clip:text; color:transparent;
    }}
    .lead {{ color:var(--muted); margin:0 0 1.1rem; max-width:38rem; }}
    .cta {{
      display:inline-flex; align-items:center; gap:.5rem; padding:.7rem 1.15rem; border-radius:999px;
      background:linear-gradient(90deg,#6739FF,#6E52C3); color:#fff !important; font-weight:700; font-size:.95rem;
    }}
    .cta:hover {{ filter:brightness(1.08); }}
    .grid-2 {{ display:grid; grid-template-columns:1.1fr .9fr; gap:1.25rem; margin:1.75rem 0; }}
    section {{
      background:rgba(18,16,42,.72); border:1px solid var(--line); border-radius:1rem; padding:1.15rem 1.25rem;
    }}
    h2 {{ margin:0 0 .85rem; font-size:1.15rem; }}
    h3 {{ margin:1.1rem 0 .5rem; font-size:1rem; color:#d6d4ff; }}
    .ticks {{ list-style:none; margin:0; padding:0; display:grid; gap:.65rem; }}
    .ticks li {{ display:flex; gap:.65rem; align-items:flex-start; color:var(--text); font-size:.95rem; }}
    .tick, .cross {{ width:18px; height:18px; flex:0 0 18px; margin-top:.15rem; }}
    .tick {{ color:var(--ok); }}
    .cross {{ color:var(--bad); opacity:.85; }}
    .compare {{ width:100%; border-collapse:collapse; font-size:.9rem; }}
    .compare th, .compare td {{ padding:.65rem .55rem; border-bottom:1px solid var(--line); text-align:left; }}
    .compare thead th {{ color:var(--muted); font-weight:600; font-size:.78rem; text-transform:uppercase; letter-spacing:.04em; }}
    .compare tbody th {{ font-weight:500; color:var(--text); }}
    .compare td {{ text-align:center; }}
    .compare td.yes {{ color:var(--ok); }}
    .compare td.no {{ color:var(--bad); }}
    .compare .tick, .compare .cross {{ margin:0 auto; display:block; }}
    details {{ border-top:1px solid var(--line); padding:.75rem 0; }}
    details:first-of-type {{ border-top:0; }}
    summary {{ cursor:pointer; font-weight:600; }}
    details p {{ margin:.55rem 0 0; color:var(--muted); }}
    .rels {{
      display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:.85rem; margin-top:1rem;
    }}
    .rel {{
      display:flex; flex-direction:column; gap:.45rem; color:var(--text); font-size:.82rem; font-weight:600; text-align:center;
    }}
    .rel img {{
      width:100%; aspect-ratio:381/434; object-fit:cover; border-radius:.85rem; border:1px solid var(--line); background:#100e28;
    }}
    footer {{ margin-top:2.5rem; color:var(--muted); font-size:.85rem; text-align:center; }}
    @media (max-width:860px) {{
      .hero, .grid-2 {{ grid-template-columns:1fr; }}
      .hero-media {{ max-width:280px; }}
      .top nav a:nth-child(n+3) {{ display:none; }}
    }}
  </style>
</head>
<body>
  <header class="top">
    <a href="/" aria-label="Home"><img src="/images/logo-48.png?v=7" alt="Logo" width="36" height="36"/></a>
    <nav>
      <a href="/">Home</a>
      <a href="/blogs/">Blogs</a>
      <a href="/contact">Contact</a>
    </nav>
  </header>
  <main class="wrap">
    <p class="crumb"><a href="/">Home</a> / <a href="/blogs/">Blogs</a> / <span>{esc(name)} Cheats</span></p>
    <div class="hero">
      <div class="hero-media">{media}</div>
      <div>
        <h1>{esc(name)} Cheats</h1>
        <p class="lead">{esc(lead(name, genre))}</p>
        <a class="cta" href="/contact">Get {esc(name)} Cheats</a>
      </div>
    </div>

    <div class="grid-2">
      <section>
        <h2>{esc(name)} cheat features</h2>
        <ul class="ticks">{bullet_html}</ul>
        <h3>Why buyers open this page</h3>
        <p style="color:var(--muted);margin:0">
          Search demand for <strong style="color:var(--text)">{esc(name)} cheats</strong> clusters around aimbot, ESP, wallhack and spoofer.
          This page stays on those terms — no gift-card filler, no unrelated rewards copy.
        </p>
      </section>
      <section>
        <h2>Quick facts</h2>
        <ul class="ticks">
          <li>{TICK}<span>Primary keyword: <strong>{esc(name)} cheats</strong></span></li>
          <li>{TICK}<span>Secondary: {esc(name)} aimbot, {esc(name)} ESP, {esc(name)} spoofer</span></li>
          <li>{TICK}<span>Delivery: instant after payment</span></li>
          <li>{TICK}<span>Support: contact page for load help</span></li>
        </ul>
      </section>
    </div>

    <section>
      <h2>{esc(name)} cheats comparison</h2>
      <p style="color:var(--muted);margin:0 0 1rem">
        Side-by-side look at common {esc(name)} cheat tiers. Green ticks mean the feature ships on that plan; red means it does not.
      </p>
      <div style="overflow-x:auto">
        <table class="compare">
          <thead>
            <tr>
              <th scope="col">Feature</th>
              <th scope="col">Pro cheats</th>
              <th scope="col">Standard</th>
              <th scope="col">ESP only</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </div>
    </section>

    <section style="margin-top:1.25rem">
      <h2>How to buy {esc(name)} cheats</h2>
      <ol style="margin:0;padding-left:1.15rem;color:var(--muted)">
        <li style="margin:.35rem 0">Pick the tier that matches the ticks you need (aimbot vs ESP-only).</li>
        <li style="margin:.35rem 0">Checkout — license and load steps arrive instantly.</li>
        <li style="margin:.35rem 0">If you need a clean HWID after a ban, use the spoofer path before launching {esc(name)}.</li>
        <li style="margin:.35rem 0">Questions go to <a href="/contact">Contact</a>.</li>
      </ol>
    </section>

    <section style="margin-top:1.25rem">
      <h2>{esc(name)} cheats FAQ</h2>
      {faq_html}
    </section>

    <section style="margin-top:1.25rem">
      <h2>More game cheats</h2>
      <div class="rels">{rel_html}</div>
    </section>

    <footer>
      <p><a href="/blogs/">All cheat blogs</a> · <a href="/">Catalog</a> · <a href="/contact">Contact</a></p>
      <p>&copy; Cheat Catalog — pages keyworded for game cheats only.</p>
    </footer>
  </main>
  <script>
    (function () {{
      var img = document.querySelector(".hero-img[data-gif]");
      if (!img) return;
      var still = img.getAttribute("data-img");
      var gif = img.getAttribute("data-gif");
      var box = img.parentElement;
      box.addEventListener("mouseenter", function () {{ img.src = gif; }});
      box.addEventListener("mouseleave", function () {{ img.src = still; }});
    }})();
  </script>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    urls = ["/blogs/", "/"]
    for p in PRODUCTS:
        slug = p["slug"]
        folder = OUT / slug
        folder.mkdir(parents=True, exist_ok=True)
        html = page_html(p, PRODUCTS)
        (folder / "index.html").write_text(html, encoding="utf-8")
        urls.append(f"/blogs/{slug}/")
        print("wrote", slug)

    # sitemap + robots
    body = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        body.append("  <url>")
        body.append(f"    <loc>{u}</loc>")
        body.append("    <changefreq>weekly</changefreq>")
        body.append("  </url>")
    body.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(body) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n",
        encoding="utf-8",
    )

    # strengthen blogs index meta if present
    idx = OUT / "index.html"
    if idx.exists():
        t = idx.read_text(encoding="utf-8")
        t = re.sub(
            r"<title>[^<]*</title>",
            "<title>Game Cheats Blog Catalog | Aimbot, ESP &amp; Spoofer Guides</title>",
            t,
            count=1,
        )
        if 'name="description"' in t:
            t = re.sub(
                r'<meta name="description" content="[^"]*"',
                '<meta name="description" content="Browse game cheats by title — aimbot, ESP, wallhack and spoofer pages with feature comparison and instant delivery."',
                t,
                count=1,
            )
        idx.write_text(t, encoding="utf-8")

    print("done", len(PRODUCTS), "pages")


if __name__ == "__main__":
    main()
