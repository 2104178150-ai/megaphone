# What 362 new open-source projects show about launch readiness

English | [简体中文](2026-10-new-repos.zh-CN.md)

October 2026. We scored 362 public GitHub repos created in August and September 2026 with
Megaphone's [21-check rubric](../skills/launch-audit/rubric.md), in four star bands, to see how
the new projects that got noticed differ from the ones that didn't.

**In short**

- **Projects that got noticed look finished.** Compared with 5–99★ projects, those with 100+ stars
  more often have a screenshot or GIF in the first screen (68% vs 40%), a getting-started section
  (89% vs 74%), a licence (96% vs 81%), a release (82% vs 63%), badges (66% vs 38%), a community
  link (51% vs 27%), issue templates (50% vs 28%) and a second-language README (33% vs 15%).
- **Some things don't differ at all:** the description, the tagline, README length, a feature
  list, an early code block, a "why" section, a code of conduct.
- **The score tracks stars only loosely** (Spearman ρ = 0.34). A third of 100★+ projects score 80
  or more, against one in seven below 100.
- **Watch out for stars with no forks.** Among the 300 most recently updated new repos with 20–99
  stars, 67% to 88% had not a single fork, across three searches within an hour. The ones we
  looked at were mostly look-alike "trainer", "mod" and "vault" repos with 50–70 stars each.

## What differs, and what doesn't

Share of repos passing each check: 200 repos with 100+ stars against 162 with 5–99 stars. *p* is a
two-sided Fisher exact test; with groups this size, gaps under about 10 points can be chance.

| Check | 100★+ | 5–99★ | *p* |
|---|---|---|---|
| Screenshot, GIF or video in the first screen | 68% | 40% | <0.001 |
| Badges | 66% | 38% | <0.001 |
| Community channel (Discussions, or a Discord / Telegram / 微信群 link) | 51% | 27% | <0.001 |
| Issue templates | 50% | 28% | <0.001 |
| At least one release | 82% | 63% | <0.001 |
| Two languages | 33% | 15% | <0.001 |
| Licence | 96% | 81% | <0.001 |
| Getting-started section | 89% | 74% | <0.001 |
| One step to try it (a command or a website) | 86% | 75% | 0.016 |
| Contributing guide | 56% | 44% | 0.020 |
| Website or demo link in the About box | 56% | 47% | 0.073 |
| At least 3 topics | 63% | 54% | 0.086 |
| "Why" or comparison section | 25% | 19% | 0.16 |
| Code of conduct | 22% | 19% | 0.52 |
| Code block early in the README | 76% | 80% | 0.53 |
| Shows what it does (features, examples) | 73% | 72% | 0.81 |
| Description, tagline, 150+ words | 74–98% | 70–98% | ≥0.41 |
| Title heading at the top | 87% | 94% | 0.034 |

The last row runs the other way: more popular READMEs often open with a centred logo or banner
instead of a heading.

By band:

| Stars | Repos | Median score | Share scoring 80+ |
|---|---|---|---|
| 5–19 | 100 | 60 | 12% |
| 20–99 | 62 | 60.5 | 16% |
| 100–499 | 100 | 72.5 | 28% |
| 500+ | 100 | 74.5 | 39% |

READMEs written mainly in Chinese (51 of 362, spread across all four bands) pass the
two-languages check far more often than those in Latin script: 57% against 19%.

## What we take from it

- **Show it working on the first screen.** A screenshot or GIF is the biggest gap we found, and
  it's entirely in your hands before launch. That matches the rubric, where the visual and a
  one-step try are the two biggest checks.
- **Add the cheap trust signals before you post:** a licence and a tagged release.
- **Don't fake the rest.** Badges, a community link and issue templates are also far more common
  above 100 stars, but projects often add them once people show up. This is correlation, not
  cause.
- **A second language is still rare in Latin-script READMEs (19%),** so it's an opening if you'll
  post in Chinese or another language's channels.
- **Don't compare your stars with repos that have no forks,** and never buy stars: GitHub's
  [Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies)
  ban "rank abuse, such as automated starring or following".

## Method

- **Sample.** GitHub search for repos created 2026-08-01..2026-09-30 that are public and neither
  forks nor archived, in four star bands: 5–19, 20–99, 100–499, 500+. From the 300 most recently
  updated results in each band we drew 100 at random (seed 1024), on 2026-10-21. The 20–99 band
  had only 62 left after the exclusions below, so we took all of them.
- **Left out.** Templates; names starting with "awesome"; names or descriptions with the words
  dotfiles, homework, leetcode, course, interview, cheatsheet, tutorial or study-notes; repos
  with 20+ stars and no forks; one repo with no README. We can't check who starred the no-fork
  repos: GitHub now shows a repo's stargazers only to its admins and collaborators, so this is a
  pattern, not proof of farming.
- **Scoring.** [`audit.py`](../skills/launch-audit/scripts/audit.py), the same rubric as the
  [web checker](https://2104178150-ai.github.io/megaphone/). Language is the main script of the
  README's prose.
- **Limits.** One point in time; "recently updated" order favours active repos; the rubric checks
  a README's shape, not whether the project is good; stars measure attention, not use. A first,
  smaller draw (200 repos, looser filters) agreed on licence, releases, badges, the second
  language and the community link, but showed a much smaller screenshot gap (60% vs 51%):
  samples of a few hundred still move around.

Run it yourself (needs a GitHub token; about 5 API calls per repo):

```bash
python3 scripts/study.py sample --created 2026-08-01..2026-09-30 --per-stratum 100 --out .megaphone/research/study.jsonl
python3 scripts/study.py report .megaphone/research/study.jsonl
```

We publish totals only, not a list of the repos: the point is the pattern, not other people's
projects.
