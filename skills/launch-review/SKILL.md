---
name: launch-review
description: Measure a launch — pull GitHub star history and traffic referrers, line them up against the launch log, and report which channels actually brought stars and visitors, plus what to do next. Use after a launch or post, when the user asks "did it work", "which channel worked", "how many stars from HN", or says 复盘 / 效果怎么样 / 哪个渠道有用.
---

# Launch review

Closes the loop: what happened after each post, measured, not guessed. Uses the
bundled script `scripts/stars.py` (Python 3.8+, standard library only).

## Steps

1. **Make sure data exists.**
   - `.megaphone/log.csv` with `date,time,channel,url,notes` rows. If it's missing, ask
     the user what they posted and when, and create it.
   - A GitHub token is **required**: GitHub only lists stargazers to authenticated
     requests. Any token works for star history; traffic data (views, referrers) needs
     push access to the repo. The script reads `GITHUB_TOKEN` or `GH_TOKEN`; if neither
     is set and the `gh` CLI is installed, suggest `export GITHUB_TOKEN=$(gh auth token)`,
     otherwise a fine-grained token from github.com/settings/personal-access-tokens.
     Ask the user to set it in their own shell. Never print, store or commit the token.
2. **Run the script** from the repo root (the path is relative to this skill's folder):

   ```bash
   python3 <this-skill-dir>/scripts/stars.py OWNER/REPO --log .megaphone/log.csv --days 30 --snapshot --out .megaphone/report-data.md
   ```

   - `--snapshot` saves today's traffic (views, clones, referrers, popular paths) to
     `.megaphone/snapshots/`. GitHub only keeps 14 days of traffic, so run it every few
     days during a launch; the report merges all snapshots.
   - For repos with more than ~40k stars GitHub may not return timestamps for every
     star; the script says so when it happens.
3. **Read the output** and write `.megaphone/report.md`:
   - **Headline**: stars gained in the window, best day, and what was posted that day.
   - **Per channel**: stars in the 48 hours after each post (the script computes this)
     and matching referrers (e.g. `news.ycombinator.com`, `reddit.com`, `v2ex.com`,
     `github.com` for Trending/topic pages).
   - **Attribution caveats**: overlapping posts share credit; stars lag views; Chinese
     apps often send no referrer (traffic shows as direct).
   - **What to do next**: double down on the channel that worked (follow-up post,
     related subreddit, write-up), fix what visitors complained about, and plan the next
     milestone worth announcing.
4. **Summarise in chat** in five lines or fewer.

## Reading the numbers

- A Show HN on the front page often shows up as a sharp one-day spike; Reddit and V2EX
  are smaller but more engaged (look at issues and comments, not only stars).
- Views ↑ but stars flat → the README isn't converting; rerun `launch-audit`.
- Stars ↑ but no issues/discussions → curiosity, not usage; ask for feedback explicitly.
- Referrer `github.com` rising after a burst → probably Trending or topic pages.
