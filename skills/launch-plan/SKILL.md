---
name: launch-plan
description: Turn launch drafts into a dated, timezone-aware launch calendar — prep tasks, which channel on which day and hour, who answers comments, and a log the results can be measured against. Use when the user asks when/in what order to post, wants a launch schedule or checklist, or says 发布计划 / 排期 / 什么时候发 / 先发哪个.
---

# Launch plan

A launch is a sequence, not a single post. The plan protects the user's attention (one
big channel per day, so every thread gets answered), concentrates traffic into a burst
(which is what GitHub Trending rewards), and records everything so `launch-review` can
tell what worked.

## Inputs

- `.megaphone/posts/*.md` (from `launch-posts`) and `.megaphone/brief.md`
- The user's timezone, launch date preference, and which days/hours they're free
- Any fixed dates: HelloGitHub publishes on the **28th** of each month; 阮一峰周刊 on
  **Fridays** — submit a few days before, inclusion isn't guaranteed

## Principles

1. **Ready before loud.** Day 0 is fixing the repo (audit items, README, release, social
   preview). No big channel until the audit says "Almost there" or better.
2. **Compounding channels first.** Topics, awesome-list PRs and newsletter submissions
   cost little and pay out over weeks; start them in the prep week.
3. **One big channel per day.** Show HN, Product Hunt, a big subreddit, V2EX — never two
   the same day. You need 2–4 hours per launch to answer comments.
4. **Cluster the big days.** Put the big channels within roughly a week so star velocity
   peaks together.
5. **Timezones.** Global channels are usually best in US morning hours; Chinese channels
   in Beijing working hours/evenings. Convert both to the user's local time and flag
   sleep conflicts honestly — a reply 8 hours later is a missed launch.
6. **Leave slack.** Something will break when real users arrive. Keep a buffer day after
   the biggest launch to fix bugs and post "thanks, fixed X" updates.

## Output — `.megaphone/plan.md`

```markdown
# Launch plan — <project>
Timezone: <user tz> · Launch week: <dates>

## Prep (T-7 → T-1)
- [ ] Fix audit blockers: …
- [ ] Release v0.x with notes
- [ ] Social preview image uploaded
- [ ] Demo GIF in README
- [ ] Awesome-list PRs: <lists>
- [ ] Newsletter submissions: <which>
- [ ] Warm up accounts: comment genuinely on HN / Reddit / V2EX this week

## Launch days
| Day | Local time | Channel | Draft | Owner | Reply window |
|---|---|---|---|---|---|
| T+0 Tue | 17:00 | Show HN | posts/hacker-news.md | you | 17:00–21:00 |
| T+1 Wed | 10:00 | V2EX 分享创造 | posts/v2ex.md | you | 10:00–13:00 |
| … |

## After
- [ ] T+2: post "what I learned / what's fixed" on X / 即刻
- [ ] T+3: snapshot traffic (`python3 stars.py <repo> --snapshot`)
- [ ] T+7: run launch-review
```

Also create `.megaphone/log.csv` with this header if it doesn't exist, and tell the user
to add a row **right after** each post goes live (the URL matters for attribution):

```csv
date,time,channel,url,notes
```

## Finish

Summarise the plan in chat as a short day-by-day list in the user's local time, and
point out the one or two most important prep items.
