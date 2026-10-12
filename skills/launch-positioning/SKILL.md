---
name: launch-positioning
description: Find the one-sentence pitch for an open-source project — who it's for, what it replaces, the proof, and why it beats the alternatives — and save it as a launch brief every post is built from. Use when a repo's pitch is vague, before writing a README or launch posts, or when the user asks 怎么介绍我的项目 / 一句话说清楚 / 定位 / tagline / elevator pitch.
---

# Launch positioning

Most launch posts fail before they're written: the author can't say in one breath who
the project is for and why it's better than what those people use today. This skill
produces `.megaphone/brief.md`, the single source every other Megaphone skill reads.

## Steps

1. **Read before asking.** README, docs, examples, issues and the first commits often
   reveal the original itch. Note what the code actually does — features the README
   doesn't mention are common.
2. **Interview briefly** (skip anything the repo already answered):
   - What were you doing the day you started this? What was annoying?
   - Who else has that problem? Be specific: "Go developers who ship CLIs", not
     "developers".
   - What do they use today instead? (Another tool, a script, a spreadsheet, nothing.)
   - What's the moment it clicks — the first result that makes someone say "oh nice"?
   - Any proof: numbers you measured, users, a before/after?
3. **Fill the canvas** below. Push for specifics; "fast", "simple" and "powerful" are
   not positions — every README says them.
4. **Write three one-liners** in different styles, recommend one, and say why:
   - *Outcome*: "Turn X into Y in one command."
   - *Contrast*: "Like A, but for B." (only if A is well known to the audience)
   - *Pain*: "Stop doing X by hand."
5. **Check them** against the tests below, then save `.megaphone/brief.md`.

## Canvas

| Field | Question | Bad | Good |
|---|---|---|---|
| Audience | Who exactly? | developers | maintainers of small open-source repos who've never launched before |
| Trigger | When do they reach for it? | when they need it | the night before they post on Hacker News |
| Alternative | What do they do today? | — | skim old blog posts and guess |
| Promise | What changes for them? | better launches | a scored checklist and channel-specific drafts in ten minutes |
| Aha | First moment of value | — | pasting a repo URL and seeing a 0–100 score with the three fixes that matter |
| Proof | Why believe it? | — | rubric is public; rules link to each platform's own guidelines |
| Contrast | Why not the alternative? | — | generic marketing skills don't know V2EX or Show HN etiquette |
| Category | What shelf does it sit on? | AI tool | launch checklist / developer marketing |

## Tests for a one-liner

- **Stranger test**: would someone who has never heard of it understand it out of
  context, e.g. in a Hacker News title list?
- **Swap test**: if you replace the project name with a competitor's, is it still true?
  If yes, it's not a position.
- **Breath test**: can it be said aloud in one breath? (≈ 12 English words or ≈ 20
  Chinese characters.)
- **No buzzword test**: remove "AI-powered", "blazing", "next-gen", "revolutionary".
  Does it still say something?

## Template for `.megaphone/brief.md`

```markdown
# Launch brief — <project>

**One-liner (EN):** …
**一句话（中文）:** …
**Alternatives considered:** … / … (and why the chosen one wins)

| | |
|---|---|
| Audience | … |
| Trigger | … |
| Today they use | … |
| Promise | … |
| Aha moment | … |
| Proof | … |
| Contrast | … |
| Category | … |

## Three bullets (for README and posts)
- **<benefit>** — <how>
- …

## Words to use / avoid
- Use: <words the audience uses for the problem>
- Avoid: <jargon, buzzwords, internal names>

## Open questions
- [TODO] …
```

Write the Chinese one-liner natively, not as a translation: Chinese developer audiences
respond to concrete pain ("再也不用手动…") and to a clear "适合谁".
