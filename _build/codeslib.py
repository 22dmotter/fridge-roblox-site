"""Shared builder for codes pages (c21+). Each g/c2x file passes verified data; this renders the standard sections."""
def _tbl(cap, head, rows):
    h="".join(f'<th scope="col">{x}</th>' for x in head)
    r="".join("<tr>"+"".join(f"<td>{c}</td>" for c in row)+"</tr>" for row in rows)
    return f'<div class="table-wrap"><table><caption>{cap}</caption><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'

def make(slug, game, short, kw, title, h1, desc, kw2, related, place_url, universe, rd_slug, extra_sources,
         players, rank_note, active, disputed, expired, redeem, req, expiry, about, tips, newcodes, links_html, faq_extra=()):
    n=len(active)
    act_rows=[(f"<code>{c}</code>", r, v) for c,r,v in active]
    dis_rows=[(f"<code>{c}</code>", r, w) for c,r,w in disputed]
    sources=[(f"{game} on Roblox (official game page)", place_url)]+list(extra_sources)+[
        (f"Roblox Den: {game} codes", f"https://robloxden.com/game-codes/{rd_slug}"),
        (f"RBLXSTAT: {game} codes", f"https://rblxstat.com/games/{universe}/codes")]
    newest = active[0][0] if active else ""
    body=f"""
<p class="lead">Here are the working <strong>{kw}</strong> for November 2026, <strong>last checked <time datetime="2026-11-11">November 11, 2026</time></strong>. There {'is' if n==1 else 'are'} <strong>{n} working code{'s' if n!=1 else ''}</strong> right now, each confirmed by at least two dated sources. {rank_note}</p>
<p class="small"><strong>Refreshed regularly:</strong> we re-check this list against live trackers and the official game page whenever a new update drops, so bookmark it.</p>
{{CHAPTERS}}
{{VIDEO_PLACEHOLDER}}

<h2 id="active">All Working {short} Codes (November 2026)</h2>
{_tbl("Working codes – last checked November 11, 2026", ["Code","Reward","Confirmed by"], act_rows)}
<p class="small">We only list a code as working when at least two dated sources agree, or the developer posted it. Copy codes exactly, including capitals, numbers and symbols.</p>

<h2 id="expiry">{short} Code Expiry Notes</h2>
<ul>{''.join(f'<li>{x}</li>' for x in expiry)}</ul>

<h2 id="redeem">How to Redeem {short} Codes</h2>
<ol class="steps">{''.join(f'<li>{x}</li>' for x in redeem)}</ol>
{f'<div class="callout"><strong>Requirement:</strong> {req}</div>' if req else ''}

<h2 id="disputed">{short} Codes That May Not Work</h2>
{_tbl("Disputed codes", ["Code","Listed reward","Why it's disputed"], dis_rows) if dis_rows else '<p>No disputed codes right now: every code we found is either confirmed or clearly expired.</p>'}
<p>Disputed codes cost nothing to try, but don't be surprised if they fail.</p>

<h2 id="expired">Expired {short} Codes</h2>
<p>These no longer work, according to Roblox Den's expired list and the other trackers we checked: {', '.join(f'<code>{c}</code>' for c in expired)}. If a code says invalid or expired, it's gone for good.</p>

<h2 id="fix">Code Not Working? Quick Fixes</h2>
<ul>
<li><strong>Check spelling and capitals.</strong> Paste the code instead of typing, and remove any space at the end.</li>
<li><strong>Check the requirement.</strong> Level, playtime or community rules block a lot of redemptions.</li>
<li><strong>Rejoin a new server.</strong> Some games only load new codes in servers started after the update.</li>
<li><strong>Already used?</strong> Every code works once per account.</li>
<li><strong>Still failing?</strong> It has probably expired. Check the disputed and expired lists above, then come back later; we update this page regularly.</li>
</ul>

<h2 id="safety">{short} Code Safety Warnings</h2>
<div class="callout warn"><strong>Stay safe:</strong> real {short} codes are only typed into the game itself. <strong>Never use a code generator</strong>, never enter your Roblox username and password on a site that promises codes or free items, and never download scripts or "auto-redeem" tools. No game code gives Robux. If a site asks you to log in, it's a scam: close it and report it.</div>

<h2 id="about">About {game}</h2>
{about}

<h2 id="tips">Tips for Using Your Free Rewards</h2>
<ul>{''.join(f'<li>{x}</li>' for x in tips)}</ul>

<h2 id="new">Where to Find New {short} Codes</h2>
<p>{newcodes}</p>
<p>{links_html} Every game we track is listed in our <a href="roblox-codes-november-2026.html">Roblox codes hub for November 2026</a>.</p>
"""
    body=_tune(body, kw, short, faq_extra)
    faq=[(f"How many {short} codes are working?", f"{n} working code{'s' if n!=1 else ''} as of November 11, 2026, each confirmed by at least two sources."),
         (f"What is the newest {short} code?", f"{newest} is the newest working code on our list." if newest else "There is no working code right now."),
         (f"How do you redeem {short} codes?", " ".join(re.sub('<[^>]+>','',x) for x in redeem[:4])),
         (f"Why is my {short} code not working?", "It has probably expired, was typed wrong, was already used on your account, or needs a requirement you haven't met yet.")]+list(faq_extra)
    chapters=[("0:00",f"Intro: free {short} rewards","active"),("0:15",f"All {n} working codes","active"),("0:45","When codes expire","expiry"),("1:00","How to redeem","redeem"),("1:25","Disputed codes","disputed"),("1:45","Safety warnings","safety")]
    howto=(f"How to redeem {short} codes", [(f"Step {i+1}", re.sub('<[^>]+>','',x), "redeem") for i,x in enumerate(redeem)])
    return dict(slug=slug, title=title, h1=h1, desc=desc, cat="Codes", game=game, date="2026-11-11", videos=[],
        kw_primary=kw, kw_secondary=kw2, related=related, chapters=chapters, howto=howto, sources=sources, body=body, faq=faq,
        code_count=n)
import re

def _plain(t): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"<!--.*?-->"," ",t,flags=re.S)))
def _tune(body, kw, short, faq_extra):
    words=len(re.findall(r"[\w'+.&-]+", _plain(body)))+190
    kwn=len(kw.split()); target=max(3, round(0.015*words/kwn))
    low=_plain(body).lower(); occ=low.count(kw.lower())+2  # ~2 in the generated FAQ
    pat=re.compile(re.escape(short)+r" (Codes|codes)")
    ms=list(pat.finditer(body))
    if kw.lower()!=(short+" codes").lower() and occ<target:
        # promote some "{short} codes" to the full keyword
        need=target-occ; out=[]; last=0; done=0
        for m in ms:
            if done>=need: break
            if "<h2" in body[max(0,m.start()-40):m.start()] and done==0: pass
            title = kw.title() if m.group(1)=="Codes" else kw[:1].upper()+kw[1:] if body[m.start()-2:m.start()] in (". ","> ") else kw
            out.append(body[last:m.start()]); out.append(title if m.group(1)=="Codes" else kw if not body[m.start()-2:m.start()] in (". ","> ") else kw[:1].upper()+kw[1:]); last=m.end(); done+=1
        out.append(body[last:]); return "".join(out)
    if occ>target and kw.lower()==(short+" codes").lower():
        extra=occ-target; keep=len(ms)-extra
        out=[]; last=0
        for i,m in enumerate(ms):
            if i<keep: continue
            out.append(body[last:m.start()]); out.append(m.group(1)); last=m.end()
        out.append(body[last:]); return "".join(out)
    return body
