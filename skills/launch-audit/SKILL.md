---
name: launch-audit
description: Check whether a GitHub repo is ready to be launched — blockers a visitor would hit, risks that grow with visibility (unofficial APIs, copyright, privacy, capacity), and a 0–100 readiness score from a public rubric — then list the fixes that matter most. Use when the user asks "is my repo ready to launch", wants a README/repo review before promoting it, or says 发布前检查 / 体检 / 帮我看看仓库哪里不行.
---

# Launch audit

Visitors from a launch decide in seconds. This audit finds what would make them leave,
what could go wrong once the project is visible, and ranks the fixes by impact. The
rubric lives in [rubric.md](rubric.md); read it first.

## Steps

Read `.megaphone/decisions.md` first if it exists, and record any new answers there — or,
with no human available, the assumptions you made.

1. **Get the score.** Run the bundled script (Python 3.8+, no dependencies):

   ```bash
   python3 <this-skill-dir>/scripts/audit.py OWNER/REPO            # what's on GitHub now
   python3 <this-skill-dir>/scripts/audit.py OWNER/REPO --readme README.md   # score a local draft
   ```

   It's the same code as the Megaphone web checker, so the numbers match. A token in
   `GITHUB_TOKEN` is optional. If the repo isn't on GitHub yet or the network is
   unavailable, score the README-based checks by hand from [rubric.md](rubric.md) and mark
   the repo-based ones `unknown`.
2. **Do the human review.** Read the README top to bottom as a stranger arriving from the
   **channel you'll launch on first** — from `.megaphone/decisions.md`, or the most likely
   one if it isn't decided yet (a Hacker News reader on a laptop, a 小红书 user on a phone, a
   V2EX regular…). Answer:
   - Within the first screen, can I tell **what it is, who it's for, and why it's better**
     than what I use now?
   - Is there something to **see** before I have to read?
   - Can I **try it in under a minute**? Count the steps to the first result. Does that
     first result actually show the headline feature?
   - Is every **hard requirement** (browser, GPU, Docker, OS, account, paid key) stated up
     front?
   - Does anything look **abandoned, broken or risky** (stale badges, dead links, "WIP"
     with no date, no license)?
   - Would I **know what to say** if I told a friend about it?
   - Does the page I land on **speak my language**? GitHub opens `README.md`; a visitor from
     V2EX, 掘金 or 小红书 who meets an English first screen may leave before finding the small
     「简体中文」 link (and the reverse for an English channel; a heuristic from our own launch).
     One line in the visitor's language under the tagline, linking to the twin, helps.
   - Is the fastest way to try it **the easiest thing to click** (for example, the hero image
     links to the hosted demo)?
   - Is there **proof that someone else got value** (a user's words, a before/after)? Optional
     at launch, but it's what turns a visit into a star later.

   Don't run the project's code unless the user asked you to; reason from the code and
   docs, and say so.
3. **Decide the blockers** from [rubric.md § Blockers](rubric.md). Any open blocker caps
   the level at 🔉 *Needs polish* regardless of the score.
4. **Answer risk & readiness** ([rubric.md § Risk & readiness](rubric.md)) — always, even
   for harmless-looking projects; "none found" is a valid answer. Quote risky wording from
   the repo and propose factual replacements. Don't give legal advice.
5. **Rank the fixes.** Label each *Blocker*, *High* or *Medium* by visitor impact, and show
   the rubric points it's worth (often +0 for the most important ones — that's fine). Name
   the Megaphone skill that fixes it when there is one.
6. **Write `.megaphone/audit.md`** (template below, headings in the user's language, check
   IDs kept), then summarise in chat: blockers, level, the top three fixes.

## Levels

| Score | Level | Meaning |
|---|---|---|
| 90–100 | 📣 Ready to launch | Spend your launch now. |
| 75–89 | 🔊 Almost there | Fix the top items first; they're cheap. |
| 55–74 | 🔉 Needs polish | A launch now wastes attention you won't get back. |
| 35–54 | 🔈 Whispering | Fix the first screen and the try-it path before anything else. |
| 0–34 | 🔇 Muted | Not ready for visitors yet. |

**Any open blocker caps the level at 🔉 Needs polish.**

## Template for `.megaphone/audit.md`

```markdown
# Launch audit — <repo> — <date>

**Level: <emoji> <level>** · rubric score NN/100 · human-adjusted NN/100 (<why, if different>)
Open blockers: N

## Blockers
| Blocker | Status | Evidence | Fix |
|---|---|---|---|
| Quick start doesn't show the point | open/closed | … | … |

## Risk & readiness
- Third parties: …
- Claims in the repo: "<quote>" → "<factual replacement>"
- Other people's data: …
- Disclaimer: present / draft: "…"
- Capacity: …
- Reachability: …

## Fix first
1. <fix> — Blocker/High/Medium — why it matters, exactly what to change (+N pts)
2. …

## Rubric detail
| Category | Score |
|---|---|
| First impression | NN/35 |
| Time to wow | NN/25 |
| Trust | NN/20 |
| Shareability | NN/20 |

- [x] A1 Description … (8/8) — <evidence>
- [ ] A5 Visual in the first screen (0/8) — <evidence>

## Human review
- First screen: …
- Try-it path: N steps — …
- Requirements: …
- Word of mouth: "<how a user would describe it in one breath>"

## Accepted trade-offs
- D1 Two languages — the author keeps a Chinese-only README on purpose (scored NN/95 → NN/100)

## Manual checks (can't be detected automatically)
- [ ] Social preview image set (Settings → General → Social preview)
- [ ] Repo pinned on the author's profile
- [ ] Demo GIF under ~10 MB and loops cleanly
```

## Notes

- Don't pad. A project nobody can try is not "almost there" because it has a license and
  badges — that's what blockers are for.
- If the user disagrees with a check (e.g. no second language), record it as an accepted
  trade-off rather than nagging.
