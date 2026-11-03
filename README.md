# quantechgraphics.com

Static website for Quantech Graphics. No framework: `build.py` turns the copy and
templates into plain HTML in `dist/`.

## Build and preview locally

```
python3 build.py
python3 -m http.server -d dist 8000   # then open http://localhost:8000
```

## Where to change things

| What | Where |
|---|---|
| Social links, Steam, emails, demo links | `site.config.json` (empty `url` shows "coming soon") |
| Theme | `site.config.json` → `theme` (`synapse`, `ops`, `chrome`) |
| Preview banner + search-engine blocking | `site.config.json` → `preview` (set `false` at launch) |
| Page copy | `build.py`, `PAGES` section |
| Styles | `src/assets/site.css`, theme overrides in `src/assets/themes/` |
| Images | Drop `src/assets/img/<slot>.jpg/.png/.webp` using the placeholder's name (see `IMG_SLOTS` in `build.py`) |

Forms (newsletter, notify-me, project brief) are not connected to a backend yet;
set `data-endpoint` in `build.py` once a form service is chosen.

## Deploy

GitHub Pages, deployed manually from **Actions → Deploy to GitHub Pages → Run workflow**.
Domain: `quantechgraphics.com` (CNAME written by the build). Social icons from
[Simple Icons](https://simpleicons.org) (CC0).
