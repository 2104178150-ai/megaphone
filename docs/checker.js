// Megaphone launch-readiness checker.
// Pure scoring logic + a small GitHub fetcher. Implements skills/launch-audit/rubric.md —
// keep the two in sync.

const API = 'https://api.github.com';

// ---------------------------------------------------------------------------
// Rubric

export const CATEGORIES = [
  { id: 'A', max: 35, name: { en: 'First impression', zh: '第一印象' } },
  { id: 'B', max: 25, name: { en: 'Time to wow', zh: '上手速度' } },
  { id: 'C', max: 20, name: { en: 'Trust', zh: '可信度' } },
  { id: 'D', max: 20, name: { en: 'Shareability', zh: '传播力' } },
];

// Fix ordering only — doesn't change the score.
const CATEGORY_WEIGHT = { A: 1.2, B: 1.2, C: 1, D: 0.8 };
// Failed checks that are blockers in rubric.md §1 go first, whatever their points:
// without a licence, nobody can legally use the project.
const BLOCKERS = new Set(['C1']);

// skill: which Megaphone skill fixes it (shown next to failed checks)
export const RUBRIC = [
  { id: 'A1', cat: 'A', max: 8, skill: 'launch-positioning',
    title: { en: 'Description (20–160 chars)', zh: '仓库简介（20–160 字符）' },
    fix: { en: 'Write a one-line description in the About box: what it is and who it’s for, 20–160 characters.',
           zh: '在仓库 About 里写一句简介：它是什么、给谁用，20–160 个字符。' } },
  { id: 'A2', cat: 'A', max: 5, skill: null,
    title: { en: 'At least 3 topics', zh: '至少 3 个 topics' },
    fix: { en: 'Add 3–8 specific topics (language, category, use case) so topic pages and search can find you.',
           zh: '加 3–8 个具体的 topics（语言、类别、用途），让话题页和搜索能找到你。' } },
  { id: 'A3', cat: 'A', max: 3, skill: 'launch-readme',
    title: { en: 'Title at the top of the README', zh: 'README 顶部有标题' },
    fix: { en: 'Start the README with the project name as a heading.',
           zh: 'README 开头用项目名作为一级标题。' } },
  { id: 'A4', cat: 'A', max: 4, skill: 'launch-readme',
    title: { en: 'Tagline near the top', zh: '开头有一句话介绍' },
    fix: { en: 'Put a plain one-sentence tagline directly under the title: the outcome, for whom.',
           zh: '在标题下面直接写一句话介绍：能带来什么结果、给谁用。' } },
  { id: 'A5', cat: 'A', max: 8, skill: 'launch-readme',
    title: { en: 'Screenshot, GIF or video in the first screen', zh: '首屏有截图、GIF 或视频' },
    fix: { en: 'Add a screenshot or a short GIF of the “aha” moment near the top — a logo doesn’t count. Visitors look before they read.',
           zh: '在 README 前部放一张截图或一段短 GIF，展示最惊艳的那一刻。访客先看图再读字。' } },
  { id: 'A6', cat: 'A', max: 4, skill: null,
    title: { en: 'Demo or website link', zh: '有演示或官网链接' },
    fix: { en: 'Set the Website field in the About box to a live demo or docs page.',
           zh: '在 About 的 Website 字段填上在线演示或文档地址。' } },
  { id: 'A7', cat: 'A', max: 3, skill: 'launch-readme',
    title: { en: 'README has substance (150+ words)', zh: 'README 内容充实（150 词以上）' },
    fix: { en: 'Explain what it does, how to use it and why it exists — at least a few paragraphs.',
           zh: '把它能做什么、怎么用、为什么做讲清楚——至少几段话。' } },

  { id: 'B1', cat: 'B', max: 7, skill: 'launch-readme',
    title: { en: 'Getting-started section', zh: '有「快速开始」章节' },
    fix: { en: 'Add a “Quick start” or “Install” section with the shortest path to a first result.',
           zh: '加一个「快速开始」或「安装」章节，写出最短的上手路径。' } },
  { id: 'B2', cat: 'B', max: 5, skill: 'launch-readme',
    title: { en: 'Code block early in the README', zh: 'README 前部有代码块' },
    fix: { en: 'Show the install or usage command in a code block near the top.',
           zh: '在靠前的位置用代码块写出安装或使用命令。' } },
  { id: 'B3', cat: 'B', max: 8, skill: 'launch-readme',
    title: { en: 'One step to try it (command or website)', zh: '一步就能试（一行命令或在线网站）' },
    fix: { en: 'Offer a single command to try it (npx, pipx/uvx, brew, docker run, go install…) or a hosted version that needs no sign-up.',
           zh: '提供一行命令就能试用（npx、pipx/uvx、brew、docker run、go install…），或者一个不用注册就能用的在线版本。' } },
  { id: 'B4', cat: 'B', max: 5, skill: 'launch-readme',
    title: { en: 'Shows what it does (features / examples)', zh: '展示它能做什么（功能 / 示例）' },
    fix: { en: 'Add a Features or Examples section, or three benefit bullets near the top.',
           zh: '加一个「功能」或「示例」章节，或在前部写三条好处。' } },

  { id: 'C1', cat: 'C', max: 6, skill: null,
    title: { en: 'License', zh: '开源协议' },
    fix: { en: 'Add a LICENSE file. Without one, people legally can’t use your code and many won’t try it.',
           zh: '加一个 LICENSE 文件。没有协议，别人在法律上无法使用你的代码，很多人会直接放弃。' } },
  { id: 'C2', cat: 'C', max: 4, skill: null,
    title: { en: 'Recently active', zh: '近期有更新' },
    fix: { en: 'Push something before you launch — a stale last commit makes visitors think it’s abandoned.',
           zh: '发布前推一次更新——最后一次提交太久远，访客会以为项目没人维护了。' } },
  { id: 'C3', cat: 'C', max: 4, skill: null,
    title: { en: 'At least one release', zh: '至少一个 Release' },
    fix: { en: 'Publish a release (v0.1.0 is fine) with short notes, so people can watch and pin versions.',
           zh: '发一个 Release（v0.1.0 就行）并写简短说明，方便别人关注和锁定版本。' } },
  { id: 'C4', cat: 'C', max: 3, skill: null,
    title: { en: 'Contributing guide', zh: '贡献指南' },
    fix: { en: 'Add CONTRIBUTING.md so launch visitors who want to help know how.',
           zh: '加 CONTRIBUTING.md，让想帮忙的访客知道怎么参与。' } },
  { id: 'C5', cat: 'C', max: 3, skill: null,
    title: { en: 'Issue templates', zh: 'Issue 模板' },
    fix: { en: 'Add issue templates for bugs and ideas — launch day brings both.',
           zh: '加上 Bug 和建议的 Issue 模板——发布当天两者都会来。' } },

  { id: 'D1', cat: 'D', max: 5, skill: 'launch-readme',
    title: { en: 'Two languages (EN + 中文)', zh: '中英双语' },
    fix: { en: 'Add README.zh-CN.md (or an English twin) to unlock Chinese channels: V2EX, HelloGitHub, 阮一峰周刊.',
           zh: '加一份 README.zh-CN.md（或英文版），打开 V2EX、HelloGitHub、阮一峰周刊等渠道。' } },
  { id: 'D2', cat: 'D', max: 4, skill: 'launch-readme',
    title: { en: '“Why” or comparison section', zh: '有「为什么 / 对比」章节' },
    fix: { en: 'Add a short “Why” section: what people use today and why this is better for them.',
           zh: '加一小节「为什么」：大家现在用什么，你的项目好在哪。' } },
  { id: 'D3', cat: 'D', max: 5, skill: null,
    title: { en: 'Community channel', zh: '有社区入口' },
    fix: { en: 'Turn on Discussions or link a Discord / Telegram / 微信群 so questions have a home.',
           zh: '开启 Discussions，或放上 Discord / Telegram / 微信群链接，让提问有地方去。' } },
  { id: 'D4', cat: 'D', max: 3, skill: 'launch-readme',
    title: { en: 'Badges', zh: '徽章' },
    fix: { en: 'Add a row of meaningful badges (version, license, CI) under the title.',
           zh: '在标题下加一行有意义的徽章（版本、协议、CI）。' } },
  { id: 'D5', cat: 'D', max: 3, skill: null,
    title: { en: 'Code of conduct', zh: '行为准则' },
    fix: { en: 'Add CODE_OF_CONDUCT.md — GitHub can generate one for you.',
           zh: '加 CODE_OF_CONDUCT.md——GitHub 可以帮你一键生成。' } },
];

export const LEVELS = [
  { min: 90, emoji: '📣', color: 'great', name: { en: 'Ready to launch', zh: '准备好喊出来了' },
    say: { en: 'Spend your launch now.', zh: '现在就可以发布了。' } },
  { min: 75, emoji: '🔊', color: 'good', name: { en: 'Almost there', zh: '就差一点' },
    say: { en: 'Fix the top items first — they’re cheap.', zh: '先改掉最前面几项，成本很低。' } },
  { min: 55, emoji: '🔉', color: 'ok', name: { en: 'Needs polish', zh: '还需打磨' },
    say: { en: 'Launching now would waste attention you won’t get back.', zh: '现在发布会浪费掉拿不回来的关注。' } },
  { min: 35, emoji: '🔈', color: 'low', name: { en: 'Whispering', zh: '小声嘀咕' },
    say: { en: 'Fix the first screen and the try-it path first.', zh: '先把首屏和上手路径做好。' } },
  { min: 0, emoji: '🔇', color: 'mute', name: { en: 'Muted', zh: '静音中' },
    say: { en: 'Not ready for visitors yet.', zh: '还没准备好迎接访客。' } },
];

export function levelFor(score) {
  return LEVELS.find((l) => score >= l.min);
}

// ---------------------------------------------------------------------------
// README facts

const BADGE_RE = /shields\.io|badgen\.net|badge|codecov|travis-ci|circleci|\/workflows\//i;
const IMAGE_RE = /!\[([^\]]*)\]\(\s*<?([^)\s>]+)/g;
const HTML_MEDIA_RE = /<(img|source|video)\b[^>]*>/gi;
// A logo or icon is branding, not a picture of the product.
const LOGO_RE = /logo|icon|avatar|favicon/i;
const SMALL_PX = 128;
// A pixel size from a width/height attribute; percentages (width="100%") aren't pixels.
const px = (v) => { const m = /^\s*(\d+)\s*(px)?\s*$/i.exec(v || ''); return m ? Number(m[1]) : 0; };
const ATTACHMENT_RE = /^\s*https:\/\/(?:github\.com\/user-attachments\/assets\/|user-images\.githubusercontent\.com\/)\S+\s*$/;
const HEADING_RE = /^\s{0,3}#{1,6}\s+\S|^\s*<h[1-6]\b/i;
const FENCE_RE = /^\s{0,3}(```|~~~)/;
const CJK_RE = /[㐀-鿿豈-﫿]/g;
const LATIN_WORD_RE = /[A-Za-z][A-Za-z'’-]*/g;

// A link to the repo's Releases page: with a release that has files, downloading the app is the one step.
const RELEASE_LINK_RE = /\/releases\b/i;
const INSTALL_RES = [
  /\bnpm\s+(?:i|install)\s+(?:-g\s+|--global\s+)?[@\w]/,
  /\bnpx\s+[@\w]/,
  /\bpnpm\s+(?:add|dlx)\s+\S/,
  /\byarn\s+(?:add|dlx|global\s+add)\s+\S/,
  /\bbun\s+(?:add|install|i|x|create)\s+[@\w]/,
  /\bbunx\s+[@\w]/,
  /\bpip3?\s+install\s+(?!-r\b)\S/,
  /\bpipx\s+(?:install|run)\s+\S/,
  /\buv\s+(?:tool\s+(?:install|run)|pip\s+install|add|run)\s+\S/,
  /\buvx\s+[@\w]/,
  /\bbrew\s+install\s+\S/,
  /\bport\s+install\s+\S/,
  /\bcargo\s+(?:install|add|binstall)\s+\S/,
  /\bgo\s+(?:install|get)\s+\S/,
  /\bdocker\s+(?:run|pull)\s+\S/,
  /\bdocker[\s-]compose\s+up\b/,
  /\b(?:curl|wget)\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba|z)?sh\b/,
  /\biwr\b[^\n|]*\|\s*iex\b/,
  /\bgem\s+install\s+\S/,
  /\bcomposer\s+(?:global\s+)?require\s+\S/,
  /\bdotnet\s+tool\s+install\s+\S/,
  /\b(?:winget|scoop|choco)\s+install\s+\S/,
  /\bapt(?:-get)?\s+install\s+\S/,
  /\b(?:snap|flatpak)\s+install\s+\S/,
  /\bnix\s+(?:run|profile\s+install|shell)\s+\S/,
  /\bhelm\s+install\s+\S/,
  /\bclaude\s+plugin\s+(?:install|marketplace\s+add)\s+\S/,
  /\/plugin\s+(?:install|marketplace\s+add)\s+\S/,
];

function stripInline(line) {
  return line
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')        // images
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')       // links → text
    .replace(/<[^>]+>/g, ' ')                      // html tags
    .replace(/[*_`~]/g, '')
    .replace(/^\s*>\s?/, '')                       // blockquote marker
    .replace(/\s+/g, ' ')
    .trim();
}

// Prose only: code, URLs, HTML and link targets don't count as words in any language.
function proseOf(text) {
  return text
    .replace(/`[^`\n]*`/g, ' ')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
    .replace(/\]\([^)]*\)/g, '] ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/https?:\/\/\S+/g, ' ');
}

function attr(tag, name) {
  const m = tag.match(new RegExp(`\\b${name}\\s*=\\s*(?:"([^"]*)"|'([^']*)'|([^\\s>]+))`, 'i'));
  return m ? (m[1] ?? m[2] ?? m[3] ?? '') : '';
}

function countWords(text) {
  const latin = (text.match(LATIN_WORD_RE) || []).length;
  const cjk = (text.match(CJK_RE) || []).length;
  return { latin, cjk, total: latin + Math.floor(cjk / 2) };
}

export function readmeFacts(md) {
  const text = (md || '').replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n');
  const lines = text.split('\n');

  // Skip fenced code when looking for headings, bullets and prose.
  const inFence = [];
  let open = false;
  for (const line of lines) {
    if (FENCE_RE.test(line)) { inFence.push(true); open = !open; continue; }
    inFence.push(open);
  }

  const nonEmpty = [];
  lines.forEach((l, i) => { if (l.trim()) nonEmpty.push(i); });

  // Each media item: { src, alt, video, small }
  const mediaIn = (from, to) => {
    const found = [];
    for (let i = from; i < Math.min(to, lines.length); i++) {
      const l = lines[i];
      for (const m of l.matchAll(IMAGE_RE)) found.push({ src: m[2], alt: m[1], video: false, small: false });
      for (const m of l.matchAll(HTML_MEDIA_RE)) {
        const tag = m[0];
        const w = px(attr(tag, 'width'));
        const h = px(attr(tag, 'height'));
        found.push({
          src: attr(tag, 'src'),
          alt: attr(tag, 'alt'),
          video: m[1].toLowerCase() !== 'img',
          small: (w > 0 && w <= SMALL_PX) || (h > 0 && h <= SMALL_PX),
        });
      }
      if (ATTACHMENT_RE.test(l)) found.push({ src: l.trim(), alt: '', video: true, small: false });
    }
    return found.filter((x) => x.src);
  };
  const isBadge = (x) => BADGE_RE.test(x.src);
  const isLogo = (x) => !x.video && (x.small || LOGO_RE.test(x.src) || LOGO_RE.test(x.alt));

  const headings = lines
    .map((l, i) => ({ l, i }))
    .filter(({ l, i }) => !inFence[i] && HEADING_RE.test(l))
    .map(({ l, i }) => ({ i, text: stripInline(l.replace(/^\s*#+\s*/, '')).toLowerCase() }));

  const titleAtTop = nonEmpty.slice(0, 15).some((i) => !inFence[i] && HEADING_RE.test(lines[i]));

  let tagline = null;
  for (const i of nonEmpty.slice(0, 25)) {
    const raw = lines[i];
    if (inFence[i] || HEADING_RE.test(raw) || FENCE_RE.test(raw)) continue;
    if (/^\s*([-*+]|\d+\.)\s/.test(raw) || /^\s*\|/.test(raw)) continue;
    const t = stripInline(raw);
    if (t.length < 10 || t.length > 200) continue;
    const w = countWords(t);
    if (w.latin < 3 && w.cjk < 8) continue;
    if (/^(english|简体中文|中文|繁體中文|日本語)(?![a-z])/i.test(t) && t.includes('|')) continue;
    tagline = t;
    break;
  }

  const firstScreen = mediaIn(0, 60);
  const visualItem = firstScreen.find((x) => !isBadge(x) && !isLogo(x));
  const visual = visualItem ? visualItem.src : null;
  const logoOnly = !visual && firstScreen.some((x) => !isBadge(x) && isLogo(x));
  const badges = mediaIn(0, 30).filter(isBadge);

  const fenceStart = lines.findIndex((l) => FENCE_RE.test(l));
  const installLine = lines.find((l) => INSTALL_RES.some((re) => re.test(l))) || null;
  const releaseLink = lines.some((l) => RELEASE_LINK_RE.test(l));

  const findHeading = (re, within = Infinity) => headings.find((h) => h.i < within && re.test(h.text)) || null;
  const gettingStarted = findHeading(/install|quick ?start|getting started|get started|setup|set up|usage|how to use|run|deploy|download|安装|怎么装|如何装|装上|快速开始|快速上手|上手|开始使用|使用|部署|运行|入门|用法|下载/);
  const showcase = findHeading(/feature|usage|example|demo|screenshot|how it works|what it does|tutorial|walkthrough|tour|showcase|gallery|功能|特性|示例|例子|演示|截图|效果|教程|展示|预览|看懂/, 120);
  const why = findHeading(/\bwhy\b|motivation|comparison|compare|\bvs\.?\b|alternative|difference|为什么|对比|比较|动机|初衷/);

  let bullets = 0;
  for (let i = 0; i < Math.min(80, lines.length); i++) {
    if (!inFence[i] && /^\s*[-*+]\s+\S/.test(lines[i]) && !BADGE_RE.test(lines[i])) bullets++;
  }

  const words = countWords(proseOf(lines.filter((_, i) => !inFence[i]).join('\n')));
  const translationLink = /README[._-]?(zh|cn|en|ja|ko|es|fr|de|ru|pt|tw|hk)[\w-]*\.md/i.test(text)
    || /\[(简体中文|中文|English|繁體中文|日本語)\]\(/.test(lines.slice(0, 40).join('\n'));
  // Inline bilingual = real prose in both languages, each at least a quarter of the words.
  // A Chinese README full of English product names and commands is still one language.
  const latinShare = words.total ? words.latin / words.total : 0;
  const inlineBilingual = words.cjk >= 30 && words.latin >= 80 && latinShare >= 0.25 && latinShare <= 0.75;
  const bilingual = inlineBilingual || translationLink;
  const communityLink = /discord\.(gg|com\/invite)|t\.me\/|slack\.com|gitter\.im|matrix\.to|微信群|qq群|QQ群|telegram/i.test(text);

  return {
    empty: !text.trim(),
    lines: lines.length,
    words,
    titleAtTop,
    tagline,
    visual,
    logoOnly,
    badges: badges.length,
    fenceStart,
    installLine: installLine && installLine.trim(),
    releaseLink,
    gettingStarted,
    showcase,
    why,
    bullets,
    bilingual,
    translationLink,
    communityLink,
    hasChinese: words.cjk >= 30,
    hasEnglish: words.latin >= 80,
    // compose files usually mean a server app; a bare `docker run` is often just a CLI image
    mentionsCompose: /docker(\s|-)compose|compose\.ya?ml/i.test(text),
  };
}

// ---------------------------------------------------------------------------
// Scoring

// The homepage counts as a demo/website only if it isn't just the repo page again.
export function externalHomepage(repo) {
  const url = (repo.homepage || '').trim().replace(/\/+$/, '').toLowerCase();
  if (!url) return null;
  const self = ('github.com/' + (repo.full_name || '')).toLowerCase();
  const bare = url.replace(/^https?:\/\//, '').replace(/^www\./, '');
  return bare === self ? null : repo.homepage.trim();
}

function daysSince(iso, now) {
  return iso ? (now - new Date(iso).getTime()) / 86400000 : Infinity;
}

const ev = (en, zh) => ({ en, zh });

export function analyze(data, now = Date.now()) {
  const { repo, readme, community, releases } = data;
  const f = readmeFacts(readme);
  const files = (community && community.files) || {};
  const desc = (repo.description || '').trim();
  const topics = repo.topics || [];

  const results = {};
  const set = (id, points, evidence) => { results[id] = { points, evidence }; };

  // A — first impression
  const descPts = (desc ? 4 : 0) + (desc.length >= 20 && desc.length <= 160 ? 4 : 0);
  set('A1', descPts, desc ? ev(`${desc.length} chars: “${desc}”`, `${desc.length} 个字符：「${desc}」`) : ev('No description', '没有简介'));
  set('A2', topics.length >= 3 ? 5 : topics.length >= 1 ? 2 : 0,
    ev(topics.length ? `${topics.length} topics: ${topics.join(', ')}` : 'No topics', topics.length ? `${topics.length} 个：${topics.join('、')}` : '没有 topics'));
  set('A3', f.titleAtTop ? 3 : 0, f.titleAtTop ? ev('Heading found at the top', '顶部有标题') : ev('No heading in the first 15 lines', '前 15 行没有标题'));
  set('A4', f.tagline ? 4 : 0, f.tagline ? ev(`“${f.tagline}”`, `「${f.tagline}」`) : ev('No plain sentence near the top', '开头没有一句话介绍'));
  set('A5', f.visual ? 8 : 0, f.visual ? ev('Found a screenshot, GIF or video near the top', '前部有截图、GIF 或视频')
    : f.logoOnly ? ev('Only a logo near the top — a logo isn’t a picture of the product', '前部只有 logo——logo 不算产品截图')
      : ev('Only badges (or nothing) in the first 60 lines', '前 60 行只有徽章或没有图片'));
  const site = externalHomepage(repo);
  set('A6', site ? 4 : 0, site ? ev(site, site)
    : repo.homepage ? ev('Website field points back to the repo itself', 'Website 字段填的是仓库自己的地址')
      : ev('Website field is empty', 'Website 字段为空'));
  set('A7', f.words.total >= 150 ? 3 : 0, ev(`≈ ${f.words.total} words`, `约 ${f.words.total} 词`));

  // B — time to wow
  set('B1', f.gettingStarted ? 7 : 0, f.gettingStarted ? ev(`Section: “${f.gettingStarted.text}”`, `章节：「${f.gettingStarted.text}」`) : ev('No install / quick start heading', '没有安装 / 快速开始章节'));
  const earlyFence = f.fenceStart >= 0 && f.fenceStart < 150;
  set('B2', earlyFence ? 5 : 0, earlyFence ? ev(`First code block at line ${f.fenceStart + 1}`, `第一个代码块在第 ${f.fenceStart + 1} 行`) : ev('No code block in the first 150 lines', '前 150 行没有代码块'));
  const latest = Array.isArray(releases) && releases.length ? releases[0] : null;
  const download = !!(latest && (latest.assets || []).length && f.releaseLink);
  set('B3', f.installLine || site || download ? 8 : 0,
    f.installLine ? ev(`\`${f.installLine.slice(0, 90)}\``, `\`${f.installLine.slice(0, 90)}\``)
      : site ? ev(`Try it online: ${site}`, `可以在线直接试用：${site}`)
        : download ? ev(`Download from Releases: ${latest.tag_name}`, `可以从 Release 下载：${latest.tag_name}`)
          : ev('No one-line install/run command, website or release download', '没有一行安装 / 运行命令、在线网站或 Release 下载'));
  const shows = f.showcase || f.bullets >= 3;
  set('B4', shows ? 5 : 0, f.showcase ? ev(`Section: “${f.showcase.text}”`, `章节：「${f.showcase.text}」`) : shows ? ev(`${f.bullets} bullet points near the top`, `前部有 ${f.bullets} 条要点`) : ev('No features / examples section', '没有功能 / 示例章节'));

  // C — trust
  set('C1', repo.license ? 6 : 0, repo.license ? ev(repo.license.spdx_id || repo.license.name, repo.license.spdx_id || repo.license.name) : ev('No license detected', '没有检测到协议'));
  const age = daysSince(repo.pushed_at, now);
  set('C2', age <= 90 ? 4 : age <= 365 ? 2 : 0, ev(`Last push ${Math.round(age)} days ago`, `最后一次推送在 ${Math.round(age)} 天前`));
  const hasRelease = Array.isArray(releases) && releases.length > 0;
  set('C3', hasRelease ? 4 : 0, hasRelease ? ev(`Latest: ${releases[0].tag_name}`, `最新：${releases[0].tag_name}`) : ev('No releases', '没有 Release'));
  set('C4', files.contributing ? 3 : 0, files.contributing ? ev('CONTRIBUTING found', '有 CONTRIBUTING') : ev('No CONTRIBUTING file', '没有 CONTRIBUTING'));
  const templates = files.issue_template || data.issueTemplates;
  set('C5', templates ? 3 : 0, templates ? ev('Issue templates found', '有 Issue 模板') : ev('No issue templates', '没有 Issue 模板'));

  // D — shareability
  set('D1', f.bilingual ? 5 : 0, f.bilingual ? ev(f.translationLink ? 'Links to a translated README' : 'English and Chinese in one README', f.translationLink ? '有翻译版 README 链接' : '一份 README 里中英都有') : ev(f.hasChinese ? 'Chinese only' : 'One language only', f.hasChinese ? '只有中文' : '只有一种语言'));
  set('D2', f.why ? 4 : 0, f.why ? ev(`Section: “${f.why.text}”`, `章节：「${f.why.text}」`) : ev('No “why” or comparison section', '没有「为什么 / 对比」章节'));
  const community_ = repo.has_discussions || f.communityLink;
  set('D3', community_ ? 5 : 0, repo.has_discussions ? ev('Discussions enabled', '已开启 Discussions') : f.communityLink ? ev('Chat link in README', 'README 里有群聊链接') : ev('No Discussions or chat link', '没有 Discussions 或群聊链接'));
  set('D4', f.badges ? 3 : 0, ev(`${f.badges} badge(s) near the top`, `前部有 ${f.badges} 个徽章`));
  const coc = files.code_of_conduct || files.code_of_conduct_file;
  set('D5', coc ? 3 : 0, coc ? ev('Code of conduct found', '有行为准则') : ev('No code of conduct', '没有行为准则'));

  const checks = RUBRIC.map((r) => ({ ...r, ...results[r.id], pass: results[r.id].points === r.max }));
  const categories = CATEGORIES.map((c) => {
    const inCat = checks.filter((x) => x.cat === c.id);
    return { ...c, score: inCat.reduce((s, x) => s + x.points, 0) };
  });
  const score = categories.reduce((s, c) => s + c.score, 0);
  // Rank fixes by impact: points to gain, weighted towards what launch visitors see first.
  const impact = (c) => (c.max - c.points) * CATEGORY_WEIGHT[c.cat];
  const fixes = checks
    .filter((c) => !c.pass)
    .map((c) => (BLOCKERS.has(c.id) ? { ...c, blocker: true } : c))
    .sort((a, b) => (b.blocker ? 1 : 0) - (a.blocker ? 1 : 0) || impact(b) - impact(a) || a.id.localeCompare(b.id));

  return {
    repo: repo.full_name,
    score,
    level: levelFor(score),
    categories,
    checks,
    fixes,
    facts: f,
    channels: recommendChannels(repo, f, results),
    archived: !!repo.archived,
  };
}

// ---------------------------------------------------------------------------
// Channel recommendations

const LANG_CHANNELS = {
  // This Week in Rust stopped taking project PRs in 2026-08; it picks project updates from r/rust.
  Rust: { sub: 'r/rust', news: null, feeds: 'This Week in Rust' },
  Go: { sub: 'r/golang', news: 'Go Weekly' },
  Python: { sub: 'r/Python', news: "PyCoder's Weekly" },
  JavaScript: { sub: 'r/javascript', news: 'JavaScript Weekly' },
  TypeScript: { sub: 'r/typescript', news: 'JavaScript Weekly' },
  Ruby: { sub: 'r/ruby', news: 'Ruby Weekly (Cooperpress)' },
  Swift: { sub: 'r/swift', news: null },
  Kotlin: { sub: 'r/Kotlin', news: null },
  'C++': { sub: 'r/cpp', news: null },
  C: { sub: 'r/C_Programming', news: null },
  Java: { sub: 'r/java', news: null },
  PHP: { sub: 'r/PHP', news: null },
  Elixir: { sub: 'r/elixir', news: null },
  Zig: { sub: 'r/Zig', news: null },
};

export function recommendChannels(repo, f, results = {}) {
  const topics = (repo.topics || []).map((t) => t.toLowerCase());
  const has = (...words) => words.some((w) => topics.includes(w));
  const runnable = !!(f.installLine || externalHomepage(repo));
  const out = [];
  const add = (id, file, name, why, weight) => out.push({ id, file, name, why, weight });

  add('github', 'github-native.md', ev('GitHub topics & social preview', 'GitHub topics 与分享卡片'),
    ev('Free, permanent, and every other channel lands here.', '零成本、长期有效，所有渠道最终都落到这里。'), 100);

  if (runnable && f.hasEnglish) {
    add('hn', 'hacker-news.md', ev('Show HN', 'Show HN'),
      ev('There’s a way to try it and an English README.', '有可直接试用的方式和英文 README。'), 90);
  }

  const lang = LANG_CHANNELS[repo.language];
  // Only name a language list for real programming languages: GitHub often reports HTML, CSS or
  // Jupyter Notebook for projects whose list would be awesome-<category>, not awesome-html.
  const listLang = lang ? repo.language.toLowerCase().replace('c++', 'cpp') : null;
  add('awesome', 'awesome-lists.md', ev('Awesome lists', 'Awesome 列表'),
    ev(listLang ? `Look for awesome-${listLang} and category lists.` : 'Find the awesome list for your category.',
       listLang ? `找 awesome-${listLang} 和对应类别的列表。` : '找到你所在类别的 awesome 列表。'), 80);

  const host = ['vscode-extension', 'vscode', 'visual-studio-code', 'obsidian-plugin', 'obsidian', 'chrome-extension',
    'browser-extension', 'firefox-addon', 'firefox-extension', 'webextension', 'raycast', 'raycast-extension',
    'jetbrains-plugin', 'intellij-plugin', 'siyuan', 'siyuan-plugin', 'plugin', 'extension'].find((t) => topics.includes(t));
  if (host) {
    add('ecosystems', 'ecosystems.md', ev('The host app’s plugin directory', '宿主应用的插件市场'),
      ev(`It’s a plugin or extension (“${host}”) — its users look in the host app’s directory first.`,
         `这是插件或扩展（「${host}」）——用户最先去宿主应用的插件市场里找。`), 92);
  }

  if (has('self-hosted', 'selfhosted', 'homelab', 'self-hosting') || f.mentionsCompose) {
    add('selfhosted', 'reddit.md', ev('r/selfhosted', 'r/selfhosted'),
      ev('It’s self-hostable (Docker Compose or a self-hosted topic).', '可以自部署（有 Docker Compose 或 self-hosted 标签）。'), 85);
  }
  if (has('llm', 'ollama', 'local-llm', 'llama', 'llamacpp', 'gguf')) {
    add('localllama', 'reddit.md', ev('r/LocalLLaMA', 'r/LocalLLaMA'),
      ev('It’s tagged for local models.', '标签显示与本地大模型相关。'), 78);
  }
  if (has('cli', 'terminal', 'command-line', 'tui', 'shell')) {
    add('commandline', 'reddit.md', ev('r/commandline', 'r/commandline'),
      ev('It’s a terminal tool — show an asciicast.', '这是终端工具——配一段 asciicast 演示。'), 72);
  }
  if (lang) {
    add('lang-sub', 'reddit.md', ev(lang.sub, lang.sub),
      lang.feeds
        ? ev(`Written in ${repo.language}; ${lang.feeds} picks project updates from ${lang.sub}.`,
          `使用 ${repo.language} 编写；${lang.feeds} 的项目栏目从 ${lang.sub} 里挑。`)
        : ev(`Written in ${repo.language}.`, `使用 ${repo.language} 编写。`), 70);
    if (lang.news) {
      add('lang-news', 'newsletters.md', ev(lang.news, lang.news),
        ev(`Newsletter for ${repo.language} developers.`, `面向 ${repo.language} 开发者的周刊。`), 65);
    }
  } else {
    add('sideproject', 'reddit.md', ev('r/SideProject', 'r/SideProject'),
      ev('Built for sharing your own projects.', '专门用来分享自己的项目。'), 55);
  }

  const ai = has('ai', 'llm', 'agent', 'agents', 'claude', 'openai', 'mcp', 'chatgpt', 'gpt', 'rag', 'ai-agent', 'claude-code', 'skills');
  if (ai) {
    add('x', 'x-twitter.md', ev('X / Bluesky demo video', 'X / Bluesky 演示视频'),
      ev('AI tools spread through short demo videos.', 'AI 工具靠短视频演示传播最快。'), 75);
  }

  if (f.hasChinese || f.translationLink) {
    add('v2ex', 'v2ex.md', ev('V2EX 分享创造', 'V2EX 分享创造'),
      ev('Chinese README — the main Chinese dev forum.', '有中文 README——国内最主要的开发者论坛。'), 88);
    add('hellogithub', 'hellogithub.md', ev('HelloGitHub 月刊', 'HelloGitHub 月刊'),
      ev('Self-submissions welcome; out on the 28th.', '欢迎自荐，每月 28 号出刊。'), 84);
    add('ruanyf', 'ruanyf-weekly.md', ev('阮一峰周刊', '阮一峰《科技爱好者周刊》'),
      ev('Submit via a GitHub issue; out on Fridays.', '在 GitHub 提 issue 投稿，每周五出刊。'), 82);
    if (ai) {
      add('jike', 'jike.md', ev('即刻', '即刻'),
        ev('Indie and AI builders hang out here.', '独立开发者和 AI 圈子聚集地。'), 68);
      add('xhs', 'xiaohongshu.md', ev('小红书', '小红书'),
        ev('AI tools do well with a strong cover image.', 'AI 工具配一张好封面效果不错。'), 60);
    }
  } else if (results.D1 && results.D1.points === 0) {
    add('unlock-cn', 'README.md', ev('Unlock Chinese channels', '解锁中文渠道'),
      ev('Add README.zh-CN.md to reach V2EX, HelloGitHub and 阮一峰周刊.', '加一份 README.zh-CN.md 就能投 V2EX、HelloGitHub 和阮一峰周刊。'), 40);
  }

  if (externalHomepage(repo) && runnable) {
    add('ph', 'product-hunt.md', ev('Product Hunt', 'Product Hunt'),
      ev('It has a website people can try.', '有可以直接访问试用的网站。'), 58);
  }

  return out.sort((a, b) => b.weight - a.weight).slice(0, 7);
}

// ---------------------------------------------------------------------------
// Input parsing and fetching

export function parseRepoInput(input) {
  const s = (input || '').trim().replace(/\.git$/, '').replace(/\/+$/, '');
  const m = s.match(/^(?:https?:\/\/)?(?:www\.)?github\.com\/([\w.-]+)\/([\w.-]+)/i) || s.match(/^([\w.-]+)\/([\w.-]+)$/);
  return m ? `${m[1]}/${m[2]}` : null;
}

export class FetchError extends Error {
  constructor(kind, message, extra = {}) {
    super(message);
    this.kind = kind;
    Object.assign(this, extra);
  }
}

function decodeBase64Utf8(b64) {
  const bin = atob(b64.replace(/\s/g, ''));
  const bytes = Uint8Array.from(bin, (c) => c.charCodeAt(0));
  return new TextDecoder('utf-8').decode(bytes);
}

const RAW = 'https://raw.githubusercontent.com';
const RAW_TIMEOUT_MS = 4000;

// raw.githubusercontent.com doesn't count against the API's 60-requests-an-hour limit,
// but it's blocked on some networks (notably mainland China). Give up quickly and return
// null so the caller falls back to the API.
async function fetchRawReadme(fullName, fetchImpl) {
  const ctrl = typeof AbortController === 'function' ? new AbortController() : null;
  const timer = ctrl ? setTimeout(() => ctrl.abort(), RAW_TIMEOUT_MS) : null;
  try {
    const res = await fetchImpl(`${RAW}/${fullName}/HEAD/README.md`, ctrl ? { signal: ctrl.signal } : {});
    return res.ok ? await res.text() : null;
  } catch (_) {
    return null;
  } finally {
    if (timer) clearTimeout(timer);
  }
}

// token: optional GitHub token from the visitor, for 5,000 instead of 60 requests an hour.
export async function fetchRepoData(fullName, { fetchImpl = fetch, token = null } = {}) {
  let rate = null;
  let apiCalls = 0;
  // A pasted token can carry invisible characters that fetch() refuses in a header.
  if (token && !/^[\x21-\x7E]+$/.test(token)) throw new FetchError('badtoken', 'The token contains characters a GitHub token never has');
  const headers = { Accept: 'application/vnd.github+json' };
  if (token) headers.Authorization = `Bearer ${token}`;

  const get = async (path, { optional = false } = {}) => {
    apiCalls++;
    const res = await fetchImpl(API + path, { headers });
    const remaining = res.headers.get('x-ratelimit-remaining');
    if (remaining !== null) {
      rate = { remaining: Number(remaining), reset: Number(res.headers.get('x-ratelimit-reset')) * 1000 };
    }
    if (res.ok) return res.json();
    if ((res.status === 403 || res.status === 429) && rate && rate.remaining === 0) {
      throw new FetchError('rate', 'GitHub API rate limit reached', { reset: rate.reset });
    }
    if (res.status === 401 && token) throw new FetchError('badtoken', 'GitHub rejected the token');
    if (optional && res.status === 404) return null;
    if (res.status === 404) throw new FetchError('notfound', 'Repository not found');
    throw new FetchError('http', `GitHub returned ${res.status}`);
  };

  // Optional lookups may fail quietly — but not on a rate limit or a bad token, or the
  // score would silently lose points.
  const softFail = (e) => {
    if (e instanceof FetchError && (e.kind === 'rate' || e.kind === 'badtoken')) throw e;
    return null;
  };

  const repo = await get(`/repos/${fullName}`);
  const [rawReadme, community, releases] = await Promise.all([
    fetchRawReadme(repo.full_name, fetchImpl),
    get(`/repos/${repo.full_name}/community/profile`, { optional: true }).catch(softFail),
    get(`/repos/${repo.full_name}/releases?per_page=1`, { optional: true }),
  ]);
  let readme = rawReadme;
  if (readme === null) {
    const readmeJson = await get(`/repos/${repo.full_name}/readme`, { optional: true });
    readme = readmeJson && readmeJson.content ? decodeBase64Utf8(readmeJson.content) : '';
  }

  // The community profile misses issue *forms* (.github/ISSUE_TEMPLATE/*.yml), so look directly.
  let issueTemplates = !!(community && community.files && community.files.issue_template);
  if (!issueTemplates) {
    const dir = await get(`/repos/${repo.full_name}/contents/.github/ISSUE_TEMPLATE`, { optional: true }).catch(softFail);
    issueTemplates = Array.isArray(dir) && dir.length > 0;
  }
  return { repo, readme, community, releases: releases || [], issueTemplates, rate, apiCalls };
}
