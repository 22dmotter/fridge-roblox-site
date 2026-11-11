# Fridge – Roblox Codes & Guides Hub

The official guide site for the **Fridge** Roblox YouTube channel ([@Fridgetherealone](https://www.youtube.com/@Fridgetherealone/videos)).

**Live site:** https://22dmotter.github.io/fridge-roblox-site/

A fast, dark-themed (amber / yellow-orange accent: `#FFB020`, hover `#E8890C`), mobile-first static site, modeled on the content-hub layout of cocajola.com: a homepage with a hero and latest-guides grid, a searchable guide listing, category (tag) pages, and one SEO-optimized article per video. No frameworks, one minified CSS file, one small deferred JS file.

## What's in the site

| File | What it is |
|---|---|
| `index.html` | Homepage: hero, latest guides, categories, channel intro, popular guides |
| `guides.html` | Every guide, with client-side search + category filter (supports `guides.html?q=scrooms`) |
| `tag-codes.html`, `tag-guides.html`, `tag-events.html`, `tag-tips.html` | Category pages (Codes, Guides, Events, Tips) |
| `about.html` | About Fridge + YouTube links |
| `404.html` | Custom not-found page (GitHub Pages serves it automatically) |
| `*.html` (12 guides) | One article per guide/video (see list below) |
| `sitemap.xml`, `robots.txt` | Search engine files (sitemap has `lastmod` for every URL) |
| `assets/` | `style.min.css`, `site.js` (video click-to-load + search), logo/favicon SVG, OG image |
| `_build/` | The generator: `build.py` + one content file per guide in `_build/g/` |

### Guides
- `steal-an-egg-codes.html` – Steal an Egg codes (Nov 2026)
- `steal-an-egg-speed-guide.html` – How to get speed in Steal an Egg
- `steal-an-egg-win-races.html` – How to win races in Steal an Egg
- `steal-an-egg-candy-corn.html` – Candy Corn farming (Halloween Dimension)
- `steal-an-egg-phantom-express-ticket.html` – Phantom Express Ticket + all 4 Lost Echo Dog items
- `scrooms-beginners-guide.html` – How to play Scrooms
- `scrooms-level-up-fast.html` – How to level up fast in Scrooms
- `scrooms-statue-locations.html` – All Scrooms statues + Halden
- `roblox-hollow-event-guide.html` – Roblox Hollow event 2026 guide, games & leaks
- `anime-dice-codes.html` – Anime Dice codes (Nov 2026)
- `huzz-valley-codes.html` – Huzz/Huss Valley codes (Nov 2026)
- `monkey-escape-sunken-shards.html` – All 9 Sunken Shards in +1 Speed Monkey Escape

### Evergreen Roblox help guides (no Fridge video yet, generated cover images in `assets/thumbs/`)
- `run-multiple-roblox-accounts.html` – How to run multiple Roblox accounts at once (Account Switcher, Error 264, risks)
- `how-to-afk-in-roblox.html` – How to AFK in Roblox safely (20-minute idle kick, macros risk)
- `bloxstrap-guide.html` – How to install Bloxstrap (2026 status, official sources only)
- `roblox-shaders.html` – Roblox shaders 2026 (RoShade/ReShade status, ban risk, safe alternatives)
- `unlock-fps-roblox.html` – How to unlock FPS in Roblox (official Maximum Frame Rate)
- `fix-roblox-lag.html` – How to fix Roblox lag
- `recover-roblox-account.html` – Roblox account recovery
- `make-roblox-thumbnails.html` – How to make Roblox thumbnails for free
- `join-someone-roblox-without-friends.html` – How to join someone on Roblox without being friends
- `delete-roblox-account.html` – How to delete a Roblox account

### Top 10 Roblox games codes pages (by live CCU, Nov 11 2026; `_build/g/c0*.py`)
- `blox-fruits-codes.html`, `rivals-codes.html`, `99-nights-in-the-forest-codes.html`, `jujutsu-shenanigans-codes.html` – working codes (≥2 agreeing trackers or official source)
- `murder-mystery-2-codes.html`, `adopt-me-codes.html` – code box exists but nothing confirmed working
- `brookhaven-codes.html`, `throw-food-for-animals-codes.html`, `break-and-steal-an-egg-codes.html` – no code system (explained honestly, free rewards listed instead)
- `steal-an-egg-codes.html` (#1 by CCU) was refreshed rather than duplicated

### More game codes pages (CCU ranks 11–20 + Anime Adventures, Nov 11 2026; `_build/g/c10`–`c20`)
- Working codes: `anime-adventures-codes.html` (5), `dandys-world-codes.html` (2), `fisch-codes.html` (2), `survive-your-ideas-codes.html` (4), `fish-it-codes.html` (3), `steal-a-brainrot-codes.html` (1)
- None confirmed (disputed code listed): `dont-splash-codes.html`, `catalog-avatar-creator-codes.html`
- No code system: `forsaken-codes.html`, `violence-district-codes.html`, `the-strongest-battlegrounds-codes.html` (sound IDs only)

### Video-ready Roblox how-to guides (`_build/g/t*.py`)
- `how-to-turn-on-voice-chat-roblox.html`, `how-to-appear-offline-roblox.html`, `add-trusted-friends-roblox.html`, `check-roblox-account-status.html`, `equip-multiple-accessories-roblox.html`, `redeem-roblox-gift-card.html`, `roblox-parental-controls-guide.html`, `how-to-emote-roblox.html`, `throw-food-for-animals-guide.html`, `99-nights-in-the-forest-guide.html`

### General Roblox guides (`_build/g/n01`–`n10`, Nov 11 2026)
- `roblox-codes-november-2026.html` – codes hub; its table is generated from `CODE_COUNTS` in `build.py` via the `{CODES_TABLE}` placeholder (update the count there whenever a codes page changes)
- `how-to-get-free-items-in-roblox.html`, `how-to-level-up-fast-in-roblox.html`, `best-roblox-pets-2026.html`, `roblox-avatar-ideas.html`, `how-to-report-a-player-on-roblox.html`, `roblox-gift-card-guide.html` (buying/value/scams; redeeming stays in `redeem-roblox-gift-card.html`), `how-to-join-a-roblox-group.html`, `roblox-age-verification.html`, `how-to-change-roblox-username.html`
- Each has a 9:16 YouTube Shorts slot (`{SHORT_PLACEHOLDER}`; see the HTML comment for how to swap in a Short ID) and HowTo schema via the optional `howto=(name, [(step, text, anchor)])` field

### Site-wide visuals
- Animated background: `.bg-fx` (10 drifting amber squares/orbs, opacity 0.04–0.08, `position:fixed`, `pointer-events:none`, transform/opacity only, 44–88 s, 5 elements under 640px, static under `prefers-reduced-motion`)
- Subscribe buttons use `.yt-sub`: YouTube red #FF0000 with bold white 1.2rem text (large-text AA, 4.0:1), hover #CC0000; inline subscribe links use #CC0000 (5.9:1), hover #A30000; visible focus ring

### Codes batch 3 (`_build/g/c21`–`c30`, Nov 11 2026; rendered by `_build/codeslib.py`)
- `dress-to-impress-codes.html` (25), `king-legacy-codes.html` (6), `bee-swarm-simulator-codes.html` (9), `blade-ball-codes.html` (10), `arise-crossover-codes.html` (11), `grow-a-garden-codes.html` (2), `anime-vanguards-codes.html` (3), `basketball-zero-codes.html` (2), `volleyball-legends-codes.html` (3), `driving-empire-codes.html` (2)
- `codeslib.make()` sets `code_count`, which feeds the codes hub table automatically
- `anime-dice-codes.html` refreshed Nov 11 (24 working, safety section, expiry notes)

### Video chapters
Each guide can define `chapters=[("0:00","Title","section-id"), ...]` and put `{CHAPTERS}` in its body. The build renders a "Video Chapters" list linking to each numbered section, plus an HTML comment telling Daniel to paste the same lines into the YouTube description. When the matching video is uploaded, add its ID to `videos=[...]`, swap `{VIDEO_PLACEHOLDER}` for `{VIDEO0}`, and adjust the timestamps to the real video.

**Adding a video to an evergreen guide:** in its `_build/g/e*.py` file, set `videos=[("VIDEO_ID", "Video title")]` and replace `{VIDEO_PLACEHOLDER}` in the body with `{VIDEO0}`, then rebuild. The card thumbnail and `og:image` switch to the YouTube thumbnail automatically. These guides also have a `sources=[...]` list rendered as an "Official sources" box; re-check those pages whenever Roblox or Bloxstrap change something.

Every page has: a keyword-first `<title>` under 60 characters, a 140–160 character meta description, canonical URL, Open Graph + Twitter card tags, breadcrumbs with `BreadcrumbList` JSON-LD, and one `<h1>`. Guide pages also have `BlogPosting` (with `VideoObject`) and `FAQPage` JSON-LD, a visible "Last updated" date, a table of contents, numbered steps, tables, a FAQ, and a related-guides section.

## The Forge section (November 11, 2026)

24 pages for The Forge (Roblox) built from all 79 Fridge videos and Shorts about the game (scraped from the channel's Videos and Shorts tabs). Videos on the same topic share one page, and every video is embedded exactly once.

- Sources: `_build/forge_videos.json` (ID, title, upload date, Short or not), `_build/forgelib.py` (shared page builder) and `_build/g/f01`–`f24`.
- Shorts use vertical 9:16 `youtube-nocookie` iframes (the `.short-slot` and `.shorts-grid` classes). Full videos use the normal click-to-play thumbnail. Add Short IDs to a page's `ids=[...]` list and they are sorted into the right player automatically.
- Each Short with a known upload date gets its own VideoObject (uploadDate = real upload date).
- `the-forge-codes.html` uses `codeslib.make()`: 4 working codes (45 rerolls), checked on Roblox Den, RBLXSTAT and the Forge Wiki. It is in the codes hub table automatically.
- Facts are checked against forgewiki.org. Each page has a callout saying the videos may show an older version of the game.
- Homepage section `forge-h`, tag page `tag-the-forge.html` (category "The Forge") and the nav link are generated by `build.py`.

## How the site is built

The HTML is generated by a small Python script (no dependencies beyond Python 3):

```bash
python3 _build/build.py
```

That regenerates every HTML page, `sitemap.xml`, `robots.txt` and the CSS/JS in place, and writes an SEO check (`_build/seo-report.json`: title/description length, word count, keyword density, internal links). Commit and push, and GitHub Pages redeploys in about a minute.

You *can* edit the HTML files directly, but your changes get overwritten the next time someone runs `build.py`. The best way is to edit the content files in `_build/g/`.

## How to swap in YouTube video IDs

Every guide currently embeds the matching **real Fridge video**. Each embed is wrapped in a clearly marked comment:

```html
<!-- YOUTUBE EMBED: Fridge video "..." (ID iqPQE1lD18s).
     To swap in a different video, replace the 11-character ID in ALL THREE places below
     (data-id, the watch?v= link and the thumbnail URL). Placeholder for a new video: VIDEO_ID_HERE -->
<div class="yt" data-id="iqPQE1lD18s" ...>
```

**Easiest way (recommended):** open the guide's file in `_build/g/` (for example `g07_sae_speed.py`) and change the ID in the `videos=[("VIDEO_ID", "Video title")]` line, then run `python3 _build/build.py`. This also updates the thumbnail, `og:image` and VideoObject schema.

**Quick way:** in the `.html` file, search for the old ID and replace every occurrence with the new one.

The video ID is the part after `watch?v=` in a YouTube URL, e.g. `https://www.youtube.com/watch?v=iqPQE1lD18s` → `iqPQE1lD18s`. Videos load only when clicked (thumbnail first), which keeps pages fast.

## How to add a new guide

1. Copy any file in `_build/g/` (e.g. `g02_anime_dice_codes.py`) to a new file such as `g13_my_new_guide.py`.
2. Edit the fields:
   - `slug` – the file name, e.g. `the-forge-pickaxe-guide` (becomes `the-forge-pickaxe-guide.html`)
   - `title` – keyword first, **under 60 characters**
   - `h1` – the on-page headline
   - `desc` – meta description, **140–160 characters**, ending with a call to action
   - `cat` – one of `Codes`, `Guides`, `Events`, `Tips`
   - `game`, `date` (YYYY-MM-DD, use the video's upload date)
   - `videos` – `[("VIDEO_ID_HERE", "Video title")]`; use `{VIDEO0}` (and `{VIDEO1}`…) in the body where each embed should go
   - `kw_primary`, `kw_secondary` – the searches you're targeting
   - `related` – 3–4 slugs of other guides
   - `body` – the article HTML (use `<h2 id="...">` sections, `<ol class="steps">` for numbered steps, `<div class="table-wrap"><table>` for tables, `<div class="callout">` for tips). Put the primary keyword in the first 100 words and add at least 3 links to other guides.
   - `faq` – 3–5 question/answer pairs (these become FAQPage schema)
3. Run `python3 _build/build.py`. The guide gets added automatically to the homepage (if it's among the newest), `guides.html`, its tag page, the footer, related sections and `sitemap.xml`.
4. Commit and push.

### Updating "Last updated" dates
Change `TODAY` and `MOD_HUMAN` at the top of `_build/build.py`, then rebuild. This updates every visible date, the `dateModified` schema and the sitemap `lastmod`.

### Updating codes
Code tables live in the guide files (`g01`, `g02`, `g03`). Only list codes you've checked in-game or that appear on several current code trackers, and move dead ones to the expired table.

## Theme colors
Accent colors live in the `:root` CSS variables at the top of `_build/build.py` (`--acc` #FFB020, `--acc2` #FFC966, `--accd` #E8890C, `--acc3` #F5A623, `--ink` #1A1000 for text on amber). Cover images in `assets/thumbs/` are regenerated by `build.py`; the social image and app icon are regenerated with `python3 _build/brand_images.py`.

## Deployment

Hosted on **GitHub Pages** from the `main` branch root (`.nojekyll` is included). Any push to `main` redeploys. If you move to a custom domain, update `BASE` in `_build/build.py` and rebuild so canonical URLs, OG URLs and the sitemap use the new domain. Then submit `sitemap.xml` in Google Search Console.

---
Not affiliated with Roblox Corporation or any game developer.
