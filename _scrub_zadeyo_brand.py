# -*- coding: utf-8 -*-
"""Remove all visible Zadeyo branding from site HTML; keep product hrefs only."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"c:\Users\ii\articles")
PRODUCTS = {p["slug"]: p for p in json.loads((ROOT / "_gen_products.json").read_text(encoding="utf-8"))}
MAPPING = json.loads((ROOT / "_zadeyo_map.json").read_text(encoding="utf-8"))


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def meta_title(name: str) -> str:
    t = f"{name} Cheats - ESP, Aimbot & Wallhack Guide"
    if len(t) <= 60:
        return t
    t = f"{name} Cheats | Aimbot, ESP & Spoofer"
    return t[:60]


def meta_desc(name: str) -> str:
    return (
        f"Compare {name} cheats: aimbot, ESP, wallhack and spoofer options. "
        f"Feature checklist, buyer notes, and market alternatives for {name}."
    )[:158]


def scrub_text(s: str) -> str:
    # Order matters — longer phrases first
    reps = [
        (r"Get ([^<]*?) Cheats on Zadeyo", r"Get \1 Cheats"),
        (r"Buy ([^<]*?) Cheats on Zadeyo", r"Get \1 Cheats"),
        (r"Buy ([^<\"]*?) cheats on Zadeyo", r"Buy \1 cheats"),
        (r"on Zadeyo", ""),
        (r"On Zadeyo", ""),
        (r"with Zadeyo", ""),
        (r"With Zadeyo", ""),
        (r"for Zadeyo", ""),
        (r"ZADEYO\s*/\s*", ""),
        (r"ZADEYO", ""),
        (r"Zadeyo", ""),
        (r"zadeyo", ""),
        (r"\s{2,}", " "),
        (r"\s+-\s+instant", " - instant"),
        (r"\s+\.", "."),
        (r"\s+,", ","),
    ]
    out = s
    for a, b in reps:
        out = re.sub(a, b, out, flags=re.I)
    return out


def rebuild_compare_neutral(name: str, html: str) -> str:
    """Rewrite comparison headings/copy without brand; keep table structure."""
    html = re.sub(
        rf"{re.escape(name)} cheats: Zadeyo vs 12 market alternatives",
        f"{esc(name)} cheats vs 12 market alternatives",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"Why [^<]* cheats are better with Zadeyo",
        f"Why these {esc(name)} cheats stand out",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<th scope="col">Zadeyo</th>',
        '<th scope="col">This offer</th>',
        html,
        flags=re.I,
    )
    html = re.sub(
        r"Zadeyo leads overall for",
        "This listing leads overall for",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"Zadeyo is the better default",
        "A clear storefront listing is the better default",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"Zadeyo wins this matrix",
        "a documented storefront wins this matrix",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"Zadeyo leads on documentation",
        "Documented storefronts lead on clarity",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<div class="brand-pill">[^<]*</div>\s*',
        '<div class="brand-pill">Cheat comparison guide</div>\n        ',
        html,
        flags=re.I,
    )
    return html


def patch_blog(slug: str) -> None:
    path = ROOT / "blogs" / slug / "index.html"
    if not path.exists():
        return
    name = PRODUCTS[slug]["name"]
    zurl = MAPPING.get(slug, {}).get("zadeyo", "https://zadeyo.com/shop")
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
    html = re.sub(
        r'<meta name="keywords" content="[^"]*"',
        f'<meta name="keywords" content="{esc(name)} cheats, {esc(name)} aimbot, {esc(name)} ESP, {esc(name)} wallhack, {esc(name)} spoofer, buy {esc(name)} cheats, compare {esc(name)} cheats, undetected {esc(name)} cheats"',
        html,
        count=1,
    )

    # H1
    html = re.sub(r"<h1>[^<]*</h1>", f"<h1>{esc(name)} Cheats</h1>", html, count=1)

    # CTA buttons — neutral label, keep product URL
    html = re.sub(
        r'<a class="cta" href="[^"]*"[^>]*>[^<]*</a>',
        f'<a class="cta" href="{esc(zurl)}" target="_blank" rel="noopener">Get {esc(name)} Cheats</a>',
        html,
    )

    # Hero aria-label without brand
    html = re.sub(
        r'aria-label="Buy [^"]* on Zadeyo"',
        f'aria-label="View {esc(name)} cheats"',
        html,
        flags=re.I,
    )
    html = re.sub(
        r'aria-label="Buy [^"]*cheats[^"]*"',
        f'aria-label="View {esc(name)} cheats"',
        html,
        flags=re.I,
    )

    # Schema brand
    html = re.sub(
        r'"name":\s*"Zadeyo"',
        '"name": "Cheat Catalog"',
        html,
    )
    html = re.sub(
        r'"seller":\s*\{\s*"@type":\s*"Organization",\s*"name":\s*"[^"]*"\s*\}',
        '"seller": {"@type": "Organization", "name": "Cheat Catalog"}',
        html,
    )

    # Features intro
    html = re.sub(
        r"feature list buyers and search engines can read clearly —[\s\S]*?for Zadeyo\.",
        f"feature list for {esc(name)} cheats — aimbot, ESP, wallhack, spoofer, and delivery details.",
        html,
        flags=re.I,
    )
    html = re.sub(
        rf'content="{re.escape(name)} cheat features on Zadeyo"',
        f'content="{esc(name)} cheat features"',
        html,
        flags=re.I,
    )
    html = re.sub(
        rf'"{re.escape(name)} cheat features on Zadeyo"',
        f'"{name} cheat features"',
        html,
    )

    # Comparison section copy
    html = rebuild_compare_neutral(name, html)

    # Summary / verdict boxes that name Zadeyo
    html = re.sub(
        r"Zadeyo [^\-<]* cheats — summary statement",
        f"{esc(name)} cheats — summary",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<strong[^>]*>Zadeyo</strong>",
        "<strong>This offer</strong>",
        html,
        flags=re.I,
    )

    # Global scrub remaining visible text (not URLs)
    def scrub_outside_urls(text: str) -> str:
        parts = re.split(r'(https://zadeyo\.com[^"\s<>]*)', text)
        out = []
        for i, part in enumerate(parts):
            if i % 2 == 1:
                out.append(part)  # keep URL
            else:
                out.append(scrub_text(part))
        return "".join(out)

    html = scrub_outside_urls(html)

    # Clean leftover awkward phrases after scrub
    html = re.sub(r"Cheats on\s*</", "Cheats</", html)
    html = re.sub(r"\s+are better\s+", " stand out ", html)
    html = re.sub(r"pages keep those points", "guides keep those points", html, flags=re.I)
    html = re.sub(r"documents which aim modes", "listings document which aim modes", html, flags=re.I)
    html = re.sub(r"lists ESP categories clearly", "ESP categories are listed clearly", html, flags=re.I)
    html = re.sub(r"states when a spoofer", "good listings state when a spoofer", html, flags=re.I)
    html = re.sub(r"treats status as patch-dependent", "status is treated as patch-dependent", html, flags=re.I)
    html = re.sub(r"Is\s+good for", f"Is this offer good for", html)
    html = re.sub(r"Why does\s+win this", "Why does this offer win this", html, flags=re.I)
    html = re.sub(r"comparison guide</div>", "Cheat comparison guide</div>", html)

    # Fix meta description in JSON-LD product description field after scrub
    html = re.sub(
        r'("description":\s*")[^"]*(")',
        rf'\1{desc.replace(chr(34), "")}\2',
        html,
        count=1,
    )

    path.write_text(html, encoding="utf-8")


def main() -> None:
    for slug in PRODUCTS:
        patch_blog(slug)

    # Home + blogs index
    for page in [ROOT / "index.html", ROOT / "blogs" / "index.html"]:
        if not page.exists():
            continue
        t = page.read_text(encoding="utf-8")
        t = re.sub(
            r"<title>[^<]*</title>",
            "<title>Game Cheats Catalog | Aimbot, ESP &amp; Wallhack</title>",
            t,
            count=1,
        )
        t = re.sub(
            r'<meta name="description" content="[^"]*"',
            '<meta name="description" content="Browse game cheats by title — aimbot, ESP, wallhack and spoofer guides with feature comparisons and buyer notes."',
            t,
            count=1,
        )
        t = re.sub(
            r'<meta property="og:title" content="[^"]*"',
            '<meta property="og:title" content="Game Cheats Catalog | Aimbot, ESP &amp; Wallhack"',
            t,
            count=1,
        )
        t = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            '<meta property="og:description" content="Browse game cheats by title — aimbot, ESP, wallhack and spoofer guides with feature comparisons."',
            t,
            count=1,
        )
        # scrub visible brand but keep href URLs
        parts = re.split(r'(https://zadeyo\.com[^"\s<>]*)', t)
        out = []
        for i, part in enumerate(parts):
            out.append(part if i % 2 == 1 else scrub_text(part))
        t = "".join(out)
        page.write_text(t, encoding="utf-8")
        print("scrubbed", page.name)

    # Verify no visible Zadeyo left in HTML (URLs allowed)
    left = []
    for path in list((ROOT / "blogs").glob("*/index.html")) + [
        ROOT / "index.html",
        ROOT / "blogs" / "index.html",
    ]:
        raw = path.read_text(encoding="utf-8")
        # remove URLs then search
        check = re.sub(r"https://zadeyo\.com[^\"\s<>]*", "", raw)
        if re.search(r"zadeyo", check, re.I):
            # find snippets
            for m in re.finditer(r".{0,40}zadeyo.{0,40}", check, re.I):
                left.append((str(path), m.group(0)))
                break
    print("remaining mentions", len(left))
    for p, s in left[:12]:
        print(" ", Path(p).name, ":", s.replace("\n", " ")[:100])

    # sample dayz
    b = (ROOT / "blogs" / "dayz" / "index.html").read_text(encoding="utf-8")
    print("title", re.search(r"<title>([^<]+)</title>", b).group(1))
    print("desc", re.search(r'name="description" content="([^"]+)"', b).group(1))
    print("cta", re.search(r'class="cta"[^>]*>([^<]+)', b).group(1))
    print("h1", re.search(r"<h1>([^<]+)</h1>", b).group(1))


if __name__ == "__main__":
    main()
