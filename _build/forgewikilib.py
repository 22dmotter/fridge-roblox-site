"""Data-driven The Forge wiki pages. Add items in forge_data.json; this module writes the list and item HTML."""
import json, os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "forge_data.json")
CHECKED = "2026-11-14"
CHECKED_HUMAN = "November 14, 2026"
GUIDE_LABELS = {
    "the-forge-beginners-guide": "Beginner guide",
    "the-forge-pickaxe-progression": "Pickaxe progression",
    "the-forge-forging-guide": "Forging guide",
    "the-forge-money-guide": "Money guide",
    "the-forge-races-guide": "Races guide",
    "the-forge-armor-guide": "Armor guide",
    "the-forge-runes-guide": "Runes guide",
    "the-forge-codes": "The Forge codes",
}

def esc(s):
    return html.escape(s, quote=True)

def load_data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)

def _check_seo(title, desc, path):
    if len(title) > 60:
        raise SystemExit(f"SEO title too long ({len(title)}) for {path}: {title}")
    if not (140 <= len(desc) <= 160):
        raise SystemExit(f"SEO desc length {len(desc)} for {path}: {desc}")

def _blank(v):
    return "—" if v in (None, "", []) else v

def _obtained(item):
    got = item.get("obtained_from") or []
    if not got:
        return "—"
    return ", ".join(got)

def _infobox(item, BASE):
    img = BASE + item["image"] if not item["image"].startswith("http") else item["image"]
    rows = [
        ("Rarity", item.get("rarity") or "—"),
        ("Location", item.get("location") or "—"),
        ("Obtained from", _obtained(item)),
        ("Drop chance", item.get("chance") or "—"),
        ("Multiplier", item.get("multiplier") or "—"),
        ("Sell price", item.get("price") or "—"),
        ("Trait", item.get("trait") or "—"),
    ]
    dl = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in rows)
    cap = "Placeholder tile" if item.get("image_kind") == "placeholder" else "Ore image"
    return f"""<aside class="wiki-infobox" aria-label="{esc(item['name'])} facts">
<figure class="wiki-art">
<img src="{esc(item['image'])}" width="600" height="600" alt="{esc(item['name'])} placeholder tile">
<figcaption>{esc(cap)}</figcaption>
</figure>
<div class="wiki-ibox-body">
<p class="wiki-ibox-kicker">The Forge · Ore</p>
<p class="wiki-ibox-name">{esc(item['name'])}</p>
<dl>{dl}</dl>
</div>
</aside>"""

def _related_icons(item, items):
    others = [x for x in items if x["id"] != item["id"]]
    tiles = []
    for x in others:
        tiles.append(
            f'<a class="wiki-icon" href="{esc(x["slug"])}.html">'
            f'<span class="wiki-icon-art"><img src="{esc(x["image"])}" width="600" height="600" alt=""></span>'
            f'<span class="wiki-icon-name">{esc(x["name"])}</span></a>'
        )
    return '<div class="wiki-icons">' + "".join(tiles) + "</div>"

def _guides(item):
    links = []
    for slug in item.get("related_guides") or []:
        label = GUIDE_LABELS.get(slug, slug.replace("the-forge-", "").replace("-", " "))
        links.append(f'<li><a href="{esc(slug)}.html">{esc(label)}</a></li>')
    return "<ul>" + "".join(links) + "</ul>" if links else ""

def _sources(item):
    lis = "".join(
        f'<li><a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["name"])}</a></li>'
        for s in item.get("sources") or []
    )
    return f'<ul>{lis}</ul>'

def _unverified(item):
    notes = item.get("unverified") or []
    if not notes:
        return ""
    lis = "".join(f"<li>{esc(n)}</li>" for n in notes)
    return (
        '<div class="callout" id="unverified"><strong>Sources disagree:</strong>'
        f"<ul>{lis}</ul></div>"
    )

def _stat_table(item):
    rows = [
        ("Rarity", item.get("rarity") or "—"),
        ("Location", item.get("location") or "—"),
        ("Obtained from", _obtained(item)),
        ("Drop chance", item.get("chance") or "—"),
        ("Multiplier", item.get("multiplier") or "—"),
        ("Sell price", item.get("price") or "—"),
        ("Trait", item.get("trait") or "—"),
    ]
    body = "".join(f"<tr><th scope='row'>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in rows)
    return (
        '<div class="table-wrap"><table>'
        f"<caption>Confirmed {esc(item['name'])} stats (checked {CHECKED_HUMAN})</caption>"
        "<thead><tr><th scope='col'>Stat</th><th scope='col'>Value</th></tr></thead>"
        f"<tbody>{body}</tbody></table></div>"
    )

def _faq(item):
    name = item["name"]
    loc = item.get("location") or "—"
    got = _obtained(item)
    chance = item.get("chance") or "—"
    trait = item.get("trait") or "—"
    price = item.get("price") or "—"
    return [
        (f"Where do you find {name} in The Forge?",
         f"{name} is listed in {loc}, from {got}, with a {chance} drop chance."),
        (f"Does {name} have a trait in The Forge?",
         f"{'No. Sources list no trait for ' + name + '.' if trait == 'None' else name + ' trait: ' + trait}"),
        (f"How much does {name} sell for in The Forge?",
         f"Sources list the sell price as {price}."),
    ]

def item_body(item, items, BASE):
    faq = _faq(item)
    faq_html = "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq
    )
    img_note = (
        f'<p class="small wiki-credit"><strong>Image:</strong> {esc(item.get("image_credit") or "Original placeholder tile.")}</p>'
    )
    return f"""<div class="wrap wiki-page">{{CRUMBS}}
<article>
<div class="wiki-item">
<header class="wiki-head">
<p class="wiki-kicker"><a href="the-forge-ores.html">The Forge ores</a></p>
<h1>{esc(item["h1"])}</h1>
<p class="updated">Last checked: <time datetime="{CHECKED}">{CHECKED_HUMAN}</time></p>
</header>
<div class="wiki-main">
<p class="lead">{item["lead"]}</p>
<h2 id="get">How to Get {esc(item["name"])}</h2>
<p>{item["how_to_get"]}</p>
<h2 id="uses">What {esc(item["name"])} Is Good For</h2>
<p>{item["uses"]}</p>
<h2 id="stats">{esc(item["name"])} Stats</h2>
<p>These numbers were checked against at least two independent sources on {CHECKED_HUMAN}. A dash (—) means we did not find two sources that agree, and we did not guess.</p>
{_stat_table(item)}
{_unverified(item)}
<h2 id="related">Related Ores</h2>
<p>These are the other starter ores in this pilot. The full set lives on the <a href="the-forge-ores.html">ores list</a>.</p>
{_related_icons(item, items)}
<h2 id="guides">Related The Forge Guides</h2>
<p>Written walkthroughs on this site that pair with this wiki page:</p>
{_guides(item)}
<h2 id="videos">Watch Fridge</h2>
<p>Fridge does not have a dedicated {esc(item["name"])} video. His <a href="the-forge-beginners-guide.html">beginner guide</a> covers the early mine, forge and sell loop these ores belong to, with the full tutorial embedded there.</p>
<h2 id="src-h">Sources</h2>
{_sources(item)}
{img_note}
<section class="faq" id="faq" aria-labelledby="faq-h">
<h2 id="faq-h">FAQ</h2>
{faq_html}
</section>
</div>
{_infobox(item, BASE)}
</div>
</article>
</div>"""

def list_body(data, items):
    tiles = []
    rows = []
    for x in items:
        tiles.append(
            f'<a class="wiki-icon" href="{esc(x["slug"])}.html">'
            f'<span class="wiki-icon-art"><img src="{esc(x["image"])}" width="600" height="600" alt="{esc(x["name"])} placeholder tile"></span>'
            f'<span class="wiki-icon-name">{esc(x["name"])}</span>'
            f'<span class="wiki-icon-sub">{esc(x.get("rarity") or "")} · {esc(x.get("chance") or "")}</span></a>'
        )
        rows.append(
            "<tr>"
            f'<th scope="row"><a href="{esc(x["slug"])}.html">{esc(x["name"])}</a></th>'
            f'<td data-sort="{esc(x.get("rarity") or "")}">{esc(x.get("rarity") or "—")}</td>'
            f'<td data-sort="{esc(x.get("location") or "")}">{esc(x.get("location") or "—")}</td>'
            f'<td data-sort="{esc(_obtained(x))}">{esc(_obtained(x))}</td>'
            f'<td data-sort="{esc(x.get("chance") or "")}">{esc(x.get("chance") or "—")}</td>'
            f'<td data-sort="{esc(x.get("multiplier") or "")}">{esc(x.get("multiplier") or "—")}</td>'
            f'<td data-sort="{esc(x.get("price") or "")}">{esc(x.get("price") or "—")}</td>'
            f'<td data-sort="{esc(x.get("trait") or "")}">{esc(x.get("trait") or "—")}</td>'
            "</tr>"
        )
    return f"""<div class="wrap wiki-page">{{CRUMBS}}
<article>
<header>
<p class="wiki-kicker"><a href="roblox-the-forge.html">The Forge</a></p>
<h1>The Forge Ores: Stats and Locations</h1>
<p class="updated">Last checked: <time datetime="{CHECKED}">{CHECKED_HUMAN}</time></p>
</header>
<p class="lead">This is a <strong>pilot</strong> of five starter ores from Stonewake's Cross. Every stat on these pages was checked against at least two sources on {CHECKED_HUMAN}. More ores will be added after this layout is reviewed. A dash (—) means we did not find two sources that agree.</p>
<div class="callout"><strong>More coming:</strong> This list is not a complete ore encyclopedia yet. It starts with Stone, Sand Stone, Copper, Iron and Gold so we can lock the page design first.</div>
<h2 id="grid">Ore Icons</h2>
<div class="wiki-icons wiki-icons-lg">{''.join(tiles)}</div>
<h2 id="table">Ore Stats Table</h2>
<p>Click a column header to sort. Open an ore name for the full wiki page.</p>
<div class="table-wrap"><table class="wiki-sort">
<caption>Starter The Forge ores (checked {CHECKED_HUMAN})</caption>
<thead><tr>
<th scope="col"><button type="button">Ore</button></th>
<th scope="col"><button type="button">Rarity</button></th>
<th scope="col"><button type="button">Location</button></th>
<th scope="col"><button type="button">Obtained from</button></th>
<th scope="col"><button type="button">Drop chance</button></th>
<th scope="col"><button type="button">Multiplier</button></th>
<th scope="col"><button type="button">Sell price</button></th>
<th scope="col"><button type="button">Trait</button></th>
</tr></thead>
<tbody>{''.join(rows)}</tbody>
</table></div>
<h2 id="guides">Related The Forge Guides</h2>
<p>These walkthroughs cover mining, forging and spending early ores:</p>
<ul>
<li><a href="the-forge-beginners-guide.html">Beginner guide</a></li>
<li><a href="the-forge-pickaxe-progression.html">Pickaxe progression</a></li>
<li><a href="the-forge-forging-guide.html">Forging guide</a></li>
<li><a href="the-forge-money-guide.html">Money guide</a></li>
<li><a href="the-forge-codes.html">The Forge codes</a></li>
</ul>
<h2 id="videos">Watch Fridge</h2>
<p>Fridge's <a href="the-forge-beginners-guide.html">beginner guide</a> embeds his full The Forge tutorial, which covers the early mine, forge and sell loop these ores are part of.</p>
<h2 id="src-h">Sources</h2>
<p>Item pages cite the sources used for each ore. The list was checked against:</p>
<ul>
<li><a href="https://forgewiki.org/wiki/Ores" rel="noopener" target="_blank">Forge Wiki: Ores list</a> and the individual Stone, Sand Stone, Copper, Iron and Gold pages</li>
<li><a href="https://game8.co/games/The-Forge/archives/572862" rel="noopener" target="_blank">Game8: List of All Ores and Traits</a> and the <a href="https://game8.co/games/The-Forge/archives/573590" rel="noopener" target="_blank">Game8 Gold page</a> (updated February 22, 2026)</li>
<li><a href="https://www.destructoid.com/all-ores-in-the-forge/" rel="noopener" target="_blank">Destructoid: All Ores in The Forge</a> (updated January 8, 2026)</li>
<li><a href="https://bloxinformer.com/wikis/the-forge/ores/" rel="noopener" target="_blank">BloxInformer: The Forge ores</a></li>
</ul>
<p class="small">Pro Game Guides published an ores guide dated January 13, 2026 whose visible snippets matched Stone, Sand Stone, Copper and Iron, but the live page returned HTTP 403 when we tried to re-fetch it on {CHECKED_HUMAN}, so it is not used as a confirming source here.</p>
</article>
</div>"""

def _item_ld(item, BASE, ORG, PERSON):
    url = BASE + item["slug"] + ".html"
    img = BASE + item["image"]
    faq = _faq(item)
    return [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": item["h1"],
            "description": item["desc"],
            "image": [img],
            "datePublished": CHECKED,
            "dateModified": CHECKED,
            "author": PERSON,
            "publisher": ORG,
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "articleSection": "The Forge Wiki",
            "keywords": f"{item['name'].lower()} ore, the forge {item['name'].lower()}, the forge ores",
            "about": {"@type": "VideoGame", "name": "The Forge", "gamePlatform": "Roblox"},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq
            ],
        },
    ]

def write_pages(page, write, BASE, ORG, PERSON):
    data = load_data()
    items = data["items"]
    if len(items) < 1:
        raise SystemExit("forge_data.json has no items")
    paths = []

    list_title = "The Forge Ores: Stats, Locations and Traits"
    list_desc = "Confirmed stats for five starter The Forge ores in Stonewake's Cross: drop chances, multipliers, sell prices and traits. More ores coming. Open the list!"
    _check_seo(list_title, list_desc, "the-forge-ores.html")
    list_path = "the-forge-ores.html"
    list_crumbs = [
        ("Home", "index.html"),
        ("Games", "games.html"),
        ("The Forge", "roblox-the-forge.html"),
        ("Ores", list_path),
    ]
    list_ld = [{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "The Forge Ores: Stats and Locations",
        "description": list_desc,
        "url": BASE + list_path,
        "datePublished": CHECKED,
        "dateModified": CHECKED,
        "publisher": ORG,
        "about": {"@type": "VideoGame", "name": "The Forge", "gamePlatform": "Roblox"},
    }]
    write(list_path, page(
        list_path,
        list_title,
        list_desc,
        list_crumbs,
        list_body(data, items),
        active="roblox-the-forge.html",
        og_type="website",
        image=BASE + "assets/forge/ores-og.webp",
        image_alt="The Forge ores wiki: starter ore placeholder tiles",
        ld=list_ld,
    ))
    paths.append(list_path)

    for item in items:
        path = item["slug"] + ".html"
        _check_seo(item["title"], item["desc"], path)
        crumbs = [
            ("Home", "index.html"),
            ("Games", "games.html"),
            ("The Forge", "roblox-the-forge.html"),
            ("Ores", list_path),
            (item["name"], path),
        ]
        write(path, page(
            path,
            item["title"],
            item["desc"],
            crumbs,
            item_body(item, items, BASE),
            active="roblox-the-forge.html",
            og_type="article",
            image=BASE + item["image"],
            image_alt=f"{item['name']} placeholder tile from the The Forge ores wiki",
            ld=_item_ld(item, BASE, ORG, PERSON),
        ))
        paths.append(path)
        print("wiki", path, "T", len(item["title"]), "D", len(item["desc"]))
    print("wiki", list_path, "T", len(list_title), "D", len(list_desc))
    return paths, CHECKED
