---
name: launch-positioning
description: Find the one-sentence pitch for an open-source project or app — who it's for, what it replaces, why now, the proof, how it beats today's alternatives, and what we must not claim — and save it as the launch brief every post is built from. Use when a repo's pitch is vague, before writing a README or launch posts, or when the user asks 怎么介绍我的项目 / 一句话说清楚 / 定位 / tagline / elevator pitch.
---

# Launch positioning

Most launch posts fail before they're written: the author can't say in one breath who the
project is for and why it's better than what those people use today. This skill produces
`.megaphone/brief.md`, the single source every other Megaphone skill reads.

## Steps

1. **Read before asking.** README (look for *why*, *motivation*, 初衷 sections), docs,
   examples, the oldest issues and the first commits often reveal the original itch. Note
   what the code actually does — features the README doesn't mention are common. Read
   `.megaphone/audit.md` if it exists: its risk section feeds *Claims we won't make*.
2. **Check the alternatives' current state.** For each alternative you'll contrast with,
   look at its latest release and its open issues/PRs for the feature you're comparing on.
   A competitor may be about to ship it. Date-stamp every contrast claim ("as of 2026-10").
3. **Interview briefly** (skip anything already answered):
   - What were you doing the day you started this? What was annoying?
   - Who else has that problem? Be specific: "Go developers who ship CLIs", not "developers".
   - What do they use today instead? (Another tool, a script, a spreadsheet, nothing.)
   - What's the moment it clicks — the first result that makes someone say "oh nice"?
   - What changed recently that makes this matter now?
   - Any proof: numbers you measured, users, a before/after?

   If the user isn't available, fill fields from the repo, mark them `[inferred]`, and leave
   the origin story as `[TODO]` — never invent it.
4. **Fill the canvas** below. Push for specifics; "fast", "simple" and "powerful" aren't
   positions — every README says them.
5. **Write three one-liners** in different styles, recommend one, and say why:
   - *Outcome*: "Turn X into Y in one command."
   - *Contrast*: "Like A, but for B." (only if A is well known to the audience)
   - *Pain*: "Stop doing X by hand."
6. **Check them** against the tests below, then save `.megaphone/brief.md`.

## Canvas

Two example columns: a developer tool and an end-user app.

| Field | Question | Developer tool | End-user app |
|---|---|---|---|
| Audience | Who exactly? | maintainers of small open-source repos launching for the first time | 网易云 users with years of playlists they don't want to lose |
| Trigger | When do they reach for it? | the night before posting on Hacker News | their membership expires, or songs in a playlist go grey |
| Today they use | What do they do now? | skim old blog posts and guess | screenshots and retyping |
| Promise | What changes for them? | a scored checklist and channel-specific drafts in ten minutes | a spreadsheet of every playlist in one click |
| Aha moment | First moment of value | pasting a repo URL and seeing the three fixes that matter | the exported file opening with every song listed |
| Why now | What changed recently? | AI agents can now do the drafting, but don't know community rules | more people switching between music apps |
| Proof | Why believe it? | public rubric; rules link to each platform's own guidelines | works on the five biggest platforms (list them) |
| Contrast | Why not the alternative? (dated) | generic marketing prompt packs don't know V2EX or Show HN etiquette (2026-10) | <tool X> doesn't support Chinese platforms (checked 2026-10) |
| Category | What shelf does it sit on? | launch checklist / developer marketing | playlist backup tool |

## Tests for a one-liner

- **Stranger test**: would someone who's never heard of it understand it out of context,
  e.g. in a list of post titles?
- **Swap test**: if you swap in a competitor's name, is it still true? If yes, it's not a
  position. In a crowded category where any plain outcome line fails this, let the
  bullets carry the difference — and say so.
- **Breath test**: can it be said aloud in one breath? (≈ 12 English words or ≈ 20 Chinese
  characters; Latin brand names inside Chinese count as one character each.)
- **No-buzzword test**: remove "AI-powered", "blazing", "next-gen", "revolutionary",
  「神器」「颠覆」. Does it still say something?
- **Founder-voice test**: every sentence in the author's voice ("I built it because…") is
  the author's own words or a `[TODO]`.
- **Claims test**: nothing in it appears under *Claims we won't make*.

## Template for `.megaphone/brief.md`

Write it in the user's language. Include the Chinese one-liner only if a Chinese channel or
README is planned (and the English one only if an English channel is).

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
| Why now | … |
| Proof | … |
| Contrast (as of <date>) | … |
| Category | … |

## Origin story (author's words only)
[TODO: ask the author] / "<quote>"

## Three bullets (for README and posts)
- **<benefit>** — <how>
- …

## Words to use / avoid
- Use: <words the audience itself uses — from issues, forum threads, reviews>
- Avoid: <jargon, buzzwords, internal names>

## Claims we won't make
- Legal or safety guarantees ("legal", "zero risk", "official", "零风险")
- Wording that reads as circumvention ("bypass", "破解", "突破限制", "抓包")
- Uses that invite misuse (e.g. looking up other people's data)
- <anything from audit.md → Risk & readiness>

## Standard disclaimer (for README and posts, if the project touches other platforms)
"<Project> is not affiliated with <platforms>. It <scope>; it does not <what it doesn't do>."

## Open questions
- [TODO] …
```

Write the Chinese one-liner natively, not as a translation: Chinese audiences respond to
concrete pain ("再也不用手动…") and a clear 「适合谁」.
