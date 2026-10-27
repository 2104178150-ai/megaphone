# Contributing to Megaphone

Thanks for helping! The most valuable contributions are **keeping channel rules
accurate** and **adding channels people actually use**. 中文贡献同样欢迎——issue 和 PR 用中文写完全没问题。

## Report a rule change

Platforms change their rules quietly. If a playbook in
[`skills/launch-posts/channels/`](skills/launch-posts/channels) is out of date, open a
**"Channel rule changed"** issue with a link to the platform's current rule page, or
send a PR that:

1. Updates the playbook text.
2. Updates the date line at the top: `Last checked: YYYY-MM-DD` in English playbooks,
   `最近核对：YYYY-MM-DD` in Chinese ones.
3. Links the source. Prefer the platform's own pages. Label a fact you couldn't confirm
   there *(commonly reported)* or *(unverified)*, and label heuristics (posting windows,
   "what usually works") as heuristics.
4. Updates [`scripts/check_sources.py`](scripts/check_sources.py) if it tracks that fact:
   change the phrase to text that now appears verbatim on the platform's page, or add a
   `(playbook, url, phrase)` entry for a new fact. Then run
   `python3 scripts/check_sources.py` and check that every source matches.

When the script reports a phrase as missing (✗), read the page before editing the
playbook: the rule may have changed, or the page may only have been reworded. Unreachable
(?) means the page couldn't be fetched (a network problem, or a site that blocks
scripts); check it in a browser.

## Add a channel

1. Use the same sections as the other playbooks, in this order, with the date line and
   sources at the top:
   - English playbooks: **Fit, Rules, Format, Timing, Template, Pitfalls**
   - Chinese playbooks: **适合什么项目, 规则与习惯, 格式, 时机, 模板, 常见坑**

   Channel-specific sections (怎么投稿, 先解决账号问题…) can sit between them.

   Keep every section even when there's little to say. "No official rules; these are
   community habits" or "No reliable timing data" is useful, because `launch-posts` and
   `launch-plan` look there for posting windows.
2. Playbooks for Chinese channels are written in Chinese with a short English summary at
   the top; the rest are in English. Write the template in the channel's own language.
3. Add a row to [`channels/README.md`](skills/launch-posts/channels/README.md), add the
   playbook to the lists in [`README.md`](README.md) and [`README.zh-CN.md`](README.zh-CN.md),
   and update the "channel playbooks" badge count in both — and the count in
   `docs/preview.svg` ("NN channel playbooks →") and `docs/social-preview.svg` ("+N more",
   then re-export `docs/social-preview.png`).
4. Add the facts the playbook relies on to `scripts/check_sources.py`.
5. If the web checker should recommend it, add a rule in `recommendChannels()` in
   [`docs/checker.js`](docs/checker.js) and a test in [`tests/checker.test.js`](tests/checker.test.js).

What we won't merge: advice to buy or trade votes, use sock-puppet accounts, mass-DM
people, or anything else that breaks a platform's rules.

## Change the rubric

The 100-point score is implemented twice, and four files must change together in the
same PR:

| File | What it is |
|---|---|
| [`skills/launch-audit/rubric.md`](skills/launch-audit/rubric.md) | The rules, for agents and humans |
| [`docs/checker.js`](docs/checker.js) | The web checker |
| [`skills/launch-audit/scripts/audit.py`](skills/launch-audit/scripts/audit.py) | A line-by-line Python port of `checker.js` |
| [`tests/fixtures/rubric-cases.json`](tests/fixtures/rubric-cases.json) | Shared cases with the expected points per check and the total |

- Keep the total at 100.
- Update the expected values in the fixtures. Work them out from the rule, not from
  whatever the code prints, and add a case for the new behaviour.
- Run both test suites: `python3 -m unittest discover -s tests` checks `audit.py` against
  the fixtures, and http://localhost:8820/tests/ checks `checker.js` against the same file.
- If you add or remove a check, update the count wherever it's stated: `rubric.md`, both
  READMEs, `docs/index.html`, `docs/app.js` and `docs/preview.svg`.
  `grep -rniE "21 (checks|mechanical)|twenty-one|21 项" --exclude-dir=tests --exclude-dir=.git .`
  lists them. The README copies in `tests/fixtures/` are test inputs; leave them alone.
- Explain in the PR why the new weight or rule is better for launch visitors.

Blockers, *Risk & readiness* and the skill/plugin checks (§ 4, SK1–SK5) are human review, not code. They live in `rubric.md` and
the audit template in [`skills/launch-audit/SKILL.md`](skills/launch-audit/SKILL.md).

## Improve a skill

Skills are plain Markdown (`skills/<name>/SKILL.md`). Keep them:

- **Actionable** — steps an agent can follow, with the output format spelled out.
- **Honest** — no invented numbers, and never the author's voice: an origin story is the
  author's own words or a `[TODO]`. Heuristics are labelled as heuristics.
- **Safe** — the agent drafts, the user publishes. Check whether visibility could hurt
  before making a project louder.
- **Usable without a human** — questions and assumptions go in `.megaphone/decisions.md`;
  anything that needs approval is written to `.megaphone/` as a proposal.

Working files live in `.megaphone/`, which `launch` adds to `.gitignore` by default. If a
skill writes a new file there, add it to the workspace table in
[`skills/launch/SKILL.md`](skills/launch/SKILL.md).

## Run it locally

From the repo root:

```bash
python3 -m unittest discover -s tests   # launch-review script, and audit.py against the shared cases
python3 scripts/check_sources.py        # do the playbooks' sources still say what we quote? (network)
python3 skills/launch-audit/scripts/audit.py OWNER/REPO --readme README.md   # score a local README

python3 -m http.server 8820             # keeps running; then open:
# checker:       http://localhost:8820/docs/
# checker tests: http://localhost:8820/tests/
```

No build step, no dependencies. The checker uses only browser APIs; the Python scripts
use only the standard library (3.8+; IANA zone names in `stars.py --tz` need 3.9+).

## Code of conduct

By taking part you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
