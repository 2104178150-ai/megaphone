# Megaphone launch-readiness rubric (v1)

100 points in four categories. The web checker (`docs/checker.js`) implements exactly
these checks; keep the two in sync when you change either.

"First lines" counts lines of the raw README Markdown. Badge images are images whose
URL contains `shields.io`, `badgen.net`, `badge`, `codecov`, `travis-ci`, `circleci`
or `/workflows/`.

## A. First impression — 35

| ID | Check | Points | Passes when |
|---|---|---|---|
| A1 | Description | 8 | Repo description exists (4) and is 20–160 characters (4) |
| A2 | Topics | 5 | ≥ 3 topics (5); 1–2 topics (2) |
| A3 | Title at the top | 3 | A Markdown or HTML heading within the first 15 non-empty lines |
| A4 | Tagline | 4 | A plain sentence of 10–200 characters (not a badge, image or bare link) within the first 25 non-empty lines |
| A5 | Visual in the first screen | 8 | A non-badge image, GIF or video within the first 60 lines |
| A6 | Demo / homepage link | 4 | The repo's homepage field is set |
| A7 | README has substance | 3 | ≥ 150 words (two CJK characters count as one word) |

## B. Time to wow — 25

| ID | Check | Points | Passes when |
|---|---|---|---|
| B1 | Getting-started section | 7 | A heading like Install, Quick start, Getting started, Usage, 安装, 快速开始, 使用 |
| B2 | Code block early | 5 | A fenced code block starts within the first 150 lines |
| B3 | One-command start | 8 | A recognised one-line install or run command (`npm i`, `npx`, `pip install`, `uvx`, `brew install`, `cargo install`, `go install`, `docker run`, `curl … \| sh`, `npx skills add`, …) |
| B4 | Shows what it does | 5 | A Features / Usage / Example / Demo / Screenshot heading (功能, 特性, 示例, 演示, 截图), or ≥ 3 bullet points in the first 80 lines |

## C. Trust — 20

| ID | Check | Points | Passes when |
|---|---|---|---|
| C1 | License | 6 | GitHub detects a license |
| C2 | Recently active | 4 | Pushed within 90 days (4); within a year (2) |
| C3 | Releases | 4 | At least one GitHub release |
| C4 | Contributing guide | 3 | GitHub's community profile finds a CONTRIBUTING file |
| C5 | Issue templates | 3 | GitHub's community profile finds issue templates, or `.github/ISSUE_TEMPLATE/` exists (issue forms) |

## D. Shareability — 20

| ID | Check | Points | Passes when |
|---|---|---|---|
| D1 | Two languages | 5 | README has substantial English and Chinese text, or links to a translated README (`README.zh-CN.md`, `README_EN.md`, …) |
| D2 | Why / comparison | 4 | A heading like Why, Motivation, Comparison, vs, Alternatives, 为什么, 对比 |
| D3 | Community channel | 5 | Discussions enabled, or a Discord / Telegram / Slack / Matrix / Gitter / 微信群 / QQ群 link in the README |
| D4 | Badges | 3 | At least one badge within the first 30 lines |
| D5 | Code of conduct | 3 | GitHub's community profile finds a code of conduct |

## Why these weights

- **First impression and time-to-wow are 60%** because launch traffic is cold traffic:
  people arrive from a title, look for a few seconds, and leave unless they see what it
  is and how to try it.
- **A visual and a one-command start are the two biggest single checks (8 each).**
  They are what turns a click into a try.
- **Two languages is 5 points**, not more: it's a reach multiplier (it unlocks the
  Chinese channels in `launch-posts`), not a quality bar.
- Stars, forks and age are deliberately **not** scored. The rubric measures what the
  maintainer can fix this week.
