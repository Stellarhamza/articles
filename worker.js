/**
 * Apex host redirect + legacy /{game} → /{game}-cheats/ + charset header.
 */
const LEGACY = {
  "/snowbreak-containment-zone": "/snowbreak-containment-zone-cheats/",
  "/snowbreak-containment-zone/": "/snowbreak-containment-zone-cheats/",
  "/call-of-duty-black-ops-7": "/call-of-duty-black-ops-7-cheats/",
  "/call-of-duty-black-ops-7/": "/call-of-duty-black-ops-7-cheats/",
  "/the-seven-deadly-sins": "/the-seven-deadly-sins-cheats/",
  "/the-seven-deadly-sins/": "/the-seven-deadly-sins-cheats/",
  "/neverness-to-everness": "/neverness-to-everness-cheats/",
  "/neverness-to-everness/": "/neverness-to-everness-cheats/",
  "/ark-survival-ascended": "/ark-survival-ascended-cheats/",
  "/ark-survival-ascended/": "/ark-survival-ascended-cheats/",
  "/the-first-descendant": "/the-first-descendant-cheats/",
  "/the-first-descendant/": "/the-first-descendant-cheats/",
  "/pioneers-of-pagonia": "/pioneers-of-pagonia-cheats/",
  "/pioneers-of-pagonia/": "/pioneers-of-pagonia-cheats/",
  "/company-of-heroes-3": "/company-of-heroes-3-cheats/",
  "/company-of-heroes-3/": "/company-of-heroes-3-cheats/",
  "/black-desert-mobile": "/black-desert-mobile-cheats/",
  "/black-desert-mobile/": "/black-desert-mobile-cheats/",
  "/escape-from-tarkov": "/escape-from-tarkov-cheats/",
  "/escape-from-tarkov/": "/escape-from-tarkov-cheats/",
  "/russian-fishing-4": "/russian-fishing-4-cheats/",
  "/russian-fishing-4/": "/russian-fishing-4-cheats/",
  "/gray-zone-warfare": "/gray-zone-warfare-cheats/",
  "/gray-zone-warfare/": "/gray-zone-warfare-cheats/",
  "/zenless-zone-zero": "/zenless-zone-zero-cheats/",
  "/zenless-zone-zero/": "/zenless-zone-zero-cheats/",
  "/duet-night-abyss": "/duet-night-abyss-cheats/",
  "/duet-night-abyss/": "/duet-night-abyss-cheats/",
  "/mongil-star-dive": "/mongil-star-dive-cheats/",
  "/mongil-star-dive/": "/mongil-star-dive-cheats/",
  "/team-fortress-2": "/team-fortress-2-cheats/",
  "/team-fortress-2/": "/team-fortress-2-cheats/",
  "/path-of-exile-2": "/path-of-exile-2-cheats/",
  "/path-of-exile-2/": "/path-of-exile-2-cheats/",
  "/etheria-restart": "/etheria-restart-cheats/",
  "/etheria-restart/": "/etheria-restart-cheats/",
  "/the-division-2": "/the-division-2-cheats/",
  "/the-division-2/": "/the-division-2-cheats/",
  "/honor-of-kings": "/honor-of-kings-cheats/",
  "/honor-of-kings/": "/honor-of-kings-cheats/",
  "/battlefield-6": "/battlefield-6-cheats/",
  "/battlefield-6/": "/battlefield-6-cheats/",
  "/7-days-to-die": "/7-days-to-die-cheats/",
  "/7-days-to-die/": "/7-days-to-die-cheats/",
  "/marvel-rivals": "/marvel-rivals-cheats/",
  "/marvel-rivals/": "/marvel-rivals-cheats/",
  "/left-4-dead-2": "/left-4-dead-2-cheats/",
  "/left-4-dead-2/": "/left-4-dead-2-cheats/",
  "/arma-reforger": "/arma-reforger-cheats/",
  "/arma-reforger/": "/arma-reforger-cheats/",
  "/steel-hunters": "/steel-hunters-cheats/",
  "/steel-hunters/": "/steel-hunters-cheats/",
  "/off-the-grid": "/off-the-grid-cheats/",
  "/off-the-grid/": "/off-the-grid-cheats/",
  "/ea-sports-fc": "/ea-sports-fc-cheats/",
  "/ea-sports-fc/": "/ea-sports-fc-cheats/",
  "/maplestory-m": "/maplestory-m-cheats/",
  "/maplestory-m/": "/maplestory-m-cheats/",
  "/mecha-break": "/mecha-break-cheats/",
  "/mecha-break/": "/mecha-break-cheats/",
  "/six-day-ful": "/six-day-ful-cheats/",
  "/six-day-ful/": "/six-day-ful-cheats/",
  "/l33t-ragemp": "/l33t-ragemp-cheats/",
  "/l33t-ragemp/": "/l33t-ragemp-cheats/",
  "/predecessor": "/predecessor-cheats/",
  "/predecessor/": "/predecessor-cheats/",
  "/point-blank": "/point-blank-cheats/",
  "/point-blank/": "/point-blank-cheats/",
  "/8-ball-pool": "/8-ball-pool-cheats/",
  "/8-ball-pool/": "/8-ball-pool-cheats/",
  "/arc-raiders": "/arc-raiders-cheats/",
  "/arc-raiders/": "/arc-raiders-cheats/",
  "/brawlhalla": "/brawlhalla-cheats/",
  "/brawlhalla/": "/brawlhalla-cheats/",
  "/titanfall2": "/titanfall2-cheats/",
  "/titanfall2/": "/titanfall2-cheats/",
  "/wunthering": "/wunthering-cheats/",
  "/wunthering/": "/wunthering-cheats/",
  "/once-human": "/once-human-cheats/",
  "/once-human/": "/once-human-cheats/",
  "/level-zero": "/level-zero-cheats/",
  "/level-zero/": "/level-zero-cheats/",
  "/last-epoch": "/last-epoch-cheats/",
  "/last-epoch/": "/last-epoch-cheats/",
  "/wot-blitz": "/wot-blitz-cheats/",
  "/wot-blitz/": "/wot-blitz-cheats/",
  "/gray-zone": "/gray-zone-cheats/",
  "/gray-zone/": "/gray-zone-cheats/",
  "/diablo-iv": "/diablo-iv-cheats/",
  "/diablo-iv/": "/diablo-iv-cheats/",
  "/tarisland": "/tarisland-cheats/",
  "/tarisland/": "/tarisland-cheats/",
  "/free-fire": "/free-fire-cheats/",
  "/free-fire/": "/free-fire-cheats/",
  "/megabonk": "/megabonk-cheats/",
  "/megabonk/": "/megabonk-cheats/",
  "/marathon": "/marathon-cheats/",
  "/marathon/": "/marathon-cheats/",
  "/humanitz": "/humanitz-cheats/",
  "/humanitz/": "/humanitz-cheats/",
  "/windrose": "/windrose-cheats/",
  "/windrose/": "/windrose-cheats/",
  "/cod-bocw": "/cod-bocw-cheats/",
  "/cod-bocw/": "/cod-bocw-cheats/",
  "/starship": "/starship-cheats/",
  "/starship/": "/starship-cheats/",
  "/deadlock": "/deadlock-cheats/",
  "/deadlock/": "/deadlock-cheats/",
  "/duckside": "/duckside-cheats/",
  "/duckside/": "/duckside-cheats/",
  "/fragpunk": "/fragpunk-cheats/",
  "/fragpunk/": "/fragpunk-cheats/",
  "/insurge": "/insurge-cheats/",
  "/insurge/": "/insurge-cheats/",
  "/bodycam": "/bodycam-cheats/",
  "/bodycam/": "/bodycam-cheats/",
  "/foxhole": "/foxhole-cheats/",
  "/foxhole/": "/foxhole-cheats/",
  "/rematch": "/rematch-cheats/",
  "/rematch/": "/rematch-cheats/",
  "/koboom": "/koboom-cheats/",
  "/koboom/": "/koboom-cheats/",
  "/roblox": "/roblox-cheats/",
  "/roblox/": "/roblox-cheats/",
  "/hytale": "/hytale-cheats/",
  "/hytale/": "/hytale-cheats/",
  "/vostok": "/vostok-cheats/",
  "/vostok/": "/vostok-cheats/",
  "/rocket": "/rocket-cheats/",
  "/rocket/": "/rocket-cheats/",
  "/cs-1-6": "/cs-1-6-cheats/",
  "/cs-1-6/": "/cs-1-6-cheats/",
  "/realm": "/realm-cheats/",
  "/realm/": "/realm-cheats/",
  "/atlas": "/atlas-cheats/",
  "/atlas/": "/atlas-cheats/",
  "/conan": "/conan-cheats/",
  "/conan/": "/conan-cheats/",
  "/chess": "/chess-cheats/",
  "/chess/": "/chess-cheats/",
  "/sa-mp": "/sa-mp-cheats/",
  "/sa-mp/": "/sa-mp-cheats/",
  "/rust": "/rust-cheats/",
  "/rust/": "/rust-cheats/",
  "/dayz": "/dayz-cheats/",
  "/dayz/": "/dayz-cheats/",
  "/pubg": "/pubg-cheats/",
  "/pubg/": "/pubg-cheats/",
  "/sand": "/sand-cheats/",
  "/sand/": "/sand-cheats/",
  "/swbf": "/swbf-cheats/",
  "/swbf/": "/swbf-cheats/",
  "/wows": "/wows-cheats/",
  "/wows/": "/wows-cheats/",
  "/halo": "/halo-cheats/",
  "/halo/": "/halo-cheats/",
  "/tptr": "/tptr-cheats/",
  "/tptr/": "/tptr-cheats/",
  "/isle": "/isle-cheats/",
  "/isle/": "/isle-cheats/",
  "/hd2": "/hd2-cheats/",
  "/hd2/": "/hd2-cheats/",
  "/moe": "/moe-cheats/",
  "/moe/": "/moe-cheats/",
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();

    // Canonical host + HTTPS (fixes Seobility www/non-www + HTTPS redirect checks)
    let needsCanonical = false;
    if (host === "www.getyourcheats.com") {
      url.hostname = "getyourcheats.com";
      needsCanonical = true;
    }
    if (url.protocol === "http:") {
      url.protocol = "https:";
      needsCanonical = true;
    }
    if (needsCanonical) {
      return Response.redirect(url.toString(), 301);
    }

    const path = url.pathname.replace(/\/+$/, "") || "/";
    const withSlash = path.endsWith("/") ? path : path + "/";
    const legacy =
      LEGACY[path] ||
      LEGACY[withSlash] ||
      LEGACY[path.replace(/\/$/, "")] ||
      null;
    if (legacy) {
      url.pathname = legacy;
      url.protocol = "https:";
      url.hostname = "getyourcheats.com";
      return Response.redirect(url.toString(), 301);
    }

    const response = await env.ASSETS.fetch(request);
    const type = response.headers.get("Content-Type") || "";
    if (!type.includes("text/html")) {
      return response;
    }

    const headers = new Headers(response.headers);
    headers.set("Content-Type", "text/html; charset=utf-8");
    headers.set("X-Content-Type-Options", "nosniff");
    headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload");

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
