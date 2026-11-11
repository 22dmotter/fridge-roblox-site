"""Shared builder for The Forge pages (g/f*.py). Video/Short titles and dates come from forge_videos.json
(scraped from Fridge's channel on November 11, 2026). Facts are checked against forgewiki.org the same day."""
import json, os, re, datetime
V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "forge_videos.json")))
W = "https://forgewiki.org/wiki/"
PLACE = "https://www.roblox.com/games/76558904092080/The-Forge"
def wiki(page, label=None): return (f"Forge Wiki: {label or page}", W + page.replace(" ", "_"))
def _h(d): return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")

def split(ids):
    vids = [(i, V[i]["title"], V[i]["date"]) for i in ids if not V[i]["short"]]
    shorts = [(i, V[i]["title"], V[i]["date"]) for i in ids if V[i]["short"]]
    return vids, shorts

def embeds(ids, heading="Watch Fridge's Video"):
    vids, shorts = split(ids)
    dates = sorted(V[i]["date"] for i in ids if V[i]["date"])
    nv, ns = len(vids), len(shorts)
    parts = []
    if nv: parts.append(f"{nv} full video{'s' if nv!=1 else ''}")
    if ns: parts.append(f"{ns} Short{'s' if ns!=1 else ''}")
    when = ""
    if dates:
        when = f" uploaded {('on ' + _h(dates[0])) if dates[0]==dates[-1] else ('between ' + _h(dates[0]) + ' and ' + _h(dates[-1]))}"
    out = [f'<h2 id="videos">{heading}</h2>',
           f'<p>Fridge covered this topic in {" and ".join(parts)}{when}. They are all embedded here, so you can watch and follow the written steps side by side.</p>']
    for k in range(nv): out.append("{VIDEO%d}" % k)
    if ns:
        out.append('<p class="small">The Shorts play in a vertical player. Tap one to watch it here, or open it on YouTube.</p>')
        out.append("{SHORTS}")
    out.append('<div class="callout"><strong>Video date check:</strong> The Forge gets updates often. The newest is version 1.09, Halloween &amp; Guilds, from October 20, 2026. Fridge\'s videos show the game as it was when he filmed them. The written steps on this page match the game as of November 11, 2026, and were checked against the <a href="https://forgewiki.org/wiki/Version_History" rel="noopener" target="_blank">Forge Wiki</a>.</div>')
    return "\n".join(out)

def make(slug, order, kw, title, h1, desc, kw2, related, ids, lead, sections, faq, sources, howto=None, heading="Watch Fridge's Video"):
    vids, shorts = split(ids)
    secs = "\n".join(f'<h2 id="{a}">{h}</h2>\n{b}' for a, h, b in sections)
    more = ('<h2 id="more">More The Forge Guides</h2>\n<p>Every Fridge guide for The Forge is listed on the <a href="tag-the-forge.html">The Forge guides page</a>. '
            'For free race rerolls, start with <a href="the-forge-codes.html">The Forge codes</a>. Other games are covered in our <a href="roblox-codes-november-2026.html">Roblox codes hub</a>.</p>')
    body = f'<p class="lead">{lead}</p>\n{embeds(ids, heading)}\n{secs}\n{more}\n'
    src = [("The Forge on Roblox (official game page)", PLACE)] + list(sources)
    G = dict(slug=slug, title=title, h1=h1, desc=desc, cat="The Forge", game="The Forge", date="2026-11-11",
             videos=vids, shorts=shorts, kw_primary=kw, kw_secondary=kw2, related=related, chapters=None,
             howto=howto, sources=src, body=body, faq=faq, forge_order=order, forge_ids=list(ids))
    return G
