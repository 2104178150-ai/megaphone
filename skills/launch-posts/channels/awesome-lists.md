# Awesome lists

> Last checked: 2026-10-15 against [sindresorhus/awesome](https://github.com/sindresorhus/awesome)
> and, as examples, the contributing rules of [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted-data/blob/master/CONTRIBUTING.md)
> and [awesome-go](https://github.com/avelino/awesome-go/blob/main/CONTRIBUTING.md).
> Every list has its own rules; **read its `CONTRIBUTING.md` and PR template before
> drafting** — they win over this page.

## Fit

Curated "awesome-*" lists are where people go when they're actively looking for a tool
in a category. A line in the right list can keep sending visitors long after launch week
(heuristic). It's low effort, but lists have entry rules that may rule you out for now.

## Finding the right lists

1. Start at [sindresorhus/awesome](https://github.com/sindresorhus/awesome) and search
   for your language and category.
2. Search GitHub: `awesome <your category>` sorted by stars, and check the last commit
   date — a list nobody merges into is worth nothing.
3. Look at where similar projects are listed: search GitHub code for a competitor's repo
   URL in `README.md` files.
4. Examples of large, active category lists: [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)
   for self-hostable software (submissions go to its separate
   [awesome-selfhosted-data](https://github.com/awesome-selfhosted/awesome-selfhosted-data)
   repo), plus per-language lists (awesome-go, awesome-rust, awesome-python…). Check each
   for activity.

## Rules (typical — the list's CONTRIBUTING wins)

- One project per PR, added in the right section, **following the list's own order**
  (often alphabetical, but not always — look at the section you're adding to).
- Follow the entry format exactly, e.g. `- [Name](link) - Description.` Match the
  punctuation, capitalisation and description length of neighbouring entries.
- **Maturity rules are common.** Examples: awesome-selfhosted wants a first release
  "more than four months old", active maintenance and working install instructions;
  awesome-go wants "at least 5 months of history", an open-source license, a `go.mod`, a
  SemVer release, test coverage of at least 80% (non-data packages), and links to
  pkg.go.dev and a coverage report.
- **Some lists don't accept AI-written submissions.** awesome-selfhosted's PR template
  asks you to confirm "The submission was done by a human, not a machine/LLM", and its
  CONTRIBUTING.md asks agents not to write the entry or PR text. For a list like that,
  Megaphone only checks eligibility and points the author to the rules; the author
  writes the entry and the PR. (CONTRIBUTING.md files can hold such notes in HTML
  comments, so read the raw file.)
- Description: neutral and factual, no "best"/"awesome", no emoji unless the list uses them.
- Disclose that you're the author when the list asks; expect review comments and answer
  them politely and quickly.

## Format

- **Entry**: one line in the list's format, in the right section and position.
- **PR**: title `Add <Name>`; a short body with what it is, license, maintenance status,
  that you're the author, and that you've read the contributing guide. Fill in the
  list's PR template if it has one.

## Timing

No timing effect on the list itself, and review can take anywhere from days to months
(heuristic). Submit once the README and demo are ready and the project meets the list's
age rule. Check the age rules early: a project with its first release last month can't
go into awesome-selfhosted or awesome-go this launch.

## Template

```
PR title: Add <Name>

- [<Name>](<repo url>) - <What it does in one neutral sentence>.

Body:
<Name> is <one sentence>. It's <license>, actively maintained (latest release <date>),
and I'm the author. I've read CONTRIBUTING.md and added it under <section>, following the
section's order.
```

## Pitfalls

- Opening PRs to ten lists with the same copy-pasted text → maintainers notice.
- Adding it to an unrelated section to get visibility → rejected.
- Submitting before the project meets the list's age or release rule → closed; resubmit later.
- Agent-written entry for a list that forbids it → rejected, and it burns goodwill.
- Not disclosing you're the author when the list asks.
