#!/usr/bin/env python3
"""Parse JSON-LD on every built HTML page and fail on BreadcrumbList / VideoObject issues."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse

TZ_DT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(Z|[+-]\d{2}:\d{2})$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
CANON_RE = re.compile(r'rel="canonical" href="([^"]+)"')
ROBOTS_RE = re.compile(r'name="robots" content="([^"]+)"')
LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")


def walk(obj, path="$"):
    if isinstance(obj, list):
        for i, item in enumerate(obj):
            yield from walk(item, f"{path}[{i}]")
    elif isinstance(obj, dict):
        yield path, obj
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}")


def types_of(obj):
    t = obj.get("@type")
    if t is None:
        return []
    return t if isinstance(t, list) else [t]


def item_url(item):
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return item.get("@id") or item.get("url") or item.get("item") or ""
    return ""


def validate_site(out_dir, base="https://robloxguides.org/"):
    out = Path(out_dir)
    errors = []
    stats = defaultdict(int)

    pages = sorted(out.glob("*.html"))
    stats["html_pages"] = len(pages)
    sitemap_pages_ok = 0

    for page in pages:
        html = page.read_text(encoding="utf-8")
        blocks = LD_RE.findall(html)
        stats["jsonld_blocks"] += len(blocks)
        if not blocks and page.name not in ("tag-the-forge.html",):
            # 404 has JSON-LD; tag-the-forge is a noindex redirect stub.
            if page.name != "tag-the-forge.html":
                pass
        for bi, raw in enumerate(blocks, 1):
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{page.name}: JSON-LD block {bi} is not valid JSON ({exc})")
                continue
            for path, obj in walk(data):
                kinds = types_of(obj)
                if "BreadcrumbList" in kinds:
                    stats["breadcrumb_lists"] += 1
                    els = obj.get("itemListElement") or []
                    if not els:
                        errors.append(f"{page.name}: BreadcrumbList has no itemListElement")
                        continue
                    for i, el in enumerate(els, 1):
                        stats["breadcrumb_items"] += 1
                        if not isinstance(el, dict):
                            errors.append(f"{page.name}: ListItem {i} is not an object")
                            continue
                        missing = [k for k in ("position", "name", "item") if k not in el or el[k] in (None, "")]
                        if missing:
                            errors.append(f"{page.name}: ListItem {i} missing {', '.join(missing)}: {el}")
                            continue
                        url = item_url(el["item"])
                        if not (isinstance(url, str) and url.startswith("https://")):
                            errors.append(f"{page.name}: ListItem {i} item is not an absolute https URL: {el.get('item')!r}")
                if "VideoObject" in kinds:
                    stats["video_objects"] += 1
                    missing = [k for k in ("name", "description", "thumbnailUrl", "uploadDate") if not obj.get(k)]
                    if not obj.get("embedUrl") and not obj.get("contentUrl"):
                        missing.append("embedUrl/contentUrl")
                    if missing:
                        errors.append(f"{page.name}: VideoObject {obj.get('name')!r} missing {', '.join(missing)}")
                    ud = obj.get("uploadDate")
                    if ud and not TZ_DT.match(str(ud)):
                        errors.append(f"{page.name}: VideoObject {obj.get('name')!r} uploadDate is not ISO 8601 with timezone: {ud!r}")
                for field in ("datePublished", "dateModified"):
                    val = obj.get(field)
                    if not val:
                        continue
                    val = str(val)
                    if "T" in val and not TZ_DT.match(val) and not val.endswith("Z"):
                        errors.append(f"{page.name}: {kinds} {field} datetime is missing a timezone: {val!r}")
                    elif "T" not in val and not DATE.match(val):
                        errors.append(f"{page.name}: {kinds} {field} is not a valid date or datetime: {val!r}")

    # --- local indexing audit ---
    sm_path = out / "sitemap.xml"
    if not sm_path.exists():
        errors.append("sitemap.xml is missing")
        locs = []
    else:
        locs = LOC_RE.findall(sm_path.read_text(encoding="utf-8"))
    stats["sitemap_urls"] = len(locs)
    if len(locs) != len(set(locs)):
        dup = [u for u, c in {u: locs.count(u) for u in locs}.items() if c > 1]
        errors.append(f"sitemap.xml has duplicate loc values: {dup}")

    robots = (out / "robots.txt").read_text(encoding="utf-8") if (out / "robots.txt").exists() else ""
    if "Disallow: /" in robots and "Allow: /" not in robots.split("Disallow: /")[0][-80:]:
        # A blanket Disallow: / would block indexing. Allow: / is present on this site.
        if re.search(r"(?im)^disallow:\s*/\s*$", robots) and not re.search(r"(?im)^allow:\s*/\s*$", robots):
            errors.append("robots.txt appears to block the whole site")
    if "Sitemap:" not in robots:
        errors.append("robots.txt is missing a Sitemap: line")

    expected_noindex = {"404.html", "tag-the-forge.html"}
    for loc in locs:
        parsed = urlparse(loc)
        if parsed.scheme != "https":
            errors.append(f"sitemap loc is not https: {loc}")
            continue
        if parsed.netloc and parsed.netloc != urlparse(base).netloc:
            errors.append(f"sitemap loc host {parsed.netloc} does not match site base {base}: {loc}")
        path = parsed.path or "/"
        if path in ("/", "/index.html"):
            rel = "index.html"
        else:
            rel = path.lstrip("/")
        fp = out / rel
        if not fp.is_file():
            errors.append(f"sitemap loc has no built file: {loc} (expected {rel})")
            continue
        html = fp.read_text(encoding="utf-8")
        can = CANON_RE.search(html)
        robots_meta = ROBOTS_RE.search(html)
        if not can:
            errors.append(f"{rel}: in sitemap but has no canonical")
            continue
        canonical = can.group(1)
        if canonical != loc:
            errors.append(f"{rel}: sitemap loc {loc} does not match canonical {canonical}")
        if robots_meta and re.search(r"\bnoindex\b", robots_meta.group(1), re.I):
            errors.append(f"{rel}: in sitemap but has noindex ({robots_meta.group(1)})")
        sitemap_pages_ok += 1

    # HTML pages not in the sitemap should be the known noindex stubs only.
    sm_files = set()
    for loc in locs:
        path = urlparse(loc).path or "/"
        sm_files.add("index.html" if path in ("/", "/index.html") else path.lstrip("/"))
    extra = sorted(p.name for p in pages if p.name not in sm_files)
    unexpected = [n for n in extra if n not in expected_noindex]
    if unexpected:
        errors.append(f"HTML pages missing from sitemap (and not known noindex stubs): {unexpected}")
    stats["sitemap_pages_ok"] = sitemap_pages_ok
    stats["html_not_in_sitemap"] = extra

    print("JSON-LD / indexing audit")
    for k in ("html_pages", "jsonld_blocks", "breadcrumb_lists", "breadcrumb_items", "video_objects", "sitemap_urls", "sitemap_pages_ok"):
        print(f"  {k}: {stats[k]}")
    print(f"  html_not_in_sitemap: {stats['html_not_in_sitemap']}")
    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for e in errors:
            print("  -", e)
        raise SystemExit(1)
    print("OK")
    return stats


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    base = sys.argv[2] if len(sys.argv) > 2 else "https://robloxguides.org/"
    validate_site(root, base)
