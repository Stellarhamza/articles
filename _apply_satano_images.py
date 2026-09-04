# -*- coding: utf-8 -*-
"""Apply downloaded Satano images to blog articles + catalog cards."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"c:\Users\ii\articles")
manifest = json.loads((ROOT / "_satano_images_manifest.json").read_text(encoding="utf-8"))
products = json.loads((ROOT / "_gen_products.json").read_text(encoding="utf-8"))
by_slug = {p["slug"]: p for p in products}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


GALLERY_CSS = """
  .satano-gallery { margin-top:1.25rem; }
  .satano-gallery h2 { margin:0 0 .85rem; font-size:1.15rem; }
  .satano-grid {
    display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:.85rem;
  }
  .satano-card {
    display:flex; flex-direction:column; gap:.45rem; text-decoration:none; color:inherit;
    background:rgba(18,16,42,.72); border:1px solid rgba(255,255,255,.10); border-radius:.9rem;
    overflow:hidden; transition:transform .2s ease, border-color .2s ease;
  }
  .satano-card:hover { transform:translateY(-2px); border-color:rgba(139,92,246,.55); }
  .satano-card img {
    width:100%; aspect-ratio:16/10; object-fit:cover; display:block; background:#100e28;
  }
  .satano-card span {
    padding:0 .65rem .7rem; font-size:.78rem; font-weight:600; color:#E2E8FF; line-height:1.3;
    display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;
  }
"""


def patch_blog(slug: str, data: dict) -> None:
    path = ROOT / "blogs" / slug / "index.html"
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    hero = data.get("hero")
    if not hero:
        return

    # Replace hero image src (first .hero-img)
    html2, n = re.subn(
        r'(<img class="hero-img" src=")[^"]+(")',
        rf'\1{hero}\2',
        html,
        count=1,
    )
    if n:
        html = html2
    # og/twitter/schema images
    html = re.sub(
        r'(property="og:image" content=")[^"]+(")',
        rf'\1{hero}\2',
        html,
        count=1,
    )
    html = re.sub(
        r'(name="twitter:image" content=")[^"]+(")',
        rf'\1{hero}\2',
        html,
        count=1,
    )
    html = re.sub(
        r'("image":\s*")[^"]+(")',
        rf'\1{hero}\2',
        html,
        count=1,
    )

    # inject gallery CSS once
    if "satano-gallery" not in html:
        html = html.replace("</style>", GALLERY_CSS + "\n  </style>", 1)

    # build gallery from versions with images
    cards = []
    for v in data.get("versions") or []:
        img = v.get("image")
        if not img:
            continue
        title = v.get("title") or v.get("slug") or "Cheat"
        # shorten title
        short = re.sub(r"\s*\(.*?\)\s*", " ", title).strip()
        short = re.sub(r"\s+", " ", short)[:64]
        cards.append(
            f'<a class="satano-card" href="/contact">'
            f'<img src="{esc(img)}" alt="{esc(short)} cheat screenshot" loading="lazy" width="320" height="200"/>'
            f"<span>{esc(short)}</span></a>"
        )
    if cards:
        gallery = (
            '<section class="satano-gallery" style="margin-top:1.25rem">'
            f"<h2>{esc(by_slug.get(slug, {}).get('name', slug))} cheat versions</h2>"
            '<p style="color:var(--muted);margin:0 0 1rem">Real cheat screenshots / builds for this game. Compare versions, then contact to buy.</p>'
            f'<div class="satano-grid">{"".join(cards)}</div></section>'
        )
        # remove old gallery if regenerating
        html = re.sub(
            r'<section class="satano-gallery"[\s\S]*?</section>',
            "",
            html,
            count=1,
        )
        # insert before FAQ or before related
        if "cheats FAQ" in html:
            html = html.replace(
                '<section style="margin-top:1.25rem">\n      <h2>',
                gallery + '\n\n    <section style="margin-top:1.25rem">\n      <h2>',
                1,
            )
            # fragile - find FAQ heading specifically
        if 'class="satano-gallery"' not in html:
            html = html.replace(
                f'<h2>{esc(by_slug.get(slug, {}).get("name", slug))} cheats FAQ</h2>',
                gallery + f'\n    </section>\n\n    <section style="margin-top:1.25rem">\n      <h2>{esc(by_slug.get(slug, {}).get("name", slug))} cheats FAQ</h2>',
                1,
            )
        # if still missing, append before footer
        if 'class="satano-gallery"' not in html:
            html = html.replace("<footer>", gallery + "\n    <footer>", 1)

    path.write_text(html, encoding="utf-8")
    print("patched blog", slug, "hero", hero, "cards", len(cards))


def patch_catalog() -> None:
    for page in [ROOT / "index.html", ROOT / "blogs" / "index.html"]:
        if not page.exists():
            continue
        t = page.read_text(encoding="utf-8")
        changed = 0
        for slug, data in manifest.items():
            hero = data.get("hero")
            if not hero:
                continue
            # replace img src inside the card linking to this blog
            pat = re.compile(
                rf'(href="/blogs/{re.escape(slug)}"[^>]*>[\s\S]*?<img src=")([^"]+)(")',
                re.M,
            )
            m = pat.search(t)
            if m and m.group(2) != hero:
                t = pat.sub(rf"\g<1>{hero}\g<3>", t, count=1)
                # also data-img if present
                t = re.sub(
                    rf'(href="/blogs/{re.escape(slug)}"[^>]*>[\s\S]*?data-img=")([^"]+)(")',
                    rf"\g<1>{hero}\g<3>",
                    t,
                    count=1,
                )
                changed += 1
        page.write_text(t, encoding="utf-8")
        print("catalog", page.name, "updated", changed)


def main() -> None:
    for slug, data in manifest.items():
        patch_blog(slug, data)
    patch_catalog()
    # update products json img fields for regen consistency
    for p in products:
        d = manifest.get(p["slug"])
        if d and d.get("hero"):
            p["img"] = d["hero"]
    (ROOT / "_gen_products.json").write_text(
        json.dumps(products, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("done")


if __name__ == "__main__":
    main()
