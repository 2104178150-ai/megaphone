// Browser tests for docs/checker.js. Open tests/index.html through a local server:
//   python3 -m http.server 8820   then visit http://localhost:8820/tests/
import { analyze, readmeFacts, parseRepoInput, recommendChannels, RUBRIC, CATEGORIES, levelFor } from '../docs/checker.js';

const results = [];
function test(name, fn) {
  try { fn(); results.push({ name, ok: true }); } catch (e) { results.push({ name, ok: false, error: e.message }); }
}
function eq(actual, expected, msg = '') {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${msg} expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}
function ok(value, msg) { if (!value) throw new Error(msg || 'expected truthy'); }

const NOW = Date.parse('2026-10-12T00:00:00Z');
const daysAgo = (n) => new Date(NOW - n * 86400000).toISOString();

const GOOD_README = `<h1 align="center">Rocket</h1>
<p align="center">Ship static sites to any CDN with one command, no config files.</p>

[![npm](https://img.shields.io/npm/v/rocket)](https://npmjs.com/rocket) [![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

English | [简体中文](README.zh-CN.md)

![Rocket deploying a site](docs/demo.gif)

- **Fast** — deploys in seconds
- **Simple** — zero config
- **Portable** — works with any CDN

## Quick start

\`\`\`bash
npx rocket deploy ./dist
\`\`\`

## Why Rocket?

Other tools need a config file per provider. Rocket detects the provider for you and keeps the same command everywhere, so moving between hosts is a one-word change.

## Features

Rocket handles uploads, cache headers, atomic switches and rollbacks. ${'It is designed to be small and predictable. '.repeat(20)}

Join us on [Discord](https://discord.gg/rocket).
`;

const GOOD_DATA = {
  repo: {
    full_name: 'acme/rocket', description: 'Ship static sites to any CDN with one command.',
    topics: ['cli', 'deploy', 'static-site', 'cdn'], homepage: 'https://rocket.dev',
    license: { spdx_id: 'MIT', name: 'MIT License' }, pushed_at: daysAgo(3),
    has_discussions: false, language: 'TypeScript', archived: false,
  },
  readme: GOOD_README,
  community: { files: { contributing: {}, issue_template: {}, code_of_conduct: {} } },
  releases: [{ tag_name: 'v1.0.0' }],
};

const EMPTY_DATA = {
  repo: { full_name: 'acme/empty', description: null, topics: [], homepage: '', license: null,
    pushed_at: daysAgo(800), has_discussions: false, language: null, archived: false },
  readme: '',
  community: null,
  releases: [],
};

test('rubric adds up to 100 and matches categories', () => {
  eq(RUBRIC.reduce((s, r) => s + r.max, 0), 100);
  for (const c of CATEGORIES) {
    eq(RUBRIC.filter((r) => r.cat === c.id).reduce((s, r) => s + r.max, 0), c.max, `category ${c.id}`);
  }
});

test('parseRepoInput accepts common forms', () => {
  eq(parseRepoInput('acme/rocket'), 'acme/rocket');
  eq(parseRepoInput('https://github.com/acme/rocket'), 'acme/rocket');
  eq(parseRepoInput('github.com/acme/rocket.git'), 'acme/rocket');
  eq(parseRepoInput('https://github.com/acme/rocket/tree/main/docs'), 'acme/rocket');
  eq(parseRepoInput('  acme/rocket/ '), 'acme/rocket');
  eq(parseRepoInput('not a repo'), null);
  eq(parseRepoInput('https://gitlab.com/acme/rocket'), null);
});

test('a launch-ready repo scores 100', () => {
  const a = analyze(GOOD_DATA, NOW);
  const failed = a.checks.filter((c) => !c.pass).map((c) => c.id);
  eq(failed, [], 'failed checks');
  eq(a.score, 100);
  eq(a.level.emoji, '📣');
});

test('an empty repo scores 0 and is muted', () => {
  const a = analyze(EMPTY_DATA, NOW);
  eq(a.score, 0);
  eq(a.level.color, 'mute');
  ok(a.facts.empty);
});

test('badges alone do not count as a visual', () => {
  const f = readmeFacts('# X\n\n[![ci](https://github.com/a/b/actions/workflows/ci.yml/badge.svg)](x)\n![v](https://img.shields.io/badge/v-1-blue)\n');
  eq(f.visual, null);
  eq(f.badges, 2);
});

test('a bare user-attachments video counts as a visual', () => {
  const f = readmeFacts('# X\n\nA tool that does a thing for people.\n\nhttps://github.com/user-attachments/assets/0f6a6c6e-1234-4c3a-9d1e-abcdef012345\n');
  ok(f.visual);
});

test('tagline skips language switchers and finds the sentence', () => {
  const f = readmeFacts('# X\n\nEnglish | [简体中文](README.zh-CN.md)\n\n> Turn any folder into a searchable wiki in seconds.\n');
  eq(f.tagline, 'Turn any folder into a searchable wiki in seconds.');
});

test('Chinese tagline is recognised', () => {
  const f = readmeFacts('# 项目\n\n一行命令把任意文件夹变成可以搜索的知识库。\n');
  eq(f.tagline, '一行命令把任意文件夹变成可以搜索的知识库。');
});

test('headings inside code fences are ignored', () => {
  const f = readmeFacts('Some intro text here for the project.\n\n```md\n# Install\n```\n');
  eq(f.gettingStarted, null);
  eq(f.titleAtTop, false);
});

test('install commands are detected', () => {
  for (const cmd of ['npm i -g foo', 'npx create-foo', 'pip install foo', 'uvx foo', 'brew install foo',
    'cargo install foo', 'go install github.com/a/b@latest', 'docker run -p 80:80 foo',
    'curl -fsSL https://foo.sh | sh', 'npx skills add a/b', '/plugin marketplace add a/b']) {
    ok(readmeFacts('```\n' + cmd + '\n```').installLine, `not detected: ${cmd}`);
  }
  eq(readmeFacts('```\npip install -r requirements.txt\n```').installLine, null, 'requirements file');
});

test('partial points: short description, few topics, older push', () => {
  const data = structuredClone(GOOD_DATA);
  data.repo.description = 'Rocket';
  data.repo.topics = ['cli'];
  data.repo.pushed_at = daysAgo(200);
  const a = analyze(data, NOW);
  const pts = Object.fromEntries(a.checks.map((c) => [c.id, c.points]));
  eq([pts.A1, pts.A2, pts.C2], [4, 2, 2]);
});

test('issue forms found outside the community profile count', () => {
  const data = structuredClone(GOOD_DATA);
  data.community.files.issue_template = null;
  eq(analyze(data, NOW).checks.find((c) => c.id === 'C5').points, 0);
  data.issueTemplates = true;
  eq(analyze(data, NOW).checks.find((c) => c.id === 'C5').points, 3);
});

test('fixes favour first impression over shareability at similar gains', () => {
  const data = structuredClone(GOOD_DATA);
  data.repo.homepage = '';                                   // A6: -4
  data.readme = data.readme.replace('English | [简体中文](README.zh-CN.md)', ''); // D1: -5
  const ids = analyze(data, NOW).fixes.map((f) => f.id);
  eq(ids.slice(0, 2), ['A6', 'D1']);
});

test('channels: Chinese README unlocks Chinese channels', () => {
  const f = readmeFacts('# 项目\n\n' + '这是一个帮助开发者推广开源项目的工具，可以自动检查仓库。'.repeat(5));
  const ids = recommendChannels({ topics: [], language: 'Go' }, f).map((c) => c.id);
  ok(ids.includes('v2ex') && ids.includes('hellogithub') && ids.includes('ruanyf'), ids.join(','));
});

test('channels: docker run alone is not self-hosted, compose or topic is', () => {
  const run = readmeFacts('# X\n\n```\ndocker run foo\n```');
  ok(!recommendChannels({ topics: [] }, run).some((c) => c.id === 'selfhosted'), 'docker run');
  const compose = readmeFacts('# X\n\n```\ndocker compose up -d\n```');
  ok(recommendChannels({ topics: [] }, compose).some((c) => c.id === 'selfhosted'), 'compose');
  ok(recommendChannels({ topics: ['self-hosted'] }, run).some((c) => c.id === 'selfhosted'), 'topic');
});

test('channels: Show HN needs a way to try it and English text', () => {
  const english = readmeFacts('# X\n\n' + 'This tool helps you do a useful thing quickly. '.repeat(20) + '\n```\nnpx x\n```');
  ok(recommendChannels({ topics: [] }, english).some((c) => c.id === 'hn'));
  const noTry = readmeFacts('# X\n\n' + 'This tool helps you do a useful thing quickly. '.repeat(20));
  ok(!recommendChannels({ topics: [], homepage: '' }, noTry).some((c) => c.id === 'hn'));
});

test('levels cover the whole range', () => {
  eq([100, 90, 89, 75, 74, 55, 54, 35, 34, 0].map((s) => levelFor(s).color),
    ['great', 'great', 'good', 'good', 'ok', 'ok', 'low', 'low', 'mute', 'mute']);
});

// ---------------------------------------------------------------------------
const passed = results.filter((r) => r.ok).length;
window.__results = { passed, failed: results.length - passed, results };
const out = document.getElementById('out');
if (out) {
  out.innerHTML = `<h1>${passed}/${results.length} passed</h1>` + results.map((r) =>
    `<div style="color:${r.ok ? 'green' : 'crimson'}">${r.ok ? '✓' : '✗'} ${r.name}${r.ok ? '' : ' — ' + r.error}</div>`).join('');
}
