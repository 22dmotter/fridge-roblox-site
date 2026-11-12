from macrolib import make, EXO_TOOLS, EXO_DL, EXO_SYS

G = make(
    slug="roblox-macros-windows-mac",
    kw="tinytask roblox",
    title="TinyTask, AutoHotkey and Mac Roblox Macros",
    h1="TinyTask, AutoHotkey and Mac Roblox Macros",
    desc="How TinyTask, AutoHotkey and Mac tools are used as Roblox macros, where to get real downloads, and the ban risk. Don't grab a fake installer!",
    kw2=["autohotkey roblox", "roblox macro mac", "tinytask macro roblox", "roblox autohotkey"],
    related=["what-is-a-roblox-macro", "best-roblox-macros", "roblox-auto-clicker", "how-to-afk-in-roblox", "tag-macro"],
    lead="TinyTask Roblox searches usually mean a Windows recorder that replays clicks; AutoHotkey and macOS shortcuts are also reused as Roblox macros. None of them is an official Roblox product. This page covers what each one is, how to stay on real official downloads, and why a recording or script that plays the game for you can still get the account actioned.",
    howto=("Evaluate a Windows or Mac Roblox macro tool more safely",[
        ("Accept the account risk","Confirm you accept that automating Roblox can violate the Terms of Use and get the account banned.","risk"),
        ("Use official sites only","Open only the official site for TinyTask alternatives, AutoHotkey, your vendor, or Apple's own Shortcuts documentation. Type the URL yourself.","tiny"),
        ("Reject look-alike downloads","Skip 'TinyTask Roblox' or 'AHK script pack' files from ads, Discord or YouTube descriptions.","tiny"),
        ("Scan files and skip unknown scripts","Scan the installer, and never paste a script you do not understand or type your Roblox password into the tool.","ahk"),
        ("Keep a start/stop hotkey","Watch the window so you can stop playback immediately.","risk"),
    ]),
    sections=[
        ("tiny", "TinyTask and other record-and-replay tools",
         """<p>TinyTask is a well-known Windows program that records mouse and keyboard input and plays the recording back. People search "TinyTask Roblox" because a short recording can repeat a harvest click, a menu path or a simple movement loop. The program itself is a generic Windows utility, not a Roblox add-on, and using it to automate play can still break the <a href="https://en.help.roblox.com/hc/en-us/articles/115004647846-Roblox-Terms-of-Use" rel="noopener" target="_blank">Terms of Use</a>.</p>
<p>The bigger practical problem is that TinyTask is old and heavily impersonated. Search ads and "TinyTask Roblox download" pages often bundle malware. If you cannot confirm you are on a real, long-standing official source, do not install it. A recording that needs you to disable antivirus is not a recording you should run.</p>
<p>Some newer hubs ship their own recorder instead. <a href="https://exopanda.com/tools" rel="noopener" target="_blank">ExoPanda's tools page</a> lists a Recorder for Windows and macOS and describes it as a TinyTask-style alternative that saves its own file format. Fridge is not affiliated with ExoPanda and cannot audit that recorder. The same <a href="roblox-auto-clicker.html">safer download habits</a> apply: official URL only, scan the file, no Roblox password, and no assumption that a recording is allowed or hidden.</p>"""),
        ("ahk", "AutoHotkey for Roblox",
         """<p>AutoHotkey is a real open-source Windows scripting project. You can bind keys, write loops and add delays. That flexibility is why "AutoHotkey Roblox" is a common search, and it is also why AHK is a favorite disguise for stolen scripts. A .ahk file from a forum, a Discord server or a "paste this farm script" video can be a password stealer just as easily as a click loop.</p>
<p>If you already use AutoHotkey for other work, you still need to treat a Roblox-related script as untrusted code. Do not run scripts you cannot read. Do not give a script your cookie or account token. And do not assume a well-known language makes the automation official. AutoHotkey is allowed software on Windows. Using it to play Roblox for you is still subject to Roblox and game rules.</p>"""),
        ("mac", "Roblox macros on Mac",
         """<p>Windows-only tools such as classic TinyTask and AutoHotkey do not cover macOS. People searching "Roblox macro Mac" usually need either a vendor that publishes a Mac build or a macOS shortcut / automation tool. <a href="https://exopanda.com/downloads" rel="noopener" target="_blank">ExoPanda's downloads page</a> lists macOS 11 or later and describes the Mac build as Apple notarized. That is the vendor's claim; notarization is not a Roblox approval, and Fridge cannot verify the files.</p>
<p>macOS also has built-in Shortcuts and, on older systems, Automator. Those can send clicks or keys, and they have the same policy problem as a Windows clicker if you use them to farm a Roblox game. System accessibility prompts that let an app control the computer are powerful. Grant them only to software you trust, and never to a random "free Roblox macro for Mac" app from outside a real official site.</p>"""),
        ("risk", "The rules are the same on every operating system",
         """<p>Whether the tool is TinyTask, AutoHotkey, a Mac shortcut or a commercial hub, automated play can be treated as cheating under Roblox's <a href="https://en.help.roblox.com/hc/en-us/articles/203312450-Cheating-and-Exploiting" rel="noopener" target="_blank">Cheating and Exploiting</a> policy. We will not provide scripts, pixel-perfect recordings or any "undetectable" setup. For the broader comparison, see <a href="best-roblox-macros.html">best Roblox macros and auto clickers</a>. For the policy background, see <a href="what-is-a-roblox-macro.html">what a Roblox macro is and whether it is bannable</a>.</p>
<p>If you only wanted to keep a session from going idle, read <a href="how-to-afk-in-roblox.html">how to AFK in Roblox</a> and skip input automation.</p>"""),
    ],
    faq=[
        ("Is TinyTask allowed on Roblox?",
         "TinyTask is a generic Windows recorder, not an official Roblox tool. Using it to automate gameplay can violate the Terms of Use and get the account actioned."),
        ("Is AutoHotkey safe for Roblox?",
         "The official AutoHotkey project is a real Windows tool, but scripts you paste from the internet are often malware, and automating Roblox with AHK still carries ban risk."),
        ("Can I use a Roblox macro on Mac?",
         "Some third-party hubs list macOS downloads, and macOS has its own shortcuts tools. There is no official Roblox macro for Mac, and the Terms of Use risk is the same as on Windows."),
        ("Where do I download TinyTask for Roblox?",
         "Be careful: many 'TinyTask Roblox' download pages are fakes. Only use a source you can independently verify as legitimate. When in doubt, do not install it."),
    ],
    sources=[
        ("ExoPanda tools (third party, not affiliated)", EXO_TOOLS),
        ("ExoPanda downloads (third party, not affiliated)", EXO_DL),
    ],
)
