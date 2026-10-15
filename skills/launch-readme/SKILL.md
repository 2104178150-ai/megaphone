---
name: launch-readme
description: Rewrite the first screen of a GitHub README so launch visitors instantly see what it is, who it's for, what it looks like, what it needs, and how to try it — title, tagline, visual, three bullets, a quick start that reaches the aha moment, requirements, badges, and an optional translated twin README. Use when the user asks to improve, rewrite or polish a README, make it launch-ready, or says 改 README / README 第一屏 / 写个中文版 README.
---

# Launch README

The README's first screen (about one phone screen — roughly the first 25 rendered lines)
is the landing page for every launch post. This skill rewrites that screen and leaves the
rest of the README alone unless asked.

## Before you edit

- Read `.megaphone/brief.md`. If it doesn't exist, do a quick pass of
  `../launch-positioning/SKILL.md` first — a README can't be sharper than its pitch.
- Read the whole current README and keep everything that's accurate. You're reorganising
  and tightening, not deleting the author's documentation.
- **Commands must be real.** Never invent flags, package names or URLs. You may compose a
  command from verified parts (documented flags, files that exist on the default branch,
  e.g. `curl -s <raw-url-of-repo-sample> | tool -`); mark it `# verify` and add "run the
  quick start on a clean machine" to the user's to-do list. If the project isn't published
  to a registry, use the real install path (clone + run).

## The first screen, in order

1. **Name + logo (optional)** as the H1. Keep the logo small; it mustn't push the tagline
   below the fold. A logo is not the visual.
2. **Tagline** — the brief's one-liner, as plain text directly under the title.
3. **Badges** — at most one row, only ones that carry information (version, license, CI,
   downloads). Remove broken or stale badges.
4. **Links row** — Demo · Docs · 中文 / English · Discord, whichever exist.
5. **Visual** — a screenshot, GIF or short video of the aha moment. If none exists, leave a
   clearly marked placeholder and put "record a demo" on the to-do list with exactly what to
   capture (the aha-moment steps, under 15 seconds, no dead time).
   - Recording: [VHS](https://github.com/charmbracelet/vhs) or asciinema for text-only
     terminal output; a screen recorder + gifski if the tool draws images (Kitty, iTerm2,
     Sixel) or has a GUI.
   - Host it where the audience can load it. For mainland-China audiences
     `raw.githubusercontent.com` is often blocked — prefer the project's own site.
   - Check `.gitignore` doesn't exclude the asset path.
6. **Three bullets** — benefits first, each with a bold lead-in and the how after a dash.
   Keep each to about one line on a phone.
7. **Quick start** — the shortest real path to **the aha moment in the brief**, not just
   to "it installed".
   - If a hosted version needs no sign-up, that link *is* the quick start: put it first,
     the install block after it.
   - Otherwise one code block; three commands at most before a "Full install" link.
   - If the headline feature needs an input (a file with a diagram, a sample playlist
     link), provide one.
8. **Requirements line** — one line naming any non-obvious runtime need: a browser,
   GPU, Docker, an OS limit, an account or paid API key. Visitors forgive a dependency they
   were told about.
9. **Disclaimer** (only for projects built on other platforms, media or personal data) —
   the brief's standard disclaimer: not affiliated with X; what it does and doesn't do.

Below the fold, make sure these exist (add short sections if missing): **Why** (honest
contrast with alternatives, dated), **Usage/Examples**, **FAQ** (optional),
**Contributing**, **License**. Remove launch scaffolding visitors shouldn't see (links to
"launch copy", internal checklists), and re-check any comparison table: every ✅ must be
fully true.

## Language twins

Create a twin only if you'll post in channels whose language differs from the README's:
`README.zh-CN.md` for an English README going to V2EX/HelloGitHub/即刻, `README.en.md` for a
Chinese README going to Hacker News/Reddit. Skip it if the README already matches every
target channel. If git history shows the author removed a twin, ask before adding it back.
Link both ways at the top: `English | [简体中文](README.zh-CN.md)`.

- Write the twin natively: short sentences, concrete pain points, 「适合谁 / 不适合谁」.
- Keep the code blocks identical.
- In Chinese text use full-width punctuation and a space between Chinese and Latin
  words/numbers (中文 English 混排 like this).

## Output

1. Show the user the new first screen as a diff or side-by-side.
2. After approval, edit `README.md` (and create the twin if requested). If approval can't
   happen now, write the proposal to `.megaphone/readme-first-screen.md` instead.
3. List what the user has to do: record the visual, run the quick start on a clean machine,
   set the repo description (≤ 160 characters) and topics (add specific ones; don't remove
   relevant existing topics — GitHub allows 20), set the homepage, upload a social preview
   image (1280×640).

## Example first screen

````markdown
# Megaphone

Launch your open-source project the way a marketer would — even if you've never done it.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

English | [简体中文](README.zh-CN.md) · [Try the checker →](https://2104178150-ai.github.io/megaphone/)

![Megaphone checker scoring a repo](docs/preview.svg)

- **Know if you're ready** — blockers, risks and a 0–100 launch score
- **Posts that fit each channel** — Show HN, Reddit, V2EX, HelloGitHub, 小红书…
- **See what worked** — stars and referrers lined up against your launch log

```bash
npx skills add 2104178150-ai/megaphone
```

Needs: an AI coding agent that supports skills (Claude Code, Codex, Cursor…). The web checker needs nothing.
````
