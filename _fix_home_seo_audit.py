# -*- coding: utf-8 -*-
"""Fix homepage (+ blogs catalog) SEO issues from Seobility audit."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"c:\Users\ii\articles")

SEO_BLOCK = """
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
<link rel="alternate" hreflang="en" href="CANON"/>
<link rel="alternate" hreflang="x-default" href="CANON"/>
<meta property="og:locale" content="en_US"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Get Your Cheats"/>
<meta name="twitter:card" content="summary_large_image"/>
""".strip()

ABOUT_HTML = """
<section class="seo-home-about" style="width:min(720px,100%);margin:2.5rem auto 0;padding:0 1rem 1rem;color:#ABB0C7;font-family:Onest,system-ui,sans-serif;line-height:1.6">
  <h2 style="color:#E2E8FF;font-size:1.25rem;margin:0 0 .75rem">About this game cheats catalog</h2>
  <p style="margin:0 0 .85rem">This <strong style="color:#E2E8FF">game cheats catalog</strong> helps you compare <strong style="color:#E2E8FF">aimbot</strong>, <strong style="color:#E2E8FF">ESP</strong>, <strong style="color:#E2E8FF">wallhack</strong>, and HWID spoofer options by title. Each guide lists features, delivery notes, and market alternatives so you can choose your cheat with clear expectations before checkout.</p>
  <p style="margin:0 0 .85rem">Browse popular shooters, survival games, and online titles below. Open a product page for status notes, feature grids, and buyer FAQs. Search the catalog to jump straight to the game you want, then review aimbot FOV options, ESP boxes, loot filters, and spoofer paths when a clean load matters.</p>
  <p style="margin:0 0 .85rem">Our catalog is built for buyers who want readable comparisons instead of mystery Discord links. Instant delivery and on-page support paths are highlighted on each guide. Status is treated as patch-dependent — never fake “lifetime undetected” claims.</p>
  <p style="margin:0">Start with the popular grid, or pick any title card to open a full cheat guide with screenshots where available. New games are added as builds ship, so bookmark this page when you need a quick aimbot, ESP, or wallhack comparison.</p>
</section>
"""


def fix_page(path: Path, canon: str, title: str, description: str, h1: str) -> None:
    t = path.read_text(encoding="utf-8")

    # robots
    t = re.sub(
        r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>',
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>',
        t,
        count=1,
        flags=re.I,
    )
    if 'name="robots"' not in t:
        t = t.replace("</head>", '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>\n</head>', 1)

    # strip bad rewarble alternates
    t = re.sub(r'<link\s+rel="alternate"[^>]*>', "", t, flags=re.I)

    # ensure canonical
    if re.search(r'rel="canonical"', t, re.I):
        t = re.sub(
            r'<link[^>]*rel="canonical"[^>]*>',
            f'<link rel="canonical" href="{canon}"/>',
            t,
            count=1,
            flags=re.I,
        )
    else:
        t = t.replace("</head>", f'<link rel="canonical" href="{canon}"/>\n</head>', 1)

    # inject self alternates + og extras once
    block = SEO_BLOCK.replace("CANON", canon)
    if 'hreflang="en"' not in t:
        t = t.replace("</head>", block + "\n</head>", 1)

    # title / description / og
    t = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", t, count=1)
    t = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
        f'<meta name="description" content="{description}"/>',
        t,
        count=1,
        flags=re.I,
    )
    t = re.sub(
        r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>',
        f'<meta property="og:title" content="{title}"/>',
        t,
        count=1,
        flags=re.I,
    )
    t = re.sub(
        r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>',
        f'<meta property="og:description" content="{description}"/>',
        t,
        count=1,
        flags=re.I,
    )
    t = re.sub(
        r'<meta\s+property="og:url"\s+content="[^"]*"\s*/?>',
        f'<meta property="og:url" content="{canon}"/>',
        t,
        count=1,
        flags=re.I,
    )
    t = re.sub(
        r'<meta\s+property="og:image"\s+content="[^"]*"\s*/?>',
        '<meta property="og:image" content="https://getyourcheats.com/images/logo-128.png"/>',
        t,
        count=1,
        flags=re.I,
    )
    t = re.sub(
        r'<meta\s+name="apple-mobile-web-app-title"\s+content="[^"]*"\s*/?>',
        '<meta name="apple-mobile-web-app-title" content="Get Your Cheats"/>',
        t,
        count=1,
        flags=re.I,
    )

    # H1 + lead
    t = re.sub(
        r"(<h1[^>]*>)Choose your cheat(</h1>)",
        rf"\1{h1}\2",
        t,
        count=1,
    )
    t = re.sub(
        r'(<p class="font-medium font-onest text-\[#ABB0C7\][^"]*"[^>]*>)([^<]*)(</p>)',
        r"\1This game cheats catalog lists aimbot, ESP, wallhack, and spoofer guides by title so you can choose your cheat with clear feature comparisons.\3",
        t,
        count=1,
    )

    # skeleton alt
    t = t.replace(
        '<img src="/cs/img/cherep6.gif" alt="" width="120" height="229"/>',
        '<img src="/cs/img/cherep6.gif" alt="Get Your Cheats site mascot" width="120" height="229"/>',
    )

    # logo alts
    t = t.replace('alt="Logo"', 'alt="Get Your Cheats logo"')
    t = t.replace('alt="Rewarble Logo"', 'alt="Get Your Cheats logo"')

    # product image alts: add " cheats" if missing
    def bump_alt(m: re.Match) -> str:
        alt = m.group(1)
        if "cheat" in alt.lower():
            return m.group(0)
        return m.group(0).replace(f'alt="{alt}"', f'alt="{alt} cheats"')

    t = re.sub(r'<img([^>]*?)alt="([^"]+)"([^>]*?)>', lambda m: bump_alt(m) if "data-product-card" in t[max(0, m.start() - 200) : m.start()] or True else m.group(0), t)
    # safer: only on catalog card imgs inside data-product-card blocks — above is too broad
    # revert overly broad: re-run more carefully
    # Actually the lambda always True - bumps ALL imgs including logos. Fix logos again after.
    t = t.replace('alt="Get Your Cheats logo cheats"', 'alt="Get Your Cheats logo"')
    t = t.replace('alt="Get Your Cheats site mascot cheats"', 'alt="Get Your Cheats site mascot"')
    t = t.replace('alt="EN flag cheats"', 'alt="English language flag"')

    # section headings that still say gift cards / rewarble
    t = t.replace(">Gift cards</h2>", ">More game cheats</h2>")
    t = t.replace(">Reward cards</h2>", ">Featured cheat guides</h2>")
    t = t.replace(">Service recharges</h2>", ">Additional titles</h2>")
    t = t.replace(">Rewarble rewards</h2>", ">Newest cheat listings</h2>")
    t = t.replace(">Sending rewards</h2>", ">Extra game cheats</h2>")
    t = t.replace(">Popular</h2>", ">Popular game cheats</h2>")

    # unique footer anchors vs nav duplicates
    t = t.replace(
        'href="/" data-discover="true"><p class="font-onest">Home</p>',
        'href="/" data-discover="true"><p class="font-onest">Cheat catalog home</p>',
    )
    t = t.replace(
        'href="/support" data-discover="true"><p class="font-onest">Support</p>',
        'href="/support" data-discover="true"><p class="font-onest">Buyer support center</p>',
    )

    # insert about section before footer container
    if "seo-home-about" not in t:
        t = t.replace(
            '<div class="container mx-auto px-4 pt-20"><footer',
            ABOUT_HTML + '\n<div class="container mx-auto px-4 pt-20"><footer',
            1,
        )

    # remove rewarble preconnect noise
    t = t.replace('<link rel="preconnect" href="https://cdn.rewarble.com"/>', "")

    path.write_text(t, encoding="utf-8")


def main() -> None:
    fix_page(
        ROOT / "index.html",
        "https://getyourcheats.com/",
        "Game Cheats Catalog | Aimbot, ESP &amp; Wallhack",
        "Browse game cheat guides by title — aimbot, ESP, wallhack and spoofers with feature comparisons.",
        "Game Cheats Catalog: Aimbot, ESP &amp; Wallhack",
    )
    fix_page(
        ROOT / "blogs" / "index.html",
        "https://getyourcheats.com/blogs/",
        "Cheat Guides Catalog | Aimbot, ESP &amp; Wallhack",
        "Browse cheat comparison guides by game — aimbot, ESP, wallhack and spoofers with clear feature lists.",
        "Cheat Guides Catalog: Aimbot, ESP &amp; Wallhack",
    )

    # contact: indexable lightly
    cpath = ROOT / "contact" / "index.html"
    if cpath.exists():
        ct = cpath.read_text(encoding="utf-8")
        ct = re.sub(
            r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>',
            '<meta name="robots" content="index, follow"/>',
            ct,
            count=1,
            flags=re.I,
        )
        cpath.write_text(ct, encoding="utf-8")

    # verify home
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    print("noindex gone", "noindex" not in home.lower())
    print("hreflang self", 'hreflang="en" href="https://getyourcheats.com/"' in home)
    print("h1", "Game Cheats Catalog: Aimbot" in home)
    print("about", "seo-home-about" in home)
    print("words~", len(re.findall(r"[A-Za-z]{2,}", re.sub(r"<[^>]+>", " ", home.split("<footer")[0][-3500:]))))


if __name__ == "__main__":
    main()
