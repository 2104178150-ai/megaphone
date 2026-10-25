# Newsletters

> Last checked: 2026-10-25. Confirmed on each newsletter's own page: This Week in Rust
> ([README](https://github.com/rust-lang/this-week-in-rust) and
> [the 2026-08 change](https://github.com/rust-lang/this-week-in-rust/issues/8575)), PyCoder's Weekly
> ([submissions](https://pycoders.com/submissions)), Changelog News
> ([submit](https://changelog.com/news/submit)), Console
> ([selection criteria](https://console.dev/selection-criteria)) and the Cooperpress
> weeklies ([contact page](https://cooperpress.com/contact); the newsletter sites
> themselves have no submission form). Editors pick what they like, so a submission is a
> suggestion, not a guarantee.

## Fit

Curated newsletters put your project in front of readers who opted in to hear about new
tools, without you needing an audience. Submitting takes minutes. The fit is about
topic: a small newsletter for your exact niche often beats a big general one (heuristic).

## Rules

- **Each newsletter sets its own** (see the table). Read its submission page first.
- One submission per newsletter, written for its readers, saying you're the author.
- No follow-up chasing. If it isn't picked, it isn't picked.

## Where to submit

| Newsletter | Audience | How to submit |
|---|---|---|
| [This Week in Rust](https://github.com/rust-lang/this-week-in-rust) | Rust | **Project announcements: no PRs after issue 664 (2026-08).** Editors pick Projects/Tooling Updates from [r/rust](https://www.reddit.com/r/rust/), so post there under its rules (see [reddit.md](reddit.md)). Other sections (how-tos, walkthroughs, calls for participation) still take a PR to the next issue's draft in `draft/` (the README says `drafts/`, but the folder is `draft/`). Articles must be written by people (LLM-written ones aren't accepted; machine translation is fine). No paywalled links, including Medium's members-only posts. Link text = the page's title |
| [PyCoder's Weekly](https://pycoders.com/submissions) | Python | "Submit Your Link" button; they want to hear about "projects you are working on" |
| [Go Weekly](https://golangweekly.com) (golangweekly.com), [JavaScript Weekly](https://javascriptweekly.com) and other Cooperpress weeklies | Go, JS, Node, frontend… | No submission form on the sites. Cooperpress's contact page lists **editor@cooperpress.com** for editorial; send one short email naming the newsletter |
| [Changelog News](https://changelog.com/news/submit) | Open source and software broadly | Sign in, then a form: URL, title, "What's interesting about it?". Your own work is welcome; they don't want how-tos/tutorials or commercial products |
| [Console](https://console.dev/selection-criteria) | Developer tools | Email **hello@console.dev**. Features 2–3 tools a week; "the more of these questions we can answer positively, the more likely" a tool is picked — e.g. is a developer the primary user, is there self-service sign-up, does it fit the dev workflow, is there a CLI/API, is it maintained and documented. Self-service sign-up is one of these questions, not a hard requirement. **Betas** are listed separately: developer tools that are pre-1.0 (SemVer), carry a pre-release label such as `1.0.0-beta`, or say "beta"/"preview" somewhere easy to find on the site, release notes or docs. GA/stable releases aren't eligible for the beta list |
| [阮一峰《科技爱好者周刊》](ruanyf-weekly.md) | Chinese tech readers | GitHub issue — see its playbook |
| [HelloGitHub 月刊](hellogithub.md) | Chinese open-source readers | Website submission — see its playbook |

Also look for the newsletter of your exact niche (a framework, a database, an editor),
and read its submission route on its own site.

## Format

- **Email or form**: one short paragraph: what it is, the one thing *this* newsletter's
  readers would care about, links (repo, demo, write-up), license. Written the way the
  editor might print it: neutral, no hype.
- **PR-based** (This Week in Rust, for a human-written article or a call for participation —
  not a project announcement): one line in the draft's format, in the right section.

## Timing

You can't time the issue: editors pick on their own schedule (weekly or monthly).
Heuristic: submit in launch week, once the README, demo and any write-up are live —
editors click once. For This Week in Rust, a merged article PR lands in the next issue's draft;
a project only gets in if editors pick your r/rust post.

## Template (email or form)

```
Subject: <Name> – <one-line what it does>

Hi <editor>,

I'm the author of <Name>, an open-source <category> that <outcome> for <audience>.

What's interesting about it: <the one thing a reader of THIS newsletter would care about>.

Repo: <link> · Demo: <link> · License: <license>

Thanks for considering it!
<name>
```

## Pitfalls

- Submitting before the README and demo are ready — editors click once.
- Mass-mailing the same text to every newsletter. Lead with what fits each one.
- Opening a This Week in Rust PR for a project announcement → not accepted since 2026-08; post on
  r/rust instead. An AI-written article → declined.
- Following up repeatedly. One polite submission is enough.
