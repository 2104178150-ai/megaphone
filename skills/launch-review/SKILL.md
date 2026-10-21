---
name: launch-review
description: Measure a launch — pull GitHub star history and traffic (views, clones, referrers), line them up against the launch log, and report what happened after each post, plus what to do next. Use after a launch or post, when the user asks "did it work", "which channel worked", "how many stars from HN", or says 复盘 / 效果怎么样 / 哪个渠道有用.
---

# Launch review

Closes the loop: what happened after each post, measured, not guessed. Uses the
bundled script `scripts/stars.py` (Python 3.8+, standard library only; IANA zone names
such as `Asia/Shanghai` need Python 3.9+).

## Steps

Read `.megaphone/decisions.md` first (timezone, where the user posted) and record new
answers or, with no human available, assumptions there.

1. **Make sure data exists.**
   - `.megaphone/log.csv` with the header `date,time,channel,url,notes`: `date` as
     YYYY-MM-DD, `time` as 24-hour HH:MM in the user's timezone (the one in
     `decisions.md`). If `time` is unknown, leave it empty: the script then counts from
     the start of that day and marks the row "(time not logged)". `channel` is the draft
     file's base name (`hacker-news`, `reddit-commandline`, `v2ex`). If the log is
     missing, ask the user what they posted and when, and create it; with no human
     available, run without a log and say in the report that posts couldn't be attributed.
   - A GitHub token is **required**: GitHub only lists stargazers to authenticated
     requests, and it announced in June 2026 that it is limiting the stargazer list to the
     repo's admins and collaborators (others may get a 403 or an empty list), so use the
     maintainer's token. Traffic data needs push access to the repo (for a fine-grained
     token, the "Administration" repository permission, read). The script reads
     `GITHUB_TOKEN` or `GH_TOKEN`; if neither is set and the `gh` CLI is installed, suggest
     `export GITHUB_TOKEN=$(gh auth token)`, otherwise a fine-grained token from
     https://github.com/settings/personal-access-tokens/new.
   - **The user sets the token in their own shell.** Never ask them to paste it into the
     chat, never print it (no `echo $GITHUB_TOKEN`), and never write it to a file, `.env`
     or a commit.
2. **Run the script** from the root of the user's repo:

   ```bash
   python3 <this-skill-dir>/scripts/stars.py OWNER/REPO --tz Asia/Shanghai --log .megaphone/log.csv --snapshot --snapshot-dir .megaphone/snapshots --days 30 --out .megaphone/report-data.md
   ```

   - **Paths.** `<this-skill-dir>` is the folder that holds this `SKILL.md`. `--log`,
     `--snapshot-dir` and `--out` are relative to the current directory, so run it from
     the user's repo root.
   - **`--tz` is the zone the times in `log.csv` were written in**, the same one as in
     `plan.md`. Give an IANA name (`Asia/Shanghai`, `America/New_York`), which uses the
     right DST offset for each post's date, or an offset (`+08:00`, `-05:30`), which is
     fixed, so it's wrong for posts on the other side of a DST switch. Days in the report
     ("Stars per day", "Best day") are counted in that zone too. Without `--tz` the script
     uses this machine's zone, which is wrong in a cloud sandbox or CI, so always pass it.
   - **`--snapshot`** saves today's traffic (views, clones, referrers, popular pages) to
     `.megaphone/snapshots/YYYY-MM-DD-OWNER__REPO.json` (UTC date; the report only reads
     snapshots of the repo you asked about). GitHub only keeps the last 14 days,
     so snapshot at T+2, T+5, T+9 and T+14 (the same cadence as `plan.md`).
   - **`--days`** must reach back past the first post; if it doesn't, that post's row says
     which value to rerun with.
   - **What the report merges.** Daily views and clones are merged across all snapshots
     (GitHub counts them per UTC day). Referrers and popular pages are only ever GitHub's
     top 10 for the 14 days before each snapshot, so they can't be added up or split by
     day. The report shows the latest list, plus one row per snapshot so early-launch
     referrers stay visible after they leave GitHub's window.
   - **Snapshots are private data.** GitHub shows traffic only to people with push access.
     Keep `.megaphone/` in `.gitignore` (the default); the script warns if a snapshot isn't
     ignored. Don't quote referrers or traffic numbers in public posts unless the user
     chooses to.
   - Log rows the script can't read are skipped and listed under **Notes** in the report.
     Fix them in `log.csv` and rerun before writing the report.
   - For repos with more than ~40k stars GitHub may not return timestamps for every star
     (a commonly reported limit); the script says so when it happens.
3. **Read the output** and write `.megaphone/report.md`:
   - **Headline**: stars gained in the window, the best day (in the log's timezone; the
     script labels it), and what was posted that day.
   - **Per post**: stars in the 48 hours after each post, from the script. A window that
     hasn't closed yet says "so far". Posts less than 48 hours apart share those stars;
     the Overlaps column lists them both ways, so name the overlap instead of splitting
     the credit.
   - **Referrers, separately**: they're 14-day totals per snapshot, not per post. Matching a
     referrer (`news.ycombinator.com`, `reddit.com`, `v2ex.com`, `github.com` for Trending
     or topic pages) to a post is a judgement call from timing: write "likely", and give
     the snapshot date it came from.
   - **Views vs. clones**: views say people looked; clones suggest someone tried it. Treat
     clones as a rough signal: automated clones (CI, mirrors) are commonly reported to be
     counted too.
   - **Attribution caveats**: overlapping posts share credit; stars lag views; Chinese
     apps often send no referrer (traffic shows as direct); rows marked "(time not
     logged)" are counted from the start of that day.
   - **What to do next**: double down on the channel that worked (follow-up post,
     related subreddit, write-up), fix what visitors complained about, and plan the next
     milestone worth announcing.
4. **Summarise in chat** in five lines or fewer.

## Reading the numbers

These are rules of thumb, not measurements:

- Compare against the **baseline before any promotion** (for example, one star every 2–3 days).
  A channel worked if the days after it beat that, not if it produced "some" stars.
- **Small samples say nothing yet.** Five views and no likes, or nine visitors and no stars, is
  within normal noise; wait for tens to hundreds before judging a channel or a page.
- Visits but no stars → check the funnel: does the landing page speak the visitor's language,
  is the fastest try one click, and is there proof someone else got value?

- A Show HN on the front page often shows up as a sharp one-day spike; Reddit and V2EX
  are smaller but more engaged (look at issues and comments, not only stars).
- Views ↑ but stars flat → the README isn't converting; rerun `launch-audit`.
- Stars ↑ but no issues/discussions → curiosity, not usage; ask for feedback explicitly.
- Referrer `github.com` rising after a burst → probably Trending or topic pages.
- Comparing with similar projects? Look at forks and issues too. In our 2026-10 sample, 67–88% of
  recently updated new repos with 20–99 stars had no forks at all, which looks like star farming
  (`../../research/2026-10-new-repos.md`). Never buy stars: GitHub's Acceptable Use
  Policies ban "rank abuse, such as automated starring".
