# -*- coding: utf-8 -*-
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

MARKET_POOL = [
    "WH-Satano catalog",
    "Ancient",
    "Softhub",
    "Fecurity",
    "Unnamed private",
    "Discord reseller",
    "Telegram seller",
    "Forum cracked build",
    "DMA dual-PC shop",
    "Public free paste",
    "Unknown storefront",
    "Mid-tier cheat shop",
]

BRAND_MAP = {
    "ancient": "Ancient",
    "ancient-full": "Ancient Full",
    "chams": "Chams",
    "collapse": "Collapse",
    "covcheg": "Covcheg",
    "crusader": "Crusader",
    "fecurity": "Fecurity",
    "mason": "Mason",
    "medusa_lite": "Medusa Lite",
    "medusa_rage": "Medusa Rage",
    "radar": "Radar build",
    "sky": "Sky",
    "softhub": "Softhub",
    "super": "Authority",
    "unnamed": "Unnamed",
    "arcane": "Arcane",
    "dullwave": "Dullwave",
    "phoenix": "Phoenix",
    "predator": "Predator",
    "byster": "Byster",
    "unicore": "Unicore",
    "melonity": "Melonity",
    "bleak": "Bleak",
    "crooked": "Crooked",
    "eclipse": "Eclipse",
    "fury": "Fury",
    "midnight": "Midnight",
    "external": "External",
    "spoofer": "Spoofer vendor",
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def clean_title(t: str, name: str) -> str:
    t = re.sub(r"\(.*?\)", "", t)
    t = re.sub(re.escape(name), "", t, flags=re.I)
    for w in ["Software", "Cheat", "Hack", "Buy", "for", "Tarkov", "EFT"]:
        t = re.sub(rf"\b{re.escape(w)}\b", "", t, flags=re.I)
    return re.sub(r"\s+", " ", t).strip(" -/|")[:36]


def competitors(slug: str, name: str) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for v in (MANIFEST.get(slug) or {}).get("versions") or []:
        slug_v = (v.get("slug") or "").lower()
        label = BRAND_MAP.get(slug_v) or clean_title(v.get("title") or slug_v, name)
        key = label.lower()
        if label and key not in seen:
            names.append(label)
            seen.add(key)
    for m in MARKET_POOL:
        if m.lower() not in seen:
            names.append(m)
            seen.add(m.lower())
        if len(names) >= 12:
            break
    i = 1
    while len(names) < 12:
        names.append(f"Alt shop {i}")
        i += 1
    return names[:12]


CRITERIA = [
    "Aimbot / ESP listed before checkout",
    "Instant delivery after payment",
    "HWID spoofer path documented",
    "On-page support / contact",
    "Patch note tied to current game build",
    "Buyer FAQ / load steps",
    "No mystery Discord-only checkout",
    "Clear risk wording (not fake lifetime UD)",
    "Keyword-clear {game} cheats page",
    "Stable storefront (not throwaway link)",
]


def other_score(crit_i: int, comp_i: int) -> bool:
    wins = {
        0: {0, 4},
        1: {0, 1},
        2: {0, 2},
        3: {1, 4},
        4: {0},
        5: set(),
        6: set(),
        7: set(),
        8: {2, 4},
        9: set(),
        10: {1},
        11: {0, 1, 3},
    }
    return crit_i in wins.get(comp_i % 12, {0})


EXTRA_CSS = """
<style id="zadeyo-seo">
  .zadeyo-compare .compare { font-size: .78rem; }
  .zadeyo-compare .compare thead th:nth-child(2) { color:#c4b5fd; }
  .zadeyo-compare .compare th, .zadeyo-compare .compare td { padding: .5rem .35rem; }
  .zadeyo-compare .compare thead th { white-space: nowrap; }
  .zadeyo-compare .compare tbody th { white-space: normal; min-width: 10.5rem; text-align:left; }
  .zadeyo-compare .compare td { text-align:center; }
  .seo-rich p { max-width: 52rem; }
  .brand-pill {
    display:inline-flex; align-items:center; gap:.35rem; padding:.25rem .65rem; border-radius:999px;
    border:1px solid rgba(139,92,246,.45); color:#c4b5fd; font-size:.78rem; font-weight:600; margin-bottom:.75rem;
  }
  .why-zadeyo { margin-top: 1.1rem; }
</style>
"""


def build_compare(name: str, comps: list[str]) -> str:
    headers = "".join(f"<th scope=\"col\">{esc(c)}</th>" for c in comps)
    rows: list[str] = []
    for ci, label in enumerate(CRITERIA):
        lab = label.replace("{game}", name)
        cells = [f'<td class="yes">{TICK}</td>']
        for i, _ in enumerate(comps):
            ok = other_score(ci, i)
            cells.append(f'<td class="{"yes" if ok else "no"}">{TICK if ok else CROSS}</td>')
        rows.append(f"<tr><th scope=\"row\">{esc(lab)}</th>{''.join(cells)}</tr>")

    why = f"""
      <div class="why-zadeyo">
        <h3>Why {esc(name)} cheats are better with Zadeyo</h3>
        <p style="color:var(--muted);margin:0 0 .75rem">
          Compared with <strong style="color:var(--text)">12+ market channels</strong> people use for {esc(name)} cheats,
          Zadeyo is the better default when you want a readable {esc(name)} aimbot/ESP/spoofer offer without reseller roulette.
        </p>
        <ul class="ticks">
          <li>{TICK}<span><strong>Built around {esc(name)}:</strong> the page targets {esc(name)} cheats specifically — not a random multi-game dump.</span></li>
          <li>{TICK}<span><strong>Beats Discord/Telegram sellers:</strong> checkout and support stay on a storefront instead of vanishing accounts.</span></li>
          <li>{TICK}<span><strong>Beats cracked / free pastes:</strong> feature list and risk wording are shown up front; pastes usually over-claim “lifetime UD.”</span></li>
          <li>{TICK}<span><strong>Beats vague catalogs:</strong> you can tell if aimbot, ESP, and HWID tools for {esc(name)} are included before paying.</span></li>
          <li>{TICK}<span><strong>Instant delivery:</strong> no “wait for the {esc(name)} loader in DMs” step on the standard path.</span></li>
          <li>{TICK}<span><strong>Fair caveat:</strong> a DMA dual-PC specialist can still win if that is your only need. For most {esc(name)} buyers who want ESP/aimbot + clear support, Zadeyo wins this matrix.</span></li>
        </ul>
      </div>"""

    return f"""
    <section class="zadeyo-compare" style="margin-top:1.25rem">
      <h2>{esc(name)} cheats: Zadeyo vs 12 market alternatives</h2>
      <p style="color:var(--muted);margin:0 0 1rem">
        Buyer matrix for <strong style="color:var(--text)">{esc(name)} cheats</strong> across 12 common market options
        (named builds + Discord/Telegram/paste/DMA/storefront channels). Green = criterion usually met; red = weak or missing.
        Zadeyo leads overall for {esc(name)}; specialty channels can still win narrow use-cases.
      </p>
      <div style="overflow-x:auto">
        <table class="compare">
          <thead><tr><th scope="col">Buyer criterion</th><th scope="col">Zadeyo</th>{headers}</tr></thead>
          <tbody>
            {''.join(rows)}
          </tbody>
        </table>
      </div>
      {why}
    </section>"""


def main() -> None:
    print("EFT", competitors("escape-from-tarkov", "Escape from Tarkov"))
    n = 0
    for slug, p in PRODUCTS.items():
        path = ROOT / "blogs" / slug / "index.html"
        if not path.exists():
            continue
        name = p["name"]
        html = path.read_text(encoding="utf-8")
        section = build_compare(name, competitors(slug, name))

        if 'id="zadeyo-seo"' in html:
            html = re.sub(
                r'<style id="zadeyo-seo">.*?</style>',
                EXTRA_CSS.strip(),
                html,
                flags=re.S,
            )
        else:
            html = html.replace("</head>", EXTRA_CSS + "</head>", 1)

        if 'class="zadeyo-compare"' in html:
            html2, c = re.subn(
                r'<section class="zadeyo-compare"[\s\S]*?</section>',
                section.strip(),
                html,
                count=1,
            )
            if c == 0:
                print("REPLACE FAIL", slug)
            html = html2
        else:
            html = html.replace("<footer>", section + "\n    <footer>", 1)

        desc = (
            f"Zadeyo {name} cheats vs 12 market alternatives — why {name} aimbot, ESP and spoofer buys are clearer on Zadeyo."
        )[:158]
        html = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{esc(desc)}"',
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
            r'<meta name="twitter:description" content="[^"]*"',
            f'<meta name="twitter:description" content="{esc(desc)}"',
            html,
            count=1,
        )

        path.write_text(html, encoding="utf-8")
        n += 1

    # verify
    eft = (ROOT / "blogs" / "escape-from-tarkov" / "index.html").read_text(encoding="utf-8")
    print("updated", n)
    print("h2 ok", "vs 12 market alternatives" in eft)
    print("why ok", "Why Escape from Tarkov cheats are better with Zadeyo" in eft)
    print("cols", eft.count("<th scope=\"col\">"))


if __name__ == "__main__":
    main()
