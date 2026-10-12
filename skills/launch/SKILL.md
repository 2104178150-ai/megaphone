---
name: launch
description: End-to-end launch of an open-source project or GitHub repo — audit readiness, sharpen positioning, rewrite the README first screen, draft channel-specific posts, schedule the launch, then track which channel worked. Use when the user wants to launch, promote, announce, market or "get stars" for a repo, side project or developer tool, or says things like 推广我的项目 / 发布开源项目 / 冷启动 / 怎么让更多人用 / 涨 star.
---

# Launch (Megaphone orchestrator)

You are the user's launch crew. Your job is to get a real project in front of the
people who would genuinely want it — not to farm stars. Every step produces a file
the user can review, so nothing goes out without their say-so.

## Ground rules

- **Never post, submit, email or DM anything yourself.** You draft; the user publishes.
  Platforms punish automated or vote-seeking behaviour, and the user's reputation is
  on the line.
- **Never ask anyone for upvotes or stars, and never suggest it.** Hacker News, Product
  Hunt and Reddit all treat vote-rings as abuse.
- **Be honest about the project.** No invented user counts, benchmarks or testimonials.
  If a claim needs a number the user hasn't given you, ask or leave a `[TODO]`.
- **Write in the user's language**, but write each post in the language its channel
  reads (English for HN/Reddit/PH, Chinese for V2EX/HelloGitHub/即刻/小红书, etc.).

## Workspace

Keep everything in a `.megaphone/` folder at the repo root:

| File | Written by | Purpose |
|---|---|---|
| `.megaphone/audit.md` | launch-audit | Readiness score and fix list |
| `.megaphone/brief.md` | launch-positioning | One-liner, audience, proof, contrast |
| `.megaphone/posts/<channel>.md` | launch-posts | Ready-to-paste drafts |
| `.megaphone/plan.md` | launch-plan | Dated launch calendar |
| `.megaphone/log.csv` | user / launch-review | What was actually posted, when, where |
| `.megaphone/report.md` | launch-review | Which channel moved the needle |

Ask the user whether `.megaphone/` should be committed or added to `.gitignore`.

## Pipeline

Run the stages in order. Each one has its own skill in a sibling folder; read that
skill's `SKILL.md` and follow it. Stop after each stage, show the user the result in a
few lines, and ask before moving on — they may want to fix things first.

1. **Audit** → `../launch-audit/SKILL.md`. Is the repo ready to receive visitors?
   Fix blockers before spending any launch: a visitor who bounces off a broken README
   is a visitor you don't get twice.
2. **Positioning** → `../launch-positioning/SKILL.md`. Who is it for, what's the
   one-sentence promise, why now, why this over the alternatives.
3. **README first screen** → `../launch-readme/SKILL.md`. Apply the positioning to
   the top of the README: title, tagline, visual, three bullets, one-command start.
4. **Posts** → `../launch-posts/SKILL.md`. Pick channels that fit, then draft one post
   per channel following that channel's playbook in `../launch-posts/channels/`.
5. **Plan** → `../launch-plan/SKILL.md`. Turn the posts into a dated sequence with
   preparation tasks and a log template.
6. **Review** (after the launch) → `../launch-review/SKILL.md`. Pull star history and
   referrers, line them up against the log, and report what worked.

If the user asks for only one stage ("just write me a Show HN post"), jump straight to
that skill — but if `.megaphone/brief.md` doesn't exist yet, do a quick positioning
pass first (five minutes, not the full interview), because every post depends on it.

## Before you start

Gather context from the repo itself before asking anything: README, package manifest
(`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`…), license, docs, examples,
screenshots, releases, and `git log --oneline | head -50`. Then ask the user only what
the repo can't tell you:

- Who did you build this for, and what were they doing before it existed?
- Is there a live demo, hosted version or GIF? If not, can we make one?
- Which channels can you actually post from? (Accounts on HN, Reddit, X, V2EX, 即刻,
  小红书… and how old/active they are — new accounts get filtered.)
- Any launch date constraints?

## Finish

End with a short summary: score before/after, the one-liner, which posts are ready,
the date of the first post, and what the user has to do by hand.
