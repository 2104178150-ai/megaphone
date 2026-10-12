---
name: launch-readme
description: Rewrite the first screen of a GitHub README so launch visitors instantly see what it is, who it's for, what it looks like and how to try it — title, tagline, visual, three bullets, one-command quick start, badges, and an optional Chinese/English twin README. Use when the user asks to improve, rewrite or polish a README, make it launch-ready, or says 改 README / README 第一屏 / 写个中文版 README.
---

# Launch README

The README's first screen (roughly the first 25 rendered lines, or one phone screen)
is the landing page for every launch post. This skill rewrites that screen and leaves
the rest of the README alone unless asked.

## Before you edit

- Read `.megaphone/brief.md`. If it doesn't exist, run a quick pass of
  `../launch-positioning/SKILL.md` first — a README can't be sharper than its pitch.
- Read the whole current README and keep everything that's accurate. You're
  reorganising and tightening, not deleting the author's documentation.
- Verify every command you put in the quick start by finding it in the code, package
  manifest or existing docs. Never invent flags, package names or URLs. If the project
  isn't published to a registry, say so and use the real install path (e.g. clone +
  run).

## The first screen, in order

1. **Name + logo (optional)** as the H1. Keep the logo small; it shouldn't push the
   tagline below the fold.
2. **Tagline** — the one-liner from the brief, as plain text directly under the title.
3. **Badges** — at most one row, only ones that carry information (version, license,
   CI, downloads). Remove broken or stale badges.
4. **Visual** — a screenshot, GIF or short video showing the aha moment. If none
   exists, leave a clearly marked placeholder and add "record a demo GIF" to the user's
   to-do list with a suggestion of what to capture (the exact steps of the aha moment,
   under 15 seconds, no dead time). Tools: [VHS](https://github.com/charmbracelet/vhs)
   or asciinema for terminals, any screen recorder + gifski for apps.
5. **Three bullets** — benefits first, each with a bold lead-in and the how after a
   dash.
6. **Quick start** — the shortest real path to first result, in one code block.
   One command is ideal; three is the maximum before a "Full install" link.
7. **Links row** — Demo · Docs · 中文 / English · Discord, whichever exist.

Below the fold, make sure these exist (add short sections if missing): **Why**
(contrast with alternatives, honest), **Usage/Examples**, **FAQ** (optional),
**Contributing**, **License**.

## Language twins

If the user wants to reach Chinese channels (V2EX, HelloGitHub, 阮一峰周刊, 即刻, 掘金,
小红书), create `README.zh-CN.md` (or the English twin if the original is Chinese) and
link both ways at the top: `English | [简体中文](README.zh-CN.md)`.

- Write the Chinese version natively: short sentences, concrete pain points, "适合谁"
  and "不适合谁". Don't translate idioms literally.
- Keep the code blocks identical between the two.
- Use full-width punctuation in Chinese text and a space between Chinese and Latin
  words/numbers (中文 English 混排 like this).

## Output

1. Show the user the new first screen as a diff or side-by-side before writing.
2. After approval, edit `README.md` (and create the twin if requested).
3. List anything you couldn't do yourself: record a GIF, set the repo description
   and topics (give the exact text: description ≤ 160 chars, 3–8 topics), set the
   homepage, upload a social preview image (1280×640).

## Example first screen

````markdown
# Megaphone

Launch your open-source project the way marketers would — without being one.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

English | [简体中文](README.zh-CN.md)

![Megaphone checker scoring a repo](docs/demo.gif)

- **Know if you're ready** — a 0–100 launch score with the three fixes that matter most
- **Posts that fit each channel** — Show HN, Reddit, Product Hunt, V2EX, HelloGitHub, 小红书…
- **See what worked** — star and referrer tracking lined up against your launch log

```bash
npx skills add 2104178150-ai/megaphone
```
````
