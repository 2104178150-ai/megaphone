# Lobsters

> Last checked: 2026-10-18 against the [about page](https://lobste.rs/about), the
> [tag list](https://lobste.rs/tags) and the submit form in Lobsters' source
> ([`_form.html.erb`](https://github.com/lobsters/lobsters/blob/main/app/views/stories/_form.html.erb),
> [`story.rb`](https://github.com/lobsters/lobsters/blob/main/app/models/story.rb)).
> Lobsters is invite-only; you need an existing member to invite you.

## Fit

A small, highly technical community focused narrowly on computing. Deep technical
write-ups, programming-language and systems work do well. Marketing and product
announcements do badly. The about page's test for a good story: "Will this improve the
reader's next program?"

## Rules (from the about page)

- **Topicality**: computing only. Entrepreneurship, management and company news are off
  topic.
- **Tags** are required, from a predefined list. Your own project goes under `show`
  ("Show Lobsters / Projects"); a release under `release`; plus one or two topic tags.
- **Self-promotion is limited.** Authors are welcome, but not "as a write-only tool for
  product announcements or driving traffic to their work". Rule of thumb: self-promo
  should be **less than a quarter** of your stories and comments. Tick "I am the author of
  the story at this URL (or this text)" when submitting your own work.
- **New users** (first 70 days) can't send invites, can't submit links to domains the
  site hasn't seen before, and **can't use some tags, including `show`**. A new account
  can't post a Show Lobsters.
- **Spam flag**: for content "designed to promote a commercial service" or "created
  without meaningful human authorship". Write the title and comment yourself.
- **Invitations**: the quickest way is to talk to someone you recognise from the site; if
  something you wrote was posted there, the about page asks you to reach out in chat.
  Inviters are accountable for the people they invite — don't put a friend in a spot by
  spamming.

## Format

- Link to a technical article or the repo.
- Title: plain and descriptive, 150 characters at most; the form asks you to remove site
  and author names.
- If you're the author, a short comment explaining the motivation and the interesting
  technical part is welcome.

## Timing

No official guidance and no reliable data; it's a small site. Post when you can answer
comments for a few hours, and not on the same day as your Show HN if you can't follow
both (heuristic).

## Template

```
URL:    <technical write-up, or the repo>
Title:  <Name>: <what it does, plainly>        (≤ 150 chars, no site/author name)
Tags:   show + 1–2 topic tags (e.g. rust, go, unix)
[x] I am the author of the story at this URL (or this text)

Comment (the author's own words, optional):
Why you built it, the interesting technical decision, what you'd like feedback on.
```

## Pitfalls

- Posting a product launch rather than something technically interesting.
- Asking for an invite just to promote your project.
- Expecting to post `show` from a new account → not allowed for the first 70 days.
- An account whose activity is mostly your own links → over the quarter rule of thumb.
