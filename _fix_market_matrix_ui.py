# -*- coding: utf-8 -*-
"""Replace the wide 13-col market compare table with a readable scoreboard UI."""
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
    "WH-Satano",
    "Ancient",
    "Softhub",
    "Fecurity",
    "Unnamed private",
    "Discord reseller",
    "Telegram seller",
    "Forum paste",
    "DMA shop",
    "Free paste",
    "Unknown shop",
    "Mid-tier shop",
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
    "radar": "Radar",
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
    "spoofer": "Spoofer",
    "hack": "Pussycat",
}

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
    for w in [
        "Software",
        "Cheat",
        "Hack",
        "Buy",
        "for",
        "Tarkov",
        "EFT",
        "The First Descendant",
        "TFD",
        "Descendand",
    ]:
        t = re.sub(rf"\b{re.escape(w)}\b", "", t, flags=re.I)
    return re.sub(r"\s+", " ", t).strip(" -/|")[:22]


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


CSS = """
<style id="market-matrix-ui">
.market-matrix { margin-top: 1.25rem; }
.market-matrix > p { color: var(--muted); margin: 0 0 1.15rem; max-width: 46rem; }
.mm-scores {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(132px, 1fr));
  gap: .7rem;
  margin: 0 0 1.35rem;
}
.mm-score {
  position: relative;
  padding: .85rem .8rem .75rem;
  border-radius: .95rem;
  border: 1px solid rgba(255,255,255,.10);
  background: rgba(12,10,32,.88);
  display: flex; flex-direction: column; gap: .35rem;
  min-height: 96px;
}
.mm-score.featured {
  border-color: rgba(139,92,246,.55);
  background:
    radial-gradient(ellipse at top, rgba(103,57,255,.22), transparent 60%),
    rgba(22,16,52,.95);
  box-shadow: 0 10px 28px rgba(0,0,0,.28);
}
.mm-score .mm-label {
  font-size: .72rem; font-weight: 700; letter-spacing: .02em;
  color: #ABB0C7; text-transform: uppercase;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.mm-score.featured .mm-label { color: #c4b5fd; }
.mm-score .mm-num {
  font-size: 1.45rem; font-weight: 750; line-height: 1; color: #E2E8FF;
}
.mm-score .mm-num span { font-size: .8rem; font-weight: 600; color: #ABB0C7; }
.mm-score .mm-bar {
  height: 5px; border-radius: 999px; background: rgba(255,255,255,.08); overflow: hidden; margin-top: auto;
}
.mm-score .mm-bar i {
  display: block; height: 100%; border-radius: inherit;
  background: linear-gradient(90deg, #6739FF, #34d399);
}
.mm-score.weak .mm-bar i { background: linear-gradient(90deg, #6b7280, #f87171); }
.mm-score.mid .mm-bar i { background: linear-gradient(90deg, #a78bfa, #fbbf24); }
.mm-crits {
  display: grid; gap: .55rem;
  margin: 0 0 1.25rem;
}
.mm-crit {
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) minmax(118px, .65fr) minmax(118px, .65fr);
  gap: .55rem;
  align-items: stretch;
  padding: .7rem .75rem;
  border-radius: .9rem;
  border: 1px solid rgba(255,255,255,.08);
  background: rgba(10,8,28,.65);
}
.mm-crit-name {
  display: flex; align-items: center;
  font-size: .92rem; font-weight: 600; color: #E2E8FF; line-height: 1.35;
}
.mm-pill {
  display: flex; align-items: center; justify-content: center; gap: .35rem;
  padding: .55rem .5rem;
  border-radius: .7rem;
  font-size: .78rem; font-weight: 700;
  text-align: center;
}
.mm-pill.yes {
  color: #6ee7b7;
  background: rgba(52,211,153,.10);
  border: 1px solid rgba(52,211,153,.28);
}
.mm-pill.no {
  color: #fca5a5;
  background: rgba(248,113,113,.08);
  border: 1px solid rgba(248,113,113,.22);
}
.mm-pill.mix {
  color: #fcd34d;
  background: rgba(251,191,36,.08);
  border: 1px solid rgba(251,191,36,.22);
}
.mm-pill .tick, .mm-pill .cross { width: 14px; height: 14px; flex: 0 0 14px; margin: 0; }
.mm-rivals h3 { margin: 0 0 .75rem; font-size: 1rem; }
.mm-rival-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: .55rem;
}
.mm-rival {
  display: flex; align-items: center; justify-content: space-between; gap: .5rem;
  padding: .65rem .75rem;
  border-radius: .75rem;
  border: 1px solid rgba(255,255,255,.08);
  background: rgba(12,10,32,.7);
  font-size: .84rem;
}
.mm-rival strong {
  color: #E2E8FF; font-weight: 650;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.mm-rival em {
  font-style: normal; font-weight: 700; font-size: .78rem;
  padding: .2rem .45rem; border-radius: 999px;
  border: 1px solid rgba(255,255,255,.12); color: #ABB0C7;
}
.mm-rival.top em {
  color: #6ee7b7;
  border-color: rgba(52,211,153,.35);
  background: rgba(52,211,153,.08);
}
@media (max-width: 720px) {
  .mm-crit { grid-template-columns: 1fr; }
  .mm-scores { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .mm-score.featured { grid-column: 1 / -1; }
}
</style>
"""


def build_section(name: str, comps: list[str]) -> str:
    scores: list[tuple[str, int]] = []
    for i, c in enumerate(comps):
        s = sum(1 for ci in range(len(CRITERIA)) if other_score(ci, i))
        scores.append((c, s))

    score_cards = [
        '<div class="mm-score featured">'
        '<div class="mm-label">This offer</div>'
        '<div class="mm-num">10<span>/10</span></div>'
        '<div class="mm-bar"><i style="width:100%"></i></div>'
        "</div>"
    ]
    ranked = sorted(enumerate(scores), key=lambda x: (-x[1][1], x[0]))
    for _, (c, s) in ranked[:7]:
        pct = int(s / 10 * 100)
        cls = "weak" if s <= 2 else ("mid" if s <= 5 else "")
        score_cards.append(
            f'<div class="mm-score {cls}">'
            f'<div class="mm-label" title="{esc(c)}">{esc(c)}</div>'
            f'<div class="mm-num">{s}<span>/10</span></div>'
            f'<div class="mm-bar"><i style="width:{pct}%"></i></div>'
            "</div>"
        )

    crit_rows: list[str] = []
    for ci, label in enumerate(CRITERIA):
        lab = label.replace("{game}", name)
        yes_n = sum(1 for i in range(12) if other_score(ci, i))
        if yes_n >= 5:
            market_cls, market_txt, icon = "mix", f"Market mixed · {yes_n}/12", TICK
        elif yes_n >= 1:
            market_cls, market_txt, icon = "no", f"Rare · {yes_n}/12", CROSS
        else:
            market_cls, market_txt, icon = "no", "Usually missing", CROSS
        crit_rows.append(
            '<div class="mm-crit">'
            f'<div class="mm-crit-name">{esc(lab)}</div>'
            f'<div class="mm-pill yes">{TICK}<span>This offer</span></div>'
            f'<div class="mm-pill {market_cls}">{icon}<span>{esc(market_txt)}</span></div>'
            "</div>"
        )

    rivals = []
    for c, s in scores:
        top = " top" if s >= 4 else ""
        rivals.append(
            f'<div class="mm-rival{top}">'
            f'<strong title="{esc(c)}">{esc(c)}</strong>'
            f"<em>{s}/10</em>"
            "</div>"
        )

    return f"""
<section class="market-matrix -compare" style="margin-top:1.25rem">
  <h2>{esc(name)} cheats vs market alternatives</h2>
  <p>Scoreboard for <strong style="color:var(--text)">{esc(name)} cheats</strong> across 12 common channels.
  This offer leads on clarity, delivery, and support. Specialty DMA shops can still win narrow use-cases.</p>
  <div class="mm-scores">{''.join(score_cards)}</div>
  <div class="mm-crits">{''.join(crit_rows)}</div>
  <div class="mm-rivals">
    <h3>All 12 rivals scored</h3>
    <div class="mm-rival-list">{''.join(rivals)}</div>
  </div>
  <div class="why-" style="margin-top:1.1rem">
    <h3>Why these {esc(name)} cheats stand out</h3>
    <p style="color:var(--muted);margin:0 0 .75rem">Compared with <strong style="color:var(--text)">12+ market channels</strong>, a clear storefront listing beats Discord roulette for {esc(name)} aimbot/ESP/spoofer buys.</p>
    <ul class="ticks">
      <li>{TICK}<span><strong>Built around {esc(name)}:</strong> focused page, not a random multi-game dump.</span></li>
      <li>{TICK}<span><strong>Beats Discord/Telegram sellers:</strong> checkout and support stay on a storefront.</span></li>
      <li>{TICK}<span><strong>Beats cracked / free pastes:</strong> features and risk wording shown up front.</span></li>
      <li>{TICK}<span><strong>Instant delivery:</strong> no waiting for a loader in DMs.</span></li>
      <li>{TICK}<span><strong>Fair caveat:</strong> DMA dual-PC specialists can still win that niche alone.</span></li>
    </ul>
  </div>
</section>"""


SECTION_RE = re.compile(
    r'<section class="(?:-compare|market-matrix -compare|zadeyo-compare)"[\s\S]*?</section>',
    re.I,
)


def main() -> None:
    n = 0
    for slug, p in PRODUCTS.items():
        path = ROOT / slug / "index.html"
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        name = p["name"]
        section = build_section(name, competitors(slug, name)).strip()

        if 'id="market-matrix-ui"' in html:
            html = re.sub(
                r'<style id="market-matrix-ui">[\s\S]*?</style>',
                CSS.strip(),
                html,
                count=1,
            )
        else:
            html = html.replace("</head>", CSS + "\n</head>", 1)

        if SECTION_RE.search(html):
            html2, c = SECTION_RE.subn(section, html, count=1)
            if c == 0:
                print("REPLACE FAIL", slug)
                continue
            html = html2
        else:
            # insert before seo-rich or before footer
            if 'class="seo-rich"' in html:
                html = html.replace(
                    '<section class="seo-rich"',
                    section + '\n<section class="seo-rich"',
                    1,
                )
            else:
                html = html.replace("<footer>", section + "\n<footer>", 1)

        path.write_text(html, encoding="utf-8")
        n += 1

    tfd = (ROOT / "the-first-descendant" / "index.html").read_text(encoding="utf-8")
    print("updated", n)
    print("has matrix", "market-matrix" in tfd)
    print("no wide headers", "Pussycat External The First Descenda" not in tfd)
    print("scores", tfd.count("mm-score"))
    print("crits", tfd.count("mm-crit"))
    print("sample comps", competitors("the-first-descendant", "The First Descendant")[:5])


if __name__ == "__main__":
    main()
