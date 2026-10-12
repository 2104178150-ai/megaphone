---
name: launch-audit
description: Score a GitHub repo's launch readiness (0–100) and list the fixes that matter most before promoting it — first impression, time-to-wow, trust signals, shareability. Use when the user asks "is my repo ready to launch", wants a README/repo review before posting, or says 发布前检查 / 体检 / 帮我看看仓库哪里不行.
---

# Launch audit

Visitors from a launch decide in seconds. This audit finds what would make them bounce
and ranks the fixes by impact. It uses the same rubric as the Megaphone web checker
([rubric.md](rubric.md)), so the numbers match, and then adds the judgement calls a
script can't make.

## Steps

1. **Collect facts.** From the local checkout read the README (and any translations),
   LICENSE, CONTRIBUTING, `.github/ISSUE_TEMPLATE/`, releases/tags (`git tag`), last
   commit date, and package manifests. If `gh` is available and the repo is on GitHub,
   also run `gh repo view --json description,repositoryTopics,homepageUrl,hasDiscussionsEnabled,isArchived,stargazerCount`.
   If you can't get a fact, mark the check "unknown" rather than guessing.
2. **Score the rubric.** Go through every check in [rubric.md](rubric.md) and record
   pass / fail / unknown with the points. Add up the four categories.
3. **Do the human review.** Read the README top to bottom as a stranger arriving from
   Hacker News on a phone, and answer:
   - Within the first screen, can I tell **what it is, who it's for, and why it's
     better than what I use now**?
   - Is there something to **see** (screenshot, GIF, demo link) before I have to read?
   - Can I **try it in under a minute**? Count the steps from landing to first result.
   - Does anything look **abandoned or risky** (stale badges, broken links, "WIP" with
     no date, no license)?
   - Would I **know what to type** if I wanted to tell a friend about it?
4. **Rank the fixes.** Order by (visitor impact × ease). Blockers first: no license, no
   way to try it, empty/placeholder README, broken install command. Name the Megaphone
   skill that fixes each item when there is one (`launch-readme` for the first screen,
   `launch-positioning` for an unclear pitch).
5. **Write `.megaphone/audit.md`** using the template below, then summarise in chat:
   score, the volume level, and the top three fixes.

## Volume levels

| Score | Level | Meaning |
|---|---|---|
| 90–100 | 📣 Ready to launch | Spend your launch now. |
| 75–89 | 🔊 Almost there | Fix the top items first; they're cheap. |
| 55–74 | 🔉 Needs polish | A launch now wastes attention you won't get back. |
| 35–54 | 🔈 Whispering | Fix the first screen and the try-it path before anything else. |
| 0–34 | 🔇 Muted | Not ready for visitors yet. |

## Template for `.megaphone/audit.md`

```markdown
# Launch audit — <repo> — <date>

**Score: NN/100 · <volume level>**

| Category | Score |
|---|---|
| First impression | NN/35 |
| Time to wow | NN/25 |
| Trust | NN/20 |
| Shareability | NN/20 |

## Fix first
1. <fix> — why it matters, exactly what to change (+N pts)
2. …

## Rubric detail
- [x] A1 Description … (8/8)
- [ ] A5 Visual in first screen … (0/8) — <evidence>

## Human review
- First screen: …
- Try-it path: N steps — …
- Trust: …
- Word of mouth: "<how a user would describe it in one breath>"

## Manual checks (can't be detected automatically)
- [ ] Social preview image set (Settings → General → Social preview)
- [ ] Repo pinned on your profile
- [ ] Demo GIF under ~10 MB and loops cleanly
```

## Notes

- Don't pad the score. A project with no way to try it is not "almost there" just
  because it has a license and badges.
- If the user disagrees with a check (e.g. they don't want a Chinese README), mark it
  as an accepted trade-off rather than nagging.
