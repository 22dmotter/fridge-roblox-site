"""Shared pieces for Roblox macro guides. Disclaimers stay honest: no undetectable claims, no affiliation."""
TOS = "https://en.help.roblox.com/hc/en-us/articles/115004647846-Roblox-Terms-of-Use"
CHEAT = "https://en.help.roblox.com/hc/en-us/articles/203312450-Cheating-and-Exploiting"
EXO = "https://exopanda.com/"
EXO_DL = "https://exopanda.com/downloads"
EXO_TOOLS = "https://exopanda.com/tools"
EXO_GUIDES = "https://exopanda.com/guides"
EXO_TOS = "https://exopanda.com/terms"
EXO_SYS = "https://exopanda.com/guides/how-to-use-the-macro-system"
EXO_GAG = "https://exopanda.com/guides/grow-a-garden-macro"
EXO_FISCH = "https://exopanda.com/guides/fisch"
EXO_BSS = "https://exopanda.com/guides/bee-swarm"
EXO_PS99 = "https://exopanda.com/guides/pet-simulator-99-macro"

DISCLAIMER = f'''<div class="callout warn"><strong>Roblox Terms of Use and ban risk:</strong> Using a macro, auto clicker, record-and-replay tool or bot to play Roblox for you can break the <a href="{TOS}" rel="noopener" target="_blank">Roblox Terms of Use</a> and a game's own rules. Roblox's <a href="{CHEAT}" rel="noopener" target="_blank">Cheating and Exploiting</a> policy says exploiting or cheating can lead to account deletion, and unofficial programs are a common way to steal passwords. Marketing that says a tool is "external," "no injection," "undetectable" or "safe" does not make it allowed, and Fridge cannot verify any safety or ban-risk claim. You can be kicked, banned from a game or actioned on your account. Use third-party software at your own risk. Fridge is not affiliated with Roblox Corporation or with any macro vendor.</div>'''

MALWARE = '''<div class="callout warn"><strong>Malware warning:</strong> A large share of "free Roblox macro" and "auto clicker" downloads on random websites, Discord servers and YouTube descriptions are malware or password stealers. Only install software you can trace to a real official site, scan the file, and never type your Roblox password into a macro tool. If a download asks you to turn off antivirus, run an executor or paste a script into Roblox, close it.</div>'''

CORE_SOURCES = [
    ("Roblox Terms of Use", TOS),
    ("Roblox Support: Cheating and Exploiting", CHEAT),
    ("ExoPanda homepage (third-party macro hub; not affiliated with Fridge)", EXO),
    ("ExoPanda Terms of Service", EXO_TOS),
]

def make(slug, kw, title, h1, desc, kw2, related, lead, sections, faq, sources=(), howto=None, heading=None, extra_body=""):
    secs = "\n".join(f'<h2 id="{a}">{h}</h2>\n{b}' for a,h,b in sections)
    more = ('<h2 id="more">More Roblox Macro Guides</h2>\n<p>Start with <a href="what-is-a-roblox-macro.html">what a Roblox macro is and whether it can get you banned</a>, '
            'the <a href="best-roblox-macros.html">best Roblox macros and auto clickers</a> overview, or the full list on our <a href="tag-macro.html">Roblox Macros</a> hub. '
            'For idle play that does not automate your inputs, see <a href="how-to-afk-in-roblox.html">how to AFK in Roblox</a>.</p>')
    body = f'<p class="lead">{lead}</p>\n{{CHAPTERS}}\n{{VIDEO_PLACEHOLDER}}\n{DISCLAIMER}\n{MALWARE}\n{secs}\n{extra_body}{more}\n'
    src = list(CORE_SOURCES) + list(sources)
    return dict(slug=slug, title=title, h1=h1, desc=desc, cat="Macro", game="Roblox", date="2026-11-12", videos=[],
                kw_primary=kw, kw_secondary=kw2, related=related, chapters=None, howto=howto, sources=src, body=body, faq=faq)
