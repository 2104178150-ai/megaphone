# Hacker News — Show HN

> Last checked: 2026-10-15 against the [Show HN guidelines](https://news.ycombinator.com/showhn.html),
> the [HN guidelines](https://news.ycombinator.com/newsguidelines.html), the
> [FAQ](https://news.ycombinator.com/newsfaq.html) and the moderators'
> [Show HN tips](https://news.ycombinator.com/item?id=22336638) (linked from the Show HN page).
> The 80-character title limit isn't written on those pages; the moderators state it in
> threads (e.g. [May 2026](https://news.ycombinator.com/item?id=48210728)).

## Fit

Technical, curious, skeptical readers who love things they can try right now. Wins:
clever tools, clean implementations, small projects with a sharp idea, honest write-ups
of how something was built. Loses: marketing copy, sign-up walls, "AI-powered" with no
substance, landing pages, text that reads as machine-written.

## Rules (from HN itself)

- Show HN is for **something you've made that people can try**: things they can run, or
  hardware they can hold (for hardware a video or detailed article is fine; for books, a
  sample chapter).
- It must be **non-trivial** ("Don't post quickly-generated one-offs"), something you've
  **worked on personally**, and you must be **around to discuss it**.
- Make it **easy to try, "ideally without barriers such as signups or emails"**. That's a
  strong preference rather than a ban, but a sign-up wall costs you most of the feedback.
- **Not** for blog posts, sign-up pages, newsletters, lists or other reading material —
  submit those as regular stories. No landing pages or fundraisers.
- Routine releases ("Foo 1.3.1 is out") generally don't qualify; a major overhaul
  probably does. The tips add: re-post a new version only if it's significantly
  different, link the previous Show HN in a comment, and not more than once or twice a year.
- Title begins with **"Show HN"**. Explain **how and why** you built it.
- **Write the text yourself.** The guidelines: "Please don't put generated text in HN
  posts" and "please don't automate posting". The tips go further: don't use an LLM to
  generate *or edit* any of it. The same applies to comments ("Don't post generated text
  or AI-edited text").
- **Don't ask anyone to upvote or comment**, and make sure friends and users don't add
  booster comments. HN penalises or bans submissions, accounts and sites that do (FAQ).
- HN isn't primarily for promotion: post your own work only part of the time.
- Reposts: if a story hasn't had significant attention in the last year or so, a small
  number of reposts is OK; otherwise they're buried as duplicates. Never delete and repost.
- Don't use your company or project name as your username (tips).

## How Megaphone drafts for HN

Because HN asks for hand-written text, **don't hand the user paste-ready prose for HN.**
In `posts/hacker-news.md`, write:

- the facts for each part of the outline below, as bullet notes from the repo and brief
  (`[TODO]` where only the author knows, such as the backstory);
- the rule checks: title ≤ 80 characters and starts with "Show HN:", no sign-up needed to
  try it, repost check done, earlier relevant HN threads found;
- likely questions, each with the facts needed to answer it.

The author writes the title, the text and every reply in their own words. You may check
what they wrote against this playbook and point out problems; don't rewrite it.

## Format

- **Title**: `Show HN: <Name> – <what it does, plainly>`. **80 characters at most** (HN
  rejects longer titles). No uppercase for emphasis, no exclamation marks, no "best"
  (guidelines: don't make titles stand out), no emoji.
  - ✅ `Show HN: Megaphone – score your GitHub repo's launch readiness`
  - ❌ `Show HN: Megaphone 🚀 The ULTIMATE AI-powered launch platform!!!`
- **URL**: the repo, or a live demo that needs no sign-up.
- **Text**: enter it in the submission's text field. Per the tips it "should show up at
  the top of the Show HN submission"; if it doesn't, add it as the first comment ("Either
  way is fine"). The FAQ says you can't make links in a text submission, so put the main
  link in the URL field and any other links in a comment.
- **Content** (tips): a clear statement of what it is (otherwise "the discussion will
  consist of 'I can't tell what this is'"), the backstory, what's different, links to any
  earlier HN threads that are relevant. No marketing or sales language.

## Timing

No official guidance. A common community heuristic is a weekday morning, US time
(roughly **08:00–10:00 Pacific**), when the "new" and "show" pages are watched by the most
people. More important than the hour: **be free for the next 3–4 hours** to answer every
comment.

08:00–10:00 Pacific in other timezones:

| Your timezone | US on daylight time (PDT) | US on standard time (PST) |
|---|---|---|
| UTC | 15:00–17:00 | 16:00–18:00 |
| London | 16:00–18:00 | 16:00–18:00 |
| Berlin, Paris | 17:00–19:00 | 17:00–19:00 |
| India | 20:30–22:30 | 21:30–23:30 |
| Beijing, Singapore | 23:00–01:00 | 00:00–02:00 (next day) |
| Tokyo, Seoul | 00:00–02:00 (next day) | 01:00–03:00 (next day) |

The US is on PDT from the 2nd Sunday of March to the 1st Sunday of November. Europe
changes on the last Sundays of March and October, so in the weeks between (e.g.
2026-10-25 → 2026-11-01) London and Berlin are one hour *earlier* than the table. If the
window falls in your night, choose honestly between staying up and posting at a time you
can be awake for 3–4 hours; an absent author hurts more than an off-peak hour (heuristic).

## Template (outline; the author writes the words)

```
Title (≤ 80 chars): Show HN: <Name> – <what it does, in plain words>
URL: <repo, or a demo that needs no sign-up>

Text, 4–8 short paragraphs:
1. What it is: one plain sentence (category, what it does, for whom).
2. Backstory: the specific situation that made you build it; what you tried first.
3. How it works: the interesting technical part (algorithm, architecture, trick, constraint).
4. What's different from <A, B>: one honest contrast, checked recently.
5. How to try it: one command or the demo; license; stack.
6. What it doesn't do yet.
7. The feedback you want: one specific question.
First comment (only if needed): links to earlier relevant HN threads, docs.
```

## Day of

- Reply to every substantive comment, especially critical ones, calmly and specifically,
  in your own words. Thank people for bug reports and fix fast — "fixed, thanks"
  mid-thread is great.
- Don't argue about downvotes or ask why the post isn't ranking.
- If it sinks without comments, don't delete and repost. Improve the project or the
  title and try again much later, within the repost rule. Questions for the moderators go
  to hn@ycombinator.com, not into a post. Putting an email address in your profile lets
  them contact you; the tips say they sometimes send repost invites.

## Pitfalls

- Linking to a sign-up page → off topic for Show HN (guidelines); a demo behind a
  sign-up gets far less feedback.
- Text that reads as LLM-written → the tips say it draws backlash; the guidelines ask
  you not to post it.
- Marketing tone in the text → top comment will call it out.
- Username that's your project or company name → reads as promotion (tips).
- Posting from a brand-new account with no comment history → often looks like spam
  (commonly observed; new accounts show in green).
- Asking for upvotes anywhere (X, Discord, WeChat groups) → can get the post penalised.
