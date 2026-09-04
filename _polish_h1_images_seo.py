# -*- coding: utf-8 -*-
"""Polish H1s + Google image meta (OG/Twitter/JSON-LD) on all cheat pages."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"c:\Users\ii\articles")
PRODUCTS = {p["slug"]: p for p in json.loads((ROOT / "_gen_products.json").read_text(encoding="utf-8"))}
MANIFEST = {}
mp = ROOT / "_satano_images_manifest.json"
if mp.exists():
    MANIFEST = json.loads(mp.read_text(encoding="utf-8"))

ORIGIN_FILE = ROOT / "site-origin.txt"


def read_origin() -> str:
    if not ORIGIN_FILE.exists():
        ORIGIN_FILE.write_text(
            "# Put your live site origin on the next line, e.g. https://yourdomain.com\n",
            encoding="utf-8",
        )
        return ""
    for line in ORIGIN_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        return line.rstrip("/")
    return ""


SITE_ORIGIN = read_origin()


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def abs_url(path: str) -> str:
    if not path:
        return path
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    if SITE_ORIGIN:
        return SITE_ORIGIN + path
    # Path-absolute (resolved against the page host when crawled)
    return path


def pick_image(slug: str, product: dict) -> str:
    """Prefer product catalog art (consistent card), else satano hero/version."""
    img = product.get("img") or ""
    # verify file exists under ROOT
    if img.startswith("/"):
        local = ROOT / img.lstrip("/").replace("/", "\\")
        if not local.exists():
            # try posix
            local = ROOT / img.lstrip("/")
        if local.exists():
            return img
    data = MANIFEST.get(slug) or {}
    if data.get("hero"):
        return data["hero"]
    for v in data.get("versions") or []:
        if v.get("image"):
            return v["image"]
    return img or "/images/logo-128.png"


def meta_title(name: str) -> str:
    # Align with H1; keep ~50-60 chars
    base = f"{name} Cheats"
    if len(base) <= 28:
        return f"{base} | Aimbot, ESP & Wallhack Guide"
    if len(base) <= 40:
        return f"{base} | Aimbot, ESP & Spoofer"
    return f"{base} | Aimbot & ESP Guide"[:60]


def meta_desc(name: str) -> str:
    return (
        f"Compare {name} cheats with aimbot, ESP, wallhack and spoofer options. "
        f"See features, market alternatives, and buyer notes for {name} cheats."
    )[:155]


def image_dims(path: str) -> tuple[int, int]:
    try:
        from PIL import Image

        local = ROOT / path.lstrip("/")
        if local.exists():
            im = Image.open(local)
            return im.size
    except Exception:
        pass
    if "satano" in path:
        return (1600, 900)
    return (381, 434)


def patch_blog(slug: str, product: dict) -> None:
    path = ROOT / "blogs" / slug / "index.html"
    if not path.exists():
        return
    name = product["name"]
    html = path.read_text(encoding="utf-8")
    img = pick_image(slug, product)
    abs_img = abs_url(img)
    w, h = image_dims(img)
    title = meta_title(name)
    desc = meta_desc(name)
    h1 = f"{name} Cheats"

    # H1 — single perfect headline
    html = re.sub(r"<h1[^>]*>[\s\S]*?</h1>", f"<h1>{esc(h1)}</h1>", html, count=1)
    # Remove extra H1s if any
    h1_count = len(re.findall(r"<h1\b", html, re.I))
    if h1_count > 1:
        # keep first only — demote others to h2
        seen = [0]

        def demote(m):
            seen[0] += 1
            if seen[0] == 1:
                return m.group(0)
            return m.group(0).replace("<h1", "<h2").replace("</h1>", "</h2>")

        html = re.sub(r"<h1\b[^>]*>[\s\S]*?</h1>", demote, html, flags=re.I)

    # Titles / descriptions
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

    # Ensure twitter:card
    if 'name="twitter:card"' not in html:
        html = html.replace(
            "</head>",
            '<meta name="twitter:card" content="summary_large_image"/>\n</head>',
            1,
        )
    else:
        html = re.sub(
            r'<meta name="twitter:card" content="[^"]*"',
            '<meta name="twitter:card" content="summary_large_image"',
            html,
            count=1,
        )

    # OG / Twitter images — full image pack for Google/social
    img_meta = f"""
  <meta property="og:image" content="{esc(abs_img)}"/>
  <meta property="og:image:secure_url" content="{esc(abs_img)}"/>
  <meta property="og:image:type" content="image/{'webp' if abs_img.endswith('.webp') else 'jpeg'}"/>
  <meta property="og:image:width" content="{w}"/>
  <meta property="og:image:height" content="{h}"/>
  <meta property="og:image:alt" content="{esc(h1)}"/>
  <meta name="twitter:image" content="{esc(abs_img)}"/>
  <meta name="twitter:image:alt" content="{esc(h1)}"/>
  <link rel="image_src" href="{esc(abs_img)}"/>
"""
    # Remove old og:image / twitter:image / image_src lines then inject fresh block
    html = re.sub(r'\s*<meta property="og:image[^"]*" content="[^"]*"\s*/?>', "", html)
    html = re.sub(r'\s*<meta name="twitter:image[^"]*" content="[^"]*"\s*/?>', "", html)
    html = re.sub(r'\s*<link rel="image_src" href="[^"]*"\s*/?>', "", html)
    # inject after og:description or after description
    if 'property="og:description"' in html:
        html = re.sub(
            r'(<meta property="og:description" content="[^"]*"\s*/?>)',
            r"\1" + img_meta,
            html,
            count=1,
        )
    else:
        html = html.replace("</head>", img_meta + "</head>", 1)

    # Product schema image as ImageObject
    image_obj = {
        "@type": "ImageObject",
        "url": abs_img,
        "contentUrl": abs_img,
        "width": w,
        "height": h,
        "caption": h1,
    }

    def patch_product_schema(m: re.Match) -> str:
        try:
            data = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        if data.get("@type") == "Product":
            data["name"] = h1
            data["description"] = desc
            data["image"] = [abs_img]
            data["image"] = image_obj
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    html = re.sub(
        r'<script type="application/ld\+json">(\{.*?"@type":\s*"Product".*?\})</script>',
        patch_product_schema,
        html,
        count=1,
        flags=re.S,
    )

    # Also patch any "image": "/..." in remaining json-ld
    html = re.sub(
        r'("image":\s*")(/[^"]+)(")',
        lambda m: m.group(1) + abs_url(m.group(2)) + m.group(3),
        html,
    )

    # Breadcrumb / hero alt
    html = re.sub(
        r'(class="hero-img"[^>]*alt=")[^"]*(")',
        lambda m: m.group(1) + esc(h1) + m.group(2),
        html,
        count=1,
    )

    path.write_text(html, encoding="utf-8")


def patch_home() -> None:
    path = ROOT / "index.html"
    t = path.read_text(encoding="utf-8")
    # Prefer one clear H1
    # existing: Choose your cheat
    if "<h1" in t:
        t = re.sub(
            r"<h1([^>]*)>[\s\S]*?</h1>",
            r'<h1\1>Choose your cheat</h1>',
            t,
            count=1,
        )
    logo = abs_url("/images/logo-128.png")
    # Ensure home has og:image absolute-ish
    if 'property="og:image"' not in t:
        t = t.replace(
            "</head>",
            f'''
  <meta property="og:image" content="{esc(logo)}"/>
  <meta property="og:image:width" content="128"/>
  <meta property="og:image:height" content="128"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:image" content="{esc(logo)}"/>
  <link rel="image_src" href="{esc(logo)}"/>
</head>''',
            1,
        )
    else:
        t = re.sub(
            r'(property="og:image" content=")[^"]+(")',
            rf'\1{esc(logo)}\2',
            t,
            count=1,
        )
    # title/desc already ok-ish — polish
    t = re.sub(
        r"<title>[^<]*</title>",
        "<title>Game Cheats Catalog | Aimbot, ESP &amp; Wallhack</title>",
        t,
        count=1,
    )
    t = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Browse game cheats by title — aimbot, ESP, wallhack and spoofer guides with feature comparisons, images, and buyer notes."',
        t,
        count=1,
    )
    path.write_text(t, encoding="utf-8")

    # blogs index
    bip = ROOT / "blogs" / "index.html"
    if bip.exists():
        b = bip.read_text(encoding="utf-8")
        b = re.sub(
            r"<title>[^<]*</title>",
            "<title>Game Cheats Blog Catalog | Aimbot, ESP &amp; Wallhack</title>",
            b,
            count=1,
        )
        if 'property="og:image"' not in b:
            b = b.replace(
                "</head>",
                f'<meta property="og:image" content="{esc(logo)}"/><meta name="twitter:image" content="{esc(logo)}"/><meta name="twitter:card" content="summary_large_image"/></head>',
                1,
            )
        bip.write_text(b, encoding="utf-8")


def main() -> None:
    for slug, p in PRODUCTS.items():
        patch_blog(slug, p)
    patch_home()

    # Audit
    bad = 0
    for slug, p in PRODUCTS.items():
        t = (ROOT / "blogs" / slug / "index.html").read_text(encoding="utf-8")
        h1 = re.search(r"<h1[^>]*>([^<]+)</h1>", t)
        og = re.search(r'property="og:image" content="([^"]+)"', t)
        tw = re.search(r'name="twitter:image" content="([^"]+)"', t)
        if not h1 or h1.group(1).strip() != f"{p['name']} Cheats":
            bad += 1
            print("H1", slug, h1.group(1) if h1 else None)
        if not og or not tw:
            bad += 1
            print("IMG", slug, og.group(1) if og else None)
        # image file exists?
        if og:
            path = og.group(1)
            if path.startswith("http"):
                # strip origin if local
                path = "/" + "/".join(path.split("/")[3:]) if "://" in path else path
            local = ROOT / path.lstrip("/")
            if not local.exists():
                bad += 1
                print("MISSING FILE", slug, path)
    print("done bad", bad)


if __name__ == "__main__":
    main()
