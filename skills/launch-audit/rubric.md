# Megaphone launch-readiness rubric (v2)

Three layers, in this order of importance:

1. **Blockers** — found by the human review. Any open blocker caps the level at
   🔉 *Needs polish*, whatever the score, and no channel is scheduled until they're closed
   (the full gate is defined once, in `launch-plan`).
2. **Risk & readiness** — always answered, never scored. What gets worse when the
   project becomes visible.
3. **The 100-point score** — 21 mechanical checks. Run `scripts/audit.py OWNER/REPO` to
   get it; it's a line-by-line port of the web checker (`docs/checker.js`), and the shared
   cases in `tests/fixtures/rubric-cases.json` keep the two in agreement.

Report the rubric score **and** a human-adjusted score when a check passed or failed on a
technicality (say why). Accepted trade-offs (e.g. the author deliberately keeps one
language) are reported as `NN/MM` with the check removed from the denominator, then
rescaled to 100.

## 1. Blockers (human review)

Mark each one open or closed in `audit.md`. Add others if they'd make a visitor leave.

| Blocker | Open when |
|---|---|
| **Quick start doesn't show the point** | Running the first command or opening the first link doesn't demonstrate the headline feature — as the README presents it, or as `brief.md` states it once positioning has run (e.g. a diagram renderer whose example has no diagram) |
| **Hidden hard requirement** | A runtime need (a browser, GPU, Docker, an OS, an account, a paid API key) isn't stated in the first screen |
| **Can't legally use it** | No license |
| **Broken try-path** | The install command, demo link or hosted site doesn't work |
| **Unresolved visibility risk** | The risk section below found exposure and the author hasn't decided how to handle it |
| **Claims that will backfire** | The README or posts make legal guarantees ("zero risk", "100% legal"), false comparisons, or invented numbers |

## 2. Risk & readiness (always answer; not scored)

A launch makes the project visible to the platforms and companies it touches and sends a
burst of traffic to anything hosted. Answer before positioning:

- **Third parties** — does it call unofficial or undocumented APIs, scrape sites, handle
  copyrighted media, or ask for another service's credentials? List which, and what
  happens if they block it or object.
- **Claims in the repo** — quote any wording that reads as a legal guarantee ("legal",
  "zero risk", "零侵权风险") or as circumvention ("bypass", "破解", "突破", "抓包"), and
  propose factual replacements.
- **Other people's data** — can it look up or expose data about someone other than the
  user? If so, posts must not advertise that use.
- **Disclaimer** — is there a non-affiliation and scope line in the README? If not, draft one.
- **Capacity** — for a hosted demo or API: quotas, rate limits, upstream limits, cost,
  what a user sees when it's overloaded, and whether there's a fallback (local CLI,
  self-host).
- **Reachability** — will the target audience load the README images and links? For
  mainland-China audiences, `raw.githubusercontent.com` and some CDNs are often blocked.

Never give legal advice. If exposure is significant, say plainly that a louder launch
raises it, and let the author decide how loud to go. List every do-not-say item in
`audit.md`; `launch-positioning` copies them into `brief.md` → *Claims we won't make*.

## 3. The 100-point score

Line limits count **raw Markdown lines, including blank lines**, unless the check says
"non-empty". Lines inside fenced code blocks are ignored when looking for headings,
bullets and prose. A **badge** is an image whose URL contains `shields.io`, `badgen.net`,
`badge`, `codecov`, `travis-ci`, `circleci` or `/workflows/`. A **logo** is a non-video
image whose URL or alt text contains `logo`, `icon`, `avatar` or `favicon`, or whose
`width`/`height` attribute is ≤ 128.

### A. First impression — 35

| ID | Check | Points | Passes when |
|---|---|---|---|
| A1 | Description | 8 | Repo description exists (4) and is 20–160 characters (4). Bilingual descriptions often run long — shorten, or accept the trade-off |
| A2 | Topics | 5 | ≥ 3 topics (5); 1–2 topics (2) |
| A3 | Title at the top | 3 | A Markdown or HTML heading within the first 15 non-empty lines |
| A4 | Tagline | 4 | Within the first 25 non-empty lines, a line that isn't a heading, list item or table row and, after removing images, tags and link syntax, is 10–200 characters with ≥ 3 English words or ≥ 8 CJK characters (language-switcher lines like "English \| 简体中文" don't count) |
| A5 | Visual in the first screen | 8 | A screenshot, GIF or video within the first 60 lines that is neither a badge nor a logo (a bare `github.com/user-attachments/assets/…` line counts as a video) |
| A6 | Demo / website link | 4 | The repo's homepage field is set to something other than the repo's own GitHub URL |
| A7 | README has substance | 3 | ≥ 150 words of prose (two CJK characters count as one word) |

### B. Time to wow — 25

| ID | Check | Points | Passes when |
|---|---|---|---|
| B1 | Getting-started section | 7 | A heading containing install, quick start, getting started, get started, setup, set up, usage, how to use, run, 安装, 快速开始, 快速上手, 上手, 开始使用 or 使用 |
| B2 | Code block early | 5 | A fenced code block starts within the first 150 lines |
| B3 | One step to try it | 8 | A recognised one-line install or run command anywhere in the README (the exact patterns are `INSTALL_RES` in `docs/checker.js`, mirrored in `scripts/audit.py`) — `npm i`, `npx`, `pnpm add/dlx`, `yarn add/dlx`, `bun add`/`bunx`, `pip install <pkg>` (not `pip install -r`), `pipx`, `uv`/`uvx`, `brew install`, `port install`, `cargo install`, `go install`/`go get`, `docker run`/`pull`, `docker compose up`, `curl … \| sh`, `iwr … \| iex`, `gem install`, `composer require`, `dotnet tool install`, `winget`/`scoop`/`choco install`, `apt install`, `snap`/`flatpak install`, `nix run`, `helm install`, `npx skills add`, `claude plugin install` — **or** a homepage that passes A6 (a hosted version people can try) |
| B4 | Shows what it does | 5 | Within the first 120 lines, a heading containing feature, usage, example, demo, screenshot, how it works, what it does, tutorial, walkthrough, tour, showcase, gallery, 功能, 特性, 示例, 例子, 演示, 截图, 效果 or 教程; or ≥ 3 `-`/`*`/`+` bullet points in the first 80 lines |

B3 is the check most likely to pass on a technicality: an install command proves the
project installs, not that the first run shows anything. That's what the *Quick start
doesn't show the point* blocker is for.

### C. Trust — 20

| ID | Check | Points | Passes when |
|---|---|---|---|
| C1 | License | 6 | GitHub detects a license |
| C2 | Recently active | 4 | Last push within 90 days (4); within a year (2). Bot-only activity (Dependabot) counts here — discount it in the human-adjusted score |
| C3 | Releases | 4 | At least one GitHub release |
| C4 | Contributing guide | 3 | GitHub's community profile finds a CONTRIBUTING file |
| C5 | Issue templates | 3 | The community profile finds issue templates, or `.github/ISSUE_TEMPLATE/` exists |

### D. Shareability — 20

| ID | Check | Points | Passes when |
|---|---|---|---|
| D1 | Two languages | 5 | Mentions a translated README file anywhere (`README.zh-CN.md`, `README_EN.md`, `README.ja.md`…), or has a `[简体中文](…)`/`[English](…)` link in the first 40 lines, **or** real prose in both English and CJK: ≥ 80 English words and ≥ 30 CJK characters, with English between 25% and 75% of the words. Code, URLs, HTML and link targets aren't prose |
| D2 | Why / comparison | 4 | A heading containing why, motivation, comparison, compare, vs, alternative, difference, 为什么, 对比, 比较, 动机 or 初衷 |
| D3 | Community channel | 5 | Discussions enabled, or a Discord / Telegram / Slack / Matrix / Gitter / 微信群 / QQ群 link in the README |
| D4 | Badges | 3 | At least one badge within the first 30 lines |
| D5 | Code of conduct | 3 | The community profile finds a code of conduct |

## Why these weights

- **First impression and time-to-wow are 60%** because launch traffic is cold traffic:
  people arrive from a title, look for a few seconds, and leave unless they see what it
  is and how to try it.
- **A visual and a one-step try are the two biggest single checks (8 each).** They turn a
  click into a try. That's also why a logo doesn't count as a visual.
- **Two languages is 5 points**, not more: it's a reach multiplier, not a quality bar.
  Skip it as an accepted trade-off if you won't launch in a second language.
- Stars, forks and age are deliberately **not** scored. The rubric measures what the
  maintainer can fix this week.
- The score measures the README's **shape**. Whether it actually works for a visitor is
  the blockers' job.
