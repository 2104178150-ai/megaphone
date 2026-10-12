---
name: launch-posts
description: Pick the developer channels that fit a project and draft a ready-to-paste launch post for each, following that channel's rules and culture — Show HN, Reddit, Product Hunt, X/Twitter, DEV, Lobsters, awesome lists, newsletters, V2EX, HelloGitHub, 阮一峰科技爱好者周刊, 即刻, 小红书, 掘金, 知乎 and more. Use when the user wants to announce or promote a project, write a Show HN / Reddit / Product Hunt post, or says 写推广文案 / 发 V2EX / 投稿 HelloGitHub / 小红书怎么发.
---

# Launch posts

Each channel has its own audience, rules and taboos. A post that wins on Show HN gets
removed on r/programming and ignored on 小红书. This skill chooses channels on purpose
and writes one native post per channel.

## Inputs

- `.megaphone/brief.md` (run `../launch-positioning/SKILL.md` first if missing)
- The README, especially the quick start and visual
- Which accounts the user has, and how established they are

## Step 1 — Choose channels

Read [channels/README.md](channels/README.md) for the full map. Score each candidate
channel on three questions and keep the top 3–6:

1. **Audience fit** — do the people in this channel have the problem?
2. **Format fit** — can this project be shown the way the channel likes (runnable demo
   for Show HN, screenshot-led for 小红书, story for 即刻)?
3. **Account fit** — does the user have a non-brand-new account there? (New accounts
   get filtered on HN, Reddit and V2EX.)

Always consider the zero-risk, compounding channels too: GitHub topics and social
preview, relevant awesome lists, and newsletters that take submissions.

Tell the user which channels you picked, which you skipped and why, in a short table.

## Step 2 — Draft one post per channel

For each chosen channel, open its playbook in `channels/` and follow it exactly:
title rules, length, language, links, what to put in the first comment, and the
pitfalls list. Then write `.megaphone/posts/<channel>.md` with:

```markdown
# <Channel> — draft
Where: <exact URL or node/subreddit to post in>
When: <best window from the playbook, in the user's timezone>
Account: <which account should post>

## Title
…

## Body
…

## First comment / follow-up (if the channel uses one)
…

## Checklist before posting
- [ ] Rule check: <the 1–3 rules most likely to get this removed>
- [ ] Links work and point to the repo/demo
- [ ] You can answer comments for the next 2–3 hours
```

### Writing rules for every channel

- **Lead with the problem or the result, not the tech stack.** The stack goes in the
  second paragraph for technical audiences.
- **Say you made it.** Disclosure is required on Reddit and expected everywhere else.
- **One link, the right one.** Usually the repo; a live demo for Show HN if it needs no
  sign-up; never a landing page with an email gate.
- **Be specific and modest.** Real numbers and limitations build more trust than
  adjectives. Include a "what it doesn't do yet" line.
- **Never ask for upvotes, stars or likes**, and never coordinate friends to vote.
  It's against HN, Product Hunt and Reddit rules and gets posts killed.
- **Native language and tone.** Write Chinese channels in Chinese from scratch; don't
  translate the English post. Match each channel's register (HN: plain and technical;
  即刻: personal; 小红书: visual and benefit-first).
- **No two posts identical.** Cross-posting the same text is a spam signal on Reddit
  and annoys people who follow you in several places.

## Step 3 — Hand off

Summarise in chat: the channel table, where each draft is, and the order you'd post
them in (or hand off to `../launch-plan/SKILL.md` for a dated schedule). Remind the user
that they publish manually and should log each post in `.megaphone/log.csv` so
`launch-review` can attribute results.
