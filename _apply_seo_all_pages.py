# -*- coding: utf-8 -*-
"""Apply homepage-level SEO audit rules to every product page + stubs + contact."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"c:\Users\ii\articles")
ORIGIN = "https://getyourcheats.com"
PRODUCTS = json.loads((ROOT / "_gen_products.json").read_text(encoding="utf-8"))

TICK_WORDS = "Aimbot, ESP & Wallhack"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def upsert_meta(t: str, kind: str, key: str, content: str) -> str:
    pat = rf'<meta[^>]*{kind}="{re.escape(key)}"[^>]*/?>'
    tag = f'<meta {kind}="{key}" content="{content}"/>'
    if re.search(pat, t, flags=re.I):
        return re.sub(pat, tag, t, count=1, flags=re.I)
    return t.replace("</head>", tag + "\n</head>", 1)


def upsert_link(t: str, rel: str, href: str, extra: str = "") -> str:
    if extra:
        # e.g. hreflang
        pat = rf'<link[^>]*rel="{re.escape(rel)}"[^>]*{extra}[^>]*/?>'
        # also match swapped attr order
        pat2 = rf'<link[^>]*{extra}[^>]*rel="{re.escape(rel)}"[^>]*/?>'
        tag = f'<link rel="{rel}" {extra} href="{href}"/>'
        if re.search(pat, t, flags=re.I):
            return re.sub(pat, tag, t, count=1, flags=re.I)
        if re.search(pat2, t, flags=re.I):
            return re.sub(pat2, tag, t, count=1, flags=re.I)
        return t.replace("</head>", tag + "\n</head>", 1)
    pat = rf'<link[^>]*rel="{re.escape(rel)}"[^>]*/?>'
    tag = f'<link rel="{rel}" href="{href}"/>'
    if re.search(pat, t, flags=re.I):
        return re.sub(pat, tag, t, count=1, flags=re.I)
    return t.replace("</head>", tag + "\n</head>", 1)


def ensure_hreflang(t: str, url: str) -> str:
    # remove foreign alternates
    t = re.sub(r'<link[^>]*rel="alternate"[^>]*>', "", t, flags=re.I)
    t = t.replace("</head>", (
        f'<link rel="alternate" hreflang="en" href="{url}"/>\n'
        f'<link rel="alternate" hreflang="x-default" href="{url}"/>\n'
        "</head>"
    ), 1)
    return t


def fix_product(p: dict) -> None:
    slug = p["slug"]
    name = p["name"]
    path = ROOT / slug / "index.html"
    if not path.exists():
        return
    t = path.read_text(encoding="utf-8")
    canon = f"{ORIGIN}/{slug}/"
    title = f"{esc(name)} Cheats | {TICK_WORDS} Guide"
    # keep amp in title for HTML
    title_html = f"{esc(name)} Cheats | Aimbot, ESP &amp; Wallhack Guide"
    desc = (
        f"Compare {esc(name)} cheats with aimbot, ESP, wallhack and spoofer options. "
        f"See features, market alternatives, and buyer notes for {esc(name)} cheats."
    )
    h1 = f"{esc(name)} Cheats: Aimbot, ESP &amp; Wallhack"
    img = p.get("img") or "/images/logo-128.png"
    if not img.startswith("http"):
        abs_img = ORIGIN + (img if img.startswith("/") else "/" + img)
    else:
        abs_img = img

    # lang
    t = re.sub(r"<html[^>]*>", '<html lang="en">', t, count=1, flags=re.I)

    # charset / viewport already present
    t = upsert_meta(t, "name", "robots", "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")
    t = upsert_meta(t, "name", "apple-mobile-web-app-title", "Get Your Cheats")
    t = upsert_meta(t, "name", "description", desc)
    t = upsert_meta(
        t,
        "name",
        "keywords",
        f"{esc(name)} cheats, {esc(name)} aimbot, {esc(name)} ESP, {esc(name)} wallhack, "
        f"{esc(name)} spoofer, buy {esc(name)} cheats, undetected {esc(name)} cheats",
    )

    if re.search(r"<title>[^<]*</title>", t):
        t = re.sub(r"<title>[^<]*</title>", f"<title>{title_html}</title>", t, count=1)
    else:
        t = t.replace("</head>", f"<title>{title_html}</title>\n</head>", 1)

    t = upsert_link(t, "canonical", canon)
    t = ensure_hreflang(t, canon)

    # Open Graph / Twitter
    t = upsert_meta(t, "property", "og:type", "product")
    t = upsert_meta(t, "property", "og:locale", "en_US")
    t = upsert_meta(t, "property", "og:site_name", "Get Your Cheats")
    t = upsert_meta(t, "property", "og:title", title_html)
    t = upsert_meta(t, "property", "og:description", desc)
    t = upsert_meta(t, "property", "og:url", canon)
    t = upsert_meta(t, "property", "og:image", abs_img)
    t = upsert_meta(t, "property", "og:image:secure_url", abs_img)
    t = upsert_meta(t, "property", "og:image:alt", f"{esc(name)} Cheats")
    t = upsert_meta(t, "name", "twitter:card", "summary_large_image")
    t = upsert_meta(t, "name", "twitter:title", title_html)
    t = upsert_meta(t, "name", "twitter:description", desc)
    t = upsert_meta(t, "name", "twitter:image", abs_img)
    t = upsert_meta(t, "name", "twitter:image:alt", f"{esc(name)} Cheats")
    t = upsert_link(t, "image_src", abs_img)

    # H1 — long enough + matches title keywords
    # Use \g<1> so names starting with digits (e.g. 7 Days) don't become group \17
    t = re.sub(
        r"(<h1[^>]*>)([\s\S]*?)(</h1>)",
        lambda m: m.group(1) + h1 + m.group(3),
        t,
        count=1,
    )

    # Ensure lead mentions catalog keywords if too thin
    lead_pat = re.compile(r'(<p class="lead">)(.*?)(</p>)', re.S)
    m = lead_pat.search(t)
    if m:
        lead = re.sub(r"\s+", " ", m.group(2)).strip()
        need = ["aimbot", "esp", "wallhack", name.lower().split()[0]]
        if sum(1 for w in need if w.lower() in lead.lower()) < 3 or len(lead.split()) < 18:
            lead = (
                f"{name} cheats cover aimbot tracking, ESP / wallhack overlays, and HWID spoofer options "
                f"when you need a clean load. This guide compares features, delivery, and market alternatives "
                f"so you can pick the right {name} cheat build."
            )
            t = lead_pat.sub(lambda m: m.group(1) + lead + m.group(3), t, count=1)

    # skeleton + logo alts
    t = t.replace(
        '<img src="/cs/img/cherep6.gif" alt="" width="120" height="229"/>',
        '<img src="/cs/img/cherep6.gif" alt="Get Your Cheats site mascot" width="120" height="229"/>',
    )
    t = t.replace('alt="Logo"', 'alt="Get Your Cheats logo"')
    t = t.replace('alt="Rewarble Logo"', 'alt="Get Your Cheats logo"')
    # any remaining empty alts
    t = re.sub(r'alt=""', 'alt="Get Your Cheats"', t)

    # hero image alt
    t = re.sub(
        r'(<img class="hero-img"[^>]*alt=")([^"]*)(")',
        lambda m: m.group(1) + f"{name} Cheats" + m.group(3),
        t,
        count=1,
    )

    # BreadcrumbList JSON-LD (replace or insert)
    crumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{ORIGIN}/"},
            {"@type": "ListItem", "position": 2, "name": f"{name} Cheats", "item": canon},
        ],
    }
    crumb_script = (
        '<script type="application/ld+json">'
        + json.dumps(crumb, ensure_ascii=False)
        + "</script>"
    )
    if '"@type": "BreadcrumbList"' in t or '"@type":"BreadcrumbList"' in t:
        t = re.sub(
            r'<script type="application/ld\+json">\{[^{}]*BreadcrumbList[\s\S]*?\}</script>',
            crumb_script,
            t,
            count=1,
        )
    else:
        t = t.replace("</head>", crumb_script + "\n</head>", 1)

    # WebPage schema snippet
    webpage = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"{name} Cheats | Aimbot, ESP & Wallhack Guide",
        "description": desc.replace("&amp;", "&"),
        "url": canon,
        "inLanguage": "en",
        "isPartOf": {"@type": "WebSite", "name": "Get Your Cheats", "url": f"{ORIGIN}/"},
        "primaryImageOfPage": abs_img,
    }
    wp_script = (
        '<script type="application/ld+json">'
        + json.dumps(webpage, ensure_ascii=False)
        + "</script>"
    )
    if '"@type": "WebPage"' in t or '"@type":"WebPage"' in t:
        t = re.sub(
            r'<script type="application/ld\+json">\{[^{}]*"@type":\s*"WebPage"[\s\S]*?\}</script>',
            wp_script,
            t,
            count=1,
        )
    else:
        t = t.replace("</head>", wp_script + "\n</head>", 1)

    # crumb visible text ok
    # Fix FAQ broken brandless sentences if still empty subjects
    t = t.replace(
        'acceptedAnswer": {"@type": "Answer", "text": " is a strong option',
        'acceptedAnswer": {"@type": "Answer", "text": "This offer is a strong option',
    )
    t = t.replace(
        "ranks ahead of typical public pastes",
        "this listing ranks ahead of typical public pastes",
    )

    path.write_text(t, encoding="utf-8")


def fix_stub(slug: str) -> None:
    path = ROOT / "blogs" / slug / "index.html"
    if not path.exists():
        return
    target = f"{ORIGIN}/{slug}/"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="robots" content="noindex, follow"/>
  <link rel="canonical" href="{target}"/>
  <meta http-equiv="refresh" content="0;url=/{slug}/"/>
  <title>Redirecting to {esc(slug)} cheats</title>
  <script>location.replace('/{slug}/');</script>
</head>
<body>
  <p>This page moved to <a href="/{slug}/">{esc(slug)} cheats</a>.</p>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def fix_contact() -> None:
    path = ROOT / "contact" / "index.html"
    if not path.exists():
        return
    t = path.read_text(encoding="utf-8")
    canon = f"{ORIGIN}/contact/"
    t = upsert_meta(t, "name", "robots", "index, follow")
    t = upsert_link(t, "canonical", canon)
    t = ensure_hreflang(t, canon)
    t = upsert_meta(t, "property", "og:url", canon)
    t = upsert_meta(t, "property", "og:locale", "en_US")
    t = upsert_meta(t, "property", "og:site_name", "Get Your Cheats")
    t = t.replace(
        '<img src="/cs/img/cherep6.gif" alt="" width="120" height="229"/>',
        '<img src="/cs/img/cherep6.gif" alt="Get Your Cheats site mascot" width="120" height="229"/>',
    )
    t = t.replace('alt="Logo"', 'alt="Get Your Cheats logo"')
    t = re.sub(r'alt=""', 'alt="Get Your Cheats"', t)
    if re.search(r"<title>", t):
        t = re.sub(r"<title>[^<]*</title>", "<title>Contact | Get Your Cheats Support</title>", t, count=1)
    path.write_text(t, encoding="utf-8")


def verify() -> None:
    bad = []
    for p in PRODUCTS:
        slug = p["slug"]
        t = (ROOT / slug / "index.html").read_text(encoding="utf-8")
        checks = {
            "canon": f'rel="canonical" href="{ORIGIN}/{slug}/"' in t,
            "hreflang": f'hreflang="en" href="{ORIGIN}/{slug}/"' in t,
            "xdef": f'hreflang="x-default" href="{ORIGIN}/{slug}/"' in t,
            "index": "noindex" not in t.lower(),
            "robots": 'name="robots"' in t,
            "og_url": f'og:url" content="{ORIGIN}/{slug}/"' in t or f"og:url\" content=\"{ORIGIN}/{slug}/\"" in t,
            "empty_alt": 'alt=""' not in t,
            "h1_long": False,
            "og_abs": True,
        }
        h1 = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", t)
        if h1:
            plain = re.sub(r"<[^>]+>", "", h1.group(1))
            plain = plain.replace("&amp;", "&").strip()
            checks["h1_long"] = len(plain) >= 20 and "Aimbot" in plain
        m = re.search(r'property="og:image" content="([^"]+)"', t)
        if not m or not m.group(1).startswith(ORIGIN):
            checks["og_abs"] = False
        fails = [k for k, v in checks.items() if not v]
        if fails:
            bad.append((slug, fails))
    print("products ok", len(PRODUCTS) - len(bad), "/", len(PRODUCTS))
    if bad:
        print("bad sample", bad[:5])


def main() -> None:
    for p in PRODUCTS:
        fix_product(p)
        fix_stub(p["slug"])
    fix_contact()
    verify()
    # sample
    t = (ROOT / "the-first-descendant" / "index.html").read_text(encoding="utf-8")
    print("TFD h1", re.search(r"<h1[^>]*>([\s\S]*?)</h1>", t).group(1)[:90])
    print("TFD hreflang", 'hreflang="en"' in t)
    print("TFD empty alt", 'alt=""' in t)


if __name__ == "__main__":
    main()
