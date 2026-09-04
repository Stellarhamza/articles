/**
 * Apex host redirect + charset header for static assets.
 * www.getyourcheats.com → https://getyourcheats.com (301)
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.hostname === "www.getyourcheats.com") {
      url.hostname = "getyourcheats.com";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }

    const response = await env.ASSETS.fetch(request);
    const type = response.headers.get("Content-Type") || "";
    if (!type.includes("text/html")) {
      return response;
    }

    const headers = new Headers(response.headers);
    if (!/charset=/i.test(type)) {
      headers.set("Content-Type", "text/html; charset=utf-8");
    }
    headers.set("X-Content-Type-Options", "nosniff");

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
