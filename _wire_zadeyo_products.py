# -*- coding: utf-8 -*-
"""Map catalog + blogs to Zadeyo product URLs; fix meta + features for Google."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(r"c:\Users\ii\articles")
PRODUCTS = json.loads((ROOT / "_gen_products.json").read_text(encoding="utf-8"))
ZADEYO_PRODUCTS = json.loads((ROOT / "_zadeyo_products.json").read_text(encoding="utf-8"))

# Manual overrides for awkward slugs
MANUAL = {
    "battlefield-6": "https://zadeyo.com/products/BF6-cheats",
    "sand": "https://zadeyo.com/products/sand-raiders-of-sophie-cheats",
    "ark-survival-ascended": "https://zadeyo.com/products/ark-ascended-cheats",
    "isle": "https://zadeyo.com/products/the-isle-novaxware-cheats",
    "conan": "https://zadeyo.com/products/conan-exiles-cheats",
    "wunthering": "https://zadeyo.com/products/wuthering-waves-cheats",
    "moe": "https://zadeyo.com/products/myth-of-empires-cheats",
    "insurge": "https://zadeyo.com/products/insurgency-sandstorm-cheats",
    "cod-bocw": "https://zadeyo.com/products/warzone-cheats",
    "call-of-duty-black-ops-7": "https://zadeyo.com/products/warzone-cheats",
    "swbf": "https://zadeyo.com/products/star-wars-battlefront-2-cheats",
    "halo": "https://zadeyo.com/products/halo-infinite-cheats",
    "hd2": "https://zadeyo.com/shop",  # no helldivers product found - shop fallback
    "ea-sports-fc": "https://zadeyo.com/products/ea-sports-fc-2026-cheats",
    "black-desert-mobile": "https://zadeyo.com/products/black-desert-online-cheats",
    "fragpunk": "https://zadeyo.com/products/fragpunk-novaxware-cheats",
    "etheria-restart": "https://zadeyo.com/products/etheria-restart-novaxware-cheats",
    "foxhole": "https://zadeyo.com/products/foxhole-novaxware-cheats",
    "path-of-exile-2": "https://zadeyo.com/products/path-of-exile-cheats",
    "the-division-2": "https://zadeyo.com/shop",
    "gray-zone": "https://zadeyo.com/products/gray-zone-warfare-cheats",
    "gray-zone-warfare": "https://zadeyo.com/products/gray-zone-warfare-cheats",
    "mecha-break": "https://zadeyo.com/products/mecha-break-cheats",
}


def norm(s: str) -> str:
    s = s.lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


# index zadeyo products by normalized path slug
za_index: dict[str, str] = {}
for url in ZADEYO_PRODUCTS:
    slug = url.rstrip("/").split("/")[-1]
    base = re.sub(r"-cheats$", "", slug, flags=re.I)
    base = re.sub(r"-novaxware$", "", base, flags=re.I)
    za_index[norm(slug)] = url
    za_index[norm(base)] = url
    za_index[norm(base.replace("-", ""))] = url

# extra aliases
ALIASES = {
    "eft": "escape-from-tarkov",
    "pubg": "pubg",
    "pybg": "pubg",
    "bf6": "BF6",
    "dayz": "dayz",
    "rust": "rust",
    "marvelrivals": "marvel-rivals",
    "thefirstdescendant": "the-first-descendant",
    "zenlesszonezero": "zenless-zone-zero",
    "lastepoch": "last-epoch",
    "arcraiders": "arc-raiders",
    "armareforger": "arma-reforger",
    "humanitz": "humanitz",
    "bodycam": "bodycam",
    "oncehuman": "once-human",
    "predecessor": "predecessor",
    "deadlock": None,  # maybe not on zadeyo
    "7daystodie": "7-days-to-die",
    "companyofheroes3": "company-of-heroes-3",
    "teamfortress2": "team-fortress-2",
}


def find_zadeyo(slug: str, name: str) -> str:
    if slug in MANUAL:
        return MANUAL[slug]
    candidates = [
        slug,
        f"{slug}-cheats",
        name,
        name.replace(":", ""),
        name.replace(" ", "-"),
    ]
    nname = norm(name)
    for c in candidates:
        nc = norm(c)
        if nc in za_index:
            return za_index[nc]
        nc2 = norm(re.sub(r"cheats?$", "", c, flags=re.I))
        if nc2 in za_index:
            return za_index[nc2]
    # fuzzy: longest zadeyo key contained in name/slug norms
    best = None
    best_len = 0
    target = norm(slug) + norm(name)
    for k, url in za_index.items():
        if len(k) < 4:
            continue
        if k in target or target in k:
            if len(k) > best_len:
                best = url
                best_len = len(k)
    return best or "https://zadeyo.com/shop"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def meta_title(name: str) -> str:
    # Match Zadeyo style, under ~60 chars
    t = f"ZADEYO / {name} Cheat - ESP, Aimbot & Wallhack"
    if len(t) <= 60:
        return t
    t = f"ZADEYO / {name} Cheats - Aimbot & ESP"
    if len(t) <= 60:
        return t
    return f"{name} Cheats | Zadeyo Aimbot & ESP"[:60]


def meta_desc(name: str) -> str:
    d = (
        f"Undetected {name} cheats with player ESP, aimbot, and wallhack. "
        f"Buy {name} cheats on Zadeyo — instant delivery, monthly and lifetime access, updated for current patches."
    )
    return d[:158]


FEATURES = [
    ("Aimbot", "Configurable FOV, smooth aim, and bone priority for cleaner fights."),
    ("ESP / Wallhack", "Player boxes, distance, and health readouts through walls."),
    ("Loot / world ESP", "Highlight valuable loot and world objects where the build supports it."),
    ("No recoil helpers", "Weapon control assists on supported titles and configs."),
    ("Triggerbot", "Fire assistance when crosshair meets a valid target."),
    ("HWID Spoofer path", "Documented spoofer pairing when hardware bans are a risk."),
    ("Stream-proof mode", "Hide overlays from capture software on supported builds."),
    ("Instant delivery", "Loader / license access after payment clears — no DM waiting."),
    ("Patch updates", "Builds tracked against current game patches with status notes."),
    ("24/7 support", "Contact path for load help instead of abandoned reseller accounts."),
]


def features_html(name: str) -> str:
    items = []
    for title, blurb in FEATURES:
        items.append(
            f'<li itemprop="itemListElement"><div class="feat">'
            f'<strong itemprop="name">{esc(title)}</strong>'
            f'<span itemprop="description">{esc(blurb.replace("game", name) if False else blurb)}</span>'
            f"</div></li>"
        )
    # game-specific first line
    return f"""
    <section class="features-block" style="margin-top:1.25rem" itemscope itemtype="https://schema.org/ItemList">
      <meta itemprop="name" content="{esc(name)} cheat features on Zadeyo"/>
      <h2 itemprop="name">{esc(name)} cheat features</h2>
      <p style="color:var(--muted);margin:0 0 1rem">
        Full <strong style="color:var(--text)">{esc(name)} cheats</strong> feature list buyers and search engines can read clearly —
        aimbot, ESP, wallhack, spoofer, and delivery details for Zadeyo.
      </p>
      <ul class="feature-list">
        {''.join(items)}
      </ul>
    </section>
"""


FEATURES_CSS = """
<style id="zadeyo-features">
  .features-block .feature-list {
    list-style: none; margin: 0; padding: 0;
    display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .75rem;
  }
  .features-block .feat {
    display: flex; flex-direction: column; gap: .25rem;
    padding: .85rem .9rem; border-radius: .85rem;
    border: 1px solid rgba(255,255,255,.10); background: rgba(12,10,32,.85);
  }
  .features-block .feat strong { color: #E2E8FF; font-size: .92rem; }
  .features-block .feat span { color: #ABB0C7; font-size: .84rem; line-height: 1.4; }
  @media (max-width:720px) {
    .features-block .feature-list { grid-template-columns: 1fr; }
  }
</style>
"""


def features_schema(name: str, url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{name} cheat features on Zadeyo",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": title,
                "description": blurb,
                "url": url,
            }
            for i, (title, blurb) in enumerate(FEATURES)
        ],
    }


def product_schema(name: str, desc: str, img: str, url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": f"{name} Cheats",
        "description": desc,
        "image": img if img.startswith("http") else f"https://zadeyo.com{img}" if img.startswith("/") else img,
        "brand": {"@type": "Brand", "name": "Zadeyo"},
        "category": "Game Cheats",
        "offers": {
            "@type": "Offer",
            "url": url,
            "availability": "https://schema.org/InStock",
            "priceCurrency": "USD",
            "seller": {"@type": "Organization", "name": "Zadeyo"},
        },
    }


def main() -> None:
    mapping = {}
    for p in PRODUCTS:
        url = find_zadeyo(p["slug"], p["name"])
        mapping[p["slug"]] = {
            "name": p["name"],
            "zadeyo": url,
            "img": p["img"],
            "gif": p.get("gif") or "",
        }
    (ROOT / "_zadeyo_map.json").write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    matched = sum(1 for v in mapping.values() if "/products/" in v["zadeyo"])
    print("mapped", len(mapping), "direct products", matched)

    # --- Catalog pages: link cards to Zadeyo product ---
    for page in [ROOT / "index.html", ROOT / "blogs" / "index.html"]:
        t = page.read_text(encoding="utf-8")
        for slug, info in mapping.items():
            zurl = info["zadeyo"]
            # replace href="/blogs/{slug}" on product cards
            t = re.sub(
                rf'href="/blogs/{re.escape(slug)}"',
                f'href="{zurl}" target="_blank" rel="noopener sponsored"',
                t,
            )
            # also without quotes variants
            t = t.replace(f'href="/blogs/{slug}"', f'href="{zurl}" target="_blank" rel="noopener sponsored"')
        page.write_text(t, encoding="utf-8")
        print("catalog linked", page.name)

    # --- Local blog pages: CTA + meta + features + schema ---
    for slug, info in mapping.items():
        path = ROOT / "blogs" / slug / "index.html"
        if not path.exists():
            continue
        name = info["name"]
        zurl = info["zadeyo"]
        html = path.read_text(encoding="utf-8")
        title = meta_title(name)
        desc = meta_desc(name)

        html = re.sub(r"<title>[^<]*</title>", f"<title>{esc(title)}</title>", html, count=1)
        html = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{esc(desc)}"',
            html,
            count=1,
        )
        html = re.sub(
            r'<meta property="og:title" content="[^"]*"',
            f'<meta property="og:title" content="{esc(title)}"',
            html,
            count=1,
        )
        html = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            f'<meta property="og:description" content="{esc(desc)}"',
            html,
            count=1,
        )
        html = re.sub(
            r'<meta property="og:url" content="[^"]*"',
            f'<meta property="og:url" content="{esc(zurl)}"',
            html,
            count=1,
        )
        html = re.sub(
            r'<meta name="twitter:title" content="[^"]*"',
            f'<meta name="twitter:title" content="{esc(title)}"',
            html,
            count=1,
        )
        html = re.sub(
            r'<meta name="twitter:description" content="[^"]*"',
            f'<meta name="twitter:description" content="{esc(desc)}"',
            html,
            count=1,
        )
        # canonical -> Zadeyo product (direct)
        if 'rel="canonical"' in html:
            html = re.sub(
                r'<link rel="canonical" href="[^"]*"\s*/?>',
                f'<link rel="canonical" href="{esc(zurl)}"/>',
                html,
                count=1,
            )
        else:
            html = html.replace(
                "</head>",
                f'<link rel="canonical" href="{esc(zurl)}"/>\n</head>',
                1,
            )

        # keywords
        html = re.sub(
            r'<meta name="keywords" content="[^"]*"',
            f'<meta name="keywords" content="{esc(name)} cheats, {esc(name)} aimbot, {esc(name)} ESP, {esc(name)} wallhack, buy {esc(name)} cheats, Zadeyo {esc(name)} cheats, undetected {esc(name)} cheats"',
            html,
            count=1,
        )

        # Replace Product JSON-LD
        prod = product_schema(name, desc, info["img"], zurl)
        html = re.sub(
            r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "Product"[\s\S]*?</script>',
            f'<script type="application/ld+json">{json.dumps(prod, ensure_ascii=False)}</script>',
            html,
            count=1,
        )

        # Features ItemList schema
        feat_schema = features_schema(name, zurl)
        if '"@type": "ItemList"' in html:
            html = re.sub(
                r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "ItemList"[\s\S]*?</script>',
                f'<script type="application/ld+json">{json.dumps(feat_schema, ensure_ascii=False)}</script>',
                html,
                count=1,
            )
        else:
            html = html.replace(
                "</head>",
                f'<script type="application/ld+json">{json.dumps(feat_schema, ensure_ascii=False)}</script>\n</head>',
                1,
            )

        if 'id="zadeyo-features"' not in html:
            html = html.replace("</head>", FEATURES_CSS + "</head>", 1)

        # Features block HTML
        feat = features_html(name)
        html = re.sub(r'<section class="features-block"[\s\S]*?</section>\s*', "", html)
        # Insert after hero / before grid-2 or after lead
        if 'class="grid-2"' in html:
            html = html.replace('<div class="grid-2">', feat + '\n\n    <div class="grid-2">', 1)
        else:
            html = html.replace('<section class="zadeyo-compare"', feat + '\n\n    <section class="zadeyo-compare"', 1)

        # CTA buttons -> Zadeyo product
        html = re.sub(
            r'<a class="cta" href="[^"]*">[^<]*</a>',
            f'<a class="cta" href="{esc(zurl)}" target="_blank" rel="noopener sponsored">Get {esc(name)} Cheats on Zadeyo</a>',
            html,
        )
        # Contact links in gallery cards that say /contact for versions - point primary buy to zadeyo
        # Hero image clickable to product
        html = re.sub(
            r'(<div class="hero-media">)([\s\S]*?)(</div>)',
            rf'\1<a href="{esc(zurl)}" target="_blank" rel="noopener sponsored" aria-label="Buy {esc(name)} cheats on Zadeyo">\2</a>\3',
            html,
            count=1,
        )
        # avoid double wrap
        html = html.replace(
            f'<a href="{zurl}" target="_blank" rel="noopener sponsored" aria-label="Buy {name} cheats on Zadeyo"><a href="{zurl}"',
            f'<a href="{zurl}" target="_blank" rel="noopener sponsored" aria-label="Buy {name} cheats on Zadeyo">',
        )

        # H1 stay game focused
        html = re.sub(
            rf"<h1>[^<]*</h1>",
            f"<h1>{esc(name)} Cheats on Zadeyo</h1>",
            html,
            count=1,
        )

        path.write_text(html, encoding="utf-8")

    # meta on home
    home = ROOT / "index.html"
    t = home.read_text(encoding="utf-8")
    t = re.sub(
        r"<title>[^<]*</title>",
        "<title>ZADEYO Game Cheats Shop | Aimbot, ESP &amp; Wallhack</title>",
        t,
        count=1,
    )
    t = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Buy undetected game cheats on Zadeyo — aimbot, ESP, wallhack and spoofer tools with instant delivery. Browse titles and open the official product page."',
        t,
        count=1,
    )
    home.write_text(t, encoding="utf-8")

    # sample
    print("dayz ->", mapping["dayz"]["zadeyo"])
    print("eft ->", mapping["escape-from-tarkov"]["zadeyo"])
    print("rust ->", mapping["rust"]["zadeyo"])
    unmatched = [s for s, v in mapping.items() if "/products/" not in v["zadeyo"]]
    print("shop fallback", len(unmatched), unmatched[:15])


if __name__ == "__main__":
    main()
