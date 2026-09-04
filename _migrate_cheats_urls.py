# -*- coding: utf-8 -*-
"""Migrate product URLs from /{slug}/ to /{slug}-cheats/ with SEO redirects."""
from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(r"c:\Users\ii\articles")
ORIGIN = "https://getyourcheats.com"
PRODUCTS = json.loads((ROOT / "_gen_products.json").read_text(encoding="utf-8"))


def new_slug(old: str) -> str:
    return old if old.endswith("-cheats") else f"{old}-cheats"


def redirect_html(old: str, new: str, name: str) -> str:
    dest = f"/{new}/"
    abs_dest = f"{ORIGIN}/{new}/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="robots" content="noindex, follow"/>
  <link rel="canonical" href="{abs_dest}"/>
  <meta http-equiv="refresh" content="0;url={dest}"/>
  <title>{name} Cheats moved</title>
  <script>location.replace('{dest}');</script>
</head>
<body>
  <p>{name} cheats moved to <a href="{dest}">{dest}</a>.</p>
</body>
</html>
"""


def rewrite_urls_in_text(text: str, mapping: list[tuple[str, str]]) -> str:
    """Replace old slug URL forms with new ones. Longest old slug first."""
    for old, new in mapping:
        # absolute
        text = text.replace(f"{ORIGIN}/{old}/", f"{ORIGIN}/{new}/")
        text = text.replace(f"{ORIGIN}/{old}\"", f"{ORIGIN}/{new}/\"")
        text = text.replace(f"{ORIGIN}/{old}'", f"{ORIGIN}/{new}/'")
        # path forms
        text = text.replace(f'href="/{old}"', f'href="/{new}"')
        text = text.replace(f"href='/{old}'", f"href='/{new}'")
        text = text.replace(f'href="/{old}/"', f'href="/{new}/"')
        text = text.replace(f"href='/{old}/'", f"href='/{new}/'")
        text = text.replace(f'url=/{old}/', f'url=/{new}/')
        text = text.replace(f"url='/{old}/'", f"url='/{new}/'")
        text = text.replace(f'location.replace(\'/{old}/\')', f"location.replace('/{new}/')")
        text = text.replace(f'location.replace("/{old}/")', f'location.replace("/{new}/")')
        # satano /images paths stay by old folder name - don't touch images/satano/{old}
    return text


def main() -> None:
    # longest-first to avoid gray-zone eating gray-zone-warfare
    pairs = sorted(
        [(p["slug"], new_slug(p["slug"]), p) for p in PRODUCTS],
        key=lambda x: len(x[0]),
        reverse=True,
    )
    mapping = [(o, n) for o, n, _ in pairs]

    # 1) Move directories + write redirect stubs
    for old, new, p in pairs:
        src = ROOT / old
        dst = ROOT / new
        if not src.exists() and dst.exists():
            print("already migrated", old)
            continue
        if src.exists() and not dst.exists():
            shutil.move(str(src), str(dst))
        elif src.exists() and dst.exists():
            # unexpected — prefer dst content, replace src with redirect
            print("both exist, keeping", new)
        else:
            print("MISSING", old)
            continue

        # rewrite inside new product page
        index = dst / "index.html"
        if index.exists():
            t = index.read_text(encoding="utf-8")
            t = rewrite_urls_in_text(t, mapping)
            # force SEO absolute targets for this page
            canon = f"{ORIGIN}/{new}/"
            t = re.sub(
                r'<link[^>]*rel="canonical"[^>]*>',
                f'<link rel="canonical" href="{canon}"/>',
                t,
                count=1,
                flags=re.I,
            )
            t = re.sub(r'<link[^>]*rel="alternate"[^>]*>', "", t, flags=re.I)
            t = t.replace(
                "</head>",
                f'<link rel="alternate" hreflang="en" href="{canon}"/>\n'
                f'<link rel="alternate" hreflang="x-default" href="{canon}"/>\n</head>',
                1,
            )
            t = re.sub(
                r'<meta[^>]*property="og:url"[^>]*>',
                f'<meta property="og:url" content="{canon}"/>',
                t,
                count=1,
                flags=re.I,
            )
            index.write_text(t, encoding="utf-8")

        # old path redirect stub
        src.mkdir(parents=True, exist_ok=True)
        (src / "index.html").write_text(
            redirect_html(old, new, p["name"]), encoding="utf-8"
        )

        # blogs stub → new URL
        blog = ROOT / "blogs" / old / "index.html"
        if blog.exists():
            blog.write_text(redirect_html(old, new, p["name"]), encoding="utf-8")
        # also blogs/{new} optional redirect from blogs
        blog_new = ROOT / "blogs" / new
        blog_new.mkdir(parents=True, exist_ok=True)
        (blog_new / "index.html").write_text(
            redirect_html(old, new, p["name"]), encoding="utf-8"
        )

    # 2) Update gen products
    for p in PRODUCTS:
        o = p["slug"]
        n = new_slug(o)
        p["slug"] = n
        p["base_slug"] = o if not o.endswith("-cheats") else o[: -len("-cheats")]
        p["href"] = f"/{n}"
    (ROOT / "_gen_products.json").write_text(
        json.dumps(PRODUCTS, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # 3) Rewrite site-wide HTML (home, blogs catalog, contact, store leftovers)
    html_files = list(ROOT.rglob("*.html"))
    skip_parts = {".git", "node_modules", "_cheatseller_source", "_source_backup"}
    for path in html_files:
        if any(part in skip_parts for part in path.parts):
            continue
        t = path.read_text(encoding="utf-8")
        t2 = rewrite_urls_in_text(t, mapping)
        if t2 != t:
            path.write_text(t2, encoding="utf-8")

    # 4) Sitemap — products first at 1.0
    today = date.today().isoformat()
    priority_bases = ["escape-from-tarkov", "rust", "dayz", "pubg"]
    order = {new_slug(s): i for i, s in enumerate(priority_bases)}
    products = sorted(PRODUCTS, key=lambda p: (order.get(p["slug"], 999), p["slug"]))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in products:
        lines += [
            "  <url>",
            f"    <loc>{ORIGIN}/{p['slug']}/</loc>",
            f"    <lastmod>{today}</lastmod>",
            "    <changefreq>daily</changefreq>",
            "    <priority>1.0</priority>",
            "  </url>",
        ]
    for loc, pri, freq in [
        (f"{ORIGIN}/", "0.5", "weekly"),
        (f"{ORIGIN}/blogs/", "0.4", "weekly"),
        (f"{ORIGIN}/contact/", "0.3", "monthly"),
    ]:
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 5) Worker with legacy 301 map
    legacy_entries = []
    for old, new, _ in pairs:
        legacy_entries.append(f'  "/{old}": "/{new}/",')
        legacy_entries.append(f'  "/{old}/": "/{new}/",')
    worker = f"""/**
 * Apex host redirect + legacy /{{game}} → /{{game}}-cheats/ + charset header.
 */
const LEGACY = {{
{chr(10).join(legacy_entries)}
}};

export default {{
  async fetch(request, env) {{
    const url = new URL(request.url);

    if (url.hostname === "www.getyourcheats.com") {{
      url.hostname = "getyourcheats.com";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }}

    const path = url.pathname.replace(/\\/+$/, "") || "/";
    const withSlash = path.endsWith("/") ? path : path + "/";
    const legacy =
      LEGACY[path] ||
      LEGACY[withSlash] ||
      LEGACY[path.replace(/\\/$/, "")] ||
      null;
    if (legacy) {{
      url.pathname = legacy;
      return Response.redirect(url.toString(), 301);
    }}

    const response = await env.ASSETS.fetch(request);
    const type = response.headers.get("Content-Type") || "";
    if (!type.includes("text/html")) {{
      return response;
    }}

    const headers = new Headers(response.headers);
    if (!/charset=/i.test(type)) {{
      headers.set("Content-Type", "text/html; charset=utf-8");
    }}
    headers.set("X-Content-Type-Options", "nosniff");

    return new Response(response.body, {{
      status: response.status,
      statusText: response.statusText,
      headers,
    }});
  }},
}};
"""
    (ROOT / "worker.js").write_text(worker, encoding="utf-8")

    # verify
    dayz_new = ROOT / "dayz-cheats" / "index.html"
    dayz_old = ROOT / "dayz" / "index.html"
    print("dayz-cheats exists", dayz_new.exists())
    print("dayz redirect exists", dayz_old.exists())
    t = dayz_new.read_text(encoding="utf-8")
    print("canonical", re.search(r'rel="canonical" href="([^"]+)"', t).group(1))
    print("hreflang", f'{ORIGIN}/dayz-cheats/' in t)
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    print("home link dayz-cheats", 'href="/dayz-cheats"' in home)
    print("home old dayz bare", 'href="/dayz"' in home and 'href="/dayz-cheats"' not in home.replace("-cheats", ""))
    # count remaining old product hrefs on home (should be 0 for bare old slugs as product cards)
    leftovers = []
    for old, new, _ in pairs:
        if f'href="/{old}"' in home or f'href="/{old}/"' in home:
            leftovers.append(old)
    print("home leftovers", leftovers[:10], "count", len(leftovers))
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    print("sitemap dayz-cheats", f"{ORIGIN}/dayz-cheats/" in sm)
    print("sitemap old dayz alone", f"{ORIGIN}/dayz/</loc>" in sm)


if __name__ == "__main__":
    main()
