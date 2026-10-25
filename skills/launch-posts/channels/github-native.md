# GitHub itself

> Last checked: 2026-10-25 against GitHub Docs: [topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics),
> [social preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview),
> [viewing traffic](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository),
> [traffic API](https://docs.github.com/en/rest/metrics/traffic) and
> [starring API](https://docs.github.com/en/rest/activity/starring). Stargazer access
> re-tested the same day (an unauthenticated request returns 401).

## Fit

Every other channel sends people *here*. Set these up before any launch post — they
cost minutes and keep working.

## Rules (from GitHub Docs)

- **Topics**: lowercase letters, numbers and hyphens; 50 characters or less; **no more
  than 20 topics**. Topic names are always public.
- **Social preview**: PNG, JPG or GIF **under 1 MB**; at least **640×320**, **1280×640**
  for best display. Transparent PNGs work, but check how they look on dark and light
  backgrounds.
- **Traffic**: anyone with push access can see clones, visitors from the **past 14
  days**, referring sites and popular content. The API returns the top 10 referrers and
  top 10 pages over the last 14 days, for repos you have write access to.
- **Stars**: listing stargazers requires authentication. With
  `Accept: application/vnd.github.star+json` each stargazer comes with a `starred_at`
  timestamp.

## Format (the checklist)

- **Description** (About box): the one-liner, under ~160 characters, no emoji soup.
  (160 is Megaphone's rubric limit so it isn't cut off in cards and search results — a
  heuristic, not a GitHub limit.)
- **Topics**: specific ones people search for: language, category, use case (`cli`,
  `self-hosted`, `markdown`, `llm`, `rust`). Add up to GitHub's 20; don't remove relevant
  existing topics just to hit a smaller number. Topic pages are browsable, so specific
  beats generic.
- **Website** field: a demo or docs URL, not the repo's own GitHub URL.
- **Social preview image** (Settings → General): the card shown when the repo is shared
  on X, Slack, WeChat, Discord. Show the product and the one-liner in large text.
- **Pin the repo** on your profile and your organisation's profile.
- **A release** (v0.1.0 is fine) with notes. Releases make the repo look alive and
  give people something to watch.
- **Discussions** on, or a clear place for questions — launch traffic brings questions.
- **Good first issues** labelled, so launch visitors who want to help can start.

## Timing

Do all of this in the prep week, before the first post: shares made before the social
preview is set show the default card. Cut the release a few days before the big
channels so its date looks current (heuristic).

## Template

```
About → Description: <one-liner from the brief, ≤ ~160 chars>
About → Website:     <demo or docs URL, not the repo>
About → Topics:      <language>, <category>, <use case>, … (keep relevant existing ones; max 20)

Release <vX.Y.Z> — <YYYY-MM-DD>
<One sentence: what it is and who it's for.>

## Highlights
- <user-visible change or feature>
## Install
<one command>
## Known limitations
- <honest limit>
```

## GitHub Trending

GitHub doesn't publish the Trending algorithm. It's widely observed to reward **star
velocity** (stars gained in a short window, relative to the repo's usual pace) rather
than total stars. Practical consequences (heuristics):

- Concentrate your biggest channels within a few days instead of spreading one post a
  week — a burst is more likely to trend than a trickle.
- Trending itself brings a second wave of visitors, so be ready (README polished,
  issues answered) *before* the burst.
- Third-party trackers such as [Trendshift](https://trendshift.io) record daily
  Trending positions if you want to see when you charted.

## Measuring

- **Star history**: [star-history.com](https://star-history.com), or
  `launch-review`'s `stars.py`, which reads `starred_at` from the stargazers API. GitHub
  only lists stargazers to authenticated requests, so it needs a token.
- **Referrers and views**: Insights → Traffic, or the traffic API. It keeps only the
  **last 14 days** and needs push access, so snapshot it regularly during a launch
  (`stars.py --snapshot`). Snapshots hold traffic data only maintainers can normally
  see; keep `.megaphone/` out of public commits.

## Pitfalls

- Generic topics only (`awesome`, `tool`) → invisible on topic pages.
- No social preview → shares show a default card.
- Launching with zero releases and the last commit months ago → looks abandoned.
