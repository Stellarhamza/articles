# -*- coding: utf-8 -*-
"""Download wh-satano cheat images and wire them into our blog articles."""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(r"c:\Users\ii\articles")
IMG_ROOT = ROOT / "images" / "satano"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}

# our blog slug -> satano category path
MATCHES = {
    "escape-from-tarkov": "escape_from_tarkov",
    "rust": "rust",
    "dayz": "dayz",
    "pubg": "pybg",
    "battlefield-6": "battlefield-6",
    "call-of-duty-black-ops-7": "cod-black-ops-7",
    "duet-night-abyss": "duet-night-abyss",
    "pioneers-of-pagonia": "pioner",
    "megabonk": "megabonk",
    "humanitz": "humanitz",
    "the-division-2": "division2",
    "the-seven-deadly-sins": "tsds-origin",
    "neverness-to-everness": "neverness-to-everness",
    "ark-survival-ascended": "ark-ascended",
    "sand": "sand-raiders",
    "cod-bocw": "cod-cheats",
    "insurge": "insurgency",
    "moe": "myth_of_empires",
    "isle": "the-isle",
    "conan": "conan-exiles",
    "wunthering": "wuthering-waves",
    "gray-zone": "gray_zone_warfare",
    "gray-zone-warfare": "gray_zone_warfare",
    "bodycam": "bodycam",
    "the-first-descendant": "the_first_descendant",
    "zenless-zone-zero": "zenless-zone-zero",
    "deadlock": "deadlock",
    "snowbreak-containment-zone": "snowbreak-containment-zone",
    "off-the-grid": "off_the_grid",
    "marvel-rivals": "marvel_rivals",
    "left-4-dead-2": "l4d2",
    "arma-reforger": "arma-reforger",
    "cs-1-6": "cs",
    "fragpunk": "fragpunk",
    "path-of-exile-2": "path-of-exile-2",
    "last-epoch": "last-epoch",
    "arc-raiders": "arc-raiders",
    "etheria-restart": "etheria-restart",
    "foxhole": "foxhole",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def fetch_bin(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def extract_images(html: str) -> list[str]:
    found: list[str] = []
    patterns = [
        r'property=["\']og:image["\'][^>]*content=["\']([^"\']+)',
        r'content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
        r'https://cdn\.wh-satano\.ru/[^"\'\s>]+\.(?:webp|png|jpe?g|gif)',
        r'https://wh-satano\.ru/storage/[^"\'\s>]+\.(?:webp|png|jpe?g|gif)',
        r'(?:src|href)=["\'](/storage/[^"\']+\.(?:webp|png|jpe?g|gif))["\']',
    ]
    for pat in patterns:
        for m in re.findall(pat, html, re.I):
            u = m
            if u.startswith("/"):
                u = "https://wh-satano.ru" + u
            if u.endswith(".svg"):
                continue
            if u not in found:
                found.append(u)
    return found


def pick_primary(imgs: list[str]) -> str | None:
    if not imgs:
        return None
    # prefer screenshot-like s1 over logos/avatars
    for u in imgs:
        low = u.lower()
        if any(x in low for x in ("avatar", "logo", "icon", "flag")):
            continue
        if re.search(r"s1|_s1|preview|menu|chams|full|radar", low):
            return u
    for u in imgs:
        if "avatar" not in u.lower():
            return u
    return imgs[0]


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1000:
        return True
    try:
        data = fetch_bin(url)
        if len(data) < 500:
            return False
        dest.write_bytes(data)
        return True
    except Exception as e:
        print("  dl fail", url, e)
        return False


def ext_from_url(url: str) -> str:
    m = re.search(r"\.(webp|png|jpe?g|gif)(?:\?|$)", url, re.I)
    return (m.group(1).lower() if m else "webp").replace("jpeg", "jpg")


def version_links(html: str, cat: str) -> list[str]:
    return sorted(
        set(
            re.findall(
                rf"https://wh-satano\.ru/en/cheats/{re.escape(cat)}/([a-zA-Z0-9_\-]+)",
                html,
            )
        )
    )


def main() -> None:
    manifest: dict = {}
    IMG_ROOT.mkdir(parents=True, exist_ok=True)

    for blog_slug, cat in MATCHES.items():
        print("==", blog_slug, cat)
        cat_url = f"https://wh-satano.ru/en/cheats/{cat}"
        try:
            cat_html = fetch(cat_url)
        except Exception as e:
            print("  cat fail", e)
            continue
        time.sleep(0.12)

        versions = version_links(cat_html, cat)
        entry = {"category": cat_url, "hero": None, "versions": []}

        # category hero
        cat_imgs = extract_images(cat_html)
        hero_remote = pick_primary(cat_imgs)
        if hero_remote:
            ext = ext_from_url(hero_remote)
            hero_path = IMG_ROOT / blog_slug / f"hero.{ext}"
            if download(hero_remote, hero_path):
                entry["hero"] = f"/images/satano/{blog_slug}/hero.{ext}"
                print("  hero", entry["hero"])

        # version pages (cap to keep runtime reasonable; EFT gets all)
        limit = 20 if blog_slug == "escape-from-tarkov" else 6
        for ver in versions[:limit]:
            vurl = f"https://wh-satano.ru/en/cheats/{cat}/{ver}"
            try:
                vhtml = fetch(vurl)
            except Exception as e:
                print("  ver fail", ver, e)
                continue
            time.sleep(0.1)
            vimgs = extract_images(vhtml)
            primary = pick_primary(vimgs)
            title_m = re.search(r"<h1[^>]*>([^<]+)</h1>", vhtml)
            title = title_m.group(1).strip() if title_m else ver
            local = None
            if primary:
                ext = ext_from_url(primary)
                dest = IMG_ROOT / blog_slug / f"{ver}.{ext}"
                if download(primary, dest):
                    local = f"/images/satano/{blog_slug}/{ver}.{ext}"
            # also grab up to 2 extra screenshots for EFT gallery
            extras = []
            if blog_slug == "escape-from-tarkov":
                for i, u in enumerate(vimgs[1:4]):
                    if "avatar" in u.lower():
                        continue
                    ext = ext_from_url(u)
                    dest = IMG_ROOT / blog_slug / f"{ver}_{i+2}.{ext}"
                    if download(u, dest):
                        extras.append(f"/images/satano/{blog_slug}/{ver}_{i+2}.{ext}")
            entry["versions"].append(
                {
                    "slug": ver,
                    "title": title,
                    "url": vurl,
                    "image": local,
                    "extras": extras,
                }
            )
            print("  ", ver, "->", local)

        # fallback hero from first version image
        if not entry["hero"]:
            for v in entry["versions"]:
                if v.get("image"):
                    entry["hero"] = v["image"]
                    break

        manifest[blog_slug] = entry

    (ROOT / "_satano_images_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("manifest games", len(manifest))


if __name__ == "__main__":
    main()
