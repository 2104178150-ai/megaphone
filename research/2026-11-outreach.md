# What happened when we sent 47 new projects two or three specific fixes

English | [简体中文](2026-11-outreach.zh-CN.md)

November 2026. Between 18 October and 11 November 2026 we opened 47 GitHub issues on new
open-source projects. Each one named two or three specific, low-effort fixes from a Megaphone
check (a licence, a screenshot on the first screen, a one-line install, a release…), said why, and
asked for nothing back. This page counts what came of it, as of 14 November 2026.

**In short**

- **At least one author in three changed their repo.** 14 of the 46 issues we can still read got a
  reply, and at least 14 projects changed their repo after our issue: 13 of the 14 who replied
  (the 14th said they'd do it later; not re-checked yet), plus one who changed it without replying.
- **Replies come within a day, or not for a while.** The median first reply took 23 hours; the
  fastest 10, the slowest 143 (six days).
- **Issues written in Chinese did better here:** 12 of 32 got a reply and 12 changed the repo,
  against 2 and 2 of 14 in English. We usually wrote in the language of the project's README, so this compares
  audiences as much as languages.
- **Sidebar fixes were always taken.** Among the projects we re-checked, every suggested topic
  list (5 of 5), About description (4 of 4) and website link (3 of 3) was added. A first-screen
  screenshot or demo, the fix we suggested most, was taken less often (6 of 10).

## The numbers

| | Count |
|---|---|
| Issues opened (18 Oct – 11 Nov 2026) | 47 |
| Still readable today | 46 |
| Got a reply from the author | 14 (30%) |
| Repo changed after our issue | at least 14 (30%) |
| Median time to first reply | 23.3 hours (range 10 – 143) |

One issue can no longer be read: its author deleted and recreated the repository, which removed
it. It had no reply before that, so it counts as sent but is left out of every rate above.

By the language we wrote in:

| Language of our issue | Issues | Replied | Changed the repo |
|---|---|---|---|
| Chinese | 32 | 12 | 12 |
| English | 14 | 2 | 2 |

## Which fixes get taken

Every numbered suggestion in our issues, coded by type. "Suggested" counts all 46 readable
issues; "Taken" is only known for the 16 projects we re-checked (the 14 that changed their repo,
and two that closed our issue without changing anything), so read it as "how often adopters took
this kind of fix", not as an overall rate.

| Kind of fix | Suggested | Taken, of those re-checked |
|---|---|---|
| Screenshot, GIF, video or real output on the first screen | 31 | 6 of 10 |
| One-line install or try-it step | 23 | 3 of 5 |
| Topics | 17 | 5 of 5 |
| A tagged release | 15 | 5 of 6 |
| Licence | 14 | 4 of 6 |
| README structure or a second language | 14 | 4 of 5 |
| About description | 13 | 4 of 4 |
| Website link in the About box | 7 | 3 of 3 |
| Agent Skill description | 3 | 0 of 1 |
| Other | 2 | not re-checked |

The cheapest fixes, the ones in the About box, were done every time. A screenshot, a demo or a
one-line install takes real work, and those were the fixes adopters most often left for later.

## Before and after

Five authors agreed to let us write up what they changed, scored with Megaphone's
[21-check rubric](../skills/launch-audit/rubric.md):

| Project | Score | What the author changed |
|---|---|---|
| [token-pilot](../examples/case-token-pilot/) | 54 → 100 | the three fixes from our issue, then the rest of the report |
| [Embedded-programming](../examples/case-embedded-programming/) | 49 → 90 | a licence, a one-line install and a real hardware build on the first screen within 14 hours, then a first release |
| [outline-skill](../examples/case-outline-skill/) | 58 → 78 | a demo image and a Chinese README |
| [Open Resume](../examples/case-open-resume/) | 70 → 79 | topics and a v1.0.0 release |
| [DragonCard](../examples/case-dragoncard/) | 54 → 71 | the demo link in the About box and four topics, in one day |

We don't name the other projects: the point is the pattern, not other people's repos.

## What we take from it

- **If you only have ten minutes, fill in the About box:** a one-line description, a website
  link and a few topics. Every adopter who was told to did it.
- **Name the exact file, line or screenshot.** One author made exactly the change we described
  (a screenshot of the example folder we named, placed where we said) without ever replying: a
  specific suggestion can be acted on without a conversation.
- **Be ready to be corrected.** One author showed that an install command we had flagged was
  valid; we [fixed the checker](../skills/launch-audit/scripts/audit.py) the same day.

## Method

- **Who we wrote to.** New public repos (mostly created in the weeks before), many of them Agent Skills or Claude Code plugins, picked by hand from GitHub search and
  Chinese developer lists. Each was checked with [`audit.py`](../skills/launch-audit/scripts/audit.py)
  first; we only wrote when there were concrete, cheap fixes to suggest. No repo got more than one
  issue.
- **Counting.** "Replied" means the author commented on the issue or answered with a pull request.
  "Changed the repo" means the repo, re-checked by hand, now has at least one of the fixes we
  suggested, made after our issue. For the one author who didn't reply, that the change came from
  our issue is our inference from how closely it matches. Repos we haven't re-checked count as
  unchanged, so this is a lower bound.
- **Coding.** Each numbered suggestion was given one type by hand; a suggestion covering two
  things (say, description and topics) counts once under each.
- **Limits.** A small sample from one sender over four weeks; the 11 November issues are only three
  days old and may still get replies. We picked the repos, so this is not a random sample of new
  projects. Language and audience are mixed up (see above). Adoption per kind of fix is only known
  for re-checked projects.

See also [what 362 new open-source projects show about launch readiness](2026-10-new-repos.md).
