from codeslib import make
import forgelib as F
IDS = ["vpcSr14Ax40","JxlCNX5P0aE","EAEddhHFG20","IVSLEN99o2w","2PkmzmYdGus","Etp9MMD_lm8","w6i5-DEB8OI","u8qsBkINbRI","2FlXciZ-bOs","1Ju4BRGaLoo","oQaO30TFWyQ"]
G = make(slug="the-forge-codes", game="The Forge", short="The Forge", kw="the forge codes",
 title="The Forge Codes (November 2026) – 4 Working, 45 Rerolls",
 h1="The Forge Codes (November 2026): Free Race Rerolls That Work",
 desc="The Forge codes for November 2026: 4 working codes worth 45 free race rerolls, how to redeem them in the Mailbox, plus disputed and expired codes. Claim them!",
 kw2=["the forge codes 2026","the forge reroll codes","the forge codes not expired","how to redeem codes in the forge","the forge free rerolls"],
 related=["the-forge-race-reroll-guide","the-forge-races-guide","the-forge-archangel-race","roblox-codes-november-2026"],
 place_url=F.PLACE, universe=7671049560, rd_slug="the-forge",
 extra_sources=[F.wiki("Codes"), F.wiki("Races")],
 players="22,800",
 rank_note="The Forge had about <strong>22,800 players online</strong> on November 11, 2026, and has passed <strong>1 billion visits</strong>. All four codes give <strong>race rerolls</strong>, <strong>45 rerolls in total</strong>.",
 active=[("AIDASAYSSORRY","10 Race Rerolls","Roblox Den, RBLXSTAT (confirmed, added November 8, 2026)"),
         ("SORRYFORSHUTDOWNN!","15 Race Rerolls","Roblox Den, RBLXSTAT (confirmed, added November 7, 2026)"),
         ("FORGECOMEBACK","10 Race Rerolls","Roblox Den, RBLXSTAT (confirmed), Forge Wiki"),
         ("TWILIGHTWAR","10 Race Rerolls","Roblox Den, RBLXSTAT (confirmed), Forge Wiki")],
 disputed=[("WAITFORHALLOWEEN","10 Race Rerolls","Roblox Den says check it; RBLXSTAT says another source lists it as expired"),
           ("CRIMSONSAKURA","15 Race Rerolls","Only Roblox Den lists it, and marks it \"check\"")],
 expired=["GOATEDCOMMUNITY","GUILDS","HALLOWEEN26","DELAYCOMPENSATION2","FORGEWEEKENDS15","RAIDUPDSOON","FORGEWEEKENDS13","FORGEWEEKENDS12","LOWGRAPHICS","GALAXITE!","FORGEWEEKENDS11","FORGEWEEKENDS10"],
 redeem=["Open <strong>The Forge</strong> on Roblox and wait for your island to load.",
         "Open the <strong>Mailbox</strong>. The Forge Wiki says to click the mailbox (letter) icon at the top right. Roblox Den shows it through the three-line menu at the top left, then <strong>Mail</strong>.",
         "Find the <strong>Codes</strong> section and click the <strong>Enter a code</strong> box.",
         "Paste the code exactly as written, including the <code>!</code> in SORRYFORSHUTDOWNN!.",
         "Press <strong>Redeem</strong>. The rerolls go straight into your race reroll count."],
 req="None. The Mailbox, and code redemption inside it, was added in version 1.05.2 on January 21, 2026. Older videos may show a different code box.",
 expiry=["The Forge codes don't show an expiry date. Most last one to three weeks, and they often end when the next update goes live.",
         "SORRYFORSHUTDOWNN! and AIDASAYSSORRY are apology codes that came out after server downtime on November 7–8, 2026. Codes like these tend to be switched off quickly, so redeem them first.",
         "FORGECOMEBACK and TWILIGHTWAR are on the Forge Wiki's own active list, so they're the most likely to still work later in November.",
         "The weekend codes (FORGEWEEKENDS10 to 15) and event codes (HALLOWEEN26, GUILDS) have already expired."],
 about="<p>The Forge is a mining, forging and fighting RPG from The Forge Community, made by FireAtacck, Umut and Cey, according to the Forge Wiki. You mine ores, forge them into weapons and armor, and fight your way through four islands, from Stonewake's Cross to the Crimson Sakura Isles. Your <strong>race</strong> gives you big passive bonuses. Codes are the main free way to get race rerolls, because rerolls otherwise cost Robux.</p><p>Fridge has made eleven Shorts and videos on new The Forge codes since December 2025. They're all embedded below, each one dated.</p>",
 tips=["Use all 45 rerolls at the Wizard's Tower or in the Race Menu. Our <a href=\"the-forge-race-reroll-guide.html\">race reroll guide</a> shows where.",
       "Luck potions and totems <strong>don't</strong> affect race rerolls, according to the Forge Wiki, so don't waste a Luck Potion before you roll.",
       "Check what each race does in our <a href=\"the-forge-races-guide.html\">The Forge races guide</a> before you reroll away a Legendary.",
       "Hoping for a Relic? The odds are in our <a href=\"the-forge-archangel-race.html\">Archangel race guide</a>."],
 newcodes="New codes come with updates, milestones and apology rounds after downtime. They're posted in the official Forge Discord and on the game's social channels, then picked up by trackers such as Roblox Den and RBLXSTAT. We re-check this page against both and the Forge Wiki whenever a new one appears.",
 links_html='Playing other RPGs? See <a href="blox-fruits-codes.html">Blox Fruits codes</a> and <a href="king-legacy-codes.html">King Legacy codes</a>.',
 faq_extra=[("Do The Forge codes give gold?","No. Every working code right now gives race rerolls only. Gold comes from mining, quests and selling forged gear."),
            ("Where is the code box in The Forge?","Inside the Mailbox. Open it from the letter icon or the menu, then use the Codes section and press Redeem.")])
G["chapters"] = None
vids, shorts = F.split(IDS)
G["videos"], G["shorts"] = vids, shorts
G["forge_order"], G["forge_ids"] = 1, IDS
G["body"] = G["body"].replace("{VIDEO_PLACEHOLDER}", F.embeds(IDS, "Fridge's The Forge Codes Videos and Shorts")
  + '\n<p class="small">Codes shown in older Shorts have mostly expired. The table below lists the codes that work today.</p>', 1)
