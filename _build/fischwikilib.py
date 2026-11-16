"""Data-driven Fisch wiki pages.

Add items in fisch_data.json (same general shape as forge_data.json items:
id, name, slug, title, h1, desc, category, lead, how_to_get, uses, image,
image_credit, sources, unverified, plus any stat fields). This module writes
list and item HTML when a category has at least one item. Empty categories stay
coming-soon cards on the hub. Do not invent items here.
"""
import json, os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "fisch_data.json")
CHECKED = "2026-11-16"
CHECKED_HUMAN = "November 16, 2026"


def esc(s):
    return html.escape(s, quote=True)


def _ver(rel):
    import hashlib
    fp = os.path.join(HERE, "..", rel)
    try:
        return rel + "?v=" + hashlib.md5(open(fp, "rb").read()).hexdigest()[:8]
    except OSError:
        return rel


def _bust(o):
    if isinstance(o, dict):
        return {k: (_ver(v) if k == "image" and isinstance(v, str) and v.startswith("assets/") else _bust(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [_bust(x) for x in o]
    return o


def load_data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return _bust(json.load(f))


def _check_seo(title, desc, path):
    if len(title) > 60:
        raise SystemExit(f"SEO title too long ({len(title)}) for {path}: {title}")
    if not (140 <= len(desc) <= 160):
        raise SystemExit(f"SEO desc length {len(desc)} for {path}: {desc}")


def categories(data=None):
    data = data or load_data()
    return list(data.get("categories") or [])


def items_for(data, category_id):
    return [it for it in (data.get("items") or []) if it.get("category") == category_id]


def wiki_cats_html(data=None):
    """Hub category cards. Linked list pages appear only after a category has items."""
    data = data or load_data()
    cards = []
    for cat in categories(data):
        n = len(items_for(data, cat["id"]))
        name = esc(cat["name"])
        if n:
            path = cat["slug"] + ".html"
            label = f"{n} page" if n == 1 else f"{n} pages"
            cards.append(f'<a class="wiki-cat" role="listitem" href="{esc(path)}">{name}<small>{esc(label)}</small></a>')
        else:
            cards.append(f'<div class="wiki-cat is-soon" role="listitem">{name}<small>Coming soon</small></div>')
    return '<div class="wiki-cats" role="list">\n' + "\n".join(cards) + "\n</div>"


def _item_ld(item, BASE, ORG, PERSON):
    path = item["slug"] + ".html"
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": item.get("h1") or item["name"],
        "description": item.get("desc") or "",
        "url": BASE + path,
        "datePublished": item.get("checked") or CHECKED,
        "dateModified": CHECKED,
        "publisher": ORG,
        "about": {"@type": "VideoGame", "name": "Fisch", "gamePlatform": "Roblox"},
    }


def write_pages(page, write, BASE, ORG, PERSON):
    """Write Fisch wiki list/item pages. Returns (paths, checked_date). No pages when items is empty."""
    data = load_data()
    items = data.get("items") or []
    paths = []
    if not items:
        print("wiki fisch scaffold: 0 items, hub categories only")
        return paths, data.get("checked") or CHECKED

    hub = data.get("hub_path") or "roblox-fisch.html"
    for cat in categories(data):
        chunk = items_for(data, cat["id"])
        if not chunk:
            continue
        list_path = cat["slug"] + ".html"
        list_title = cat.get("title") or f"{cat['name']} in Roblox Fisch"
        list_desc = cat.get("desc") or (
            f"Confirmed {cat['name'].lower()} in Roblox Fisch, checked against two or more sources. "
            "Open the list!"
        )
        # Keep generated fallbacks in range if a category later omits custom SEO.
        if not (140 <= len(list_desc) <= 160) or len(list_title) > 60:
            raise SystemExit(f"SEO needed on Fisch category {cat['id']}: T {len(list_title)} D {len(list_desc)}")
        _check_seo(list_title, list_desc, list_path)
        crumbs = [
            ("Home", "index.html"),
            ("Games", "games.html"),
            ("Fisch", hub),
            (cat["name"], list_path),
        ]
        body = f"""<div class="wrap wiki-page">{{CRUMBS}}
<article>
<p class="wiki-kicker"><a href="{esc(hub)}">Fisch</a></p>
<h1>{esc(list_title)}</h1>
<p class="updated">Last checked: <time datetime="{CHECKED}">{CHECKED_HUMAN}</time></p>
<p class="lead">This list will grow as entries in this category are confirmed with two or more sources.</p>
<div class="wiki-icons wiki-icons-lg">
{''.join(
    f'<a class="wiki-icon" href="{esc(it["slug"])}.html"><span class="wiki-icon-name">{esc(it["name"])}</span></a>'
    for it in chunk
)}
</div>
</article>
</div>"""
        write(list_path, page(
            list_path, list_title, list_desc, crumbs, body,
            active="roblox-fisch.html", og_type="website",
            ld=[{"@context": "https://schema.org", "@type": "CollectionPage",
                 "name": list_title, "url": BASE + list_path, "dateModified": CHECKED, "publisher": ORG,
                 "about": {"@type": "VideoGame", "name": "Fisch", "gamePlatform": "Roblox"}}],
        ))
        paths.append(list_path)
        print("wiki", list_path, "T", len(list_title), "D", len(list_desc), "n", len(chunk))

    for item in items:
        path = item["slug"] + ".html"
        _check_seo(item["title"], item["desc"], path)
        cat_name = item.get("category")
        cat = next((c for c in categories(data) if c["id"] == cat_name), None)
        crumbs = [
            ("Home", "index.html"),
            ("Games", "games.html"),
            ("Fisch", hub),
        ]
        if cat:
            crumbs.append((cat["name"], cat["slug"] + ".html"))
        crumbs.append((item["name"], path))
        body = f"""<div class="wrap wiki-page">{{CRUMBS}}
<article>
<p class="wiki-kicker"><a href="{esc(hub)}">Fisch</a></p>
<h1>{esc(item['h1'])}</h1>
<p class="updated">Last checked: <time datetime="{CHECKED}">{CHECKED_HUMAN}</time></p>
<p class="lead">{item.get('lead') or ''}</p>
{item.get('how_to_get') or ''}
{item.get('uses') or ''}
<p class="small">{esc(item.get('image_credit') or 'Game artwork © the game\'s developer.')}</p>
</article>
</div>"""
        img = item.get("image")
        write(path, page(
            path, item["title"], item["desc"], crumbs, body,
            active="roblox-fisch.html", og_type="article",
            image=(BASE + img) if img else None,
            image_alt=f"{item['name']} icon",
            ld=[_item_ld(item, BASE, ORG, PERSON)],
        ))
        paths.append(path)
        print("wiki", path, "T", len(item["title"]), "D", len(item["desc"]))
    return paths, data.get("checked") or CHECKED
