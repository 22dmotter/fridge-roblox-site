"""Data-driven The Forge wiki pages. Add items in forge_data.json; this module writes the list and item HTML."""
import json, os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "forge_data.json")
CHECKED = "2026-11-15"
CHECKED_HUMAN = "November 15, 2026"
GUIDE_LABELS = {
    "the-forge-beginners-guide": "Beginner guide",
    "the-forge-pickaxe-progression": "Pickaxe progression",
    "the-forge-forging-guide": "Forging guide",
    "the-forge-money-guide": "Money guide",
    "the-forge-races-guide": "Races guide",
    "the-forge-armor-guide": "Armor guide",
    "the-forge-runes-guide": "Runes guide",
    "the-forge-codes": "The Forge codes",
    "the-forge-island-3-guide": "Island 3 / Frostspire Expanse guide",
    "the-forge-goblin-cave": "Goblin Cave guide",
    "the-forge-raven-cave": "Raven Cave guide",
}

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

def _blank(v):
    return "—" if v in (None, "", []) else v

def _obtained(item):
    got = item.get("obtained_from") or []
    if not got:
        return "—"
    return ", ".join(got)



def _rarity_class(rarity):
    raw = (rarity or "").strip().lower().replace(" ", "-")
    if raw in ("", "—", "-", "none"):
        return ""
    raw = {"mythical": "mythic"}.get(raw, raw)
    return "rarity-" + raw

def _rarity_html(rarity):
    label = rarity or "—"
    cls = _rarity_class(rarity)
    if not cls:
        return esc(label)
    return f'<span class="rarity {cls}">{esc(label)}</span>'

def _icon_credit_html(item, *, linked_name=True):
    page = item.get("image_file_page")
    if page:
        name = '<a href="%s" rel="noopener" target="_blank">The Forge Wiki (forgewiki.org)</a>' % esc(page)
    else:
        name = "The Forge Wiki (forgewiki.org)"
    return f"Item icon: {name}, game artwork © the game's developer"

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
    cells = []
    for k, v in rows:
        val = _rarity_html(v) if k == "Rarity" else esc(v)
        cells.append(f"<div><dt>{esc(k)}</dt><dd>{val}</dd></div>")
    dl = "".join(cells)
    credit = _icon_credit_html(item)
    rcls = _rarity_class(item.get("rarity"))
    art_cls = ("wiki-art " + rcls).strip()
    return f"""<aside class="wiki-infobox" aria-label="{esc(item['name'])} facts">
<figure class="{art_cls}">
<img src="{esc(item['image'])}" width="600" height="600" alt="{esc(item['name'])} item icon">
<figcaption>{credit}</figcaption>
</figure>
<div class="wiki-ibox-body">
<p class="wiki-ibox-kicker">The Forge · Ore</p>
<p class="wiki-ibox-name">{esc(item['name'])}</p>
<dl>{dl}</dl>
</div>
</aside>"""


def _related_intro(item):
    loc = item.get("location") or "this world"
    labels = {
        "Stonewake's Cross": "other Stonewake's Cross (World 1) ores",
        "Forgotten Kingdom": "other Forgotten Kingdom (World 2) ores",
        "Frostspire Expanse": "other Frostspire Expanse (World 3) ores",
        "Goblin Cave": "other Goblin Cave ores",
        "The Peak": "other The Peak ores",
        "Raven Cave": "other Raven Cave ores",
        "Bamboo Forest": "other Bamboo Forest ores",
        "Holy Tree": "other Holy Tree ores",
    }
    label = labels.get(loc, f"other {loc} ores")
    return (
        f"These are {label}. The full confirmed set lives on the "
        '<a href="the-forge-ores.html">ores list</a>.'
    )

def _related_icons(item, items):
    loc = item.get("location")
    others = [x for x in items if x["id"] != item["id"] and x.get("location") == loc]
    if not others:
        others = [x for x in items if x["id"] != item["id"]]
    tiles = []
    for x in others:
        rcls = _rarity_class(x.get("rarity"))
        art = ("wiki-icon-art " + rcls).strip()
        tiles.append(
            f'<a class="wiki-icon" href="{esc(x["slug"])}.html">'
            f'<span class="{art}"><img src="{esc(x["image"])}" width="600" height="600" alt=""></span>'
            f'<span class="wiki-icon-name">{esc(x["name"])}</span>'
            f'<span class="wiki-icon-sub">{_rarity_html(x.get("rarity"))}</span></a>'
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
    body_rows = []
    for k, v in rows:
        val = _rarity_html(v) if k == "Rarity" else esc(v)
        body_rows.append(f"<tr><th scope='row'>{esc(k)}</th><td>{val}</td></tr>")
    body = "".join(body_rows)
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
    img_note = f'<p class="small wiki-credit">{_icon_credit_html(item)}</p>' 
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
<p>{_related_intro(item)}</p>
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


def _world_short_label(heading, hid):
    if ": " in heading:
        return heading.split(": ", 1)[0]
    if hid.startswith("world-") and hid.split("-", 1)[-1].isdigit():
        return "World " + hid.split("-", 1)[-1]
    return heading

def _world_jump_nav(items):
    links = []
    for hid, heading, group in _worlds(items):
        if not group:
            continue
        short = _world_short_label(heading, hid)
        label = f"{heading} ({len(group)} ores)"
        links.append(
            f'<a class="wiki-world-jump" href="#{esc(hid)}" title="{esc(label)}" aria-label="{esc(label)}">{esc(short)}</a>'
        )
    if not links:
        return ""
    return f'<nav class="wiki-world-nav" aria-label="Jump to a world">{"".join(links)}</nav>'

def _worlds(items):
    # Official wiki filter order. Empty groups are omitted so jump buttons
    # appear only for areas that have confirmed ores on this site.
    groups = [
        ("world-1", "World 1: Stonewake's Cross", "Stonewake's Cross"),
        ("world-2", "World 2: Forgotten Kingdom", "Forgotten Kingdom"),
        ("goblin-cave", "Goblin Cave", "Goblin Cave"),
        ("world-3", "World 3: Frostspire Expanse", "Frostspire Expanse"),
        ("the-peak", "The Peak", "The Peak"),
        ("raven-cave", "Raven Cave", "Raven Cave"),
        ("bamboo-forest", "Bamboo Forest", "Bamboo Forest"),
        ("holy-tree", "Holy Tree", "Holy Tree"),
        ("jade-spirit-cave", "Jade Spirit Cave", "Jade Spirit Cave"),
        ("aurelia-hall", "Aurelia Hall", "Aurelia Hall"),
        ("void-cave", "Void Cave", "Void Cave"),
        ("tower-of-hell", "Tower of Hell", "Tower of Hell"),
        ("special", "Special", "Special"),
    ]
    used = set()
    out = []
    for hid, heading, loc in groups:
        chunk = [x for x in items if x.get("location") == loc]
        used.update(id(x) for x in chunk)
        if chunk:
            out.append((hid, heading, chunk))
    leftover = [x for x in items if id(x) not in used]
    if leftover:
        out.append(("world-other", "Other ores", leftover))
    return out

def _ore_icon_tiles(items):
    tiles = []
    for x in items:
        rcls = _rarity_class(x.get("rarity"))
        art = ("wiki-icon-art " + rcls).strip()
        tiles.append(
            f'<a class="wiki-icon" href="{esc(x["slug"])}.html">'
            f'<span class="{art}"><img src="{esc(x["image"])}" width="600" height="600" alt="{esc(x["name"])} item icon"></span>'
            f'<span class="wiki-icon-name">{esc(x["name"])}</span>'
            f'<span class="wiki-icon-sub">{_rarity_html(x.get("rarity"))} · {esc(x.get("chance") or "")}</span></a>'
        )
    return tiles

def _ore_table(items, caption):
    rows = []
    for x in items:
        rows.append(
            "<tr>"
            f'<th scope="row"><a href="{esc(x["slug"])}.html">{esc(x["name"])}</a></th>'
            f'<td data-sort="{esc(x.get("rarity") or "")}">{_rarity_html(x.get("rarity"))}</td>'
            f'<td data-sort="{esc(x.get("location") or "")}">{esc(x.get("location") or "—")}</td>'
            f'<td data-sort="{esc(_obtained(x))}">{esc(_obtained(x))}</td>'
            f'<td data-sort="{esc(x.get("chance") or "")}">{esc(x.get("chance") or "—")}</td>'
            f'<td data-sort="{esc(x.get("multiplier") or "")}">{esc(x.get("multiplier") or "—")}</td>'
            f'<td data-sort="{esc(x.get("price") or "")}">{esc(x.get("price") or "—")}</td>'
            f'<td data-sort="{esc(x.get("trait") or "")}">{esc(x.get("trait") or "—")}</td>'
            "</tr>"
        )
    return (
        '<div class="table-wrap"><table class="wiki-sort">'
        f"<caption>{caption}</caption>"
        "<thead><tr>"
        '<th scope="col"><button type="button">Ore</button></th>'
        '<th scope="col"><button type="button">Rarity</button></th>'
        '<th scope="col"><button type="button">Location</button></th>'
        '<th scope="col"><button type="button">Obtained from</button></th>'
        '<th scope="col"><button type="button">Drop chance</button></th>'
        '<th scope="col"><button type="button">Multiplier</button></th>'
        '<th scope="col"><button type="button">Sell price</button></th>'
        '<th scope="col"><button type="button">Trait</button></th>'
        "</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )

def list_body(data, items):
    sections = []
    for hid, heading, group in _worlds(items):
        if not group:
            continue
        tiles = _ore_icon_tiles(group)
        caption = f"{heading} ores (checked {CHECKED_HUMAN})"
        sections.append(
            f'<h2 id="{hid}">{heading}</h2>'
            f'<div class="wiki-icons wiki-icons-lg">{"".join(tiles)}</div>'
            f"{_ore_table(group, caption)}"
        )
    jump_nav = _world_jump_nav(items)
    list_credit = "Item icons: " + ", ".join(
        f'<a href="{esc(x["image_file_page"])}" rel="noopener" target="_blank">{esc(x["name"])}</a>'
        for x in items if x.get("image_file_page")
    ) + " on The Forge Wiki (forgewiki.org), game artwork © the game's developer"
    return f"""<div class="wrap wiki-page">{{CRUMBS}}
<article>
<header>
<p class="wiki-kicker"><a href="roblox-the-forge.html">The Forge</a></p>
<h1>The Forge Ores: Stats and Locations</h1>
<p class="updated">Last checked: <time datetime="{CHECKED}">{CHECKED_HUMAN}</time></p>
</header>
<p class="lead">This list covers every ore we could confirm with two or more sources across World 1 (Stonewake's Cross), World 2 (Forgotten Kingdom), Goblin Cave, World 3 (Frostspire Expanse), The Peak, Raven Cave, Bamboo Forest, and the Holy Tree, in official Forge Wiki list order. Every stat on these pages was checked against at least two sources on {CHECKED_HUMAN}. A dash (—) means we did not find two sources that agree.</p>
{jump_nav}
<div class="callout"><strong>114 confirmed ores:</strong> This list has the full Stonewake's Cross set (14), the Forgotten Kingdom set from Cobalt through Darkryte (25), Goblin Cave (7), the Frostspire Expanse set from Grass through Prismatic Heart (16), The Peak (17), Raven Cave (8), Bamboo Forest (12), and the Holy Tree (15). Royal Boneite and Shikanite appear on the official wiki list but could not be confirmed with a second independent source, so they are not on this site yet. The same is true of later official areas (Jade Spirit Cave, Aurelia Hall, Void Cave, Tower of Hell) and the Special event ores Pumpkinite, Candy Ore, and Bismuth. For most Peak and Raven Cave ores, and for many World 3 ores, sources disagree on drop chance and sometimes multiplier, so those fields are dashes.</div>
{''.join(sections)}
<p class="small wiki-credit" id="icon-credit">{list_credit}</p>
<h2 id="guides">Related The Forge Guides</h2>
<p>These walkthroughs cover mining, forging and spending ores:</p>
<ul>
<li><a href="the-forge-beginners-guide.html">Beginner guide</a></li>
<li><a href="the-forge-island-3-guide.html">Island 3 / Frostspire Expanse guide</a></li>
<li><a href="the-forge-goblin-cave.html">Goblin Cave guide</a></li>
<li><a href="the-forge-raven-cave.html">Raven Cave guide</a></li>
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
<li><a href="https://forgewiki.org/wiki/Ores" rel="noopener" target="_blank">Forge Wiki: Ores list</a> and the individual pages for the confirmed ores in this list</li>
<li><a href="https://game8.co/games/The-Forge/archives/572862" rel="noopener" target="_blank">Game8: List of All Ores and Traits</a> (updated February 24, 2026)</li>
<li><a href="https://www.destructoid.com/all-ores-in-the-forge/" rel="noopener" target="_blank">Destructoid: All Ores in The Forge</a> (updated January 8, 2026)</li>
<li><a href="https://bloxinformer.com/wikis/the-forge/ores/" rel="noopener" target="_blank">BloxInformer: The Forge ores</a> (updated September 7, 2026)</li>
<li><a href="https://www.pockettactics.com/the-forge-ore" rel="noopener" target="_blank">Pocket Tactics: All The Forge ores</a> (updated March 3, 2026)</li>
</ul>
<p class="small">Destructoid's tables (updated January 8, 2026) go through Raven Cave and are not used as a confirming source for Bamboo Forest or Holy Tree ores, or for World 1–2 ores they omit (Fichillium, Boneite, Dark Boneite, Slimite, Volcanic Rock Ore, and Grass). Game8 (February 24, 2026), BloxInformer (September 7, 2026), and Pocket Tactics (March 3, 2026) cover Goblin Cave through the Holy Tree, but not later official areas. For most World 3, Peak, and Raven Cave ores, the official wiki and BloxInformer list lower drop-chance denominators (and often lower multipliers) than Game8, Destructoid, and Pocket Tactics; those fields are dashes where two source camps disagree. Holy Tree sell prices are dashes because BloxInformer and Pocket Tactics list them as TBA. Pro Game Guides published an ores guide dated January 13, 2026, but the live page returned HTTP 403 when we tried to re-fetch it on {CHECKED_HUMAN}, so it is not used as a confirming source here.</p>
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
    list_desc = "Confirmed stats for 114 ores in The Forge across Worlds 1-3, Goblin Cave, The Peak, Raven Cave, Bamboo Forest, and the Holy Tree. Open the list!"
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
        image=BASE + _ver("assets/forge/ores-og.webp"),
        image_alt="The Forge ores wiki: ore icons from World 1 through the Holy Tree",
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
            image_alt=f"{item['name']} item icon from The Forge Wiki",
            ld=_item_ld(item, BASE, ORG, PERSON),
        ))
        paths.append(path)
        print("wiki", path, "T", len(item["title"]), "D", len(item["desc"]))
    print("wiki", list_path, "T", len(list_title), "D", len(list_desc))
    return paths, CHECKED
