# 📣 Megaphone 大喇叭

用营销人的方法发布你的开源项目——哪怕你从来没发布过任何东西。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![技能数: 7](https://img.shields.io/badge/agent%20skills-7-e8501c)](skills)
[![渠道手册: 16](https://img.shields.io/badge/channel%20playbooks-16-e8501c)](skills/launch-posts/channels)
[![支持 Claude Code、Codex、OpenClaw](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20OpenClaw-1f1b16)](#快速开始)

[English](README.md) | 简体中文 · [**在线检测你的项目 →**](https://2104178150-ai.github.io/megaphone/)

![Megaphone 给一个仓库打分：84/100，最该先改的三件事，以及适合去哪里发](docs/preview.svg)

- **先知道准备好了没有**——21 项检查，给出 0–100 的发布就绪分和最该先改的几件事。[打开网页就能测](https://2104178150-ai.github.io/megaphone/)，不用安装。
- **每个渠道一篇「原生」文案**——Show HN、Reddit、Product Hunt、X、V2EX、HelloGitHub、阮一峰周刊、小红书……每篇都按该平台的规则来写，规则注明出处和核对日期。
- **看清到底哪个渠道有用**——把 star 增长和流量来源，对上你在什么时候发了什么。

## 快速开始

把技能装进你的 AI 编程助手（支持 Claude Code、Codex、OpenClaw、Cursor 等 [70 多种](https://github.com/vercel-labs/skills#supported-agents)）：

```bash
npx skills add 2104178150-ai/megaphone
```

然后在你的项目里对 AI 说：

> 帮我推广这个项目

想用 Claude Code 插件的方式安装：

```bash
claude plugin marketplace add 2104178150-ai/megaphone
claude plugin install megaphone@megaphone
```

装好后，在会话里可以直接用 `/megaphone:launch`、`/megaphone:launch-audit` 等命令。

## 为什么做这个

大多数好的开源项目没火起来，不是因为做得不好，而是作者往 Hacker News 发了一个链接，
拿到两个赞，就以为没人在乎。把一个项目发布好，其实是一门手艺：定位、能留住人的 README、
懂每个社区的规矩、挑对时机、事后复盘——而大部分开发者从来没有机会学。

| | Megaphone | 通用营销提示词包 | 「推广渠道大全」清单 |
|---|---|---|---|
| 先读懂你的仓库再动笔 | ✅ | ❌ | ❌ |
| 渠道规则注明出处和核对日期 | ✅ | 部分 | ❌ |
| 覆盖中文开发者渠道（V2EX、HelloGitHub、即刻、小红书…） | ✅ | ❌ | 部分 |
| 复盘哪个渠道真正有效 | ✅ | ❌ | ❌ |
| 不安装也能先试 | ✅ [网页检测](https://2104178150-ai.github.io/megaphone/) | ❌ | — |
| 拒绝刷票、求赞 | ✅ | 不一定 | 不一定 |

## 里面有什么

### 技能（Skills）

| 技能 | 做什么 | 产出 |
|---|---|---|
| [`launch`](skills/launch/SKILL.md) | 串起下面整条流程，每一步都停下来让你确认 | — |
| [`launch-audit`](skills/launch-audit/SKILL.md) | 按[公开的评分标准](skills/launch-audit/rubric.md)打分，再加一轮「像真人访客一样」的审视 | `.megaphone/audit.md` |
| [`launch-positioning`](skills/launch-positioning/SKILL.md) | 找到一句话定位：给谁用、替代什么、凭什么信、和别人比好在哪 | `.megaphone/brief.md` |
| [`launch-readme`](skills/launch-readme/SKILL.md) | 重写 README 首屏，可选生成中英双语版本 | `README.md` |
| [`launch-posts`](skills/launch-posts/SKILL.md) | 选渠道，每个渠道写一篇原生文案 | `.megaphone/posts/*.md` |
| [`launch-plan`](skills/launch-plan/SKILL.md) | 按时区排好日期的发布日历和发布记录表 | `.megaphone/plan.md` |
| [`launch-review`](skills/launch-review/SKILL.md) | star 曲线、流量来源、每篇帖子带来的增长 | `.megaphone/report.md` |

### 渠道手册

每份手册都包含：适合什么项目、硬性规则、格式、时机、模板和常见坑，并尽量链接到平台自己的规则页面。[查看全部 →](skills/launch-posts/channels)

**海外：** [Hacker News](skills/launch-posts/channels/hacker-news.md) ·
[Reddit](skills/launch-posts/channels/reddit.md) ·
[Product Hunt](skills/launch-posts/channels/product-hunt.md) ·
[X / Bluesky](skills/launch-posts/channels/x-twitter.md) ·
[DEV 与博客](skills/launch-posts/channels/dev-blogs.md) ·
[Lobsters](skills/launch-posts/channels/lobsters.md) ·
[Awesome 列表](skills/launch-posts/channels/awesome-lists.md) ·
[Newsletter](skills/launch-posts/channels/newsletters.md) ·
[GitHub 本身](skills/launch-posts/channels/github-native.md)

**国内：** [V2EX](skills/launch-posts/channels/v2ex.md) ·
[HelloGitHub](skills/launch-posts/channels/hellogithub.md) ·
[阮一峰周刊](skills/launch-posts/channels/ruanyf-weekly.md) ·
[即刻](skills/launch-posts/channels/jike.md) ·
[小红书](skills/launch-posts/channels/xiaohongshu.md) ·
[掘金](skills/launch-posts/channels/juejin.md) ·
[知乎 / B 站 / 开源中国 / 少数派 / Gitee](skills/launch-posts/channels/china-other.md)

> 手册正文用英文写，方便全球开发者也能看懂怎么在中文社区发布；所有中文渠道的模板都是直接用中文写的。

### 网页检测器

[`docs/`](docs) 是一个纯静态页面（不用构建、没有依赖、没有服务器），用同一套标准给任意公开仓库打分、推荐渠道，并生成一枚可以放进 README 的徽章。它在浏览器里直接调用 GitHub 公开 API，国内网络也能打开。

## 一次发布是怎么跑的

```text
体检 ──▶ 定位 ──▶ README 首屏 ──▶ 各渠道文案 ──▶ 排期 ──▶（你亲自发）──▶ 复盘
 │        │          │               │            │                     │
audit.md brief.md  README.md      posts/*.md    plan.md             report.md
```

所有产出都放在仓库里的 `.megaphone/` 文件夹，你可以先看、再改、最后决定。Megaphone 永远不会替你发帖、投稿或发邮件。

## 原则

- **你来发，AI 只负责写稿。** 平台会惩罚自动化行为，而且署的是你的名字。
- **绝不求赞、求 star。** 这违反 Hacker News、Product Hunt 和 Reddit 的规则，帖子会直接被降权。
- **只说真话。** 不编数据、不编用户评价；不确定的地方标成 `[TODO]`。
- **原生而不是翻译。** 中文渠道的文案直接用中文、按中文社区的习惯来写。

## 常见问题

**用了就能涨 star 吗？** 它能让对的人、以他们愿意尝试的方式看到你的项目。至于会不会点 star，取决于项目本身。

**需要 GitHub token 吗？** 只有 `launch-review` 需要：GitHub 只对登录请求开放 stargazers 列表，流量数据还需要仓库的推送权限。其他功能都不需要。

**网页检测安全吗？** 完全在你的浏览器里运行，只调用 GitHub 公开 API。匿名请求每个 IP 每小时 60 次，每次检测大约用 5 次。

**我的项目只有中文 / 只有英文，会扣很多分吗？** 不会。双语只占 100 分里的 5 分，因为它能解锁更多渠道；用不到的话可以跳过。

## 参与贡献

平台规则一直在变，手册的准确度取决于最近一次是谁核对的。发现过时的地方，欢迎[提交「渠道规则变了」的 issue](../../issues/new/choose) 或直接发 PR——每份手册都有「Last checked」日期和出处链接。新增渠道或修改评分标准，请看 [CONTRIBUTING.md](CONTRIBUTING.md)。

运行测试：

```bash
python3 -m unittest discover -s tests       # launch-review 脚本
python3 -m http.server 8820                  # 然后打开 http://localhost:8820/tests/ 测检测器
```

有问题、想分享你的发布经历，欢迎来 [Discussions](../../discussions)。

## 开源协议

[MIT](LICENSE)
