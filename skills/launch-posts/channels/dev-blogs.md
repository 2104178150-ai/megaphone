# DEV, Hashnode, Medium (and your own blog)

> Last checked: 2026-10-15 against DEV's [editor guide](https://dev.to/p/editor_guide),
> [terms](https://dev.to/terms) and [guidelines for AI-assisted articles](https://dev.to/guidelines-for-ai-assisted-articles-on-dev),
> and Medium's help article [Set a canonical link](https://help.medium.com/hc/en-us/articles/360033930293-Set-a-canonical-link).
> Hashnode's help page on canonical links returned 404 this time; its setting below is
> unverified — confirm it in the editor.

## Fit

People searching for how to solve a problem. An article can rank in search and keep
sending readers for months, unlike a post that's gone in a day (heuristic). Best for
projects with an interesting build story or a tutorial angle.

## Rules (from the platforms)

- **DEV terms**: posts must be on-topic and "not designed primarily for the purposes of
  promotion or creating backlinks", and must contain substantial content, not just a
  link to the full post elsewhere.
- **DEV and AI**: AI-assisted or AI-generated articles must say so (the
  `#ABotWroteThis` tag or a line in the post), be fact-checked, and "should not … Promote
  any business, program, or course (including your own)". So a launch article on DEV
  should be written by the author; Megaphone supplies the outline and the facts.
- **DEV tags**: "max of four tags". Pick the most specific.
- **Canonical URLs** keep a cross-posted copy from competing with the original in search:
  - DEV: the `canonical_url` field (editor guide).
  - Medium: only the author can set it: edit the story → ⋯ → More settings → Advanced
    Settings → "This story was originally published elsewhere". Medium's import tool sets
    it automatically.
  - Hashnode: article settings → "Are you republishing?" → add the original URL
    *(unverified this time)*.

## What to write

Not "Announcing X". Write the article your target user would search for:

- **"How I built X"** — architecture, trade-offs, mistakes. Technical readers share these.
- **"How to <solve problem> in <language/tool>"** — a tutorial where your project is the
  natural last step, not the whole point.
- **"I compared A, B and C for <task>"** — honest comparison including your project and
  its weaknesses.

## Format

- Title that matches what people search for.
- Problem in the first paragraph, demo GIF early, code blocks that run.
- Repo link near the top and at the end.
- Publish the original on the blog you control and set canonical URLs on the copies.
- Keep it free to read: some newsletters won't link paywalled posts (This Week in Rust
  excludes Medium's members-only stories).

## Timing

No strong timing effect worth planning around: readers mostly arrive later, from search
and links (heuristic). What matters is order: publish the "how it works" article a day or
more before your Show HN or Reddit post so those can link it, or after the launch as a
write-up of what you learned. On DEV and Hashnode, be around for comments on the day you
publish.

## Template outline

```
# How I <did X> with <stack> (and why I open-sourced it)

The problem — 2 short paragraphs
What I tried first — and why it didn't work
The approach — diagram or key code
Results — real numbers, screenshots
Try it — one command, repo link
What's next / what I'd do differently
```

## Pitfalls

- Thin articles that are just an ad → low engagement, and against DEV's terms.
- AI-written article on DEV without the disclosure → against DEV's AI guidelines.
- Cross-posting without canonical URLs → the copies compete in search.
- A paywalled article → newsletters and readers skip it.
