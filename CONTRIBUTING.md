# Contributing to Megaphone

Thanks for helping! The most valuable contributions are **keeping channel rules
accurate** and **adding channels people actually use**. 中文贡献同样欢迎——issue 和 PR 用中文写完全没问题。

## Report a rule change

Platforms change their rules quietly. If a playbook in
[`skills/launch-posts/channels/`](skills/launch-posts/channels) is out of date, open a
**"Channel rule changed"** issue with a link to the platform's current rule page, or
send a PR that:

1. Updates the playbook text.
2. Updates the `Last checked: YYYY-MM` line at the top.
3. Links the source. Prefer the platform's own pages; if a fact only comes from
   third-party guides, label it *(commonly reported)*.

## Add a channel

1. Copy the structure of an existing playbook: **Fit, Rules, Format, Timing, Template,
   Pitfalls**, with a `Last checked` line and sources at the top.
2. Write the template in the channel's own language.
3. Add a row to [`channels/README.md`](skills/launch-posts/channels/README.md).
4. If the web checker should recommend it, add a rule in `recommendChannels()` in
   [`docs/checker.js`](docs/checker.js) and a test in [`tests/checker.test.js`](tests/checker.test.js).

What we won't merge: advice to buy or trade votes, use sock-puppet accounts, mass-DM
people, or anything else that breaks a platform's rules.

## Change the rubric

The rubric lives in two places that must agree:
[`skills/launch-audit/rubric.md`](skills/launch-audit/rubric.md) (for agents and humans)
and [`docs/checker.js`](docs/checker.js) (for the web checker). Change both, keep the
total at 100, and explain in the PR why the new weight is better for launch visitors.

## Improve a skill

Skills are plain Markdown (`skills/<name>/SKILL.md`). Keep them:

- **Actionable** — steps an agent can follow, with the output format spelled out.
- **Honest** — no invented numbers; unknowns become `[TODO]`.
- **Safe** — the agent drafts, the user publishes.

## Run it locally

```bash
python3 -m http.server 8820
# checker: http://localhost:8820/docs/
# checker tests: http://localhost:8820/tests/
python3 -m unittest discover -s tests   # launch-review script tests
```

No build step, no dependencies. The checker uses only browser APIs; the review script
uses only the Python standard library (3.8+).

## Code of conduct

By taking part you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
