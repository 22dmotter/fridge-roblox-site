import glob, importlib.util, json, os, re, html, shutil, datetime
BASE = "https://22dmotter.github.io/fridge-roblox-site/"
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = "Fridge"
YT = "https://www.youtube.com/@Fridgetherealone"
SUB = YT + "?sub_confirmation=1"
TODAY = "2026-11-10"
MOD_HUMAN = "November 10, 2026"
CATS = {
 "Codes": ("tag-codes.html", "Roblox Codes", "Working Roblox codes for November 2026 (Steal an Egg, Anime Dice, Huzz Valley), checked against live sources with every Fridge upload."),
 "Guides": ("tag-guides.html", "Roblox Guides", "Step-by-step Roblox walkthroughs: Scrooms and +1 Speed Monkey Escape, plus Bloxstrap, account recovery, thumbnails, joining players and account deletion."),
 "Events": ("tag-events.html", "Roblox Events", "Roblox event guides: the Hollow 2026, the Steal an Egg Halloween Dimension, Candy Corn and the Phantom Express."),
 "Tips": ("tag-tips.html", "Roblox Tips", "Fast Roblox tips: Steal an Egg Speed, Scrooms leveling, plus safe ways to unlock FPS, fix lag, AFK, run multiple accounts and the truth about shaders."),
}
def esc(s): return html.escape(s, quote=True)

# ---------- load guides ----------
guides = []
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "g", "*.py"))):
    spec = importlib.util.spec_from_file_location("m", f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    guides.append(m.G)
guides.sort(key=lambda g: g["date"], reverse=True)
BY = {g["slug"]: g for g in guides}
def human(d): return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")

# ---------- generated covers for guides without a video ----------
def make_cover(g):
    from PIL import Image, ImageDraw, ImageFont
    d = os.path.join(OUT, "assets", "thumbs"); os.makedirs(d, exist_ok=True)
    W,H = 1280,720
    im = Image.new("RGB",(W,H),"#0a0f14"); dr = ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; dr.line([(0,y),(W,y)], fill=(int(10+16*t),int(15+30*t),int(20+40*t)))
    F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    f_tag=ImageFont.truetype(F,34); f_brand=ImageFont.truetype(F,40)
    dr.rounded_rectangle([70,70,70+dr.textlength(g["cat"].upper(),font=f_tag)+40,124],radius=12,fill="#5ce1ff")
    dr.text((90,76),g["cat"].upper(),font=f_tag,fill="#0a0f14")
    title=g["h1"].split(" (")[0]
    size=78
    while True:
        f=ImageFont.truetype(F,size); words=title.split(); lines=[""]
        for w in words:
            tst=(lines[-1]+" "+w).strip()
            if dr.textlength(tst,font=f)<=W-140: lines[-1]=tst
            else: lines.append(w)
        if len(lines)<=4 or size<=48: break
        size-=6
    y=190
    for ln in lines: dr.text((70,y),ln,font=f,fill="#e6eef5"); y+=int(size*1.18)
    dr.rectangle([70,H-120,W-70,H-116],fill="#1f2e3d")
    dr.text((70,H-95),"FRIDGE",font=f_brand,fill="#5ce1ff")
    dr.text((250,H-88),"Roblox Codes & Guides · 2026",font=ImageFont.truetype(F,30),fill="#9fb3c4")
    im.save(os.path.join(d, g["slug"]+".png"), optimize=True)

for _g in guides:
    if not _g["videos"]: make_cover(_g)

# ---------- CSS ----------
CSS = r"""
:root{--bg:#0a0f14;--bg2:#101821;--card:#131d28;--line:#1f2e3d;--txt:#e6eef5;--mut:#9fb3c4;--acc:#5ce1ff;--acc2:#a6f0ff;--accd:#1aa7c9;--r:14px;--max:1160px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,Ubuntu,sans-serif}
a{color:var(--acc)}a:hover{color:var(--acc2)}img{max-width:100%;height:auto;display:block}
.wrap{max-width:var(--max);margin:0 auto;padding:0 16px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:var(--acc);color:#000;padding:8px;z-index:9}
header.top{position:sticky;top:0;z-index:5;background:rgba(10,15,20,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;padding:10px 0}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--txt);font-weight:800;font-size:1.25rem;letter-spacing:.3px}
.brand img{width:34px;height:34px}.brand span b{color:var(--acc)}
nav.main{order:3;width:100%;overflow-x:auto}nav.main ul{display:flex;gap:4px;list-style:none;margin:0;padding:0}
nav.main a{display:block;padding:6px 12px;border-radius:999px;color:var(--mut);text-decoration:none;font-weight:600;white-space:nowrap}
nav.main a:hover,nav.main a[aria-current=page]{color:#001018;background:var(--acc)}
form.hs{margin-left:auto;display:flex}form.hs input{width:140px;background:var(--bg2);border:1px solid var(--line);color:var(--txt);border-radius:999px;padding:7px 12px;font:inherit;font-size:.9rem}
form.hs input:focus{outline:2px solid var(--acc);border-color:transparent}
.crumbs{font-size:.85rem;color:var(--mut);margin:18px 0 8px}.crumbs ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0}
.crumbs li+li:before{content:"›";margin-right:6px;color:var(--line)}.crumbs a{color:var(--mut)}
.hero{padding:44px 0 28px;background:radial-gradient(1200px 400px at 10% -10%,rgba(92,225,255,.18),transparent),radial-gradient(800px 300px at 90% 0,rgba(26,167,201,.15),transparent)}
.hero h1{font-size:clamp(1.9rem,6vw,3.2rem);line-height:1.1;margin:.2em 0}.hero h1 b{color:var(--acc)}
.hero p{color:var(--mut);font-size:1.1rem;max-width:640px}
.btn{display:inline-block;padding:11px 20px;border-radius:999px;background:var(--acc);color:#001018;font-weight:800;text-decoration:none;margin:6px 8px 0 0}
.btn:hover{background:var(--acc2);color:#001018}.btn.ghost{background:transparent;color:var(--acc);border:1px solid var(--acc)}
h1,h2,h3{line-height:1.25}h2{font-size:1.5rem;margin:1.8em 0 .6em}h3{font-size:1.15rem;margin:1.4em 0 .4em}
.sec-h{display:flex;justify-content:space-between;align-items:baseline;gap:10px}.sec-h a{font-weight:700;text-decoration:none}
.grid{display:grid;gap:18px;grid-template-columns:1fr}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-3px);border-color:var(--accd)}
.card a.thumb{position:relative;aspect-ratio:16/9;overflow:hidden;background:#000}.card a.thumb img{width:100%;height:100%;object-fit:cover}
.card .bd{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.card h2,.card h3{margin:0;font-size:1.08rem}.card h2 a,.card h3 a{color:var(--txt);text-decoration:none}.card h2 a:hover,.card h3 a:hover{color:var(--acc)}
[hidden]{display:none!important}
.card p{margin:0;color:var(--mut);font-size:.93rem}.meta{font-size:.8rem;color:var(--mut);display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.tag{display:inline-block;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.6px;padding:3px 9px;border-radius:999px;background:rgba(92,225,255,.12);color:var(--acc);text-decoration:none;border:1px solid rgba(92,225,255,.3)}
.more{margin-top:auto;font-weight:700;text-decoration:none;font-size:.9rem}
.cats{display:grid;gap:12px;grid-template-columns:repeat(2,1fr)}
.cats a{display:block;padding:18px;border-radius:var(--r);background:var(--bg2);border:1px solid var(--line);text-decoration:none;color:var(--txt);font-weight:800}
.cats a small{display:block;color:var(--mut);font-weight:500;margin-top:4px}.cats a:hover{border-color:var(--acc)}
.intro{display:grid;gap:20px;background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);padding:22px;margin:36px 0}
.layout{display:grid;gap:28px;grid-template-columns:1fr}
article.post{min-width:0}article.post h1{font-size:clamp(1.7rem,5vw,2.5rem);margin:.2em 0 .3em}
.post .lead{font-size:1.1rem;color:#cfe0ec}.post p,.post li{max-width:72ch}
.post ol.steps{counter-reset:s;list-style:none;padding:0}.post ol.steps>li{counter-increment:s;position:relative;padding:10px 12px 10px 50px;margin:8px 0;background:var(--bg2);border:1px solid var(--line);border-radius:10px}
.post ol.steps>li:before{content:counter(s);position:absolute;left:12px;top:10px;width:26px;height:26px;border-radius:50%;background:var(--acc);color:#001018;font-weight:800;text-align:center;line-height:26px;font-size:.85rem}
.callout{border-left:4px solid var(--acc);background:rgba(92,225,255,.08);padding:12px 16px;border-radius:0 10px 10px 0;margin:18px 0}
.callout.warn{border-left-color:#ffb020;background:rgba(255,176,32,.10)}.side-box ul{margin:0;padding-left:20px}
.table-wrap{overflow-x:auto;margin:16px 0;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.95rem}caption{text-align:left;padding:10px 12px;color:var(--mut);font-size:.85rem;caption-side:top}
th,td{padding:10px 12px;border-top:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--bg2);color:var(--acc2)}
code{background:#06212b;color:var(--acc2);padding:2px 7px;border-radius:6px;font-size:.92em;user-select:all}kbd{background:var(--bg2);border:1px solid var(--line);border-radius:5px;padding:1px 6px;font-size:.85em}
.small{font-size:.85rem;color:var(--mut)}
.updated{display:inline-block;font-size:.85rem;color:var(--mut);margin-bottom:6px}.updated strong{color:var(--acc)}
.yt{position:relative;aspect-ratio:16/9;border-radius:var(--r);overflow:hidden;background:#000;border:1px solid var(--line);margin:14px 0}
.yt a,.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}.yt img{width:100%;height:100%;object-fit:cover;opacity:.85}
.yt-play{position:absolute;left:50%;top:50%;width:72px;height:50px;margin:-25px 0 0 -36px;background:var(--acc);border-radius:14px}
.yt-play:after{content:"";position:absolute;left:29px;top:14px;border-style:solid;border-width:11px 0 11px 18px;border-color:transparent transparent transparent #001018}
.yt a:hover img{opacity:1}
.toc,.side-box{background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);padding:16px 18px}
.toc ol{margin:0;padding-left:20px}.toc a{color:var(--mut);text-decoration:none}.toc a:hover{color:var(--acc)}
.faq details{background:var(--bg2);border:1px solid var(--line);border-radius:10px;margin:10px 0;padding:12px 16px}
.faq summary{cursor:pointer;font-weight:700}.faq details p{margin:.6em 0 0;color:#cfe0ec}
.related{margin:40px 0}.searchbox{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}
.searchbox input{flex:1;min-width:220px;background:var(--bg2);border:1px solid var(--line);color:var(--txt);border-radius:999px;padding:12px 18px;font:inherit}
.searchbox input:focus{outline:2px solid var(--acc);border-color:transparent}
.filters{display:flex;gap:8px;flex-wrap:wrap}.filters button{background:var(--bg2);border:1px solid var(--line);color:var(--mut);border-radius:999px;padding:8px 14px;font:inherit;font-weight:700;cursor:pointer}
.filters button[aria-pressed=true]{background:var(--acc);color:#001018;border-color:var(--acc)}
.empty{display:none;color:var(--mut)}
footer.site{margin-top:60px;border-top:1px solid var(--line);background:var(--bg2);padding:30px 0;color:var(--mut);font-size:.9rem}
footer.site .cols{display:grid;gap:20px;grid-template-columns:1fr}footer.site h2{font-size:1rem;color:var(--txt);margin:0 0 8px}
footer.site ul{list-style:none;margin:0;padding:0}footer.site li{margin:4px 0}footer.site a{color:var(--mut)}footer.site a:hover{color:var(--acc)}
.notfound{text-align:center;padding:60px 0}.notfound h1{font-size:clamp(3rem,14vw,6rem);margin:0;color:var(--acc)}
@media(min-width:640px){.grid{grid-template-columns:repeat(2,1fr)}.cats{grid-template-columns:repeat(4,1fr)}footer.site .cols{grid-template-columns:2fr 1fr 1fr}}
@media(min-width:900px){nav.main{order:0;width:auto}form.hs{margin-left:auto}form.hs input{width:190px}.grid{grid-template-columns:repeat(3,1fr)}
.layout{grid-template-columns:minmax(0,1fr) 300px}.layout aside{position:sticky;top:80px;align-self:start;display:grid;gap:16px}.intro{grid-template-columns:2fr 1fr;align-items:center}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""
def minify_css(c):
    c = re.sub(r"/\*.*?\*/", "", c, flags=re.S); c = re.sub(r"\s+", " ", c)
    c = re.sub(r"\s*([{};,>])\s*", r"\1", c); c = re.sub(r";}", "}", c)
    return c.strip()

JS = r"""(function(){
document.querySelectorAll('.yt[data-id]').forEach(function(box){var a=box.querySelector('a');if(!a)return;a.addEventListener('click',function(e){e.preventDefault();var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+box.dataset.id+'?autoplay=1&rel=0';f.title=box.dataset.title||'YouTube video';f.allow='accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture';f.allowFullscreen=true;f.loading='lazy';box.innerHTML='';box.appendChild(f);});});
var input=document.getElementById('guide-search');if(!input)return;
var cards=[].slice.call(document.querySelectorAll('.card[data-search]'));var btns=[].slice.call(document.querySelectorAll('.filters button'));var empty=document.querySelector('.empty');var cat='all';
function run(){var q=input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);var shown=0;cards.forEach(function(c){var t=c.dataset.search;var ok=(cat==='all'||c.dataset.cat===cat)&&q.every(function(w){return t.indexOf(w)>-1});c.hidden=!ok;if(ok)shown++;});if(empty)empty.style.display=shown?'none':'block';}
btns.forEach(function(b){b.addEventListener('click',function(){cat=b.dataset.cat;btns.forEach(function(x){x.setAttribute('aria-pressed',x===b)});run();});});
var p=new URLSearchParams(location.search);if(p.get('q'))input.value=p.get('q');input.addEventListener('input',run);run();
})();"""

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="t"><title id="t">Fridge logo</title><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a6f0ff"/><stop offset="1" stop-color="#1aa7c9"/></linearGradient></defs><rect x="12" y="3" width="40" height="58" rx="9" fill="url(#g)"/><rect x="12" y="24" width="40" height="3" fill="#0a0f14"/><rect x="18" y="10" width="4" height="10" rx="2" fill="#0a0f14"/><rect x="18" y="32" width="4" height="14" rx="2" fill="#0a0f14"/><path d="M38 38l3-5 3 5-3 5z" fill="#fff" opacity=".9"/><path d="M33 13l2-3 2 3-2 3z" fill="#fff" opacity=".8"/></svg>"""

def nav(active):
    items = [("index.html","Home"),("guides.html","All Guides"),("tag-codes.html","Codes"),("tag-guides.html","Guides"),("tag-events.html","Events"),("tag-tips.html","Tips"),("about.html","About")]
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a></li>' for h,t in items)
    return li

def head(title, desc, path, og_type="website", image=None, image_alt=None, extra_ld=None, prefix=""):
    url = BASE + ("" if path=="index.html" else path)
    image = image or BASE + "assets/og-default.png"
    image_alt = image_alt or "Fridge Roblox guides and codes hub"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",",":"))}</script>' for x in (extra_ld or []))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0a0f14">
<meta property="og:site_name" content="Fridge">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:alt" content="{esc(image_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{image}">
<meta name="twitter:image:alt" content="{esc(image_alt)}">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://i.ytimg.com">
<link rel="stylesheet" href="{prefix}assets/style.min.css">
<script src="{prefix}assets/site.js" defer></script>
{lds}
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
"""

def header(active, prefix=""):
    n = nav(active)
    if prefix: n = re.sub(r'href="', f'href="{prefix}', n)
    return f"""<header class="top"><div class="wrap bar">
<a class="brand" href="{prefix}index.html" aria-label="Fridge home"><img src="{prefix}assets/logo.svg" alt="Fridge logo" width="34" height="34"><span><b>Fridge</b> Guides</span></a>
<nav class="main" aria-label="Main"><ul>{n}</ul></nav>
<form class="hs" action="{prefix}guides.html" method="get" role="search"><label class="skip" for="hs-q">Search guides</label><input id="hs-q" name="q" type="search" placeholder="Search guides…" autocomplete="off"></form>
</div></header>
<main id="content">
"""

def footer(prefix=""):
    latest = "".join(f'<li><a href="{prefix}{g["slug"]}.html">{esc(g["h1"].split(":")[0])}</a></li>' for g in guides[:5])
    cats = "".join(f'<li><a href="{prefix}{v[0]}">{v[1]}</a></li>' for v in CATS.values())
    return f"""</main>
<footer class="site"><div class="wrap cols">
<div><h2>Fridge</h2><p>Roblox codes, guides and event coverage from the Fridge YouTube channel. Guides are updated with new videos and re-checked for accuracy.</p><p><a class="btn" href="{SUB}" rel="noopener" target="_blank">Subscribe on YouTube</a></p></div>
<div><h2>Latest guides</h2><ul>{latest}</ul></div>
<div><h2>Categories</h2><ul>{cats}<li><a href="{prefix}about.html">About Fridge</a></li><li><a href="{prefix}sitemap.xml">Sitemap</a></li></ul></div>
</div><div class="wrap"><p class="small">© 2026 Fridge (@Fridgetherealone). Not affiliated with Roblox Corporation or any game developer. Game names belong to their owners.</p></div></footer>
</body>
</html>
"""

def crumbs(items):
    # items: list of (name, path or None)
    li = []
    for i,(n,p) in enumerate(items):
        if p and i < len(items)-1: li.append(f'<li><a href="{p}">{esc(n)}</a></li>')
        else: li.append(f'<li aria-current="page">{esc(n)}</li>')
    ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+("" if p in (None,"index.html") and i==0 else (p or ""))} for i,(n,p) in enumerate(items)]}
    # fix last item url
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>{"".join(li)}</ol></nav>', ld

def bc_ld(items):
    els=[]
    for i,(n,p) in enumerate(items):
        url = BASE if p=="index.html" else BASE+p
        els.append({"@type":"ListItem","position":i+1,"name":n,"item":url})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":els}
def bc_html(items):
    li=[]
    for i,(n,p) in enumerate(items):
        if i < len(items)-1: li.append(f'<li><a href="{p}">{esc(n)}</a></li>')
        else: li.append(f'<li aria-current="page">{esc(n)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(li)}</ol></nav>'

def thumb(vid): return f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
def g_img(g, absolute=False):
    if g["videos"]: return thumb(g["videos"][0][0])
    return (BASE if absolute else "") + f"assets/thumbs/{g['slug']}.png"
def g_img_alt(g):
    if g["videos"]: return f"{g['game']} guide thumbnail: {g['videos'][0][1]}"
    return f"Fridge guide cover image: {g['h1']}"
PLACEHOLDER = """<!-- YOUTUBE EMBED PLACEHOLDER: no matching Fridge video yet.
     When a video exists, add ("VIDEO_ID", "Video title") to this guide's videos=[...] list in _build/g/
     and replace {VIDEO_PLACEHOLDER} in the body with {VIDEO0}, then run python3 _build/build.py.
     Raw HTML alternative: copy any <div class="yt" data-id="VIDEO_ID_HERE"> block from another guide. -->
<div class="callout"><strong>Video coming soon:</strong> Fridge hasn't made a video for this guide yet. Subscribe on <a href="https://www.youtube.com/@Fridgetherealone?sub_confirmation=1" rel="noopener" target="_blank">YouTube</a> to catch it when it drops.</div>
<!-- /YOUTUBE EMBED PLACEHOLDER -->"""

def card(g, lvl="h3"):
    cat = g["cat"]
    search = " ".join([g["title"], g["h1"], g["desc"], g["game"], cat, g["kw_primary"], " ".join(g["kw_secondary"])]).lower()
    return f"""<article class="card" data-cat="{cat}" data-search="{esc(search)}">
<a class="thumb" href="{g['slug']}.html" tabindex="-1" aria-hidden="true"><img src="{g_img(g)}" alt="{esc(g_img_alt(g))}" loading="lazy" width="480" height="270"></a>
<div class="bd"><div class="meta"><a class="tag" href="{CATS[cat][0]}">{cat}</a><time datetime="{g['date']}">{human(g['date'])}</time></div>
<{lvl}><a href="{g['slug']}.html">{esc(g['h1'])}</a></{lvl}>
<p>{esc(g['desc'])}</p><a class="more" href="{g['slug']}.html" aria-label="Read: {esc(g['h1'])}">Read guide →</a></div></article>"""

def video_embed(vid, title, game):
    return f"""<!-- YOUTUBE EMBED: Fridge video "{esc(title)}" (ID {vid}).
     To swap in a different video, replace the 11-character ID in ALL THREE places below
     (data-id, the watch?v= link and the thumbnail URL). Placeholder for a new video: VIDEO_ID_HERE -->
<div class="yt" data-id="{vid}" data-title="{esc(title)}">
<a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener" aria-label="Play video: {esc(title)}"><img src="{thumb(vid)}" alt="Fridge YouTube video thumbnail: {esc(title)} ({esc(game)})" loading="lazy" width="480" height="360"><span class="yt-play" aria-hidden="true"></span></a>
</div>
<!-- /YOUTUBE EMBED -->"""

def write(path, s):
    with open(os.path.join(OUT, path), "w") as f: f.write(s)

ORG = {"@type":"Organization","name":"Fridge","url":BASE,"logo":BASE+"assets/apple-touch-icon.png","sameAs":[YT]}
PERSON = {"@type":"Person","name":"Fridge","url":BASE+"about.html","sameAs":[YT]}

def page(path, title, desc, crumbs_items, body, active=None, og_type="website", image=None, image_alt=None, ld=None):
    ld = (ld or []) + [bc_ld(crumbs_items)]
    return head(title, desc, path, og_type, image, image_alt, ld) + header(active or path) + body.replace("{CRUMBS}", bc_html(crumbs_items)) + footer()

report = []
# ---------- guide pages ----------
for g in guides:
    body = g["body"]
    for i,(vid,t) in enumerate(g["videos"]):
        body = body.replace("{VIDEO%d}"%i, video_embed(vid,t,g["game"]))
    body = body.replace("{VIDEO_PLACEHOLDER}", PLACEHOLDER)
    h2s = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    toc = "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>","",t)}</a></li>' for i,t in h2s) + '<li><a href="#faq">FAQ</a></li>'
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q,a in g["faq"])
    rel = [BY[s] for s in g["related"] if s in BY][:3]
    sources_html = ""
    if g.get("sources"):
        sources_html = '<section class="side-box" aria-labelledby="src-h" style="margin-top:28px"><h2 id="src-h" style="margin-top:0">Official sources</h2><ul>' + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{esc(n)}</a></li>' for n,u in g["sources"]) + '</ul></section>'
    rel_html = "".join(card(r) for r in rel)
    catp, catn, _ = CATS[g["cat"]]
    items = [("Home","index.html"),(catn,catp),(g["h1"].split(":")[0], g["slug"]+".html")]
    url = BASE + g["slug"] + ".html"
    ld_post = {"@context":"https://schema.org","@type":"BlogPosting","headline":g["h1"],"description":g["desc"],"image":[g_img(g, True)],
      "datePublished":g["date"],"dateModified":TODAY,"author":PERSON,"publisher":ORG,"mainEntityOfPage":{"@type":"WebPage","@id":url},
      "articleSection":g["cat"],"keywords":", ".join([g["kw_primary"]]+g["kw_secondary"]),"about":{"@type":"VideoGame","name":g["game"],"gamePlatform":"Roblox"},
      **({} if not g["videos"] else {"video":[{"@type":"VideoObject","name":t,"embedUrl":f"https://www.youtube.com/embed/{v}","contentUrl":f"https://www.youtube.com/watch?v={v}","thumbnailUrl":thumb(v),"uploadDate":g["date"],"description":f"Fridge's Roblox video: {t}"} for v,t in g["videos"]]})}
    ld_faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in g["faq"]]}
    content = f"""<div class="wrap">{{CRUMBS}}
<div class="layout">
<article class="post">
<header>
<a class="tag" href="{catp}">{g['cat']}</a>
<h1>{esc(g['h1'])}</h1>
<p class="updated">By <a href="about.html">Fridge</a> · Published <time datetime="{g['date']}">{human(g['date'])}</time> · <strong>Last updated: <time datetime="{TODAY}">{MOD_HUMAN}</time></strong></p>
</header>
{body}
{sources_html}
<section class="faq" id="faq" aria-labelledby="faq-h">
<h2 id="faq-h">{esc(g['game'])} FAQ</h2>
{faq_html}
</section>
<p class="callout">Found this helpful? <a href="{SUB}" rel="noopener" target="_blank">Subscribe to Fridge on YouTube</a> for new {esc(g['game'])} videos. {"This guide is updated with every new upload." if g["videos"] else "This guide is re-checked against official Roblox sources when things change."}</p>
</article>
<aside>
<nav class="toc" aria-label="Table of contents"><strong>On this page</strong><ol>{toc}</ol></nav>
<div class="side-box"><strong>More {esc(g['cat'])}</strong><ul>{''.join(f'<li><a href="{x["slug"]}.html">{esc(x["h1"].split(":")[0])}</a></li>' for x in guides if x["cat"]==g["cat"] and x is not g)}</ul><a href="{catp}">See all {g['cat'].lower()} →</a></div>
</aside>
</div>
<section class="related" aria-labelledby="rel-h"><div class="sec-h"><h2 id="rel-h">Related Guides</h2><a href="guides.html">All guides →</a></div><div class="grid">{rel_html}</div></section>
</div>"""
    write(g["slug"]+".html", page(g["slug"]+".html", g["title"], g["desc"], items, content, active="guides.html", og_type="article",
        image=g_img(g, True), image_alt=g_img_alt(g), ld=[ld_post, ld_faq]))
    # stats
    text = re.sub(r"<!--.*?-->", " ", body, flags=re.S); text = re.sub(r"<[^>]+>", " ", text)
    fq = " ".join(q+" "+a for q,a in g["faq"])
    words = re.findall(r"[\w'+.&-]+", html.unescape(text+" "+fq).lower())
    full = " ".join(words)
    kw = g["kw_primary"].lower()
    occ = full.count(kw)
    first100 = " ".join(re.findall(r"[\w'+.&-]+", html.unescape(re.sub(r"<[^>]+>"," ",body)).lower())[:100])
    links = len(re.findall(r'<a href="[a-z0-9-]+\.html">', body))
    report.append(dict(slug=g["slug"], title_len=len(g["title"]), desc_len=len(g["desc"]), words=len(words), kw=kw, occ=occ,
        density=round(100*occ*len(kw.split())/len(words),2), kw_first100=kw in first100, body_links=links, h1=g["h1"], title=g["title"], sec=g["kw_secondary"]))

# ---------- index ----------
feat = "".join(card(g) for g in guides[:6])
game_feat = "".join(card(g) for g in [x for x in guides if x["videos"]][:6])
help_feat = "".join(card(g) for g in [x for x in guides if not x["videos"]][6:10])
cats_html = "".join(f'<a href="{v[0]}">{v[1]}<small>{sum(1 for g in guides if g["cat"]==k)} guides</small></a>' for k,v in CATS.items())
idx_ld = [{"@context":"https://schema.org","@type":"WebSite","name":"Fridge Guides","url":BASE,"potentialAction":{"@type":"SearchAction","target":BASE+"guides.html?q={search_term_string}","query-input":"required name=search_term_string"}},
          dict({"@context":"https://schema.org"}, **ORG)]
idx_body = f"""<section class="hero"><div class="wrap">{{CRUMBS}}
<p class="tag">Roblox codes · guides · events</p>
<h1>Roblox Codes &amp; Guides by <b>Fridge</b></h1>
<p>Working Roblox codes, beginner guides and event walkthroughs for Steal an Egg, Scrooms, Anime Dice, the Hollow event and more. Game guides match Fridge's YouTube videos, and evergreen Roblox help guides cover FPS, lag, Bloxstrap and account safety.</p>
<a class="btn" href="guides.html">Browse all guides</a><a class="btn ghost" href="{SUB}" rel="noopener" target="_blank">Subscribe on YouTube</a>
</div></section>
<div class="wrap">
<section aria-labelledby="latest-h"><div class="sec-h"><h2 id="latest-h">Latest Roblox Guides</h2><a href="guides.html">View all →</a></div><div class="grid">{feat}</div></section>
<section aria-labelledby="game-h"><div class="sec-h"><h2 id="game-h">Latest Game Codes &amp; Guides</h2><a href="tag-codes.html">All codes →</a></div><div class="grid">{game_feat}</div></section>
<section aria-labelledby="cat-h"><h2 id="cat-h">Browse by Category</h2><div class="cats">{cats_html}</div></section>
<section class="intro" aria-labelledby="ch-h"><div><h2 id="ch-h">Welcome to the Fridge Content Hub</h2>
<p>Fridge is a Roblox YouTube channel focused on fast, no-nonsense guides: the newest codes, the quickest ways to level up, and full walkthroughs for big events like the Roblox Hollow. This site is the written companion to the channel, so you can copy codes, check tables and skim steps without scrubbing through a video.</p>
<p>Start with the <a href="steal-an-egg-speed-guide.html">Steal an Egg speed guide</a>, the <a href="scrooms-beginners-guide.html">Scrooms beginner's guide</a> or the latest <a href="anime-dice-codes.html">Anime Dice codes</a>.</p></div>
<div><a class="btn" href="{YT}/videos" rel="noopener" target="_blank">Watch Fridge's videos</a><a class="btn ghost" href="about.html">About Fridge</a></div></section>
<section aria-labelledby="pop-h"><h2 id="pop-h">Popular Right Now</h2><div class="grid">{"".join(card(BY[s]) for s in ["steal-an-egg-codes","roblox-hollow-event-guide","huzz-valley-codes"])}</div></section>
<section aria-labelledby="help-h"><h2 id="help-h">More Roblox Help Guides</h2><div class="grid">{help_feat}</div></section>
</div>"""
write("index.html", page("index.html", "Fridge – Roblox Codes & Guides Hub (November 2026)",
 "Fridge's Roblox hub: working codes for Anime Dice and Huzz Valley, Steal an Egg speed tips, Scrooms guides and Hollow event coverage. Find your guide now!",
 [("Home","index.html")], idx_body, active="index.html", ld=idx_ld))

# ---------- guides listing ----------
all_cards = "".join(card(g, "h2") for g in guides)
filt = '<button type="button" data-cat="all" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-cat="{k}" aria-pressed="false">{k}</button>' for k in CATS)
list_ld = [{"@context":"https://schema.org","@type":"CollectionPage","name":"All Fridge Roblox Guides","url":BASE+"guides.html","mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+g["slug"]+".html","name":g["h1"]} for i,g in enumerate(guides)]}}]
gl_body = f"""<div class="wrap">{{CRUMBS}}
<h1>All Roblox Guides &amp; Codes</h1>
<p class="updated"><strong>Last updated: <time datetime="{TODAY}">{MOD_HUMAN}</time></strong> · {len(guides)} guides</p>
<p>Every Fridge guide in one place: Roblox codes, beginner walkthroughs, event guides and quick tips. Search by game or keyword, or filter by category.</p>
<div class="searchbox" role="search"><label class="skip" for="guide-search">Search guides</label><input id="guide-search" type="search" placeholder="Search guides, e.g. Steal an Egg speed, Scrooms, codes…" autocomplete="off"><div class="filters" aria-label="Filter by category">{filt}</div></div>
<p class="empty" role="status">No guides match that search. Try a game name like "Scrooms" or "Steal an Egg".</p>
<div class="grid">{all_cards}</div>
</div>"""
write("guides.html", page("guides.html", "All Roblox Guides & Codes (2026) | Fridge",
 "Browse every Fridge Roblox guide: Steal an Egg, Scrooms, Anime Dice and Huzz Valley codes, Hollow event guides and tips. Search or filter to find yours now!",
 [("Home","index.html"),("All Guides","guides.html")], gl_body, active="guides.html", ld=list_ld))

# ---------- tag pages ----------
TAGMETA = {
 "Codes": ("Roblox Codes November 2026 – Working Codes | Fridge", "Working Roblox codes for November 2026: Anime Dice rerolls, Huzz Valley free spins and the truth about Steal an Egg codes. Copy them and redeem today!"),
 "Guides": ("Roblox Game Guides & Walkthroughs | Fridge", "Step-by-step Roblox guides from Fridge: how to play Scrooms, every Scrooms statue, and all 9 Monkey Escape shards. Pick a walkthrough and start now!"),
 "Events": ("Roblox Event Guides 2026 – Hollow & Halloween | Fridge", "Roblox event guides for 2026: the Hollow event recap, Steal an Egg Halloween Dimension, Candy Corn farming and the Phantom Express. Catch up on it all!"),
 "Tips": ("Roblox Tips: Speed, XP & Racing Tricks | Fridge", "Quick Roblox tips from Fridge: how to get speed in Steal an Egg, level up fast in Scrooms, and win every race. Use these tricks to progress faster today!"),
}
for k,(p,n,intro) in CATS.items():
    gs = [g for g in guides if g["cat"]==k]
    t, d = TAGMETA[k]
    ld = [{"@context":"https://schema.org","@type":"CollectionPage","name":n,"description":d,"url":BASE+p,"mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+g["slug"]+".html","name":g["h1"]} for i,g in enumerate(gs)]}}]
    others = " · ".join(f'<a href="{v[0]}">{v[1]}</a>' for kk,v in CATS.items() if kk!=k)
    b = f"""<div class="wrap">{{CRUMBS}}
<h1>{n} by Fridge</h1>
<p class="updated"><strong>Last updated: <time datetime="{TODAY}">{MOD_HUMAN}</time></strong> · {len(gs)} guides</p>
<p>{intro}</p>
<div class="grid">{"".join(card(g,"h2") for g in gs)}</div>
<p style="margin-top:28px">More categories: {others} · <a href="guides.html">All guides</a></p>
</div>"""
    write(p, page(p, t, d, [("Home","index.html"),(n,p)], b, active=p, ld=ld))

# ---------- about ----------
ab_ld = [{"@context":"https://schema.org","@type":"AboutPage","name":"About Fridge","url":BASE+"about.html","mainEntity":dict(ORG, description="Roblox YouTube channel making codes, guides and event videos.")}]
ab_body = f"""<div class="wrap">{{CRUMBS}}
<article class="post">
<h1>About Fridge: Roblox Guides on YouTube</h1>
<p class="updated"><strong>Last updated: <time datetime="{TODAY}">{MOD_HUMAN}</time></strong></p>
<p class="lead">Fridge (<a href="{YT}" rel="noopener" target="_blank">@Fridgetherealone</a>) is a Roblox YouTube channel that makes quick, useful guides: working codes, the fastest ways to level up and get stronger, collectible locations, and full coverage of big Roblox events.</p>
<h2>What Fridge covers</h2>
<ul>
<li><strong>Codes:</strong> working code lists for games like <a href="anime-dice-codes.html">Anime Dice</a> and <a href="huzz-valley-codes.html">Huzz Valley</a>, plus honest answers when a game like <a href="steal-an-egg-codes.html">Steal an Egg</a> has no codes at all.</li>
<li><strong>Guides:</strong> beginner walkthroughs such as <a href="scrooms-beginners-guide.html">how to play Scrooms</a> and location guides like the <a href="monkey-escape-sunken-shards.html">Monkey Escape shards</a>.</li>
<li><strong>Events:</strong> leaks, confirmed games and badge guides for events like the <a href="roblox-hollow-event-guide.html">Roblox Hollow event</a>.</li>
<li><strong>Tips:</strong> speed, XP and racing tricks that save you hours of grinding.</li>
</ul>
<p>Past videos have also covered The Forge (pickaxe upgrades, money-making methods and Crimson Depths), Steal an Egg rare eggs and more.</p>
<h2>How this site works</h2>
<p>Each guide on this site goes with a Fridge video. The written version lets you copy codes, scan tables and follow numbered steps at your own pace. Guides show a visible "Last updated" date, and code pages are rechecked against current sources whenever a new video goes up. If something has expired or changed, the page says so. We never list made-up codes or present rumors as facts.</p>
<h2>Watch and subscribe</h2>
<p>New videos drop regularly on the channel. Subscribe so you don't miss new codes and event guides.</p>
<p><a class="btn" href="{SUB}" rel="noopener" target="_blank">Subscribe to Fridge</a><a class="btn ghost" href="{YT}/videos" rel="noopener" target="_blank">See all videos</a></p>
<h2>Disclaimer</h2>
<p class="small">Fridge is an independent creator and is not affiliated with Roblox Corporation or any game developer. Game names, logos and assets belong to their owners. Code rewards and event details can change at any time.</p>
</article></div>"""
write("about.html", page("about.html", "About Fridge – Roblox YouTuber (@Fridgetherealone)",
 "Meet Fridge (@Fridgetherealone), the Roblox YouTuber behind these codes, guides and event videos. See what the channel covers and subscribe for new uploads!",
 [("Home","index.html"),("About","about.html")], ab_body, active="about.html", ld=ab_ld))

# ---------- 404 (absolute paths so it works at any depth) ----------
P = "/fridge-roblox-site/"
nf = head("Page Not Found (404) | Fridge Roblox Guides", "This page doesn't exist or has moved. Search Fridge's Roblox guides or jump to the latest codes for Steal an Egg, Anime Dice and Huzz Valley right here.", "404.html", prefix=P, extra_ld=[bc_ld([("Home","index.html"),("Page not found","404.html")])])
nf = nf.replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex,follow">')
nf += header("", prefix=P) + f"""<div class="wrap">{bc_html([("Home",P+"index.html"),("Page not found","")])}
<section class="notfound"><h1>404</h1><h2>This page melted.</h2><p>The guide you're looking for doesn't exist or has moved. Try a search or pick a popular guide below.</p>
<form action="{P}guides.html" method="get" role="search" class="searchbox" style="max-width:520px;margin:20px auto"><label class="skip" for="nf-q">Search guides</label><input id="nf-q" name="q" type="search" placeholder="Search guides…"></form>
<a class="btn" href="{P}index.html">Back to home</a><a class="btn ghost" href="{P}guides.html">All guides</a></section>
<div class="grid">{"".join(card(BY[s]).replace('href="', 'href="'+P).replace('href="'+P+'http','href="http') for s in ["steal-an-egg-codes","anime-dice-codes","scrooms-beginners-guide"])}</div></div>""" + footer(prefix=P)
write("404.html", nf)

# ---------- sitemap / robots ----------
urls = [("",TODAY,"1.0","daily"),("guides.html",TODAY,"0.9","daily"),("about.html",TODAY,"0.5","monthly")] + \
       [(v[0],TODAY,"0.7","weekly") for v in CATS.values()] + [(g["slug"]+".html",TODAY,"0.8","weekly") for g in guides]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{BASE}{u}</loc><lastmod>{d}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n" for u,d,p,c in urls) + "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")

# ---------- assets ----------
os.makedirs(os.path.join(OUT,"assets"), exist_ok=True)
write("assets/style.min.css", minify_css(CSS))
write("assets/site.js", JS)
write("assets/logo.svg", LOGO_SVG)
write("assets/favicon.svg", LOGO_SVG)
write(".nojekyll", "")
json.dump(report, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"seo-report.json"),"w"), indent=1)
for r in report: print(r["slug"], "T",r["title_len"], "D",r["desc_len"], "W",r["words"], "kw",r["occ"], r["density"], "first100",r["kw_first100"], "links",r["body_links"])
