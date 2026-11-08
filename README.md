# The ADHD Task Paralysis Handbook

A gentle, low-shame manual for getting unstuck when a task will not start —
the five-minute doorway trick, body doubling, timers that help (and one that
hurts), visible progress cards, and AI nudges that actually help. Includes a
static site with a **printable stuck-task ladder**.

Written "like a friend would": plain English, step by step, never
condescending. Built for brains that can't always press "start."

## What's in here

| Path | What it is |
|---|---|
| `docs/` | The manual — 8 chapters of Markdown, start-to-finish readable |
| `site/` | A static HTML site with chapter cards and a printable ladder card |
| `docs/07-stuck-task-ladder.md` | The ladder in chapter form (the site has the print version) |

Chapters:

1. [Start Here](docs/00-start-here.md) — who it's for, how to use it, the one rule
2. [Why You're Stuck](docs/01-why-youre-stuck.md) — what task paralysis is, minus the shame
3. [The Five-Minute Doorway](docs/02-five-minute-doorway.md) — the lowest-cost way in
4. [Body Doubling](docs/03-body-doubling.md) — borrowing another brain's presence
5. [Timers That Help (and Hurt)](docs/04-timers.md) — promise, defiance, switch
6. [Visible Progress Cards](docs/05-progress-cards.md) — making progress physical
7. [AI Nudges That Actually Help](docs/06-ai-nudges.md) — three tested prompts, plus traps
8. [The Stuck-Task Ladder](docs/07-stuck-task-ladder.md) + [Quick Reference](docs/quick-reference.md)

## How to read the manual

Open anything in `docs/` here on GitHub, or in any Markdown viewer. No
reading order required — pick the chapter that made you wince slightly.

## How to run the site

No build step. It's plain HTML, CSS, and one browser API (`window.print()`).

```sh
# option 1: just open it
open site/index.html          # macOS
xdg-open site/index.html      # Linux

# option 2: serve it (recommended, so relative doc links resolve cleanly)
python3 -m http.server 8080 --directory .
# then visit http://localhost:8080/site/
```

Click **Print the ladder** on the site and you'll get a one-page, binder- and
fridge-friendly stuck-task ladder (print styles hide everything else).

## Verification

Run `python3 tools/verify.py` — it checks that all Markdown links resolve;
that the site HTML is well-formed and references only existing local files;
that the printable ladder card has all ten rungs; that the LICENSE carries the
exact required copyright; that the README credits the LLC and documents how
to run the site; and that no secret-shaped strings appear anywhere. Vanilla
standard library only.

## Design principles

- **Low shame by design.** Gentleness isn't a tone here; it's the mechanism.
  Every tool is built to lower the cost of starting, not to add guilt.
- **Paper first.** No apps required. The progress system is a sheet of paper
  and a pen.
- **No secrets, no accounts, no network.** The site is fully local-first.
- **Boring tech.** One HTML file, one CSS file. It will still open in 2035.

## Related projects

Distinct from `gentle-productivity-manual` (general gentle productivity) and
`low-energy-chore-planner` (the app). This one is specific to the moment a
task will not start — the wall, the starting gate, and what to do there.

## Author & license

By **Dylan Asdale** — registered nurse turned AI author, founder of Asdale
Dynamics, LLC. Plain-English AI education: *The Massive AI Manual* and hub
site `dylanasdale.github.io`. Asdale Dynamics, LLC publishes beginner-friendly
AI books, guides, and practical tools.

Released under the [MIT License](LICENSE) — Copyright (c) 2026 Asdale
Dynamics, LLC.

Education and practical tooling only. **Never medical advice.**
