# GitHub itself

> Last checked: 2026-10 against GitHub Docs: [topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics),
> [social preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview),
> [traffic API](https://docs.github.com/en/rest/metrics/traffic).

Every other channel sends people *here*. Set these up before any launch post — they
cost minutes and keep working forever.

## Checklist

- **Description** (About box): the one-liner, under ~160 characters, no emoji soup.
- **Topics**: 3–8 specific topics (GitHub allows up to 20). Use the words people search
  for: language, category, use case (`cli`, `self-hosted`, `markdown`, `llm`, `rust`).
  Topic pages are browsable, so specific beats generic.
- **Website** field: demo or docs URL.
- **Social preview image** (Settings → General): GitHub recommends **1280×640** (at
  least 640×320), PNG/JPG/GIF under 1 MB. This is the card shown when the repo is
  shared on X, Slack, WeChat, Discord. Show the product and the one-liner, large text.
- **Pin the repo** on your profile and your organisation's profile.
- **A release** (v0.1.0 is fine) with notes. Releases make the repo look alive and
  give people something to watch.
- **Discussions** on, or a clear place for questions — launch traffic brings questions.
- **Good first issues** labelled, so launch visitors who want to help can start.

## GitHub Trending

GitHub doesn't publish the Trending algorithm. It's widely observed to reward **star
velocity** (stars gained in a short window, relative to the repo's usual pace) rather
than total stars. Practical consequences:

- Concentrate your biggest channels within a few days instead of spreading one post a
  week — a burst is more likely to trend than a trickle.
- Trending itself brings a second wave of visitors, so be ready (README polished,
  issues answered) *before* the burst.
- Third-party trackers such as [Trendshift](https://trendshift.io) record daily
  Trending positions if you want to see when you charted.

## Measuring

- **Star history**: [star-history.com](https://star-history.com), or
  `launch-review`'s `stars.py`, which uses the stargazers API with
  `Accept: application/vnd.github.star+json` to get `starred_at` timestamps. GitHub
  only lists stargazers to authenticated requests, so it needs a token.
- **Referrers and views**: Insights → Traffic, or the traffic API. It keeps only the
  **last 14 days** and needs push access, so snapshot it regularly during a launch
  (`stars.py --snapshot`).

## Pitfalls

- Generic topics only (`awesome`, `tool`) → invisible on topic pages.
- No social preview → shares show a grey default card with your avatar.
- Launching with zero releases and the last commit months ago → looks abandoned.
