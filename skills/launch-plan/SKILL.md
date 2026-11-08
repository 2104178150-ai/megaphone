---
name: launch-plan
description: "Turn launch drafts into a dated launch calendar in the user's own timezone — a readiness gate with a go/no-go, prep tasks, which channel on which day and hour, and the log and traffic snapshots launch-review measures against. Use when the user asks when or in what order to post, wants a launch schedule or checklist, or says 发布计划 / 排期 / 什么时候发 / 先发哪个."
---

# Launch plan

A launch is a sequence, not a single post. The plan gets the repo ready before traffic
arrives, keeps to one big channel per day so every thread gets answered, and logs what
happened for `launch-review`. `plan.md` is the only file with dates (posts carry a time
window), so reschedule here. Write it in the user's language. `<megaphone-skills-dir>` is
the folder that holds this skill and its siblings.

## Inputs

- `.megaphone/posts/README.md` and `posts/*.md`: channels, where, which account, window.
- `.megaphone/brief.md` (*Claims we won't make*, disclaimer) and `audit.md` (blockers,
  level, *Risk & readiness*).
- `.megaphone/decisions.md`: timezone (IANA name, e.g. `Asia/Shanghai`), when the user can
  spend 2–4 hours replying, languages, accounts, date constraints, how loud to go. Ask for
  what's missing and record it; if nobody can answer, record an assumption there and mark
  it `[assumed]` in the plan.
- Launch material already in the repo (`docs/launch*`): reuse what's accurate, note changes.

## The gate

This is the one definition of the gate; other skills point here.

- **Every channel** waits until every blocker in `audit.md` is closed — awesome-list PRs,
  submissions and small rooms included. An `unverified` blocker counts as not closed until
  someone has run the quick start.
- **Big channels** (below) also need the level to be 🔊 Almost there or better, judged on
  the human-adjusted score when the audit gives one, otherwise the rubric score — out of
  100, before any trade-off rescaling.
- **Plugins and extensions** also wait until the store or plugin-directory listing is live
  ([ecosystems.md](../launch-posts/channels/ecosystems.md): review times aren't promised, and
  announcements should link to a live listing).

- **T-2 README.** If `.megaphone/readme-first-screen.md` exists, the user applies or
  rejects it before the re-audit, and any draft written against it is checked again.
- **T-2 re-audit.** With the fixes pushed, rerun `launch-audit` (or
  `python3 <megaphone-skills-dir>/launch-audit/scripts/audit.py OWNER/REPO`), re-check each
  blocker by hand — the script can't see them — and update `audit.md`. An `unverified`
  blocker should be settled as soon as the user can run the quick start from a clean setup
  (it holds back the prep-week channels too); this is the last chance, and it becomes closed
  or open.
- **T-2 go/no-go.** Go only if the gate holds and prep is done. Otherwise (a blocker is
  still open, say) move the **whole schedule by a week** rather than squeezing channels.
  Record the call in `decisions.md`.

## Prep (T-7 → T-1)

Size this against the user's free hours; if it doesn't fit, move the launch week.

1. **Fix the blockers**, then the High items in `audit.md`.
2. **Risk wording**: nothing from brief → *Claims we won't make* in the README, docs or
   drafts; the disclaimer in the README if the project touches other platforms. If a
   louder launch raises exposure, ask how loud to go; going quieter (fewer channels, spread
   out) is a valid answer.
3. **Capacity** (hosted demo or API): quotas, rate limits and upstream limits known; a
   clear overload message instead of a blank error; a fallback (local CLI, self-host); a
   way to notice it's down.
4. **Release** with notes; description, topics, homepage; **social preview**
   (`../launch-posts/channels/github-native.md`); a **demo visual** in the README that the
   audience can load (for mainland-China channels, not only on `raw.githubusercontent.com`).
5. **Awesome-list PRs** once the README and demo are up; merges can take days or weeks.
6. **Warm up accounts genuinely** where you'll post: join threads you care about. Send
   the ask for each `ask first` row in the channel table early in prep; that space gets a
   slot in the calendar only after its maintainer or moderator says yes. Leave it out of
   Launch days until then; when the user reports a yes, rerun `launch-posts` for that row
   and add its slot here.
7. **Store or plugin listing** (plugins and extensions): submitted early in prep week,
   since review times aren't promised; announcements wait until it's live.
8. **Help first (optional, small projects)**: offer two or three specific fixes to a few
   similar, recently launched projects — one issue each, posted by the user after reading that
   repo's CONTRIBUTING file (if it bans AI-written issues, the user writes it), with the findings
   written out rather than a link to your own tool. If someone adopts them, ask whether you may
   show the before/after as a case study. Never ask for stars in return.
9. **Final drafts**: no `[TODO]` left in launch-week drafts; for author-written channels
   (Show HN, a DEV launch article, Lobsters, V2EX, 掘金, some awesome lists) the author has written the
   text from the fact sheet; each risk and AI-disclosure check ticked. Reddit drafts usually
   arrive with `[TODO]`s an agent can't clear (reddit.com blocks most agents): list each one
   here as a prep task for the user — the repost search, and the sidebar, rules page and
   pinned posts (including any fixed day or weekly thread; if one applies, move that row in
   plan.md) — so they're done before launch week, not on the morning of the post.

## Sequencing

- **One big channel per day.** Big = you must be live for 2–4 hours: Show HN, Product
  Hunt, a large subreddit, V2EX. A subreddit is large when you expect to be replying for 2+
  hours (rule of thumb, not a Reddit figure: over about 100k members). If you can't see the
  member count, ask the user; with no human, treat it as big and mark it `[assumed]` in
  plan.md. Submissions and posts
  to your own followers (X, 即刻) can share a day if you can still answer them.
- **Cluster the big days within about a week.** GitHub Trending is widely observed (not
  documented) to reward star velocity, so a burst does more than one post a week.
- **Before launch week, try small channels one at a time** if you don't yet know which ones work
  for this project: 2–3 days apart, so each one's effect shows up against the baseline in
  `launch-review`. Opening five on one day left us unable to tell which one brought anyone (our
  own launch). If prep is shorter than a week (asked on a Wednesday to launch next week, say)
  but its tasks still fit the user's hours (otherwise move the launch week), run the small
  tests at the start of launch week instead, 2 days apart, with the first big channel 2 days
  after the last test. T+0 is still the first post, so snapshot days count from the first
  test. The big days that follow keep to the two rules above.
- **Landing page before traffic.** Before each new channel, re-read the README as that channel's
  visitor (language, device, what they can click) — see the human review in
  `../launch-audit/SKILL.md`. Traffic sent to a page that doesn't speak the visitor's language
  is spent.
- **HelloGitHub after the fixes, not on day one.** It takes each repo once
  (`../launch-posts/channels/hellogithub.md`), so submit once the landing page works for its
  readers. Other channels allow another try, but a user's words or a before/after gives any post
  something to point at (a heuristic, not part of the gate).
- **Post inside the window, not when the draft is ready.** If it's ready at 3 a.m. for the
  audience, use the platform's scheduler or wait; on feed-ranked platforms a post's first hours matter most
  (a heuristic).
- **Smaller rooms before bigger ones**: a niche subreddit or language community before
  Hacker News or Product Hunt, so wording and bugs get fixed before the big day.
- **Buffer day after the biggest launch**: fix what broke, post "thanks, fixed X".
- **Newsletters in launch week**, after the README and demo are live (editors click once).
- **Fixed dates.** HelloGitHub publishes on the **28th** (we found no published
  cut-off: submit early in the month). 阮一峰周刊 publishes on **Fridays** (submitting
  Mon–Wed for that issue is a heuristic). Inclusion isn't guaranteed; don't build the
  burst on them.

## Timezones

- Posts carry each window in the playbook's own timezone; **this file is the only place
  it's converted**. Convert per date and show both: `23:00 (= 08:00 PT)`. If you move the
  schedule, recompute the conversions here — nothing in `posts/` needs to change. If a
  playbook gives no window, pick a time the user can cover and write "no data — chose X
  because Y".
- **Flag sleep conflicts honestly** with options: post at the edge of the window, stay up
  one night and recover on the buffer day, or give the slot to a channel that suits the
  user's hours. A reply eight hours late is a missed launch.
- **DST.** US: second Sunday of March, first Sunday of November. EU and UK: last Sunday of
  March and of October. China and Japan: none. Check whether the launch week straddles a
  switch: 09:00 PT is 17:00 in London on 2026-10-20 but 16:00 on 2026-10-27, and the HN
  heuristic (08:00–10:00 PT) is 23:00–01:00 Beijing time until 2026-11-01, 00:00–02:00
  after. Other regions: check the local rules.

## Output — `.megaphone/plan.md`

The example rows are for a user in Europe/London in the week of 2026-10-19. Compute your own.

```markdown
# Launch plan — <project>
Timezone: <IANA name> · Launch week: <YYYY-MM-DD → YYYY-MM-DD> · DST switch: <none / date>
Gate: open blockers <N> · unverified <N> · level <…> · go/no-go on <T-2 date>

## Prep (T-7 → T-1)
- [ ] Blockers: <each from audit.md> · risk wording · disclaimer in README
- [ ] Capacity: <limits> · overload message · fallback: <…>
- [ ] Release <version> · description, topics, homepage · social preview · demo visual
- [ ] Awesome-list PRs: <lists> · HelloGitHub / 阮一峰周刊: <dates> · warm-up: <where>
- [ ] Landing check per channel: <channel → first screen speaks its language, fastest try is clickable>
- [ ] HelloGitHub after the landing fixes: <date> · proof to point at: <user words / before-after / none yet>
- [ ] Help first (optional): <projects> · case-study permission: <yes / no / n/a>
- [ ] Store / plugin directory (if any): submitted <date> · live: <yes/no> — announcements wait
- [ ] Ask first (if any): <space → ask sent <date> · answer: pending / yes / no>
- [ ] Reddit checks by hand (agents can't read reddit.com): <r/sub → repost search · rules/sidebar/pinned · fixed day?>
- [ ] README proposal (readme-first-screen.md, if any): applied / rejected
- [ ] T-2 re-audit: <score, open blockers, unverified> · go/no-go: <go / moved to …>

## Launch days
| Day | Time (Europe/London) | Channel | Draft | Who replies | Reply window |
|---|---|---|---|---|---|
| T+0 Mon | 15:00 (= 10:00 ET) | r/commandline | posts/reddit-commandline.md | you | 15:00–17:00 |
| T+0 Mon | — | Newsletters: <which> | posts/newsletters.md | — | — |
| T+1 Tue | 17:00 (= 09:00 PT) | Show HN | posts/hacker-news.md | you | 17:00–21:00 |
| T+2 Wed | — | Buffer: fixes, "thanks, fixed X" | — | you | — |

## After
- [ ] T+2, T+5, T+9, T+14: traffic snapshot · T+7 or later: launch-review
```

**Log.** If `.megaphone/log.csv` is missing, create it with the header
`date,time,channel,url,notes`. The user adds a row **right after** each post goes live:
`date` YYYY-MM-DD, `time` 24-hour HH:MM in the timezone recorded in `decisions.md`,
`channel` the draft file's base name (`hacker-news`, `reddit-commandline`, `v2ex`), `url`
the live post.

**Snapshots.** GitHub keeps only 14 days of traffic, so snapshot at T+2, T+5, T+9 and T+14:

```bash
python3 <megaphone-skills-dir>/launch-review/scripts/stars.py OWNER/REPO --log .megaphone/log.csv --tz <IANA or ±HH:MM> --snapshot
```

`--tz` is the timezone from `decisions.md`; prefer the IANA name (a fixed offset is wrong
across a DST switch). The script needs `GITHUB_TOKEN` (push access for traffic), set by the
user in their own shell; never print or store it. Then run `launch-review` at T+7 or later.

## Finish

Summarise in chat: gate status and go/no-go date, a day-by-day list in the user's local
time (date, time, channel), any sleep or DST conflicts, the one or two prep items that
matter most, and a reminder to log each post and take the snapshots.
