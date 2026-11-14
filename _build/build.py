import glob, importlib.util, json, os, re, html, shutil, datetime
BASE = os.environ.get("SITE_BASE", "https://robloxguides.org/").rstrip("/") + "/"
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = "Fridge"
YT = "https://www.youtube.com/@Fridgetherealone"
SUB = YT + "?sub_confirmation=1"
TODAY = "2026-11-12"
MOD_HUMAN = "November 12, 2026"
CATS = {
 "Codes": ("tag-codes.html", "Roblox Codes", "Working Roblox codes for November 2026 for the top 20 games by players (Steal an Egg, Blox Fruits, RIVALS, Fisch, Steal a Brainrot, Anime Adventures and more) plus The Forge, Dress To Impress, King Legacy, Blade Ball, Bee Swarm Simulator, Arise Crossover, Anime Dice, Huzz Valley and more, all collected in the November 2026 codes hub. Each code is checked against at least two live sources, and games with no codes say so."),
 "Guides": ("tag-guides.html", "Roblox Guides", "Step-by-step Roblox walkthroughs: voice chat, Trusted Friends, appearing offline, parental controls, gift cards, account status and accessories, free items, leveling, pets, reporting players, Communities, age checks and username changes, plus The Forge (races, pickaxes and money), Scrooms, Bloxstrap, account recovery and more."),
 "Events": ("tag-events.html", "Roblox Events", "Roblox event guides: a November 2026 leak about a Twin Atlas test place named Slippers that trackers tie to a possible Christmas or winter event, the Hollow 2026 recap, and the Steal an Egg Halloween Dimension, Candy Corn and the Phantom Express."),
"Tips": ("tag-tips.html", "Roblox Tips", "Fast Roblox tips: beginner guides for Throw Food For Animals and 99 Nights in the Forest, avatar outfit ideas, emotes, Steal an Egg Speed and Scrooms leveling, plus safe ways to unlock FPS, fix lag and AFK."),
 "Macro": ("tag-macro.html", "Roblox Macros", "Guides to Roblox macros and auto clickers: what they are, whether they can get you banned, safer download habits, TinyTask and AutoHotkey, Mac tools, and game-specific notes for Grow a Garden, Fisch and Bee Swarm Simulator. Every page includes a Roblox Terms of Use and malware warning. Fridge is not affiliated with any macro vendor, and no tool is described as allowed or undetectable."),
}
def esc(s): return html.escape(s, quote=True)

def email_link(text=None):
    enc = "".join(f"&#{ord(c)};" for c in "blazingblox49@gmail.com")
    return f'<a href="mailto:{enc}">{text if text is not None else enc}</a>'


# ---------- load guides ----------
guides = []
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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
        t=y/H; dr.line([(0,y),(W,y)], fill=(int(10+24*t),int(15+14*t),int(20+2*t)))
    F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    f_tag=ImageFont.truetype(F,34); f_brand=ImageFont.truetype(F,40)
    dr.rounded_rectangle([70,70,70+dr.textlength(g["cat"].upper(),font=f_tag)+40,124],radius=12,fill="#ffb020")
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
    dr.rectangle([70,H-120,W-70,H-116],fill="#3a2a10")
    dr.text((70,H-95),"FRIDGE",font=f_brand,fill="#ffb020")
    dr.text((250,H-88),"Roblox Codes & Guides · 2026",font=ImageFont.truetype(F,30),fill="#9fb3c4")
    im.save(os.path.join(d, g["slug"]+".png"), optimize=True)

for _g in guides:
    cover = _g.get("cover") or ""
    if cover.endswith(f"/thumbs/{_g['slug']}.png") or cover.endswith(f"thumbs/{_g['slug']}.png") or (not _g["videos"] and not _g.get("cover")):
        make_cover(_g)

# ---------- CSS ----------
CSS = r"""
.bg-fx{position:fixed;inset:0;z-index:-1;pointer-events:none;overflow:hidden}
.bg-fx canvas{display:block;width:100%;height:100%}
@media (prefers-reduced-motion:reduce){.bg-fx{display:none}}
.short-slot{margin:22px auto;max-width:300px}.short-ph{aspect-ratio:9/16;width:100%;border:2px dashed var(--acc);border-radius:18px;background:var(--bg2);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;text-align:center;padding:18px;color:var(--mut)}
.short-ph strong{color:var(--txt)}.short-ic{width:56px;height:56px;border-radius:14px;background:#FF0000;color:#fff;display:flex;align-items:center;justify-content:center;font-size:1.4rem}
.shorts-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:16px;margin:18px 0}.shorts-grid .short-slot{margin:0;max-width:none}
.short-slot iframe{aspect-ratio:9/16;width:100%;height:auto;border:0;border-radius:18px}.short-slot figcaption{text-align:center;margin-top:6px}
figure.shot{margin:20px 0;background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);overflow:hidden}figure.shot img{width:100%;height:auto;display:block;background:#000}figure.shot figcaption{padding:10px 14px;font-size:.85rem;color:var(--mut);line-height:1.45}figure.shot figcaption a{font-weight:700}
:root{--bg:#0a0f14;--bg2:#101821;--card:#131d28;--line:#1f2e3d;--txt:#e6eef5;--mut:#9fb3c4;--acc:#ffb020;--acc2:#ffc966;--accd:#e8890c;--acc3:#f5a623;--ink:#1a1000;--r:14px;--max:1160px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,Ubuntu,sans-serif}
a{color:var(--acc)}a:hover{color:var(--accd)}img{max-width:100%;height:auto;display:block}
.wrap{max-width:var(--max);margin:0 auto;padding:0 16px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:var(--acc);color:#000;padding:8px;z-index:9}
header.top{position:sticky;top:0;z-index:5;background:rgba(10,15,20,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;padding:10px 0}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--txt);font-weight:800;font-size:1.25rem;letter-spacing:.3px}
.brand img{width:34px;height:34px}.brand span b{color:var(--acc)}
nav.main{order:3;width:100%;overflow-x:auto}nav.main ul{display:flex;gap:4px;list-style:none;margin:0;padding:0}
nav.main a{display:block;padding:6px 12px;border-radius:999px;color:var(--mut);text-decoration:none;font-weight:600;white-space:nowrap}
nav.main a:hover,nav.main a[aria-current=page]{color:var(--ink);background:var(--acc)}
form.hs{margin-left:auto;display:flex}form.hs input{width:140px;background:var(--bg2);border:1px solid var(--line);color:var(--txt);border-radius:999px;padding:7px 12px;font:inherit;font-size:.9rem}
form.hs input:focus{outline:2px solid var(--acc);border-color:transparent}
.crumbs{font-size:.85rem;color:var(--mut);margin:18px 0 8px}.crumbs ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0}
.crumbs li+li:before{content:"›";margin-right:6px;color:var(--line)}.crumbs a{color:var(--mut)}
.hero{padding:44px 0 28px;background:radial-gradient(1200px 400px at 10% -10%,rgba(255,176,32,.16),transparent),radial-gradient(800px 300px at 90% 0,rgba(232,137,12,.14),transparent)}
.hero h1{font-size:clamp(1.9rem,6vw,3.2rem);line-height:1.1;margin:.2em 0}.hero h1 b{color:var(--acc)}
.hero p{color:var(--mut);font-size:1.1rem;max-width:640px}
.btn{display:inline-block;padding:11px 20px;border-radius:999px;background:var(--acc);color:var(--ink);font-weight:800;text-decoration:none;margin:6px 8px 0 0}
.btn:hover{background:var(--accd);color:var(--ink)}.btn.ghost:hover{background:rgba(255,176,32,.12);color:var(--acc2);border-color:var(--acc2)}.btn.ghost{background:transparent;color:var(--acc);border:1px solid var(--acc)}
.yt-sub{background:transparent;color:#FF4D4D!important;font-weight:800;text-decoration:none;border-radius:999px;border:2px solid #FF0000;transition:background-color .2s ease,color .2s ease,border-color .2s ease,box-shadow .2s ease}
a.yt-sub:not(.btn){display:inline-block;padding:2px 12px;margin:2px 0;line-height:1.4}
.btn.yt-sub{background:transparent;color:#FF4D4D!important;border:2px solid #FF0000;font-size:1.2rem;padding:10px 22px}
.yt-sub:hover,.yt-sub:focus-visible,.yt-sub:active,
a.btn.yt-sub:hover,a.btn.yt-sub:focus-visible,a.btn.yt-sub:active{
background:#FF0000;color:#fff!important;border-color:#FF0000}
.yt-sub:focus-visible,a.btn.yt-sub:focus-visible{outline:3px solid #fff;outline-offset:2px;box-shadow:0 0 0 6px #FF0000}
h1,h2,h3{line-height:1.25}h2{font-size:1.5rem;margin:1.8em 0 .6em}h3{font-size:1.15rem;margin:1.4em 0 .4em}
.sec-h{display:flex;justify-content:space-between;align-items:baseline;gap:10px}.sec-h a{font-weight:700;text-decoration:none}
.grid{display:grid;gap:18px;grid-template-columns:1fr}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-3px);border-color:var(--accd)}
.card a.thumb{position:relative;aspect-ratio:16/9;overflow:hidden;background:#000}.card a.thumb img{width:100%;height:100%;object-fit:cover}
.card .bd{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.card h2,.card h3{margin:0;font-size:1.08rem}.card h2 a,.card h3 a{color:var(--txt);text-decoration:none}.card h2 a:hover,.card h3 a:hover{color:var(--acc)}
[hidden]{display:none!important}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.card p{margin:0;color:var(--mut);font-size:.93rem}.meta{font-size:.8rem;color:var(--mut);display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.tag{display:inline-block;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.6px;padding:3px 9px;border-radius:999px;background:rgba(255,176,32,.12);color:var(--acc);text-decoration:none;border:1px solid rgba(255,176,32,.35)}
.more{margin-top:auto;font-weight:700;text-decoration:none;font-size:.9rem}
.cats{display:grid;gap:12px;grid-template-columns:repeat(2,1fr)}
.cats a{display:block;padding:18px;border-radius:var(--r);background:var(--bg2);border:1px solid var(--line);text-decoration:none;color:var(--txt);font-weight:800}
.cats a small{display:block;color:var(--mut);font-weight:500;margin-top:4px}.cats a:hover{border-color:var(--acc)}
.intro{display:grid;gap:20px;background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);padding:22px;margin:36px 0}
.layout{display:grid;gap:28px;grid-template-columns:1fr}
article.post{min-width:0}article.post h1{font-size:clamp(1.7rem,5vw,2.5rem);margin:.2em 0 .3em}
.post .lead{font-size:1.1rem;color:#cfe0ec}.post p,.post li{max-width:72ch}
.post ol.steps{counter-reset:s;list-style:none;padding:0}.post ol.steps>li{counter-increment:s;position:relative;padding:10px 12px 10px 50px;margin:8px 0;background:var(--bg2);border:1px solid var(--line);border-radius:10px}
.post ol.steps>li:before{content:counter(s);position:absolute;left:12px;top:10px;width:26px;height:26px;border-radius:50%;background:var(--acc);color:var(--ink);font-weight:800;text-align:center;line-height:26px;font-size:.85rem}
.callout{border-left:4px solid var(--acc);background:rgba(255,176,32,.08);padding:12px 16px;border-radius:0 10px 10px 0;margin:18px 0}
.chapters{background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);padding:14px 18px;margin:18px 0}.chapters h2{margin:0 0 4px;font-size:1.2rem}.chapters ol{margin:8px 0 0;padding-left:22px}.chapters .ts{display:inline-block;min-width:3.2em;font-variant-numeric:tabular-nums;color:var(--acc);font-weight:700}
.callout.warn{border-left-color:#ff6b3d;background:rgba(255,107,61,.10)}.callout.warn strong:first-child{color:#ff9a75}.side-box ul{margin:0;padding-left:20px}
.table-wrap{overflow-x:auto;margin:16px 0;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.95rem}caption{text-align:left;padding:10px 12px;color:var(--mut);font-size:.85rem;caption-side:top}
th,td{padding:10px 12px;border-top:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--bg2);color:var(--acc2)}
code{background:#2a1d06;color:var(--acc2);padding:2px 7px;border-radius:6px;font-size:.92em;user-select:all}kbd{background:var(--bg2);border:1px solid var(--line);border-radius:5px;padding:1px 6px;font-size:.85em}
.small{font-size:.85rem;color:var(--mut)}
.updated{display:inline-block;font-size:.85rem;color:var(--mut);margin-bottom:6px}.updated strong{color:var(--acc)}
.yt{position:relative;aspect-ratio:16/9;border-radius:var(--r);overflow:hidden;background:#000;border:1px solid var(--line);margin:14px 0}
.yt a,.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}.yt img{width:100%;height:100%;object-fit:cover;opacity:.85}
.yt-play{position:absolute;left:50%;top:50%;width:72px;height:50px;margin:-25px 0 0 -36px;background:var(--acc);border-radius:14px}
.yt-play:after{content:"";position:absolute;left:29px;top:14px;border-style:solid;border-width:11px 0 11px 18px;border-color:transparent transparent transparent var(--ink)}
.yt a:hover img{opacity:1}
.toc,.side-box{background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);padding:16px 18px}
.toc ol{margin:0;padding-left:20px}.toc a{color:var(--mut);text-decoration:none}.toc a:hover{color:var(--acc)}
.faq details{background:var(--bg2);border:1px solid var(--line);border-radius:10px;margin:10px 0;padding:12px 16px}
.faq summary{cursor:pointer;font-weight:700}.faq details p{margin:.6em 0 0;color:#cfe0ec}
.related{margin:40px 0}.searchbox{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}
.searchbox input{flex:1;min-width:220px;background:var(--bg2);border:1px solid var(--line);color:var(--txt);border-radius:999px;padding:12px 18px;font:inherit}
.searchbox input:focus{outline:2px solid var(--acc);border-color:transparent}
.filters{display:flex;gap:8px;flex-wrap:wrap}.filters button{background:var(--bg2);border:1px solid var(--line);color:var(--mut);border-radius:999px;padding:8px 14px;font:inherit;font-weight:700;cursor:pointer}
.filters button[aria-pressed=true]{background:var(--acc);color:var(--ink);border-color:var(--acc)}
.empty{display:none;color:var(--mut)}
footer.site{margin-top:60px;border-top:1px solid var(--line);background:var(--bg2);padding:30px 0;color:var(--mut);font-size:.9rem}
footer.site .cols{display:grid;gap:20px;grid-template-columns:1fr}footer.site h2{font-size:1rem;color:var(--txt);margin:0 0 8px}
footer.site ul{list-style:none;margin:0;padding:0}footer.site li{margin:4px 0}footer.site a{color:var(--mut)}footer.site a:hover{color:var(--acc)}footer.site .legal{margin-top:18px;padding-top:16px;border-top:1px solid var(--line)}footer.site .legal-nav{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0 0 12px}footer.site .legal-nav a{color:var(--txt);font-weight:600}footer.site .disclosure{max-width:70rem;margin:0 0 8px;line-height:1.55}
.notfound{text-align:center;padding:60px 0}.notfound h1{font-size:clamp(3rem,14vw,6rem);margin:0;color:var(--acc)}
@media(min-width:640px){.grid{grid-template-columns:repeat(2,1fr)}.cats{grid-template-columns:repeat(4,1fr)}footer.site .cols{grid-template-columns:2fr 1fr 1fr}}
@media(min-width:900px){nav.main{order:0;width:auto;overflow:visible}form.hs{margin-left:auto}form.hs input{width:190px}.grid{grid-template-columns:repeat(3,1fr)}
.layout{grid-template-columns:minmax(0,1fr) 300px}.layout aside{position:sticky;top:80px;align-self:start;display:grid;gap:16px}.intro{grid-template-columns:2fr 1fr;align-items:center}}
/* Games nav dropdown: the Games label links to games.html; the caret toggles the menu */
nav.main .nav-dd{position:static}
nav.main .nav-dd-label{display:inline-flex;align-items:center;border-radius:999px;color:var(--mut);background:transparent}
nav.main a.nav-dd-link{padding:6px 8px 6px 12px;border-radius:999px 0 0 999px;color:inherit;background:transparent}
nav.main a.nav-dd-link:hover,nav.main a.nav-dd-link[aria-current=page]{color:inherit;background:transparent}
nav.main .nav-dd-btn{display:flex;align-items:center;justify-content:center;margin:0;padding:6px 12px 6px 4px;border-radius:0 999px 999px 0;color:inherit;background:transparent;border:0;font:inherit;cursor:pointer;line-height:1}
nav.main .nav-dd-btn .caret{display:inline-block;width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid currentColor}
nav.main .nav-dd-label:hover,nav.main .nav-dd:hover>.nav-dd-label,nav.main .nav-dd:focus-within>.nav-dd-label,nav.main .nav-dd.is-open>.nav-dd-label,nav.main .nav-dd-label.is-current{color:var(--ink);background:var(--acc)}
nav.main .nav-dd-btn:focus-visible,nav.main a.nav-dd-link:focus-visible{outline:2px solid var(--acc2);outline-offset:2px;z-index:1}
nav.main .nav-dd-panel{display:none;margin:0;padding:8px;list-style:none;background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:0 10px 28px rgba(0,0,0,.45)}
nav.main .nav-dd-panel a{display:block;padding:8px 12px;border-radius:8px;color:var(--txt);text-decoration:none;font-weight:600;white-space:nowrap}
nav.main .nav-dd-panel a:hover,nav.main .nav-dd-panel a:focus-visible,nav.main .nav-dd-panel a[aria-current=page]{color:var(--ink);background:var(--acc)}
.games-page h1{font-size:clamp(1.8rem,5vw,2.5rem);margin:.15em 0 .9em}
.game-icons{display:grid;gap:16px 10px;grid-template-columns:repeat(3,1fr);margin:0 0 48px}
.game-icon{display:flex;flex-direction:column;align-items:center;gap:8px;text-decoration:none;color:var(--txt);text-align:center;min-width:0;padding:2px;border-radius:16px}
.game-icon:hover,.game-icon:focus-visible{color:var(--acc)}
.game-icon:hover .game-icon-art,.game-icon:focus-visible .game-icon-art{border-color:var(--acc);transform:translateY(-2px)}
.game-icon-art{display:block;width:100%;aspect-ratio:1;border-radius:18px;overflow:hidden;background:var(--card);border:1px solid var(--line);transition:transform .15s,border-color .15s}
.game-icon-art img{width:100%;height:100%;object-fit:cover;object-position:center;display:block}
.game-icon-ph{display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--ph,var(--acc)),var(--accd));color:var(--ink);font-weight:800;font-size:clamp(1.1rem,3.4vw,1.55rem);letter-spacing:.04em}
.game-icon-name{font-weight:700;font-size:.82rem;line-height:1.25;max-width:100%;hyphens:auto}
@media(min-width:640px){.game-icons{grid-template-columns:repeat(5,1fr);gap:18px 14px}.game-icon-name{font-size:.85rem}}
@media(min-width:900px){.game-icons{grid-template-columns:repeat(6,1fr)}}
@media(min-width:1100px){.game-icons{grid-template-columns:repeat(8,1fr)}}
/* Mobile: wrap instead of clipping a panel inside overflow-x:auto; panel sits under the whole nav */
@media(max-width:899px){
nav.main{overflow:visible;position:relative}
nav.main>ul{flex-wrap:wrap}
.nav-dd-panel{position:absolute;left:0;right:0;top:100%;z-index:8;margin-top:8px}
.nav-dd.is-open>.nav-dd-panel,.nav-dd:focus-within>.nav-dd-panel{display:block}
}
@media(min-width:900px){
nav.main .nav-dd{position:relative}
nav.main .nav-dd-panel{position:absolute;top:calc(100% + 8px);left:0;min-width:240px;z-index:8}
nav.main .nav-dd:hover>.nav-dd-panel,nav.main .nav-dd:focus-within>.nav-dd-panel,nav.main .nav-dd.is-open>.nav-dd-panel{display:block}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""
def minify_css(c):
    c = re.sub(r"/\*.*?\*/", "", c, flags=re.S); c = re.sub(r"\s+", " ", c)
    c = re.sub(r"\s*([{};,>])\s*", r"\1", c); c = re.sub(r";}", "}", c)
    return c.strip()

JS = r"""(function(){
var dds=[].slice.call(document.querySelectorAll('.nav-dd'));
if(!dds.length)return;
function closeAll(except){dds.forEach(function(dd){if(dd===except)return;var b=dd.querySelector('.nav-dd-btn');if(b)b.setAttribute('aria-expanded','false');dd.classList.remove('is-open');});}
dds.forEach(function(dd){
  var btn=dd.querySelector('.nav-dd-btn');
  if(!btn)return;
  btn.addEventListener('click',function(e){
    e.stopPropagation();
    var open=btn.getAttribute('aria-expanded')==='true';
    closeAll();
    if(!open){btn.setAttribute('aria-expanded','true');dd.classList.add('is-open');}
  });
});
document.addEventListener('click',function(e){if(!e.target.closest('.nav-dd'))closeAll();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeAll();}});
})();
(function(){
document.querySelectorAll('.yt[data-id]').forEach(function(box){var a=box.querySelector('a');if(!a)return;a.addEventListener('click',function(e){e.preventDefault();var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+box.dataset.id+'?autoplay=1&rel=0';f.title=box.dataset.title||'YouTube video';f.allow='accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture';f.allowFullscreen=true;f.loading='lazy';box.innerHTML='';box.appendChild(f);});});
var input=document.getElementById('guide-search');if(!input)return;
var cards=[].slice.call(document.querySelectorAll('.card[data-search]'));var btns=[].slice.call(document.querySelectorAll('.filters button'));var empty=document.querySelector('.empty');var cat='all';
function run(){var q=input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);var shown=0;cards.forEach(function(c){var t=c.dataset.search;var ok=(cat==='all'||c.dataset.cat===cat)&&q.every(function(w){return t.indexOf(w)>-1});c.hidden=!ok;if(ok)shown++;});if(empty)empty.style.display=shown?'none':'block';}
btns.forEach(function(b){b.addEventListener('click',function(){cat=b.dataset.cat;btns.forEach(function(x){x.setAttribute('aria-pressed',x===b)});run();});});
var p=new URLSearchParams(location.search);if(p.get('q'))input.value=p.get('q');input.addEventListener('input',run);run();
})();
(function(){
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var root=document.querySelector('.bg-fx');
if(!root)return;
if(reduce){root.parentNode&&root.parentNode.removeChild(root);return;}
var c=root.querySelector('canvas');
if(!c){c=document.createElement('canvas');root.appendChild(c);}
var ctx=c.getContext('2d',{alpha:true});
if(!ctx){root.parentNode&&root.parentNode.removeChild(root);return;}
var particles=[],running=false,raf=0,dpr=1,w=0,h=0,last=0;
function cap(){return window.innerWidth<640?25:60;}
function spawn(anywhere){
  var amber=Math.random()<0.55;
  return {x:Math.random()*w,y:anywhere?Math.random()*h:h+Math.random()*24,r:1+Math.random()*2,vx:(Math.random()-0.5)*8,vy:-(4+Math.random()*10),a:0.15+Math.random()*0.25,color:amber?'255,176,32':'230,238,245'};
}
function make(){var n=cap(),i;particles=[];for(i=0;i<n;i++)particles.push(spawn(true));}
function resize(){
  dpr=Math.min(window.devicePixelRatio||1,2);
  w=Math.max(1,window.innerWidth);h=Math.max(1,window.innerHeight);
  c.width=Math.floor(w*dpr);c.height=Math.floor(h*dpr);
  c.style.width=w+'px';c.style.height=h+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0);
  if(particles.length!==cap())make();
}
function tick(ts){
  if(!running)return;
  var dt=last?Math.min(0.05,(ts-last)/1000):0.016,i,p;last=ts;
  ctx.clearRect(0,0,w,h);
  for(i=0;i<particles.length;i++){
    p=particles[i];
    p.vx+=(Math.random()-0.5)*2*dt;
    if(p.vx>10)p.vx=10;if(p.vx<-10)p.vx=-10;
    p.x+=p.vx*dt;p.y+=p.vy*dt;
    if(p.y+p.r<0){particles[i]=p=spawn(false);}
    if(p.x<-8)p.x=w+8;else if(p.x>w+8)p.x=-8;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle='rgba('+p.color+','+p.a+')';ctx.fill();
  }
  raf=requestAnimationFrame(tick);
}
function start(){if(running)return;running=true;last=0;raf=requestAnimationFrame(tick);}
function stop(){running=false;last=0;if(raf)cancelAnimationFrame(raf);}
window.addEventListener('resize',resize,{passive:true});
document.addEventListener('visibilitychange',function(){if(document.hidden)stop();else start();});
resize();start();
})();"""

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="t"><title id="t">Fridge logo</title><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffc966"/><stop offset="1" stop-color="#e8890c"/></linearGradient></defs><rect x="12" y="3" width="40" height="58" rx="9" fill="url(#g)"/><rect x="12" y="24" width="40" height="3" fill="#0a0f14"/><rect x="18" y="10" width="4" height="10" rx="2" fill="#0a0f14"/><rect x="18" y="32" width="4" height="14" rx="2" fill="#0a0f14"/><path d="M38 38l3-5 3 5-3 5z" fill="#fff" opacity=".9"/><path d="M33 13l2-3 2 3-2 3z" fill="#fff" opacity=".8"/></svg>"""

GAME_PAGES = {"games.html", "roblox-the-forge.html"}

def nav(active):
    before = [("index.html","Home"),("guides.html","All Guides"),("tag-codes.html","Codes"),("tag-guides.html","Guides")]
    after = [("tag-events.html","Events"),("tag-tips.html","Tips"),("tag-macro.html","Macro"),("about.html","About")]
    def item(h,t):
        return f'<li><a href="{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a></li>'
    games_on = active in GAME_PAGES
    games_cur = ' aria-current="page"' if active=="games.html" else ""
    label_cur = " is-current" if games_on else ""
    all_cur = ' aria-current="page"' if active=="games.html" else ""
    forge_cur = ' aria-current="page"' if active=="roblox-the-forge.html" else ""
    games = (
        '<li class="nav-dd">'
        f'<div class="nav-dd-label{label_cur}">'
        f'<a class="nav-dd-link" href="games.html"{games_cur}>Games</a>'
        '<button type="button" class="nav-dd-btn" aria-expanded="false" aria-controls="nav-games-menu" aria-haspopup="true" aria-label="Games menu"><span class="caret" aria-hidden="true"></span></button>'
        '</div>'
        '<ul id="nav-games-menu" class="nav-dd-panel">'
        f'<li><a href="games.html"{all_cur}>All Games</a></li>'
        f'<li><a href="roblox-the-forge.html"{forge_cur}>The Forge</a></li>'
        '</ul></li>'
    )
    return "".join(item(h,t) for h,t in before) + games + "".join(item(h,t) for h,t in after)

def head(title, desc, path, og_type="website", image=None, image_alt=None, extra_ld=None, prefix=""):
    url = BASE + ("" if path=="index.html" else path)
    image = image or BASE + "assets/og-default.png"
    image_alt = image_alt or "Fridge Roblox guides and codes hub"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",",":"))}</script>' for x in (extra_ld or []))
    return f"""<!doctype html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-54BMLPB9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#ffb020">
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
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6703417075646187" crossorigin="anonymous"></script>
{lds}
</head>
<body>
<div class="bg-fx" aria-hidden="true"><canvas></canvas></div>
<a class="skip" href="#content">Skip to content</a>
"""

def header(active, prefix=""):
    n = nav(active)
    if prefix: n = re.sub(r'href="', f'href="{prefix}', n)
    return f"""<header class="top"><div class="wrap bar">
<a class="brand" href="{prefix}index.html" aria-label="Roblox Guides home"><img src="{prefix}assets/logo.svg" alt="Roblox Guides logo" width="34" height="34"><span><b>Roblox</b> Guides</span></a>
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
<div><h2>Fridge</h2><p>Roblox codes, guides and event coverage from the Fridge YouTube channel. Guides are updated with new videos and re-checked for accuracy.</p><p><a class="btn yt-sub" href="{SUB}" rel="noopener" target="_blank">Subscribe on YouTube</a></p></div>
<div><h2>Latest guides</h2><ul>{latest}</ul></div>
<div><h2>Categories</h2><ul>{cats}<li><a href="{prefix}games.html">Games</a></li><li><a href="{prefix}about.html">About Fridge</a></li><li><a href="{prefix}sitemap.xml">Sitemap</a></li></ul></div>
</div><div class="wrap legal">
<p class="legal-nav"><a href="{prefix}privacy-policy.html">Privacy Policy</a><a href="{prefix}terms.html">Terms of Use</a><a href="{prefix}contact.html">Contact</a><a href="{prefix}about.html">About</a></p>
<p class="small">Site email: {email_link()}</p>
<p class="small disclosure"><strong>Disclosure:</strong> This site may display advertisements, including ads served by Google. Links to third-party tools such as ExoPanda are provided for context and are not sponsored unless a page says otherwise. We are not affiliated with those vendors or with Roblox Corporation.</p>
<p class="small">If you are in the EEA, the UK or Switzerland, Google requires a Google-certified consent management platform before personalized ads can be shown. We have not added an unofficial cookie banner. After AdSense approval, the operator intends to enable Google's Privacy &amp; messaging GDPR (and applicable US state) messages. See the <a href="{prefix}privacy-policy.html">Privacy Policy</a> for cookies, ads and your choices.</p>
<p class="small">© 2026 Fridge (@Fridgetherealone). Not affiliated with Roblox Corporation or any game developer. Game names belong to their owners.</p>
</div></footer>
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
        el={"@type":"ListItem","position":i+1,"name":n}
        if p:
            el["item"] = BASE if p=="index.html" else BASE+p
        els.append(el)
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":els}
def bc_html(items):
    li=[]
    for i,(n,p) in enumerate(items):
        if i < len(items)-1:
            li.append(f'<li><a href="{p}">{esc(n)}</a></li>' if p else f'<li>{esc(n)}</li>')
        else: li.append(f'<li aria-current="page">{esc(n)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(li)}</ol></nav>'

def thumb(vid): return f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
def g_img(g, absolute=False):
    if g.get("cover"): return (BASE if absolute else "") + g["cover"]
    if g["videos"]: return thumb(g["videos"][0][0])
    if g.get("shorts"): return thumb(g["shorts"][0][0])
    return (BASE if absolute else "") + f"assets/thumbs/{g['slug']}.png"
def g_img_alt(g):
    if g.get("image_alt"): return g["image_alt"]
    if g["videos"]: return f"{g['game']} guide thumbnail: {g['videos'][0][1]}"
    if g.get("shorts"): return f"{g['game']} guide thumbnail from Fridge's Short: {g['shorts'][0][1]}"
    return f"Fridge guide cover image: {g['h1']}"
PLACEHOLDER = """<!-- YOUTUBE EMBED PLACEHOLDER: no matching Fridge video yet.
     When a video exists, add ("VIDEO_ID", "Video title") to this guide's videos=[...] list in _build/g/
     and replace {VIDEO_PLACEHOLDER} in the body with {VIDEO0}, then run python3 _build/build.py.
     Raw HTML alternative: copy any <div class="yt" data-id="VIDEO_ID_HERE"> block from another guide. -->
<p class="small"><strong>No matching Fridge video yet.</strong> The written guide above is complete on its own. <a class="yt-sub" href="https://www.youtube.com/@Fridgetherealone?sub_confirmation=1" rel="noopener" target="_blank">Subscribe on YouTube</a> if you want to catch a video version later.</p>
<!-- /YOUTUBE EMBED PLACEHOLDER -->"""

SHORT_PLACEHOLDER = """<!-- YOUTUBE SHORTS EMBED SLOT (9:16): no matching Fridge Short yet.
     When the Short is live, replace the inner <div class="short-ph"> with:
     <iframe src="https://www.youtube-nocookie.com/embed/SHORT_ID_HERE" title="Fridge YouTube Short" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
     (SHORT_ID_HERE = the 11-character ID from youtube.com/shorts/SHORT_ID_HERE). -->
<!-- Short placeholder hidden until a real Short ID is added to this guide. -->
<!-- /YOUTUBE SHORTS EMBED SLOT -->"""

def card(g, lvl="h3"):
    cat = g["cat"]
    search = " ".join([g["title"], g["h1"], g["desc"], g["game"], cat, g["kw_primary"], " ".join(g["kw_secondary"])]).lower()
    return f"""<article class="card" data-cat="{cat}" data-search="{esc(search)}">
<a class="thumb" href="{g['slug']}.html" tabindex="-1" aria-hidden="true"><img src="{g_img(g)}" alt="{esc(g_img_alt(g))}" loading="lazy" width="480" height="270"></a>
<div class="bd"><div class="meta"><a class="tag" href="{CATS[cat][0]}">{cat}</a><time datetime="{g['date']}">{human(g['date'])}</time></div>
<{lvl}><a href="{g['slug']}.html">{esc(g['h1'])}</a></{lvl}>
<p>{esc(g['desc'])}</p><a class="more" href="{g['slug']}.html" aria-label="Read: {esc(g['h1'])}">Read guide →</a></div></article>"""

def video_embed(vid, title, game, poster=None):
    src = poster or thumb(vid)
    # 16:9 posters (local maxres) use 480x270; YouTube hqdefault is 4:3 480x360
    wh = (480, 270) if poster else (480, 360)
    return f"""<!-- YOUTUBE EMBED: Fridge video "{esc(title)}" (ID {vid}).
     To swap in a different video, replace the 11-character ID in ALL THREE places below
     (data-id, the watch?v= link and the thumbnail URL). Placeholder for a new video: VIDEO_ID_HERE -->
<div class="yt" data-id="{vid}" data-title="{esc(title)}">
<a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener" aria-label="Play video: {esc(title)}"><img src="{src}" alt="Fridge YouTube video thumbnail: {esc(title)} ({esc(game)})" loading="lazy" width="{wh[0]}" height="{wh[1]}"><span class="yt-play" aria-hidden="true"></span></a>
</div>
<!-- /YOUTUBE EMBED -->"""

def short_embed(vid, title, date=None):
    d = f" · {human(date)}" if date else ""
    return f"""<!-- YOUTUBE SHORT EMBED (vertical 9:16): Fridge Short "{esc(title)}" (ID {vid}). To swap it, replace the ID in the iframe src and the link. -->
<figure class="short-slot"><iframe src="https://www.youtube-nocookie.com/embed/{vid}?rel=0" title="Fridge YouTube Short: {esc(title)}" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe><figcaption class="small"><a href="https://www.youtube.com/shorts/{vid}" rel="noopener" target="_blank">{esc(title)}</a>{d}</figcaption></figure>"""

def write(path, s):
    with open(os.path.join(OUT, path), "w") as f: f.write(s)

ORG = {"@type":"Organization","name":"Fridge","url":BASE,"logo":BASE+"assets/apple-touch-icon.png","sameAs":[YT]}
PERSON = {"@type":"Person","name":"Fridge","url":BASE+"about.html","sameAs":[YT]}

def page(path, title, desc, crumbs_items, body, active=None, og_type="website", image=None, image_alt=None, ld=None):
    ld = (ld or []) + [bc_ld(crumbs_items)]
    return head(title, desc, path, og_type, image, image_alt, ld) + header(active or path) + body.replace("{CRUMBS}", bc_html(crumbs_items)) + footer()

# working-code counts per codes page (from each page's verified table); None = game has no code system
CODE_COUNTS = {"steal-an-egg-codes":None,"blox-fruits-codes":24,"rivals-codes":8,"99-nights-in-the-forest-codes":3,"jujutsu-shenanigans-codes":2,
 "murder-mystery-2-codes":0,"adopt-me-codes":0,"brookhaven-codes":None,"throw-food-for-animals-codes":None,"break-and-steal-an-egg-codes":None,
 "anime-adventures-codes":5,"forsaken-codes":None,"dandys-world-codes":2,"fisch-codes":2,"survive-your-ideas-codes":4,"fish-it-codes":3,
 "violence-district-codes":None,"dont-splash-codes":0,"steal-a-brainrot-codes":1,"catalog-avatar-creator-codes":0,"the-strongest-battlegrounds-codes":None,
 "anime-dice-codes":24,"huzz-valley-codes":4}
def codes_table():
    for x in guides:
        if "code_count" in x: CODE_COUNTS[x["slug"]] = x["code_count"]
    rows=[]
    for x in sorted([x for x in guides if x["cat"]=="Codes" and x["slug"] in CODE_COUNTS], key=lambda x:(CODE_COUNTS[x["slug"]] is None, -(CODE_COUNTS[x["slug"]] or 0), x["game"].lower())):
        c=CODE_COUNTS[x["slug"]]
        cnt = "No code system" if c is None else (f"{c} working" if c else "0 confirmed right now")
        rows.append(f'<tr><td>{esc(x["game"])}</td><td>{cnt}</td><td><a href="{x["slug"]}.html">{esc(x["game"])} codes</a></td></tr>')
    return '<div class="table-wrap"><table><caption>Every Fridge codes page, sorted by working codes (checked '+MOD_HUMAN+')</caption><thead><tr><th scope="col">Game</th><th scope="col">Working codes</th><th scope="col">Page</th></tr></thead><tbody>'+"".join(rows)+'</tbody></table></div>'
report = []
# ---------- guide pages ----------
for g in guides:
    body = g["body"]
    for i,v in enumerate(g["videos"]):
        body = body.replace("{VIDEO%d}"%i, video_embed(v[0],v[1],g["game"], poster=(g["cover"] if i==0 and g.get("cover") else None)))
    sh = g.get("shorts", [])
    for i,v in enumerate(sh):
        body = body.replace("{SHORT%d}"%i, short_embed(v[0],v[1],v[2] if len(v)>2 else None))
    if "{SHORTS}" in body:
        body = body.replace("{SHORTS}", '<div class="shorts-grid">' + "".join(short_embed(v[0],v[1],v[2] if len(v)>2 else None) for v in sh) + '</div>')
    body = body.replace("{VIDEO_PLACEHOLDER}", PLACEHOLDER)
    body = body.replace("{SHORT_PLACEHOLDER}", SHORT_PLACEHOLDER)
    if "{CODES_TABLE}" in body: body = body.replace("{CODES_TABLE}", codes_table())
    if g.get("chapters"):
        ch = "".join(f'<li><span class="ts">{esc(ts)}</span> <a href="#{an}">{esc(t)}</a></li>' for ts,t,an in g["chapters"])
        body = body.replace("{CHAPTERS}", f"""<!-- VIDEO CHAPTERS: suggested YouTube chapter timestamps for the matching Fridge video. Each chapter maps to the linked section below; paste them into the video description as "0:00 Title" lines. -->
<section class="chapters" aria-labelledby="chap-h"><h2 id="chap-h">Video Chapters</h2><p class="small">Planned segments for the matching Fridge video. Each one jumps to the section it covers, so you can read along or skip ahead.</p><ol>{ch}</ol></section>""")
    body = body.replace("{CHAPTERS}", "")
    h2s = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    toc = "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>","",t)}</a></li>' for i,t in h2s) + '<li><a href="#faq">FAQ</a></li>'
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q,a in g["faq"])
    rel = [BY[s] for s in g["related"] if s in BY][:3]
    sources_html = ""
    if g.get("sources"):
        sources_html = '<section class="side-box" aria-labelledby="src-h" style="margin-top:28px"><h2 id="src-h" style="margin-top:0">Sources</h2><ul>' + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{esc(n)}</a></li>' for n,u in g["sources"]) + '</ul></section>'
    rel_html = "".join(card(r) for r in rel)
    catp, catn, _ = CATS[g["cat"]]
    items = [("Home","index.html"),(catn,catp),(g["h1"].split(":")[0], g["slug"]+".html")]
    url = BASE + g["slug"] + ".html"
    vids_ld = [{"@type":"VideoObject","name":v[1],"embedUrl":f"https://www.youtube.com/embed/{v[0]}","contentUrl":f"https://www.youtube.com/watch?v={v[0]}","thumbnailUrl":(g_img(g, True) if i==0 and g.get("cover") else thumb(v[0])),"uploadDate":(v[2] if len(v)>2 else g["date"]),"description":f"Fridge's Roblox video: {v[1]}"} for i,v in enumerate(g["videos"]) if len(v)<3 or v[2]] + \
              [{"@type":"VideoObject","name":v[1],"embedUrl":f"https://www.youtube.com/embed/{v[0]}","contentUrl":f"https://www.youtube.com/shorts/{v[0]}","thumbnailUrl":thumb(v[0]),"uploadDate":v[2],"description":f"Fridge's Roblox YouTube Short: {v[1]}"} for v in g.get("shorts",[]) if len(v)>2 and v[2]]
    ld_post = {"@context":"https://schema.org","@type":"BlogPosting","headline":g["h1"],"description":g["desc"],"image":[g_img(g, True)],
      "datePublished":g["date"],"dateModified":TODAY,"author":PERSON,"publisher":ORG,"mainEntityOfPage":{"@type":"WebPage","@id":url},
      "articleSection":g["cat"],"keywords":", ".join([g["kw_primary"]]+g["kw_secondary"]),"about":{"@type":"VideoGame","name":g["game"],"gamePlatform":"Roblox"},
      **({} if not vids_ld else {"video":vids_ld})}
    ld_faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in g["faq"]]}
    lds_extra = [ld_post, ld_faq]
    if g.get("howto"):
        hn, steps = g["howto"]
        lds_extra.append({"@context":"https://schema.org","@type":"HowTo","name":hn,"description":g["desc"],"image":g_img(g, True),
          "step":[{"@type":"HowToStep","position":i+1,"name":n,"text":t,"url":url+"#"+a} for i,(n,t,a) in enumerate(steps)]})
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
<p class="callout">Found this helpful? <a class="yt-sub" href="{SUB}" rel="noopener" target="_blank">Subscribe to Fridge on YouTube</a> for new {esc(g['game'])} videos. {"This guide is updated with every new upload." if (g["videos"] or g.get("shorts")) else "This guide is re-checked against official Roblox sources when things change."}</p>
</article>
<aside>
<nav class="toc" aria-label="Table of contents"><strong>On this page</strong><ol>{toc}</ol></nav>
<div class="side-box"><strong>More {esc(g['cat'])}</strong><ul>{''.join(f'<li><a href="{x["slug"]}.html">{esc(x["h1"].split(":")[0])}</a></li>' for x in guides if x["cat"]==g["cat"] and x is not g)}</ul><a href="{catp}">See all {g['cat'].lower()} →</a></div>
</aside>
</div>
<section class="related" aria-labelledby="rel-h"><div class="sec-h"><h2 id="rel-h">Related Guides</h2><a href="guides.html">All guides →</a></div><div class="grid">{rel_html}</div></section>
</div>"""
    write(g["slug"]+".html", page(g["slug"]+".html", g["title"], g["desc"], items, content, active="guides.html", og_type="article",
        image=g_img(g, True), image_alt=g_img_alt(g), ld=lds_extra))
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
NEW_EVENT = "roblox-christmas-event-2026-leak"
feat_guides = ([BY[NEW_EVENT]] if NEW_EVENT in BY else []) + [g for g in guides if g["slug"] != NEW_EVENT]
feat = "".join(card(g) for g in feat_guides[:6])
game_feat = "".join(card(g) for g in [x for x in guides if x["videos"] and x["game"]!="The Forge"][:6])
FORGE = [x["slug"] for x in sorted([x for x in guides if x["game"]=="The Forge"], key=lambda x:x.get("forge_order",99))]
TOP10_CODES = ["steal-an-egg-codes","murder-mystery-2-codes","brookhaven-codes","throw-food-for-animals-codes","blox-fruits-codes","99-nights-in-the-forest-codes","rivals-codes","adopt-me-codes","break-and-steal-an-egg-codes","jujutsu-shenanigans-codes"]
HOWTO_NEW = ["how-to-turn-on-voice-chat-roblox","add-trusted-friends-roblox","how-to-appear-offline-roblox","roblox-parental-controls-guide","redeem-roblox-gift-card","check-roblox-account-status","equip-multiple-accessories-roblox","how-to-emote-roblox","throw-food-for-animals-guide","99-nights-in-the-forest-guide"]
MORE_CODES = ["anime-adventures-codes","forsaken-codes","dandys-world-codes","fisch-codes","survive-your-ideas-codes","fish-it-codes","violence-district-codes","dont-splash-codes","steal-a-brainrot-codes","catalog-avatar-creator-codes","the-strongest-battlegrounds-codes"]
top_feat = "".join(card(BY[s]) for s in TOP10_CODES)
more_feat = "".join(card(BY[s]) for s in MORE_CODES)
howto_feat = "".join(card(BY[s]) for s in HOWTO_NEW)
GENERAL_NEW = ["roblox-codes-november-2026","how-to-get-free-items-in-roblox","how-to-level-up-fast-in-roblox","best-roblox-pets-2026","roblox-avatar-ideas","how-to-report-a-player-on-roblox","roblox-gift-card-guide","how-to-join-a-roblox-group","roblox-age-verification","how-to-change-roblox-username"]
general_feat = "".join(card(BY[s]) for s in GENERAL_NEW)
NEW_CODES = ["the-forge-codes","dress-to-impress-codes","king-legacy-codes","arise-crossover-codes","blade-ball-codes","bee-swarm-simulator-codes","anime-vanguards-codes","volleyball-legends-codes","grow-a-garden-codes","basketball-zero-codes","driving-empire-codes"]
newcodes_feat = "".join(card(BY[s]) for s in NEW_CODES if s in BY)
MACRO = ["what-is-a-roblox-macro","best-roblox-macros","roblox-auto-clicker","grow-a-garden-macro","fisch-macro","bee-swarm-simulator-macro","roblox-macros-windows-mac"]
macro_feat = "".join(card(BY[s]) for s in MACRO if s in BY)
help_feat = "".join(card(g) for g in [x for x in guides if not x["videos"] and x["slug"] not in TOP10_CODES+HOWTO_NEW+MORE_CODES+GENERAL_NEW+NEW_CODES+FORGE+MACRO][:4])
cats_html = "".join(f'<a href="{v[0]}">{v[1]}<small>{sum(1 for g in guides if g["cat"]==k)} guides</small></a>' for k,v in CATS.items())
idx_ld = [{"@context":"https://schema.org","@type":"WebSite","name":"Roblox Guides","url":BASE,"potentialAction":{"@type":"SearchAction","target":BASE+"guides.html?q={search_term_string}","query-input":"required name=search_term_string"}},
          dict({"@context":"https://schema.org"}, **ORG)]
idx_body = f"""<section class="hero"><div class="wrap">{{CRUMBS}}
<p class="tag">Roblox codes · guides · events</p>
<h1>Roblox Codes &amp; Guides by <b>Fridge</b></h1>
<p>Working Roblox codes for the top 10 games, beginner guides and event walkthroughs for Steal an Egg, Blox Fruits, RIVALS, Scrooms, Anime Dice and more, plus how-tos for voice chat, Trusted Friends and parental controls. Game guides match Fridge's YouTube videos, and evergreen Roblox help guides cover FPS, lag, Bloxstrap and account safety.</p>
<a class="btn" href="guides.html">Browse all guides</a><a class="btn yt-sub" href="{SUB}" rel="noopener" target="_blank">Subscribe on YouTube</a>
</div></section>
<div class="wrap">
<section aria-labelledby="latest-h"><div class="sec-h"><h2 id="latest-h">Latest Roblox Guides</h2><a href="guides.html">View all →</a></div><div class="grid">{feat}</div></section>
<section aria-labelledby="macro-h"><div class="sec-h"><h2 id="macro-h">Roblox Macro Guides</h2><a href="tag-macro.html">All macro guides →</a></div><p class="small">What a Roblox macro is, whether macros can get you banned, auto clicker setup, TinyTask and Mac tools, and game-specific notes for Grow a Garden, Fisch and Bee Swarm Simulator. Every page includes a Terms of Use and malware warning. Fridge is not affiliated with any macro vendor.</p><div class="grid">{macro_feat}</div></section>
<section aria-labelledby="game-h"><div class="sec-h"><h2 id="game-h">Latest Game Codes &amp; Guides</h2><a href="tag-codes.html">All codes →</a></div><div class="grid">{game_feat}</div></section>
<section aria-labelledby="gen-h"><div class="sec-h"><h2 id="gen-h">Essential Roblox Guides</h2><a href="guides.html">All guides →</a></div><p class="small">Every Roblox code in one hub, plus free items, leveling, pets, avatar ideas, reporting, gift cards, Communities, age checks and username changes. Checked against official Roblox pages on November 11, 2026.</p><div class="grid">{general_feat}</div></section>
<section aria-labelledby="top-h"><div class="sec-h"><h2 id="top-h">Codes for the Top 10 Roblox Games</h2><a href="tag-codes.html">All codes →</a></div><p class="small">The ten most-played Roblox games by live player count on November 11, 2026, with every working code checked against at least two sources. Games without a code system say so.</p><div class="grid">{top_feat}</div></section>
<section aria-labelledby="more-h"><div class="sec-h"><h2 id="more-h">More Roblox Game Codes</h2><a href="tag-codes.html">All codes →</a></div><p class="small">The next most-played Roblox games (ranks 11–20 by live players on November 11, 2026, plus Anime Adventures), each checked against at least two sources. Games with no codes say so.</p><div class="grid">{more_feat}</div></section>
<section aria-labelledby="nc-h"><div class="sec-h"><h2 id="nc-h">New Codes: The Forge, Dress To Impress and More</h2><a href="roblox-codes-november-2026.html">Codes hub →</a></div><p class="small">More high-traffic Roblox games with active codes, including The Forge, Dress To Impress and King Legacy, each checked against at least two sources on November 11, 2026.</p><div class="grid">{newcodes_feat}</div></section>
<section aria-labelledby="howto-h"><div class="sec-h"><h2 id="howto-h">New Roblox How-To Guides</h2><a href="tag-guides.html">All guides →</a></div><div class="grid">{howto_feat}</div></section>
<section aria-labelledby="cat-h"><h2 id="cat-h">Browse by Category</h2><div class="cats">{cats_html}</div></section>
<section class="intro" aria-labelledby="ch-h"><div><h2 id="ch-h">Welcome to the Fridge Content Hub</h2>
<p>Fridge is a Roblox YouTube channel focused on fast, no-nonsense guides: the newest codes, the quickest ways to level up, and full walkthroughs for big events like the Roblox Hollow. This site is the written companion to the channel, so you can copy codes, check tables and skim steps without scrubbing through a video.</p>
<p>Start with the <a href="steal-an-egg-speed-guide.html">Steal an Egg speed guide</a>, the <a href="scrooms-beginners-guide.html">Scrooms beginner's guide</a> or the latest <a href="anime-dice-codes.html">Anime Dice codes</a>.</p></div>
<div><a class="btn" href="{YT}/videos" rel="noopener" target="_blank">Watch Fridge's videos</a><a class="btn ghost" href="about.html">About Fridge</a></div></section>
<section aria-labelledby="pop-h"><h2 id="pop-h">Popular Right Now</h2><div class="grid">{"".join(card(BY[s]) for s in ["steal-an-egg-codes","blox-fruits-codes","throw-food-for-animals-guide"])}</div></section>
<section aria-labelledby="help-h"><h2 id="help-h">More Roblox Help Guides</h2><div class="grid">{help_feat}</div></section>
</div>"""
write("index.html", page("index.html", "Fridge – Roblox Codes & Guides Hub (November 2026)",
 "Fridge's Roblox hub: working codes for the top 10 games, Steal an Egg and Scrooms guides, plus voice chat, Trusted Friends and parental control help. Dive in!",
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
 "Events": ("Roblox Event Guides 2026 – Hollow & Christmas Leak | Fridge", "Roblox event guides for 2026: the Slippers Christmas leak, the Hollow recap, and Steal an Egg Halloween Dimension guides. See what is confirmed!"),
 "Tips": ("Roblox Tips: Speed, XP & Racing Tricks | Fridge", "Quick Roblox tips from Fridge: how to get speed in Steal an Egg, level up fast in Scrooms, and win every race. Use these tricks to progress faster today!"),
 "Macro": ("Roblox Macros: Ban Risk, Auto Clickers & Guides | Fridge", "Roblox macro guides: ban risk, auto clickers, Grow a Garden, Fisch and Bee Swarm, plus TinyTask and Mac tools. Read the Terms of Use warning first!"),
}
for k,(p,n,intro) in CATS.items():
    gs = [g for g in guides if g["cat"]==k]
    t, d = TAGMETA[k]
    ld = [{"@context":"https://schema.org","@type":"CollectionPage","name":n,"description":d,"url":BASE+p,"mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+g["slug"]+".html","name":g["h1"]} for i,g in enumerate(gs)]}}]
    others = " · ".join(f'<a href="{v[0]}">{v[1]}</a>' for kk,v in CATS.items() if kk!=k)
    extra = ""
    if k == "Macro":
        from macrolib import DISCLAIMER, MALWARE
        extra = DISCLAIMER + MALWARE
    b = f"""<div class="wrap">{{CRUMBS}}
<h1>{n} by Fridge</h1>
<p class="updated"><strong>Last updated: <time datetime="{TODAY}">{MOD_HUMAN}</time></strong> · {len(gs)} guides</p>
<p>{intro}</p>
{extra}
<div class="grid">{"".join(card(g,"h2") for g in gs)}</div>
<p style="margin-top:28px">More categories: {others} · <a href="guides.html">All guides</a></p>
</div>"""
    write(p, page(p, t, d, [("Home","index.html"),(n,p)], b, active=p, ld=ld))

# Lightweight redirect so old /tag-the-forge.html links do not 404. Excluded from the sitemap.
write("tag-the-forge.html", f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Forge Guides moved | Fridge</title>
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{BASE}tag-guides.html">
<meta http-equiv="refresh" content="0;url=tag-guides.html">
</head>
<body>
<p>The Forge guides now live under <a href="tag-guides.html">Roblox Guides</a>. The Forge codes are under <a href="tag-codes.html">Roblox Codes</a> and in the <a href="roblox-codes-november-2026.html">codes hub</a>.</p>
</body>
</html>
""")

# ---------- Games index ----------
# Attach a few platform-tagged pages to the game they actually cover.
GAME_PAGE_ALIASES = {
    "grow-a-garden-macro": "Grow a Garden",
    "fisch-macro": "Fisch",
    "bee-swarm-simulator-macro": "Bee Swarm Simulator",
}
# The Forge is pinned first on the icon grid; remaining titles follow this
# coverage-first order, then the rest alphabetically.
GAME_ORDER = [
    "The Forge",
    "Steal an Egg",
    "Scrooms",
    "Anime Dice",
    "The Hollow",
    "+1 Speed Monkey Escape",
    "99 Nights in the Forest",
    "Throw Food For Animals",
]
GAME_HUBS = {
    "The Forge": "roblox-the-forge.html",
    "Steal an Egg": "steal-an-egg-codes.html",
    "Scrooms": "scrooms-beginners-guide.html",
    "Anime Dice": "anime-dice-codes.html",
    "The Hollow": "roblox-hollow-event-guide.html",
    "+1 Speed Monkey Escape": "monkey-escape-sunken-shards.html",
    "99 Nights in the Forest": "99-nights-in-the-forest-guide.html",
    "Throw Food For Animals": "throw-food-for-animals-guide.html",
}
_GAME_ICON_COLORS = ("#ffb020","#e8890c","#5b8def","#3dbe8c","#e36b6b","#b07cff","#f08ab8","#4ecdc4")

def _game_name_for(g):
    return GAME_PAGE_ALIASES.get(g["slug"], g["game"])

def _game_initials(name):
    words = re.findall(r"[A-Za-z0-9]+", name.replace("'", ""))
    small = {"the", "a", "an", "and", "of", "in", "for"}
    main = [w for w in words if w.lower() not in small] or words
    if len(main) == 1:
        if words and words[0].lower() in small:
            return (words[0][0] + main[0][0]).upper()
        w = main[0]
        return (w if w.isdigit() else w[:2]).upper()
    parts = []
    if words and words[0].lower() == "the" and len(main) >= 2:
        parts.append("T")
    for w in main:
        parts.append(w if w.isdigit() else w[0].upper())
        if sum(len(p) for p in parts) >= 3 and len(parts) >= 2:
            break
    return "".join(parts)[:4]

def _game_icon_color(name):
    return _GAME_ICON_COLORS[sum(map(ord, name)) % len(_GAME_ICON_COLORS)]

def _pick_hub(name, pages):
    if name in GAME_HUBS:
        return GAME_HUBS[name]
    for g in pages:
        if "beginners" in g["slug"]:
            return g["slug"] + ".html"
    for g in pages:
        if g["cat"] not in ("Codes", "Macro") and g["slug"].endswith("-guide"):
            return g["slug"] + ".html"
    for g in pages:
        if g["cat"] == "Codes":
            return g["slug"] + ".html"
    return pages[0]["slug"] + ".html"

def _yt_icon(vid):
    # mqdefault is 16:9, so a center square crop avoids hqdefault letterbox bars.
    return f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg"

def _is_generated_cover(g, rel):
    # 16:9 typography covers crop badly as square icons; skip them.
    slug_png = f"assets/thumbs/{g['slug']}.png"
    cover = (g.get("cover") or "").lstrip("/")
    return rel == slug_png or cover.endswith(f"thumbs/{g['slug']}.png")

def _game_image(pages, hub_path):
    # Prefer a real video thumb (crops cleanly to a square icon). Skip the
    # auto-generated 16:9 title cards; those become initials fallbacks.
    hub_slug = hub_path.replace(".html", "")
    ordered = [g for g in pages if g["slug"] == hub_slug] + [g for g in pages if g["slug"] != hub_slug]
    for g in ordered:
        if g.get("videos"):
            return _yt_icon(g["videos"][0][0]), g_img_alt(g)
        if g.get("shorts"):
            return _yt_icon(g["shorts"][0][0]), g_img_alt(g)
    for g in ordered:
        if g.get("cover"):
            rel = g["cover"].lstrip("/")
            if not _is_generated_cover(g, rel) and os.path.exists(os.path.join(OUT, rel)):
                return rel, g_img_alt(g)
        for ext in (".png", ".webp"):
            rel = f"assets/thumbs/{g['slug']}{ext}"
            if os.path.exists(os.path.join(OUT, rel)) and not _is_generated_cover(g, rel):
                return rel, g_img_alt(g)
    return None, None

def _build_game_catalog():
    by = {}
    for g in guides:
        name = _game_name_for(g)
        if name == "Roblox":
            continue
        by.setdefault(name, []).append(g)
    catalog = []
    for name, pages in by.items():
        pages = sorted(pages, key=lambda x: (0 if x["cat"] != "Codes" else 1, x.get("date", ""), x["slug"]))
        hub = _pick_hub(name, pages)
        img, img_alt = _game_image(pages, hub)
        catalog.append({
            "name": name,
            "hub": hub,
            "img": img,
            "img_alt": img_alt or f"{name} icon",
            "initials": _game_initials(name),
            "color": _game_icon_color(name),
        })
    pin = {n: i for i, n in enumerate(GAME_ORDER)}
    catalog.sort(key=lambda x: (0, pin[x["name"]]) if x["name"] in pin else (1, x["name"].lower()))
    return catalog

def game_icon(item):
    name = esc(item["name"])
    if item["img"]:
        art = (
            f'<span class="game-icon-art">'
            f'<img src="{esc(item["img"])}" alt="" width="256" height="256" loading="lazy">'
            f"</span>"
        )
    else:
        art = (
            f'<span class="game-icon-art game-icon-ph" style="--ph:{item["color"]}" aria-hidden="true">'
            f'{esc(item["initials"])}</span>'
        )
    return f'<a class="game-icon" href="{item["hub"]}" title="{name}">{art}<span class="game-icon-name">{name}</span></a>'

_all_games = _build_game_catalog()
_games_title = "Games | Roblox Guides and Codes"
_games_desc = "Browse Roblox games on Roblox Guides: The Forge, Steal an Egg, Scrooms, Anime Dice and more, with codes and walkthroughs one click away. Pick a game!"
_games_ld = [
    {"@context":"https://schema.org","@type":"CollectionPage","name":"Games","url":BASE+"games.html","description":_games_desc,"dateModified":TODAY,"publisher":ORG,
     "mainEntity":{"@type":"ItemList","numberOfItems":len(_all_games),"itemListElement":[
         {"@type":"ListItem","position":i+1,"name":it["name"],"url":BASE+it["hub"]} for i,it in enumerate(_all_games)
     ]}},
]
_games_og = BASE + "assets/thumbs/the-forge-races-guide.png"
_icon_grid = "".join(game_icon(it) for it in _all_games)
_games_body = (
    '<div class="wrap games-page">{CRUMBS}'
    "<h1>Games</h1>"
    f'<div class="game-icons">{_icon_grid}</div>'
    "</div>"
)
write("games.html", page(
    "games.html",
    _games_title,
    _games_desc,
    [("Home","index.html"),("Games","games.html")],
    _games_body,
    active="games.html",
    image=_games_og,
    image_alt="Roblox game guides and codes on Roblox Guides",
    ld=_games_ld,
))

# ---------- Games placeholder hubs ----------
_forge_hub_desc = "Find Roblox The Forge codes and existing walkthroughs on Roblox Guides. This game hub is a placeholder while we build it out. Open the pages now!"
_forge_cards = []
for _slug in ("the-forge-codes", "the-forge-beginners-guide", "the-forge-forging-guide", "the-forge-races-guide"):
    if _slug not in BY:
        raise SystemExit(f"missing forge guide {_slug}")
    _forge_cards.append(card(BY[_slug], "h2"))
_guides_card = """<article class="card">
<div class="bd"><div class="meta"><span class="tag">Guides</span></div>
<h2><a href="tag-guides.html">All Guides (including The Forge)</a></h2>
<p>Open the Guides category for The Forge walkthroughs already on the site, plus other Roblox game guides.</p>
<a class="more" href="tag-guides.html">Browse Guides →</a></div></article>"""
_forge_body = f"""<div class="wrap">{{CRUMBS}}
<article>
<h1>Roblox The Forge</h1>
<p class="updated"><strong>Last updated: <time datetime="{TODAY}">{MOD_HUMAN}</time></strong></p>
<p>This is a placeholder game hub for Roblox The Forge, a game already covered on Roblox Guides with codes and walkthroughs. Use it to jump to those existing pages from the new Games menu.</p>
<p><strong>Game hub coming soon.</strong> A fuller hub will live here later. For now, start with The Forge codes, the Guides category, and a few walkthroughs already on the site.</p>
<div class="grid">{_guides_card}{''.join(_forge_cards)}</div>
</article>
</div>"""
write("roblox-the-forge.html", page(
    "roblox-the-forge.html",
    "Roblox The Forge Hub | Codes and Guides",
    _forge_hub_desc,
    [("Home","index.html"),("Games","games.html"),("Roblox The Forge","roblox-the-forge.html")],
    _forge_body,
    active="roblox-the-forge.html",
    ld=[{"@context":"https://schema.org","@type":"WebPage","name":"Roblox The Forge","url":BASE+"roblox-the-forge.html","dateModified":TODAY,"publisher":ORG}],
))

# ---------- about / legal ----------
from legalpages import privacy_body, terms_body, contact_body, about_body

def write_legal(path, title, desc, crumb, body, page_type="WebPage"):
    ld = [{"@context":"https://schema.org","@type":page_type,"name":title.split("|")[0].strip(),"url":BASE+path,"dateModified":TODAY,"publisher":ORG}]
    write(path, page(path, title, desc, [("Home","index.html"),(crumb,path)], body, active="about.html" if path=="about.html" else path, ld=ld))

ab_ld_name = "About Roblox Guides and Fridge"
write_legal("about.html",
    "About Roblox Guides and Fridge | Official Site",
    "Meet Roblox Guides and Fridge (@Fridgetherealone): who runs the site, how we verify codes with a two-source rule, and how often pages are updated. Read it!",
    "About", about_body(), page_type="AboutPage")
write_legal("privacy-policy.html",
    "Privacy Policy | Roblox Guides",
    "How Roblox Guides handles logs, YouTube embeds, cookies and ads, including Google AdSense disclosures, COPPA, GDPR and CCPA rights. Read the policy!",
    "Privacy Policy", privacy_body())
write_legal("terms.html",
    "Terms of Use | Roblox Guides",
    "Terms of Use for Roblox Guides: informational content, editorial rules, third-party links, ads, and unofficial-tool disclaimers. Read the terms today!",
    "Terms of Use", terms_body())
write_legal("contact.html",
    "Contact Roblox Guides | Fridge on YouTube",
    "Contact Roblox Guides through the Fridge YouTube channel. Use it for corrections, privacy requests or feedback — no personal email is published here. Reach out!",
    "Contact", contact_body())

# ---------- 404 (absolute paths so it works at any depth) ----------
P = "/"
nf = head("Page Not Found (404) | Fridge Roblox Guides", "This page doesn't exist or has moved. Search Fridge's Roblox guides or jump to the latest codes for Steal an Egg, Anime Dice and Huzz Valley right here.", "404.html", prefix=P, extra_ld=[bc_ld([("Home","index.html"),("Page not found","404.html")])])
nf = nf.replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex,follow">')
nf += header("", prefix=P) + f"""<div class="wrap">{bc_html([("Home",P+"index.html"),("Page not found","")])}
<section class="notfound"><h1>404</h1><h2>This page melted.</h2><p>The guide you're looking for doesn't exist or has moved. Try a search or pick a popular guide below.</p>
<form action="{P}guides.html" method="get" role="search" class="searchbox" style="max-width:520px;margin:20px auto"><label class="skip" for="nf-q">Search guides</label><input id="nf-q" name="q" type="search" placeholder="Search guides…"></form>
<a class="btn" href="{P}index.html">Back to home</a><a class="btn ghost" href="{P}guides.html">All guides</a></section>
<div class="grid">{"".join(card(BY[s]).replace('href="', 'href="'+P).replace('href="'+P+'http','href="http') for s in ["steal-an-egg-codes","anime-dice-codes","scrooms-beginners-guide"])}</div></div>""" + footer(prefix=P)
write("404.html", nf)

# ---------- sitemap / robots ----------
urls = [("",TODAY,"1.0","daily"),("guides.html",TODAY,"0.9","daily"),("games.html",TODAY,"0.8","weekly"),("about.html",TODAY,"0.5","monthly"),("privacy-policy.html",TODAY,"0.5","yearly"),("terms.html",TODAY,"0.5","yearly"),("contact.html",TODAY,"0.5","yearly"),("roblox-the-forge.html",TODAY,"0.7","weekly")] + \
       [(v[0],TODAY,"0.7","weekly") for v in CATS.values()] + [(g["slug"]+".html",TODAY,"0.8","weekly") for g in guides]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{BASE}{u}</loc><lastmod>{d}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n" for u,d,p,c in urls) + "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: Mediapartners-Google\nAllow: /\n\nUser-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
write("ads.txt", """# ads.txt for robloxguides.org
google.com, pub-6703417075646187, DIRECT, f08c47fec0942fa0
""")

# ---------- assets ----------
os.makedirs(os.path.join(OUT,"assets"), exist_ok=True)
write("assets/style.min.css", minify_css(CSS))
write("assets/site.js", JS)
write("assets/logo.svg", LOGO_SVG)
write("assets/favicon.svg", LOGO_SVG)
write(".nojekyll", "")
json.dump(report, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"seo-report.json"),"w"), indent=1)
for r in report: print(r["slug"], "T",r["title_len"], "D",r["desc_len"], "W",r["words"], "kw",r["occ"], r["density"], "first100",r["kw_first100"], "links",r["body_links"])
