# STATUS

## What was built

**The ADHD Task Paralysis Handbook** — a gentle, low-shame manual for getting
unstuck when a task will not start, plus a static site with a printable
stuck-task ladder. Authored as Dylan Asdale / Asdale Dynamics, LLC.

- `docs/` — 9 Markdown files (~13,000 words): start-here, why-you're-stuck,
  five-minute doorway trick, body doubling, timers (promise / defiance /
  switch timers, plus the harmful kind), visible progress cards,
  AI nudges that actually help (3 tested prompts + anti-patterns + privacy
  notes), the 10-rung stuck-task ladder, and a one-page quick reference.
- `site/index.html` + `site/style.css` — static, build-free site: chapter
  cards linking into `docs/`, and a print-optimized 10-rung ladder card
  (a "Print the ladder" button triggers a print stylesheet that shows only
  the ladder, one page).
- `tools/verify.py` — dependency-free verification script.
- `README.md` — overview, run instructions, credits Asdale Dynamics, LLC.
- `LICENSE` — MIT, with the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`.

Distinct from `gentle-productivity-manual` and `low-energy-chore-planner`
(app): this covers specifically the moment a task will not start.

## How to run it

- **Manual:** open any file in `docs/` (GitHub-rendered or any Markdown viewer).
- **Site:** `python3 -m http.server 8080 --directory .` then visit
  `http://localhost:8080/site/` — or just open `site/index.html` directly.
- **Print ladder:** on the site click "Print the ladder" (or Ctrl/Cmd+P).
- **Verify:** `python3 tools/verify.py`

## Verification results

- `python3 tools/verify.py` — **19/19 checks passed**, exit code 0:
  docs links resolve (9 files), HTML is well-formed, site references only
  existing local files, zero network dependencies, no `<script>` tags,
  print stylesheet + all 10 rungs present, LICENSE line exact, README
  credits LLC, no secret-shaped strings.
- Live serve test with `python3 -m http.server 8191`: `/site/`,
  `/site/index.html`, `/site/style.css`, `/docs/07-stuck-task-ladder.md`,
  `/README.md` — all returned **200**.
- One manual content review pass (typos, non-ASCII artifacts, prompt blocks).

## Git

Initialized in-folder; single commit `a5e750b`
("Add ADHD task paralysis handbook: markdown manual and printable site"),
committed as the existing identity (Dylan Asdale). No remote, nothing pushed.

## Known gaps

- No screenshots: the print layout was verified structurally (print media
  queries + parsed rungs) but not rendered to PDF from a browser.
- Chapter cross-links are file-relative; they work on disk, over the dev
  server, and on GitHub, but a GitHub Pages deploy would need a small path
  tweak for the site's `../docs/` links (not done — no publishing).
- No automated prose checks (spell-check/lint of Markdown is manual only).
- Content is education/tooling only; intentionally not medical advice.
