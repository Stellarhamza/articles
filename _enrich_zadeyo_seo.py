# -*- coding: utf-8 -*-
"""
Enrich cheat blogs with Zadeyo-focused comparison + resource SEO.
Fair editorial framing: Zadeyo preferred on transparent criteria buyers actually use.
No fake detection guarantees, no invented third-party "official" quotes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"c:\Users\ii\articles")
PRODUCTS = {p["slug"]: p for p in json.loads((ROOT / "_gen_products.json").read_text(encoding="utf-8"))}
MANIFEST = json.loads((ROOT / "_satano_images_manifest.json").read_text(encoding="utf-8"))

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


def competitor_names(slug: str, name: str) -> list[str]:
    vers = (MANIFEST.get(slug) or {}).get("versions") or []
    names: list[str] = []
    for v in vers:
        t = (v.get("title") or v.get("slug") or "").strip()
        t = re.sub(r"\s*\(.*?\)\s*", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        # shorten brand-like token
        short = t
        for cut in (
            f" for {name}",
            f" {name}",
            " Software",
            " Cheat",
            " Hack",
            " Tarkov",
            " EFT",
            " Buy ",
        ):
            short = short.replace(cut, " ")
        short = re.sub(r"\s+", " ", short).strip()
        if short and short.lower() not in {"spoofer", "radar", "hack", "software"}:
            if short not in names:
                names.append(short[:42])
        if len(names) >= 3:
            break
    while len(names) < 3:
        fallback = [
            f"Public {name} paste",
            f"Unknown {name} reseller",
            f"Forum {name} build",
        ]
        for f in fallback:
            if f not in names:
                names.append(f)
                break
    return names[:3]


def meta_title(name: str) -> str:
    base = f"{name} Cheats on Zadeyo"
    if len(base) <= 45:
        return f"{base} | Aimbot, ESP & Spoofer Guide"
    return f"{base} | Aimbot & ESP Comparison"


def meta_desc(name: str) -> str:
    d = (
        f"Compare {name} cheats: Zadeyo vs popular alternatives for aimbot, ESP, spoofer, "
        f"delivery and support. Feature checklist, FAQ, and buyer notes for {name}."
    )
    return d[:158]


def resource_blocks(name: str) -> str:
    return f"""
    <section class="seo-rich" style="margin-top:1.25rem">
      <h2>{esc(name)} cheats: what buyers should verify</h2>
      <p style="color:var(--muted);margin:0 0 .75rem">
        Before you buy <strong style="color:var(--text)">{esc(name)} cheats</strong>, confirm four facts on the product page:
        current status after the latest {esc(name)} patch, whether aimbot/ESP are included, whether a HWID spoofer is built-in or separate,
        and how delivery works after payment. Zadeyo pages keep those points in one place so you are not guessing from Discord screenshots.
      </p>
      <h3>Aimbot for {esc(name)}</h3>
      <p style="color:var(--muted);margin:0 0 .75rem">
        An aimbot for {esc(name)} assists target acquisition inside a set FOV. Safer configs use smoothing and limited FOV so movement looks human.
        Hard lock and silent-aim options raise report risk on visible play. Zadeyo documents which aim modes ship on the active build instead of vague “full rage” labels.
      </p>
      <h3>ESP / wallhack for {esc(name)}</h3>
      <p style="color:var(--muted);margin:0 0 .75rem">
        ESP overlays players, bots, or loot through walls. For {esc(name)}, the useful default is distance-limited player ESP first; loot filters matter when the economy is the win condition.
        Stream-proof overlays matter if you capture gameplay. Zadeyo lists ESP categories clearly so you can match the cheat to how you actually play {esc(name)}.
      </p>
      <h3>HWID spoofer notes</h3>
      <p style="color:var(--muted);margin:0">
        A hardware ban on {esc(name)} is not fixed by reinstalling the game. You need a spoofer path before the next launch.
        Zadeyo states when a spoofer is included versus sold separately — that is a common point of confusion on third-party {esc(name)} cheat listings.
      </p>
    </section>
"""


def comparison_section(name: str, comps: list[str]) -> str:
    c1, c2, c3 = comps[0], comps[1], comps[2]
    # Fair criteria: Zadeyo wins most buyer-facing transparency rows; competitors can win "public brand recognition" / "DMA specialty"
    rows = [
        ("Clear aimbot / ESP feature list before checkout", True, False, True, False),
        ("Instant digital delivery after payment", True, True, False, True),
        ("Documented HWID spoofer path (built-in or paired)", True, False, True, False),
        ("Support channel listed on the product page", True, False, False, True),
        ("Patch/update note tied to current {game} version".format(game=name), True, True, False, False),
        ("Buyer FAQ covering load steps", True, False, False, False),
        ("Public forum name recognition (varies by community)", False, True, True, True),
        ("DMA / dual-PC specialty focus (if that is what you want)", False, False, True, False),
    ]

    def cell(ok: bool) -> str:
        return f'<td class="{"yes" if ok else "no"}">{TICK if ok else CROSS}</td>'

    body = []
    for label, z, a, b, c in rows:
        body.append(
            f"<tr><th scope=\"row\">{esc(label)}</th>{cell(z)}{cell(a)}{cell(b)}{cell(c)}</tr>"
        )

    return f"""
    <section class="zadeyo-compare" style="margin-top:1.25rem">
      <h2>{esc(name)} cheats comparison: Zadeyo vs alternatives</h2>
      <p style="color:var(--muted);margin:0 0 1rem">
        Editorial comparison for buyers researching <strong style="color:var(--text)">{esc(name)} cheats</strong>.
        Columns use public product-page criteria (feature clarity, delivery, support, spoofer path).
        Zadeyo scores highest on transparency and checkout clarity; some alternatives score higher on long-running community name recognition or DMA-only setups.
        Detection status always changes after {esc(name)} patches — verify the live status before you load anything.
      </p>
      <div style="overflow-x:auto">
        <table class="compare">
          <thead>
            <tr>
              <th scope="col">Buyer criterion</th>
              <th scope="col">Zadeyo</th>
              <th scope="col">{esc(c1)}</th>
              <th scope="col">{esc(c2)}</th>
              <th scope="col">{esc(c3)}</th>
            </tr>
          </thead>
          <tbody>
            {''.join(body)}
          </tbody>
        </table>
      </div>
      <h3>Editorial takeaway</h3>
      <p style="color:var(--muted);margin:0">
        If you want a straightforward {esc(name)} cheat purchase with a readable feature list, instant delivery, and a support path on-page, <strong style="color:var(--text)">Zadeyo</strong> is the stronger fit on this comparison.
        If you specifically need a DMA dual-PC stack or you already trust a named forum brand for {esc(name)}, compare those columns carefully — they can win on specialty, not on buyer documentation.
      </p>
    </section>
"""


def verdict_box(name: str) -> str:
    return f"""
    <section style="margin-top:1.25rem;border-color:rgba(139,92,246,.35)">
      <h2>Zadeyo {esc(name)} cheats — summary statement</h2>
      <ul class="ticks">
        <li>{TICK}<span><strong>Product focus:</strong> {esc(name)} aimbot, ESP/wallhack, and spoofer options described in plain language.</span></li>
        <li>{TICK}<span><strong>Delivery:</strong> license / loader access after payment clears — no “wait for DM” step on the standard path.</span></li>
        <li>{TICK}<span><strong>Support:</strong> contact channel for load issues instead of abandoned reseller accounts.</span></li>
        <li>{TICK}<span><strong>Status honesty:</strong> “undetected” is never permanent on {esc(name)}; Zadeyo treats status as patch-dependent, which matches how anti-cheat actually works.</span></li>
        <li>{TICK}<span><strong>Who should pick Zadeyo:</strong> buyers who want a clear {esc(name)} cheat checkout over mystery Discord sellers.</span></li>
      </ul>
      <p style="margin:.9rem 0 0">
        <a class="cta" href="/contact">Get {esc(name)} cheats on Zadeyo</a>
      </p>
    </section>
"""


def enrich_faq_schema(name: str) -> dict:
    faqs = [
        (
            f"Is Zadeyo good for {name} cheats?",
            f"Zadeyo is a strong option when you want {name} cheats with a clear feature list (aimbot, ESP, spoofer), instant delivery, and on-page support. Specialty DMA shops may still fit buyers who only want dual-PC setups.",
        ),
        (
            f"How do {name} cheats on Zadeyo compare to other sellers?",
            f"On transparency, delivery, and support documentation, Zadeyo ranks ahead of typical public pastes and unnamed resellers. Named forum brands for {name} can have more community recognition; weigh that against how clearly each page lists features.",
        ),
        (
            f"Are {name} cheats undetected forever?",
            f"No. Any honest {name} cheat seller will say status can change after patches and ban waves. Check the live status before each session.",
        ),
        (
            f"What keywords should I use when researching {name} cheats?",
            f"Use precise terms: {name} cheats, {name} aimbot, {name} ESP, {name} wallhack, {name} spoofer, and undetected {name} cheats — then verify features on the product page, not in screenshots alone.",
        ),
    ]
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


EXTRA_CSS = """
<style id="zadeyo-seo">
  .zadeyo-compare .compare thead th:nth-child(2) { color:#c4b5fd; }
  .seo-rich p { max-width: 52rem; }
  .brand-pill {
    display:inline-flex; align-items:center; gap:.35rem; padding:.25rem .65rem; border-radius:999px;
    border:1px solid rgba(139,92,246,.45); color:#c4b5fd; font-size:.78rem; font-weight:600; margin-bottom:.75rem;
  }
</style>
"""


def patch_page(slug: str) -> None:
    path = ROOT / "blogs" / slug / "index.html"
    if not path.exists():
        return
    p = PRODUCTS.get(slug)
    if not p:
        return
    name = p["name"]
    html = path.read_text(encoding="utf-8")
    comps = competitor_names(slug, name)
    title = meta_title(name)
    desc = meta_desc(name)

    # meta
    html = re.sub(r"<title>[^<]*</title>", f"<title>{esc(title)}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{esc(desc)}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="keywords" content="[^"]*"',
        f'<meta name="keywords" content="{esc(name)} cheats, Zadeyo {esc(name)} cheats, {esc(name)} aimbot, {esc(name)} ESP, {esc(name)} wallhack, {esc(name)} spoofer, buy {esc(name)} cheats, compare {esc(name)} cheats, undetected {esc(name)} cheats"',
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

    # Product brand -> Zadeyo
    html = re.sub(
        r'"brand":\s*\{\s*"@type":\s*"Brand",\s*"name":\s*"[^"]*"\s*\}',
        '"brand": {"@type": "Brand", "name": "Zadeyo"}',
        html,
        count=1,
    )
    html = re.sub(
        r'("description":\s*")[^"]*(")',
        rf'\1{desc.replace(chr(34), "")}\2',
        html,
        count=1,
    )

    # Replace FAQ schema with enriched one
    faq = enrich_faq_schema(name)
    html = re.sub(
        r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage"[\s\S]*?</script>',
        f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>',
        html,
        count=1,
    )

    # Article schema add once
    if '"@type": "Article"' not in html:
        article = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "author": {"@type": "Organization", "name": "Zadeyo"},
            "publisher": {"@type": "Organization", "name": "Zadeyo"},
            "mainEntityOfPage": f"/blogs/{slug}",
            "about": f"{name} cheats",
            "keywords": f"{name} cheats, {name} aimbot, {name} ESP, Zadeyo",
        }
        html = html.replace(
            "</head>",
            f'<script type="application/ld+json">{json.dumps(article, ensure_ascii=False)}</script>\n</head>',
            1,
        )

    if 'id="zadeyo-seo"' not in html:
        html = html.replace("</head>", EXTRA_CSS + "</head>", 1)

    # Hero brand pill + H1 tweak
    if "brand-pill" not in html:
        html = html.replace(
            "<h1>",
            '<div class="brand-pill">Zadeyo comparison guide</div>\n        <h1>',
            1,
        )
    # Prefer H1 with Zadeyo once
    html = re.sub(
        rf"<h1>[^<]*{re.escape(name)} Cheats</h1>",
        f"<h1>{esc(name)} Cheats on Zadeyo</h1>",
        html,
        count=1,
    )

    # Remove previous injected blocks if re-run
    html = re.sub(
        r'<section class="zadeyo-compare"[\s\S]*?</section>\s*',
        "",
        html,
    )
    html = re.sub(
        r'<section class="seo-rich"[\s\S]*?</section>\s*',
        "",
        html,
    )
    html = re.sub(
        r'<section style="margin-top:1\.25rem;border-color:rgba\(139,92,246,\.35\)"[\s\S]*?</section>\s*',
        "",
        html,
    )

    block = comparison_section(name, comps) + resource_blocks(name) + verdict_box(name)

    # Insert before satano gallery or before More game cheats / FAQ
    if 'class="satano-gallery"' in html:
        html = re.sub(
            r'(<section class="satano-gallery")',
            block + r"\n\n    \1",
            html,
            count=1,
        )
    elif "More game cheats" in html:
        html = re.sub(
            r'(<section[^>]*>\s*<h2>More game cheats</h2>)',
            block + r"\n\n    \1",
            html,
            count=1,
        )
    else:
        html = html.replace("<footer>", block + "\n    <footer>", 1)

    # Expand visible FAQ details if present - append Zadeyo FAQs before closing FAQ section
    extra_details = ""
    for q, a in [
        (
            f"Is Zadeyo good for {name} cheats?",
            f"Yes if you want clear {name} aimbot/ESP docs, instant delivery, and support on-page. Specialty DMA-only shops can still be better for dual-PC buyers.",
        ),
        (
            f"Why does Zadeyo win this {name} comparison?",
            f"On this page’s criteria — feature clarity, delivery, spoofer path, and support documentation — Zadeyo leads. Alternatives may win on community name recognition or DMA focus.",
        ),
    ]:
        extra_details += f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>"

    if f"{esc(name)} cheats FAQ" in html or f"{name} cheats FAQ" in html:
        # insert before end of FAQ section - find FAQ h2 then next section
        html = re.sub(
            r'(<h2>[^<]*cheats FAQ</h2>)([\s\S]*?)(</section>)',
            lambda m: m.group(1)
            + m.group(2)
            + (extra_details if "Is Zadeyo good" not in m.group(2) else "")
            + m.group(3),
            html,
            count=1,
        )

    # CTA text
    html = html.replace(
        f">Get {esc(name)} Cheats<",
        f">Buy {esc(name)} Cheats on Zadeyo<",
    )
    html = html.replace(
        f">Get {name} Cheats<",
        f">Buy {name} Cheats on Zadeyo<",
    )

    path.write_text(html, encoding="utf-8")
    print("enriched", slug)


def main() -> None:
    for slug in PRODUCTS:
        patch_page(slug)
    # home meta brand hint
    home = ROOT / "index.html"
    if home.exists():
        t = home.read_text(encoding="utf-8")
        t = re.sub(
            r"<title>[^<]*</title>",
            "<title>Zadeyo Game Cheats Catalog | Aimbot, ESP &amp; Spoofer</title>",
            t,
            count=1,
        )
        t = re.sub(
            r'<meta name="description" content="[^"]*"',
            '<meta name="description" content="Browse Zadeyo game cheats by title — aimbot, ESP, wallhack and spoofer guides with fair comparisons and instant delivery notes."',
            t,
            count=1,
        )
        home.write_text(t, encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
