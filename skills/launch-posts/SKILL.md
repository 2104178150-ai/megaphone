---
name: launch-posts
description: Pick the channels where a project's audience actually is — developer communities for developer tools, the platforms end users already browse for apps, plugin directories for extensions — and prepare a rule-checked draft for each, or, where the platform wants the author's own words (Show HN, a DEV launch article, Lobsters, awesome lists that refuse LLM-written entries), a fact sheet the author writes from: Show HN, Reddit, Product Hunt, X/Twitter, DEV, Lobsters, awesome lists, newsletters, V2EX, HelloGitHub, 阮一峰科技爱好者周刊, 即刻, 小红书, 掘金, 知乎, B 站 and more. Use when the user wants to announce or promote a project or app, write a Show HN / Reddit / Product Hunt post, or says 写推广文案 / 发帖推广 / 发 V2EX / 投稿 HelloGitHub / 小红书怎么发.
---

# Launch posts

Each channel has its own audience, rules and taboos. A post that wins on Show HN gets
removed on r/programming and ignored on 小红书. This skill picks channels on purpose and
prepares one native draft per target — or, where the platform asks for the author's own
words, the facts the author writes from.

## Inputs

Read these first; ask only for what's missing and record answers (or, with no human
available, your assumptions) in `.megaphone/decisions.md`.

- `.megaphone/brief.md`: one-liner, audience, bullets, origin story, dated contrast,
  **Claims we won't make** and the **standard disclaimer**. If it's missing, run
  `../launch-positioning/SKILL.md` first (a quick brief is enough).
- `.megaphone/audit.md`: open blockers and **Risk & readiness** (third parties, other
  people's data, capacity, reachability). Drafting can start with blockers open; when
  posts can go out is decided by the gate in `../launch-plan/SKILL.md`.
- `.megaphone/decisions.md`: is the user the author, their accounts and how established,
  **which languages they can read and reply in**, where they plan to launch first,
  timezone and free hours, and where the project has been posted before.
- The README (quick start, visual, hosted link). If `.megaphone/readme-first-screen.md`
  exists and hasn't been applied yet, draft against that proposal and say so in the
  channel table — posts must match the README visitors will land on.
- Any launch copy already in the repo (`docs/launch*`): reuse what's accurate and note
  where you differ.

## Step 1 — Choose channels

Read [channels/README.md](channels/README.md) and start from where *this* audience is:
developer tools → HN, Reddit, language communities; end-user apps → where those users
already browse (小红书, 即刻, B 站, Product Hunt, r/SideProject…). For a plugin or
integration, the host app's channels (plugin directory, release notes, forum) often beat
everything else: see [ecosystems.md](channels/ecosystems.md), and ask the host's
maintainer before posting in their space. A regional channel with no playbook (e.g. Zenn
for a Japanese user) can be a candidate; read its own rules first.

Mark each candidate ✅ / ⚠️ / ❌ on:

1. **Audience fit**: do the people here have the problem?
2. **Format fit**: can it be shown the way this channel likes, with assets ready in time
   (a no-sign-up demo for Show HN, 3–6 images for 小红书, a personal story for 即刻)?
3. **Account fit**: does the user have an account that won't be filtered (new ones often
   are on HN, Reddit and V2EX), **in a language they can read and reply in**? Submission
   channels usually need only a GitHub login or email; a language the user can't read is ❌.

Draft every channel with **no ❌ and at least two ✅**, up to **six posting channels** (if
more qualify, keep the six with the most ✅ and say which you cut). **Compounding
channels** — awesome lists and newsletters, including HelloGitHub and 阮一峰周刊 — are
extra, drafted whenever they pass the same test. GitHub itself (topics, social preview, a
release) needs no post: add its to-dos from [github-native.md](channels/github-native.md)
to the table. If the user isn't the author, skip Show HN (it's "for something you've
made").

**Repost check before HN or Reddit.** HN: open
`https://hn.algolia.com/api/v1/search?query=github.com/OWNER/REPO&restrictSearchableAttributes=url&tags=story`,
then search the project name at hn.algolia.com. Reddit: search reddit.com and each target
subreddit for the repo URL and name; if Reddit blocks automated requests, write
`[TODO: check for earlier posts]`. HN allows a small number of reposts only if the story
hasn't had significant attention in the last year or so, and never delete-and-repost
([FAQ](https://news.ycombinator.com/newsfaq.html)); each subreddit sets its own rule. After
a big earlier thread, skip the channel or wait for a major release.

Save the table to `.megaphone/posts/README.md` (in the user's language) and show it in chat:

```markdown
# Channels — <project>
README assumed: current README / proposal in readme-first-screen.md (not applied yet)

| Channel / target | Audience | Format | Account | Decision | Why (incl. repost check) | File | Status |
|---|---|---|---|---|---|---|---|
| Show HN | ✅ | ✅ | ✅ | author writes | no earlier submissions (hn.algolia.com, <date>) | hacker-news.md | fact sheet ready; author to write |
| r/commandline | ✅ | ✅ | ⚠️ | draft | none found | reddit-commandline.md | [TODO] origin story |
| 小红书 | ✅ | ⚠️ | ❌ | skip | user has no account | — | — |
| GitHub itself | — | — | — | to-dos | <topics, social preview, release> | — | — |
```

## Step 2 — Prepare one file per target

Name files after the playbook: one per **posting target** (`posts/hacker-news.md`,
`posts/reddit-commandline.md`, `posts/reddit-golang.md`), one per **submission channel**
with a section per target (`posts/awesome-lists.md`, `posts/newsletters.md`; HelloGitHub
and 阮一峰周刊 have their own playbooks and files). Follow the playbook in `channels/`:
title rules, length, language, links, first comment, pitfalls.

**Author-written channels.** Some platforms ask for the author's own words, and their
playbooks say so: Show HN ([hacker-news.md](channels/hacker-news.md)), a DEV launch
article ([dev-blogs.md](channels/dev-blogs.md)), the Lobsters title and comment
([lobsters.md](channels/lobsters.md)), and awesome lists whose rules refuse LLM-written
entries or PRs ([awesome-lists.md](channels/awesome-lists.md)). For these, don't write
prose: use the same file and header, but replace `## Title` / `## Body` with
`## Facts for the author` (bullet facts for each part of the playbook's outline, `[TODO]`
where only the author knows) and keep *Likely questions* as facts to answer from, not
scripted replies. Their Status is "author writes" until the user says the text is done.

For every other channel, write:

```markdown
# <Channel> — <target> — draft
Where: <exact URL, node, subreddit or submission form>
Window: <the playbook's window in the playbook's own timezone, e.g. "08:00–10:00 PT (heuristic)", or "no data — chose <X> because <Y>">
Account: <which account posts>

## Title
<only if the channel has titles>
## Body
## First comment / follow-up
<only if the playbook uses one>

## Likely questions
- "<predictable objection>" — <short honest answer, or [TODO: ask the author]>

## Checklist before posting
- [ ] Rule check: <the 1–3 rules most likely to get this removed: playbook + this target's own rules (sidebar, CONTRIBUTING.md), or [TODO: read <where>]>
- [ ] Risk check: nothing from brief → Claims we won't make; disclaimer included (if the project touches other platforms)
- [ ] AI disclosure: <what this channel expects, e.g. 小红书 asks for AI-assisted content to be labelled; or "none required">
- [ ] Links work and are reachable for this audience
- [ ] Assets ready: <images / GIF / video this post needs>
- [ ] Reply window free (see plan.md)
```

(Author-written files keep the same checklist, plus `- [ ] The author wrote the text in
their own words`.)

- **Window**: keep it in the playbook's own timezone. `launch-plan` converts it to the
  user's local date and time in `plan.md`, so moving the launch (even across a DST
  switch) never leaves stale times in the posts.
- **Likely questions**: 3–5 objections this audience will raise ("why not X?", "why does it
  need Y?", "is this allowed?", "what about my data?"), answered from the repo and brief.
  Never answer a legal question with a guarantee; point to the disclaimer.

### Writing rules for every channel

- **Lead with the problem or the result**, not the tech stack (that comes second).
- **Say you made it** (or your relation to it). Many subreddits require it; all expect it.
  In neutral-blurb formats (HelloGitHub, 阮一峰周刊, newsletters, awesome lists) disclose it
  only the way the form or list asks, e.g. 【开源自荐】 in a 阮一峰周刊 title.
- **Label AI help where the channel asks for it.** These drafts are AI-assisted. 小红书's
  community guidelines ask for AI-assisted content to be labelled, some subreddits and DEV
  have rules on AI-written posts, and V2EX readers resent hidden AI text — follow each
  playbook, and when in doubt, let the author rewrite it in their own words.
- **One link: the one this channel's readers can use** — the hosted app for end users, the
  repo for developers, none where outbound links are penalised (commonly reported for
  小红书; say what to search for, as its playbook does). Add the repo as a second link only
  where the playbook template has a separate repo or source line (`Source:`, `Repo:`,
  `开源地址`, `仓库链接`…).
- **Be specific and modest.** Real numbers and limitations beat adjectives; contrast
  claims come only from the brief, with their date.
- **Say what it doesn't do yet**, except in neutral-blurb formats, which you write the way
  the editor or list would print them.
- **Never ask for upvotes, stars or likes**, or coordinate friends to vote: it breaks HN,
  Product Hunt and Reddit rules and gets posts killed.
- **Native language and tone.** Write each post from scratch in its channel's language and
  register (HN: plain and technical; 即刻: personal; 小红书: visual, benefit-first).
- **No two posts identical.** Reuse facts, not sentences.
- **The author's voice comes only from the author.** "I built it because…" comes from the
  brief's origin story or the user's own words in `decisions.md`; otherwise write
  `[TODO: in your words, why you built it]`. Unknown numbers stay `[TODO]` too.

## Step 3 — Hand off

Summarise in chat: the channel table, where each file is, which drafts are ready to paste,
which are fact sheets the author writes from, which still have `[TODO]`s (and what each
needs), and the assets to make. Hand off to `../launch-plan/SKILL.md` for order, dates and
reply windows. Remind the user that they publish manually, and that right after each post
goes live they add a row to `.megaphone/log.csv`: `date` as YYYY-MM-DD, `time` as 24 h
HH:MM in their timezone, `channel` as the file's base name (`hacker-news`,
`reddit-commandline`, `v2ex`), and the post's URL — so `launch-review` can attribute
results.
