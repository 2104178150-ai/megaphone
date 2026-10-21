import { analyze, fetchRepoData, parseRepoInput, FetchError, CATEGORIES, LEVELS } from './checker.js';

// The repo this site lives in. On GitHub Pages it's derived from the URL
// (2104178150-ai.github.io/REPO); elsewhere it falls back to this default.
const DEFAULT_PROJECT = '2104178150-ai/megaphone';

const STRINGS = {
  en: {
    eyebrow: 'Launch-readiness check for GitHub repos',
    heroTitle: 'Is your repo <em>ready to launch?</em>',
    heroSub: 'Paste a GitHub repo. Get a 0–100 launch score, the fixes that matter most, and where to post it.',
    inputLabel: 'GitHub repository',
    placeholder: 'owner/repo or https://github.com/owner/repo',
    check: 'Check',
    try: 'Try:',
    checking: 'Warming up the megaphone…',
    errInvalid: 'That doesn’t look like a GitHub repo. Try owner/repo.',
    errNotFound: 'Repo not found. It may be private or misspelled.',
    errRate: (t) => `GitHub’s hourly limit for anonymous requests is used up. Try again after ${t}.`,
    errHttp: (m) => `GitHub didn’t answer as expected (${m}). Try again in a moment.`,
    errNetwork: 'Couldn’t reach GitHub. Check your connection and try again.',
    outOf: 'out of 100',
    archived: 'This repo is archived — visitors will see it as finished or abandoned.',
    noReadme: 'No README found — that’s the first thing to write.',
    fixFirst: 'Fix these first',
    fixWith: 'Your agent can do this with',
    allGood: 'Nothing left to fix. Go launch it.',
    handT: 'Hand it to your AI agent',
    handHint: 'Open Claude Code, Codex, Cursor or any agent with the Megaphone skills in your local copy of the repo, and paste this.',
    handInstall: 'Install the skills ↓',
    handPrompt: (repo, score, items, total) => items.length
      ? `Use the Megaphone launch skills on this repo (github.com/${repo}). It scored ${score}/100 on the launch-readiness check. ${total > items.length ? `The ${items.length} biggest of ${total} failed checks` : 'Failed checks'}: ${items.join('; ')}. Fix what you can in the files and show me each change before you make it. For anything only I can decide or that changes the repo on GitHub (license, releases, About box, topics, website, Discussions), tell me exactly what to do instead. Then re-score the local README with launch-audit (audit.py ${repo} --readme README.md).`
      : `Use the Megaphone launch skills to plan the launch of this repo (github.com/${repo}, launch readiness ${score}/100): sharpen the pitch, prepare the right post for each channel that fits (a fact sheet where the platform wants my own words), and give me a dated plan.`,
    allChecks: 'All checks',
    where: 'Where to launch',
    playbook: 'Playbook →',
    badgeT: 'Show off your score',
    badgeHint: 'Paste into your README. It links back here so others can check theirs.',
    shareT: 'Share the result',
    starHint: 'Found this useful? A ⭐ on GitHub helps other developers find Megaphone.',
    shareText: (r, s, lvl, fix, url) => `📣 ${r} scored ${s}/100 on Megaphone’s launch-readiness check — ${lvl}.${fix ? ` Top fix: ${fix}.` : ''} Check yours: ${url}`,
    copy: 'Copy',
    copied: 'Copied ✓',
    howTitle: 'From score to launch',
    s1t: 'Score it',
    s1d: 'Twenty-one checks across first impression, time to wow, trust and shareability — the things that decide whether a visitor tries your project or leaves.',
    s2t: 'Let your AI agent fix it',
    s2d: 'Megaphone’s skills sharpen your pitch, rewrite the README’s first screen and prepare the right post for each channel — a native draft, or a fact sheet where the platform wants your own words — for Show HN, Reddit, V2EX, HelloGitHub, 小红书 and more.',
    s3t: 'Launch and measure',
    s3d: 'Get a dated launch plan, then line up star history and referrers against what you posted to see which channel actually worked.',
    installT: 'Install the skills (Claude Code, Codex, OpenClaw, Cursor and 70+ agents)',
    installCC: 'Or as a Claude Code plugin (two commands):',
    installThen: 'Then ask your agent: “launch this repo” — or “帮我推广这个项目”.',
    privacy: 'Runs entirely in your browser: repo data comes straight from GitHub (the API and raw.githubusercontent.com), the badge preview from shields.io. Nothing is stored on a server.',
    rate: (n) => `GitHub API: ${n} requests left this hour`,
    tokenPrompt: 'Out of anonymous requests? Paste a GitHub token to keep checking (5,000 requests an hour).',
    tokenPlaceholder: 'github_pat_… or ghp_…',
    tokenRetry: 'Retry with token',
    tokenHint: 'Create one at <a href="https://github.com/settings/personal-access-tokens/new" target="_blank" rel="noopener">github.com/settings/personal-access-tokens</a> — read-only access to public repositories is enough. It stays in this browser tab and is only sent to api.github.com.',
    tokenActive: 'Using your GitHub token',
    tokenClear: 'Forget it',
    errBadToken: 'GitHub rejected that token. Check it and try again.',
    pts: 'pts',
    sampleTag: 'Example result',
    sampleFixK: 'Fix first',
    sampleFix: 'Put a screenshot in the first screen',
    sampleWhereK: 'Post on',
  },
  zh: {
    eyebrow: 'GitHub 仓库发布体检',
    heroTitle: '你的开源项目，<em>准备好被看见了吗？</em>',
    heroSub: '粘贴一个 GitHub 仓库，得到 0–100 的发布就绪分、最该先改的几件事，以及适合去哪里发。',
    inputLabel: 'GitHub 仓库',
    placeholder: 'owner/repo 或 https://github.com/owner/repo',
    check: '检测',
    try: '试试：',
    checking: '喇叭预热中……',
    errInvalid: '这看起来不像 GitHub 仓库，试试 owner/repo 的格式。',
    errNotFound: '找不到这个仓库，可能是私有仓库或拼写有误。',
    errRate: (t) => `GitHub 匿名请求的每小时额度用完了，请在 ${t} 之后再试。`,
    errHttp: (m) => `GitHub 返回异常（${m}），稍后再试一次。`,
    errNetwork: '连不上 GitHub，检查一下网络再试。',
    outOf: '满分 100',
    archived: '这个仓库已归档——访客会以为它已经停更或废弃。',
    noReadme: '没有找到 README——这是第一件要写的东西。',
    fixFirst: '先改这几项',
    fixWith: '可以让 AI 用这个技能来改：',
    allGood: '没有要改的了，去发布吧！',
    handT: '交给你的 AI 助手',
    handHint: '在本地仓库目录里打开装了 Megaphone 技能的 Claude Code、Codex、Cursor 等 AI 助手，把这段话粘贴进去。',
    handInstall: '安装技能 ↓',
    handPrompt: (repo, score, items, total) => items.length
      ? `用 Megaphone 的发布技能处理这个仓库（github.com/${repo}）。它的发布就绪分是 ${score}/100，${total > items.length ? `没通过的 ${total} 项里影响最大的 ${items.length} 项` : '没通过的检查项'}：${items.join('；')}。能在文件里改的，先给我看改动再改；协议、Release、About 简介、topics、网站、Discussions 这类要我决定或会直接改 GitHub 上仓库的，告诉我具体怎么做，不要自己动手。改完用 launch-audit 给本地 README 重新打分（audit.py ${repo} --readme README.md）。`
      : `用 Megaphone 的发布技能帮这个仓库（github.com/${repo}，发布就绪分 ${score}/100）规划发布：提炼定位，为合适的渠道各准备一份文案（要求作者亲笔的平台给我一份事实清单），再给我一份带日期的发布计划。`,
    allChecks: '全部检查项',
    where: '去哪里发',
    playbook: '查看玩法 →',
    badgeT: '晒出你的分数',
    badgeHint: '贴进 README，徽章会链接回这里，别人也能来测自己的项目。',
    shareT: '分享结果',
    starHint: '觉得有用？去 GitHub 给 Megaphone 点个 ⭐，能让更多开发者看到它。',
    shareText: (r, s, lvl, fix, url) => `📣 ${r} 在 Megaphone 发布就绪检测中得了 ${s}/100 分——${lvl}。${fix ? `最该改的：${fix}。` : ''}测测你的项目：${url}`,
    copy: '复制',
    copied: '已复制 ✓',
    howTitle: '从打分到发布',
    s1t: '打分',
    s1d: '21 项检查，覆盖第一印象、上手速度、可信度和传播力——正是这些决定了访客是试一试，还是直接离开。',
    s2t: '让 AI 帮你改',
    s2d: 'Megaphone 的技能会帮你提炼定位、重写 README 首屏，并为每个渠道准备对症的文案：原生草稿，或者在要求作者亲笔的平台给你一份事实清单——Show HN、Reddit、V2EX、HelloGitHub、小红书等等。',
    s3t: '发布并复盘',
    s3d: '生成带日期的发布计划，再把 star 增长和流量来源对上你发过的帖子，看清到底哪个渠道有用。',
    installT: '安装技能（支持 Claude Code、Codex、OpenClaw、Cursor 等 70 多种 agent）',
    installCC: '或者作为 Claude Code 插件安装（两条命令）：',
    installThen: '然后对你的 AI 说：「帮我推广这个项目」——或者 “launch this repo”。',
    privacy: '完全在你的浏览器里运行：仓库数据直接来自 GitHub（API 和 raw.githubusercontent.com），徽章预览来自 shields.io，不在任何服务器上保存数据。',
    rate: (n) => `GitHub API 本小时剩余 ${n} 次请求`,
    tokenPrompt: '匿名额度用完了？粘贴一个 GitHub token 就能继续检测（每小时 5000 次）。',
    tokenPlaceholder: 'github_pat_… 或 ghp_…',
    tokenRetry: '用 token 重试',
    tokenHint: '在 <a href="https://github.com/settings/personal-access-tokens/new" target="_blank" rel="noopener">github.com/settings/personal-access-tokens</a> 创建，只给「公开仓库只读」权限就够了。token 只保存在当前标签页，只会发给 api.github.com。',
    tokenActive: '正在使用你的 GitHub token',
    tokenClear: '清除',
    errBadToken: 'GitHub 不认这个 token，检查一下再试。',
    pts: '分',
    sampleTag: '示例结果',
    sampleFixK: '先改',
    sampleFix: '首屏放一张截图或动图',
    sampleWhereK: '去哪发',
  },
};

const HTML_KEYS = new Set(['heroTitle', 'tokenHint']);
const SHIELD_COLORS = { great: 'brightgreen', good: 'green', ok: 'yellow', low: 'orange', mute: 'red' };

let lang = pickLanguage();
let last = null; // { analysis, data }

const $ = (sel) => document.querySelector(sel);
const t = (key) => STRINGS[lang][key];
const L = (obj) => (obj && typeof obj === 'object' ? obj[lang] : obj);

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
}

function pickLanguage() {
  try {
    const saved = localStorage.getItem('megaphone-lang');
    if (saved === 'en' || saved === 'zh') return saved;
  } catch (_) { /* storage blocked */ }
  return (navigator.language || '').toLowerCase().startsWith('zh') ? 'zh' : 'en';
}

function project() {
  const host = location.hostname;
  if (host.endsWith('.github.io')) {
    const owner = host.split('.')[0];
    const repo = location.pathname.split('/').filter(Boolean)[0] || 'megaphone';
    return `${owner}/${repo}`;
  }
  return DEFAULT_PROJECT;
}

function playbookUrl(file) {
  if (location.hostname.endsWith('.github.io')) {
    return `https://github.com/${project()}/blob/main/skills/launch-posts/channels/${file}`;
  }
  // Served from a local checkout: the docs folder sits next to skills/.
  return `../skills/launch-posts/channels/${file}`;
}

function checkerUrl(repo) {
  const base = location.origin + location.pathname;
  return repo ? `${base}?repo=${encodeURIComponent(repo)}` : base;
}

// ---------------------------------------------------------------------------
// Static text

function applyLanguage() {
  document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.dataset.i18n;
    if (HTML_KEYS.has(key)) el.innerHTML = t(key);
    else el.textContent = t(key);
  });
  document.querySelectorAll('[data-i18n-ph]').forEach((el) => { el.placeholder = t(el.dataset.i18nPh); });
  $('#lang').textContent = lang === 'zh' ? 'English' : '中文';
  const p = project();
  $('#gh-link').href = `https://github.com/${p}`;
  $('#install-npx').textContent = `npx skills add ${p}`;
  $('#install-cc').textContent = `/plugin marketplace add ${p}`;
  $('#install-cc2').textContent = `/plugin install ${p.split('/')[1]}@${p.split('/')[1]}`;
  renderTokenState();
  renderSample();
  if (last) render(last.analysis);
}

// A static example in the hero, so visitors see what they'll get before they type.
const SAMPLE = { score: 84, cats: { A: 27, B: 25, C: 16, D: 16 } };

function renderSample() {
  const lvl = LEVELS.find((l) => SAMPLE.score >= l.min);
  const c = 2 * Math.PI * 50;
  $('#sample').innerHTML = `
    <div class="sample-card">
      <span class="sample-tag">${esc(t('sampleTag'))}</span>
      <div class="sample-head">
        <div class="mini-dial"><svg viewBox="0 0 120 120"><circle class="track" cx="60" cy="60" r="50"/>
          <circle class="value c-${lvl.color}" cx="60" cy="60" r="50" stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${(c * (1 - SAMPLE.score / 100)).toFixed(1)}"/></svg>
          <b class="c-${lvl.color}">${SAMPLE.score}</b></div>
        <div><div class="sample-repo">your-name/your-repo</div>
          <div class="sample-level c-${lvl.color}">${lvl.emoji} ${esc(L(lvl.name))}</div></div>
      </div>
      <div class="sample-bars">${CATEGORIES.map((cat) => `
        <div class="sb"><span>${esc(L(cat.name))}</span><i><b style="width:${(SAMPLE.cats[cat.id] / cat.max) * 100}%"></b></i><em>${SAMPLE.cats[cat.id]}/${cat.max}</em></div>`).join('')}
      </div>
      <div class="sample-row"><span class="k">${esc(t('sampleFixK'))}</span><span class="v">${esc(t('sampleFix'))}</span><span class="gain">+8</span></div>
      <div class="sample-row"><span class="k">${esc(t('sampleWhereK'))}</span><span class="v tags"><span>Show HN</span><span>r/golang</span><span>V2EX</span><span>HelloGitHub</span></span></div>
    </div>`;
}

// ---------------------------------------------------------------------------
// Checking

function setStatus(text, isError = false) {
  const el = $('#status');
  el.textContent = text || '';
  el.classList.toggle('error', isError);
}

function setLoading(on) {
  $('#go').disabled = on;
  $('#art').classList.toggle('loading', on);
}

// Results are cached in this browser for an hour so re-checks don't spend the
// 60-requests-an-hour anonymous GitHub API budget.
const CACHE_PREFIX = 'megaphone:cache:';
const CACHE_TTL = 60 * 60 * 1000;
const CACHE_MAX = 15;

function cacheGet(key) {
  try {
    const hit = JSON.parse(localStorage.getItem(CACHE_PREFIX + key) || 'null');
    if (hit && Date.now() - hit.at < CACHE_TTL) return hit.data;
  } catch (_) { /* storage blocked or corrupt */ }
  return null;
}

function cacheSet(key, data) {
  try {
    const keys = Object.keys(localStorage).filter((k) => k.startsWith(CACHE_PREFIX));
    if (keys.length >= CACHE_MAX) {
      keys.map((k) => [k, (JSON.parse(localStorage.getItem(k) || '{}') || {}).at || 0])
        .sort((a, b) => a[1] - b[1])
        .slice(0, keys.length - CACHE_MAX + 1)
        .forEach(([k]) => localStorage.removeItem(k));
    }
    const { rate, apiCalls, ...rest } = data;
    localStorage.setItem(CACHE_PREFIX + key, JSON.stringify({ at: Date.now(), data: rest }));
  } catch (_) { /* quota or blocked */ }
}

// A visitor's own token lifts the limit to 5,000 requests an hour. It lives only in
// this tab's sessionStorage and is only ever sent to api.github.com.
function getToken() {
  try { return sessionStorage.getItem('megaphone-token') || null; } catch (_) { return null; }
}

function setToken(value) {
  try {
    if (value) sessionStorage.setItem('megaphone-token', value);
    else sessionStorage.removeItem('megaphone-token');
  } catch (_) { /* storage blocked */ }
  renderTokenState();
}

function renderTokenState() {
  const el = $('#token-state');
  if (getToken()) {
    el.hidden = false;
    el.innerHTML = `${esc(t('tokenActive'))} · <button class="link-btn" type="button" id="token-clear">${esc(t('tokenClear'))}</button>`;
  } else {
    el.hidden = true;
    el.textContent = '';
  }
}

function showTokenForm(show) {
  $('#token-form').hidden = !show;
  if (show) $('#token').focus();
}

// Each check gets an id; a slower earlier check never overwrites a newer one.
let currentRun = 0;

async function run(input) {
  const runId = ++currentRun;
  const full = parseRepoInput(input);
  if (!full) { setStatus(t('errInvalid'), true); return; }
  $('#repo').value = full;
  history.replaceState(null, '', checkerUrl(full));

  setLoading(true);
  setStatus(t('checking'));
  try {
    const key = full.toLowerCase();
    let data = cacheGet(key);
    if (!data) {
      const token = getToken();
      data = await fetchRepoData(full, { token });
      if (runId !== currentRun) return;
      // Only cache what anyone could see: never results fetched with a visitor's token
      // (they may include private repos), which would outlive the token in localStorage.
      if (!token && !(data.repo && data.repo.private)) cacheSet(key, data);
      if (data.rate) $('#rate').textContent = t('rate')(data.rate.remaining);
    }
    if (runId !== currentRun) return;
    const analysis = analyze(data);
    last = { analysis, data };
    setStatus('');
    showTokenForm(false);
    render(analysis, true);
  } catch (err) {
    if (runId !== currentRun) return;
    if (err instanceof FetchError) {
      if (err.kind === 'notfound') setStatus(t('errNotFound'), true);
      else if (err.kind === 'rate') {
        setStatus(t('errRate')(new Date(err.reset).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })), true);
        showTokenForm(true);
      } else if (err.kind === 'badtoken') {
        setToken(null);
        setStatus(t('errBadToken'), true);
        showTokenForm(true);
      } else setStatus(t('errHttp')(err.message), true);
    } else {
      console.error(err);
      setStatus(t('errNetwork'), true);
    }
  } finally {
    if (runId === currentRun) setLoading(false);
  }
}

// ---------------------------------------------------------------------------
// Rendering

function volumeFor(score) {
  return score >= 90 ? 4 : score >= 75 ? 3 : score >= 55 ? 2 : score >= 35 ? 1 : 0;
}

function render(a, animate = false) {
  const lvl = a.level;
  const circumference = 2 * Math.PI * 86;
  const fixes = a.fixes.slice(0, 3);
  const repoUrl = `https://github.com/${a.repo}`;
  const badgeImg = `https://img.shields.io/badge/launch%20readiness-${a.score}%2F100-${SHIELD_COLORS[lvl.color]}`;
  const badgeMd = `[![Launch readiness: ${a.score}/100](${badgeImg})](${checkerUrl(a.repo)})`;
  const handoff = t('handPrompt')(a.repo, a.score,
    a.fixes.slice(0, 5).map((f) => `${f.id} ${L(f.title)}${f.skill ? (lang === 'zh' ? `（${f.skill}）` : ` (${f.skill})`) : ''}`), a.fixes.length);
  const share = t('shareText')(a.repo, a.score, `${lvl.emoji} ${L(lvl.name)}`, fixes[0] ? L(fixes[0].title) : '', checkerUrl(a.repo));

  const notices = [];
  if (a.archived) notices.push(t('archived'));
  if (a.facts.empty) notices.push(t('noReadme'));

  const html = `
    <div class="card score-card">
      <div class="dial" role="img" aria-label="${a.score} / 100">
        <svg viewBox="0 0 200 200"><circle class="track" cx="100" cy="100" r="86"/>
          <circle class="value c-${lvl.color}" cx="100" cy="100" r="86"
            stroke-dasharray="${circumference.toFixed(1)}"
            stroke-dashoffset="${(animate ? circumference : circumference * (1 - a.score / 100)).toFixed(1)}"
            data-target="${(circumference * (1 - a.score / 100)).toFixed(1)}"/></svg>
        <div class="center"><div class="num c-${lvl.color}" id="num">${animate ? 0 : a.score}</div><div class="of">${esc(t('outOf'))}</div></div>
      </div>
      <div>
        <div class="repo-line"><a href="${esc(repoUrl)}" target="_blank" rel="noopener">${esc(a.repo)}</a></div>
        <p class="level c-${lvl.color}"><span aria-hidden="true">${lvl.emoji}</span>${esc(L(lvl.name))}</p>
        <p class="level-say">${esc(L(lvl.say))}</p>
        <div class="cats">
          ${a.categories.map((c) => `
            <div class="cat-row"><span>${esc(L(c.name))}</span>
              <div class="bar"><span style="width:${animate ? 0 : (c.score / c.max) * 100}%" data-w="${(c.score / c.max) * 100}"></span></div>
              <span class="cat-score">${c.score}/${c.max}</span></div>`).join('')}
        </div>
        ${notices.map((n) => `<p class="notice">${esc(n)}</p>`).join('')}
      </div>
    </div>

    <div class="split">
    <div class="card">
      <h2>${esc(t('fixFirst'))}</h2>
      ${fixes.length ? `<ol class="fixes">${fixes.map((f) => `
        <li><div><div class="fix-title">${esc(L(f.title))}</div>
          <div class="fix-body">${esc(L(f.fix))}</div>
          ${f.skill ? `<div class="fix-skill">${esc(t('fixWith'))} <code>${esc(f.skill)}</code></div>` : ''}</div>
          <span class="gain">+${f.max - f.points} ${esc(t('pts'))}</span></li>`).join('')}</ol>`
        : `<p>${esc(t('allGood'))}</p>`}
      <div class="prompt">
        <div class="prompt-head"><h3>${esc(t('handT'))}</h3><button class="copy" type="button" data-copy="handoff">${esc(t('copy'))}</button></div>
        <p id="handoff">${esc(handoff)}</p>
      </div>
      <p class="hint">${esc(t('handHint'))} <a href="#install">${esc(t('handInstall'))}</a></p>
    </div>

    <div class="card">
      <h2>${esc(t('where'))}</h2>
      <div class="channels">${a.channels.map((c) => `
        <div class="channel"><div class="channel-head"><b>${esc(L(c.name))}</b>
          ${c.file !== 'README.md' ? `<a href="${esc(playbookUrl(c.file))}" target="_blank" rel="noopener">${esc(t('playbook'))}</a>` : ''}</div>
          <p>${esc(L(c.why))}</p></div>`).join('')}
      </div>
    </div>
    </div>

    <div class="card">
      <h2>${esc(t('allChecks'))} <span class="count">${a.checks.filter((c) => c.pass).length}/${a.checks.length}</span></h2>
      ${CATEGORIES.map((cat) => {
        const items = a.checks.filter((c) => c.cat === cat.id);
        const score = items.reduce((s, c) => s + c.points, 0);
        return `<details class="cat"${score < cat.max ? ' open' : ''}><summary>${esc(L(cat.name))}<span class="s">${score}/${cat.max}</span></summary>
          <ul class="checks">${items.map((c) => {
            const state = c.pass ? 'pass' : c.points > 0 ? 'partial' : 'fail';
            const ico = c.pass ? '✓' : c.points > 0 ? '◐' : '✗';
            return `<li class="${state}"><span class="ico" aria-hidden="true">${ico}</span>
              <span>${esc(L(c.title))}<span class="ev">${esc(L(c.evidence))}</span></span>
              <span class="pts">${c.points}/${c.max}</span></li>`;
          }).join('')}</ul></details>`;
      }).join('')}
    </div>

    <div class="two">
      <div class="card">
        <h2>${esc(t('badgeT'))}</h2>
        <img class="badge-preview" src="${esc(badgeImg)}" alt="Launch readiness ${a.score}/100">
        <div class="codebox"><code id="badge-md">${esc(badgeMd)}</code><button class="copy" type="button" data-copy="badge-md">${esc(t('copy'))}</button></div>
        <p class="hint">${esc(t('badgeHint'))}</p>
      </div>
      <div class="card">
        <h2>${esc(t('shareT'))}</h2>
        <div class="codebox"><code id="share-text" class="prose">${esc(share)}</code><button class="copy" type="button" data-copy="share-text">${esc(t('copy'))}</button></div>
        <p class="hint"><a href="https://github.com/${esc(project())}" target="_blank" rel="noopener">${esc(t('starHint'))}</a></p>
      </div>
    </div>`;

  const el = $('#result');
  el.innerHTML = html;
  el.hidden = false;
  document.body.classList.add('has-result');
  $('#art').dataset.volume = String(volumeFor(a.score));

  if (animate) {
    requestAnimationFrame(() => requestAnimationFrame(() => {
      el.querySelectorAll('.bar > span').forEach((s) => { s.style.width = s.dataset.w + '%'; });
      const ring = el.querySelector('.dial .value');
      ring.style.strokeDashoffset = ring.dataset.target;
      countUp($('#num'), a.score);
    }));
    el.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
  }
}

function countUp(node, target) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { node.textContent = target; return; }
  const start = performance.now();
  const dur = 900;
  const step = (now) => {
    const p = Math.min(1, (now - start) / dur);
    node.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

async function copyText(btn) {
  const text = document.getElementById(btn.dataset.copy).textContent;
  try {
    await navigator.clipboard.writeText(text);
  } catch (_) {
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
  }
  btn.textContent = t('copied');
  setTimeout(() => { btn.textContent = t('copy'); }, 1500);
}

// ---------------------------------------------------------------------------
// Wiring

$('#form').addEventListener('submit', (e) => { e.preventDefault(); run($('#repo').value); });
$('#token-form').addEventListener('submit', (e) => {
  e.preventDefault();
  // Strip whitespace and zero-width characters that ride along when copying from rich text.
  const value = $('#token').value.replace(/[\s\u200B-\u200D\u2060\uFEFF]/g, '');
  if (!value) return;
  if (!/^[\x21-\x7E]+$/.test(value)) { setStatus(t('errBadToken'), true); return; }
  $('#token').value = '';
  setToken(value);
  run($('#repo').value);
});
document.addEventListener('click', (e) => {
  if (e.target.id === 'token-clear') setToken(null);
});
document.querySelectorAll('.chip').forEach((c) => c.addEventListener('click', () => run(c.dataset.repo)));
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.copy');
  if (btn) copyText(btn);
});
$('#lang').addEventListener('click', () => {
  lang = lang === 'zh' ? 'en' : 'zh';
  try { localStorage.setItem('megaphone-lang', lang); } catch (_) { /* ignore */ }
  applyLanguage();
});

applyLanguage();
const initial = new URLSearchParams(location.search).get('repo');
if (initial) run(initial);
