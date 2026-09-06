/**
 * Build a clean assets folder for Cloudflare Workers.
 * Never copies .git (pack files exceed the 25 MiB asset limit).
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DIST = path.join(ROOT, "dist");

const SKIP = new Set([
  ".git",
  ".wrangler",
  ".cursor",
  "node_modules",
  "dist",
  "agent-transcripts",
  "_cheatseller_source",
  "_source_backup",
  "_store_backup",
  ".npm",
  ".cache",
]);

const SKIP_FILES = new Set([
  "worker.js",
  "wrangler.jsonc",
  "wrangler.toml",
  "package.json",
  "package-lock.json",
  ".gitignore",
  ".assetsignore",
  ".env",
  ".dev.vars",
]);

function shouldSkipName(name) {
  if (SKIP.has(name)) return true;
  if (name.startsWith("_") && (name.endsWith(".py") || name.endsWith(".json") || name.endsWith(".html") || name.endsWith(".xml") || name.endsWith(".mjs"))) {
    return true;
  }
  if (name.endsWith(".pyc") || name === "Thumbs.db" || name === ".DS_Store") return true;
  return false;
}

function copyRecursive(src, dest) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const name of fs.readdirSync(src)) {
      if (shouldSkipName(name)) continue;
      if (SKIP_FILES.has(name) && path.dirname(src) === ROOT) continue;
      copyRecursive(path.join(src, name), path.join(dest, name));
    }
    return;
  }
  fs.copyFileSync(src, dest);
}

function main() {
  fs.rmSync(DIST, { recursive: true, force: true });
  fs.mkdirSync(DIST, { recursive: true });

  for (const name of fs.readdirSync(ROOT)) {
    if (shouldSkipName(name)) continue;
    if (SKIP_FILES.has(name)) continue;
    // skip scripts tooling folder contents? keep scripts out of dist
    if (name === "scripts") continue;
    copyRecursive(path.join(ROOT, name), path.join(DIST, name));
  }

  // Safety: never allow .git inside dist
  fs.rmSync(path.join(DIST, ".git"), { recursive: true, force: true });

  fs.writeFileSync(
    path.join(DIST, ".assetsignore"),
    [".git", ".git/", ".git/**", "**/.git/**", "**/*.pack", "node_modules/", ".wrangler/"].join("\n") + "\n",
    "utf8"
  );

  const packHits = [];
  function walk(dir) {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, ent.name);
      if (ent.isDirectory()) walk(p);
      else if (ent.name.endsWith(".pack") || p.includes(`${path.sep}.git${path.sep}`)) {
        packHits.push(p);
      }
    }
  }
  walk(DIST);
  if (packHits.length) {
    console.error("Refusing to ship git objects:", packHits);
    process.exit(1);
  }

  console.log("Prepared dist/ for Cloudflare Workers assets (no .git).");
}

main();
