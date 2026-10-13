# 📣 Megaphone

Launch your open-source project the way a marketer would — even if you've never launched anything.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Agent skills: 7](https://img.shields.io/badge/agent%20skills-7-e8501c)](skills)
[![Channel playbooks: 16](https://img.shields.io/badge/channel%20playbooks-16-e8501c)](skills/launch-posts/channels)
[![Works with Claude Code, Codex, OpenClaw](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20OpenClaw-1f1b16)](#quick-start)

English | [简体中文](README.zh-CN.md) · [**Try the checker →**](https://2104178150-ai.github.io/megaphone/)

![Megaphone scoring a repo: 84/100, the three fixes that matter most, and where to launch it](docs/preview.svg)

- **Know if you're ready** — a 0–100 launch score from 21 checks, with the fixes that matter most. [Try it in your browser](https://2104178150-ai.github.io/megaphone/), no install.
- **A native post for every channel** — Show HN, Reddit, Product Hunt, X, V2EX, HelloGitHub, 阮一峰周刊, 小红书 and more, each written to that platform's rules, with sources and a "last checked" date.
- **See what actually worked** — star history and referrers lined up against what you posted, when.

## Quick start

Install the skills into your coding agent (Claude Code, Codex, OpenClaw, Cursor and [70+ others](https://github.com/vercel-labs/skills#supported-agents)):

```bash
npx skills add 2104178150-ai/megaphone
```

Then, inside your project, ask your agent:

> launch this repo

Prefer a Claude Code plugin?

```bash
claude plugin marketplace add 2104178150-ai/megaphone
claude plugin install megaphone@megaphone
```

Inside a session the skills are then available as `/megaphone:launch`, `/megaphone:launch-audit` and so on.

## Why Megaphone?

Most good open-source projects don't fail because they're bad. They fail because the
author posts one link to Hacker News, gets two upvotes, and concludes nobody cares.
Launching well is a skill — positioning, a README that converts, knowing each
community's rules, timing, and measuring — and most developers never had a reason to
learn it.

| | Megaphone | Generic marketing prompt packs | "Where to post" lists |
|---|---|---|---|
| Reads your repo before writing anything | ✅ | ❌ | ❌ |
| Channel rules with sources and dates | ✅ | Partly | ❌ |
| Chinese developer channels (V2EX, HelloGitHub, 即刻, 小红书…) | ✅ | ❌ | Some |
| Measures which channel worked | ✅ | ❌ | ❌ |
| Try it without installing anything | ✅ [web checker](https://2104178150-ai.github.io/megaphone/) | ❌ | — |
| Refuses vote-gaming | ✅ | Varies | Varies |

## What's inside

### Skills

| Skill | What it does | Writes |
|---|---|---|
| [`launch`](skills/launch/SKILL.md) | Runs the whole pipeline below, pausing for your review at each step | — |
| [`launch-audit`](skills/launch-audit/SKILL.md) | Scores readiness with the [public rubric](skills/launch-audit/rubric.md) plus a human-eyes review | `.megaphone/audit.md` |
| [`launch-positioning`](skills/launch-positioning/SKILL.md) | Finds the one-liner: audience, alternative, proof, contrast | `.megaphone/brief.md` |
| [`launch-readme`](skills/launch-readme/SKILL.md) | Rewrites the README's first screen; optional Chinese/English twin | `README.md` |
| [`launch-posts`](skills/launch-posts/SKILL.md) | Picks channels and drafts one native post per channel | `.megaphone/posts/*.md` |
| [`launch-plan`](skills/launch-plan/SKILL.md) | Dated, timezone-aware launch calendar and a log | `.megaphone/plan.md` |
| [`launch-review`](skills/launch-review/SKILL.md) | Star history, traffic and per-post attribution | `.megaphone/report.md` |

### Channel playbooks

Each one covers fit, rules, format, timing, a template and pitfalls — and links to the
platform's own rules where they exist. [Browse all →](skills/launch-posts/channels)

**Global:** [Hacker News](skills/launch-posts/channels/hacker-news.md) ·
[Reddit](skills/launch-posts/channels/reddit.md) ·
[Product Hunt](skills/launch-posts/channels/product-hunt.md) ·
[X / Bluesky](skills/launch-posts/channels/x-twitter.md) ·
[DEV & blogs](skills/launch-posts/channels/dev-blogs.md) ·
[Lobsters](skills/launch-posts/channels/lobsters.md) ·
[Awesome lists](skills/launch-posts/channels/awesome-lists.md) ·
[Newsletters](skills/launch-posts/channels/newsletters.md) ·
[GitHub itself](skills/launch-posts/channels/github-native.md)

**Chinese:** [V2EX](skills/launch-posts/channels/v2ex.md) ·
[HelloGitHub](skills/launch-posts/channels/hellogithub.md) ·
[阮一峰周刊](skills/launch-posts/channels/ruanyf-weekly.md) ·
[即刻](skills/launch-posts/channels/jike.md) ·
[小红书](skills/launch-posts/channels/xiaohongshu.md) ·
[掘金](skills/launch-posts/channels/juejin.md) ·
[知乎 / B 站 / 开源中国 / 少数派 / Gitee](skills/launch-posts/channels/china-other.md)
— written in Chinese, each with an English summary at the top.

### Web checker

[`docs/`](docs) is a static page (no build, no dependencies, no server) that scores any
public repo with the same rubric, recommends channels, and gives you a badge for your
README. It runs in the browser against GitHub's public API.

## How a launch runs

```text
audit ──▶ positioning ──▶ README first screen ──▶ channel posts ──▶ plan ──▶ (you post) ──▶ review
  │            │                   │                     │             │                        │
audit.md    brief.md           README.md            posts/*.md      plan.md               report.md
```

Everything lands in a `.megaphone/` folder in your repo so you can read, edit and
decide. Megaphone never publishes, submits or emails anything on your behalf.

## Principles

- **You publish; the agent drafts.** Platforms punish automation, and your name is on it.
- **Never ask for votes or stars.** It's against Hacker News, Product Hunt and Reddit
  rules, and it gets posts killed.
- **Honest claims only.** No invented numbers or testimonials; unknowns become `[TODO]`.
- **Native, not translated.** Chinese channels get posts written in Chinese, for that
  audience.

## FAQ

**Will this get me stars?** It gets your project in front of the people who'd want it,
in a form they'll actually try. Whether they star it is up to the project.

**Do I need a GitHub token?** Only for `launch-review`: GitHub lists stargazers only to
authenticated requests, and traffic data needs push access. Everything else works
without one.

**Is the checker private?** It runs entirely in your browser and only calls GitHub's
public API. Anonymous requests are limited to 60 per hour per IP; each check uses about five.

**My project is in Chinese / English only. Is that a problem?** No. Two languages is
worth 5 of the 100 points because it unlocks more channels — skip it if you don't need them.

## Contributing

Platforms change their rules; the playbooks are only as good as the last person who
checked them. If you notice drift, [open a "channel rule changed" issue](../../issues/new/choose)
or send a PR — every playbook has a "Last checked" line and links to its sources.
See [CONTRIBUTING.md](CONTRIBUTING.md) for adding a channel or changing the rubric.

Run the tests:

```bash
python3 -m unittest discover -s tests       # launch-review script
python3 -m http.server 8820                  # then open http://localhost:8820/tests/ for the checker
```

Questions and launch stories are welcome in [Discussions](../../discussions).

## License

[MIT](LICENSE)
