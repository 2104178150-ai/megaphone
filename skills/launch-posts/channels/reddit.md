# Reddit

> Last checked: 2026-10-15 against Reddit's site-wide [Reddit Rules](https://redditinc.com/policies/reddit-rules)
> and its help article on [spam](https://support.reddithelp.com/hc/en-us/articles/360043504051).
> Subreddit rules could **not** be read this time (reddit.com blocks automated reads), so
> every subreddit note below is unverified. Rules change often and are enforced by
> volunteer moderators — **read the sidebar, rules page and pinned posts of every
> subreddit before posting**, and put what you found in the post's checklist.

## Fit

Reddit is a set of very different rooms. The right subreddit can send the most
engaged users you'll ever get; the wrong one gets you removed or banned in minutes.

## Rules

From Reddit itself:

- **Participate authentically.** Rule 2: "Participate authentically in communities where
  you have a personal interest, and do not spam". The spam article adds: if your
  contributions are mostly links to something you run or benefit from, "be thoughtful
  about the frequency of posting", and moderators decide what counts as spam in their
  community.
- **No mass-posting.** The spam article lists "Mass-posting repetitive content for the
  purpose of exposure". Don't post the same text to many subreddits on the same day;
  space them out and rewrite for each audience.
- **No vote manipulation.** Rule 2 bans "content manipulation"; never ask for upvotes or
  brigade a thread.

Rules of thumb (not Reddit policy):

- **Be a participant first.** Moderators check post history; an account that only posts
  its own links looks like a spammer. The often-quoted "9:1" or "~90% normal
  participation" ratio is folklore: neither page above sets a ratio. Some subreddits set
  their own; the sidebar wins.
- **Disclose that you made it.** Many subreddits require it, and undisclosed
  self-promotion is the quickest way to a ban.
- Use the subreddit's **flair** and any required title format (e.g. `[Project]`, `[OC]`).
- Some subreddits have rules about AI-written posts or AI-built projects; check the
  sidebar.

## Where to post (unverified notes — check each sidebar)

| Subreddit | Fits | Notes |
|---|---|---|
| r/SideProject | Almost any side project | Built for sharing your own projects; engage with others' posts too |
| r/opensource | Open-source releases | Lead with the license and why it's open |
| r/selfhosted | Self-hostable apps | A March 2026 rules update reportedly limits projects younger than three months to Fridays ("New Project Friday") *(seen via a Reddit mirror, unverified)*. Include Docker / install instructions and screenshots |
| r/coolgithubprojects | GitHub repos of any kind | Low effort, low reach — good for a first test |
| r/webdev | Web projects | Self-promotion is commonly reported to be limited to the weekly **Showoff Saturday** thread *(unverified)* |
| r/programming | Articles about programming | Commonly reported as very strict about self-promotion; a deep technical write-up has a better chance than a project link |
| r/commandline, r/linux, r/unixporn | CLIs, terminal tools, ricing | Show a screenshot or asciicast |
| Language subs: r/rust, r/golang, r/Python, r/javascript, r/typescript, r/reactjs, r/node… | Libraries and tools in that language | Many route project posts to a recurring thread; e.g. r/golang has run a weekly "Small Projects" thread since 2025 *(seen via a Reddit mirror, unverified)*. r/rust also feeds This Week in Rust: since 2026-08 its editors pick project updates only from r/rust posts ([announcement](https://github.com/rust-lang/this-week-in-rust/issues/8575)), which points to r/rust's ["No more code dumps"](https://www.reddit.com/r/rust/comments/1wkmzun/no_more_code_dumps/) rules — read them first |
| r/LocalLLaMA | Tools that run or serve local models | Hostile to thin API wrappers; show real local-model use |
| r/MachineLearning | Research code | Uses `[P]` (project) tags; expects substance |
| r/devops, r/sysadmin, r/homelab | Infra and ops tools | Show the problem it solves in production terms |
| r/Entrepreneur, r/startups | Rarely the right place for dev tools | Usually strict no-promotion rules |

## Format

- **Title**: what it is + who it's for, plainly. `I built X, a <thing> for <people> that <does Y>`
  is a common, widely accepted pattern. Follow any tag/flair rule.
- **Body** (text post, link in body): problem → what you built → screenshot/GIF →
  how to try it → what's next → "I'm the author, happy to answer questions".
- Images and GIFs usually get more attention than walls of text (heuristic).

## Timing

No official guidance. Heuristic for English subs: a weekday US morning, Eastern
(about 08:00–10:00 ET = 12:00–14:00 UTC while the US is on daylight time, 13:00–15:00 UTC
on standard time; = 20:00–22:00 Beijing in summer). A subreddit's fixed days override
this: recurring showcase threads and any day-of-week rule (e.g. r/selfhosted's Fridays,
above). Stay online for the first couple of hours; early replies keep the thread alive
(heuristic). Leave a day or more between subreddits.

## Template

```
Title: I built <Name> – <what it does> for <audience> (open source)

Hi r/<sub>! I'm the author of <Name>.

The problem: <one or two sentences, in the sub's language>.

What it does:
- <benefit> — <how>
- <benefit> — <how>

<screenshot or GIF>

Try it: <one command or link>. Source: <repo>. License: <license>.

What it doesn't do yet: <honest limits>. I'd really like feedback on <question>.
```

## Pitfalls

- Posting from a fresh or low-karma account → many subreddits filter these
  automatically (thresholds are set by each sub's moderators).
- Link post with no context → reads as spam.
- Arguing with a moderator in public → ban. Message the mods politely instead.
- Same text in five subs in an hour → Reddit's spam rules ("mass-posting repetitive
  content"), and often a site-wide filter.
