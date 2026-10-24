# 📣 Megaphone 大喇叭

用营销人的方法发布你的开源项目——哪怕你从来没发布过任何东西。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![技能数: 7](https://img.shields.io/badge/agent%20skills-7-e8501c)](skills)
[![渠道手册: 17](https://img.shields.io/badge/channel%20playbooks-17-e8501c)](skills/launch-posts/channels)
[![支持 Claude Code、Codex、OpenClaw](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20OpenClaw-1f1b16)](#快速开始)

[English](README.md) | 简体中文 · [**在线检测你的项目 →**](https://2104178150-ai.github.io/megaphone/) · 案例：[DragonCard 54 → 71](examples/case-dragoncard/)、[outline-skill 58 → 78](examples/case-outline-skill/)

[![Megaphone 给一个仓库打分：84/100，最该先改的三件事，以及适合去哪里发——点图片直接试](docs/preview.svg)](https://2104178150-ai.github.io/megaphone/)

- **先知道准备好了没有**——会让访客掉头就走的阻断项、曝光后会放大的风险，再加 21 项检查给出的 0–100 分。[打开网页就能给任意仓库打分](https://2104178150-ai.github.io/megaphone/)，不用安装。
- **每个渠道对症的文案**——Show HN、Reddit、Product Hunt、X、V2EX、HelloGitHub、阮一峰周刊、小红书……按各平台规则写好原生草稿；要求作者亲笔的平台（Show HN、V2EX、掘金、Lobsters 等）给你一份事实清单，由你自己来写。规则都注明出处和核对日期。
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

需要：一个支持 skills 的 AI 编程助手；自带的脚本需要 Python 3.8+（只用标准库）。网页检测器有浏览器就能用。

**看一次真实的发布：**[Megaphone 给自己做的发布](examples/self-launch/)——小红书配图和文案、V2EX 的事实清单（V2EX 不许 AI 代写，正文由作者本人写），以及最后真的发出去的内容。

**看别人的项目：**[DragonCard 一天从 54 分到 71 分](examples/case-dragoncard/)——作者第二天就改好了我们建议里最快的两条。[outline-skill 从 58 分到 78 分](examples/case-outline-skill/)——加了演示图和中文 README，作者说 Megaphone「挺好用的」。

**新项目被看到，差在哪：**[362 个新仓库的体检数据](research/2026-10-new-repos.zh-CN.md)——100 星以上的项目 68% 首屏有截图，5–99 星的只有 40%。

## 为什么做这个

> 我是学传播的，本来想做个大家都能用的东西。后来发现很多好项目做出来了却没人看。
>
> 我觉得程序员推广时最大的问题是只讲技术不讲好处，或者光顾着做功能，却把怎样吸引用户忘了。
>
> 我不会写代码。代码是 AI 写的，我负责定方向和把关。
>
> 我最满意的是帮 7 个独立开发者看了他们的项目。
>
> —— 作者 [@2104178150-ai](https://github.com/2104178150-ai)

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
| [`launch`](skills/launch/SKILL.md) | 串起下面整条流程，每一步都停下来让你确认，并记下你的回答 | `.megaphone/decisions.md` |
| [`launch-audit`](skills/launch-audit/SKILL.md) | 找出阻断项，回答「风险与就绪」的问题，再按[公开的评分标准](skills/launch-audit/rubric.md)给 README 打分 | `.megaphone/audit.md` |
| [`launch-positioning`](skills/launch-positioning/SKILL.md) | 找到一句话定位：给谁用、替代什么、凭什么信、和别人比好在哪，以及哪些话不能说 | `.megaphone/brief.md` |
| [`launch-readme`](skills/launch-readme/SKILL.md) | 重写 README 首屏，可选生成另一种语言的版本 | `README.md`，或先把方案放进 `.megaphone/` |
| [`launch-posts`](skills/launch-posts/SKILL.md) | 选渠道并说明为什么跳过其他渠道，每个渠道写一篇原生文案（要求作者亲笔的平台给事实清单） | `.megaphone/posts/` |
| [`launch-plan`](skills/launch-plan/SKILL.md) | 按时区排好日期的发布日历（含 go/no-go 检查点）和发布记录表 | `.megaphone/plan.md`、`log.csv` |
| [`launch-review`](skills/launch-review/SKILL.md) | star 曲线、流量来源、每篇帖子带来的增长 | `.megaphone/report.md` |

### 体检分三层：阻断项、风险、分数

1. **阻断项（Blockers）**——会让访客掉头就走的问题。把自己当成首发渠道的读者，从头读一遍 README 就能找到：快速开始展示不出项目的亮点、硬性依赖没写在首屏、没有许可证、安装命令跑不通。只要还有一个阻断项没解决，等级最高只能是「还需打磨」，分数再高也一样。
2. **风险与就绪**——项目被更多人看到之后，哪些问题会变严重：非官方 API、版权、隐私、托管的演示扛不住流量高峰。只回答，不计分。
3. **100 分制评分**——按[公开的评分标准](skills/launch-audit/rubric.md)做 21 项机械检查。如果某一项只是按字面规则算通过（或没通过），体检会另给一个人工修正分，并写明原因。

### 渠道手册

每份手册都包含：适合什么项目、硬性规则、格式、时机、模板和常见坑，并注明核对日期。平台有官方规则页面的，尽量直接链接；社区习惯和经验判断会明确标出来。[查看全部 →](skills/launch-posts/channels)

**海外：** [Hacker News](skills/launch-posts/channels/hacker-news.md) ·
[Reddit](skills/launch-posts/channels/reddit.md) ·
[Product Hunt](skills/launch-posts/channels/product-hunt.md) ·
[X / Bluesky](skills/launch-posts/channels/x-twitter.md) ·
[DEV 与博客](skills/launch-posts/channels/dev-blogs.md) ·
[Lobsters](skills/launch-posts/channels/lobsters.md) ·
[Awesome 列表](skills/launch-posts/channels/awesome-lists.md) ·
[Newsletter](skills/launch-posts/channels/newsletters.md) ·
[GitHub 本身](skills/launch-posts/channels/github-native.md) ·
[插件市场与宿主应用](skills/launch-posts/channels/ecosystems.md)

**国内：** [V2EX](skills/launch-posts/channels/v2ex.md) ·
[HelloGitHub](skills/launch-posts/channels/hellogithub.md) ·
[阮一峰周刊](skills/launch-posts/channels/ruanyf-weekly.md) ·
[即刻](skills/launch-posts/channels/jike.md) ·
[小红书](skills/launch-posts/channels/xiaohongshu.md) ·
[掘金](skills/launch-posts/channels/juejin.md) ·
[知乎 / B 站 / 开源中国 / 少数派 / Gitee](skills/launch-posts/channels/china-other.md)

> 海外渠道的手册用英文写，中文渠道的手册用中文写，开头附英文摘要，方便海外开发者也能看懂怎么在中文社区发布。

### 网页检测器和体检脚本

[`docs/`](docs) 是一个纯静态页面（不用构建、没有依赖、没有服务器），用同一套标准给任意公开仓库打分、推荐渠道，写好一段把没通过的检查项交给 AI 去改的指令，并生成一枚可以放进 README 的徽章。它在浏览器里直接读取 GitHub 的数据：API，以及用来读 README 的 raw.githubusercontent.com（打不开时自动改用 API）。它只给分数；阻断项和风险要靠 `launch-audit` 里的人工审视。

[`audit.py`](skills/launch-audit/scripts/audit.py) 在终端里给出同样的分数，还能在推送之前给本地草稿打分。[`tests/fixtures/rubric-cases.json`](tests/fixtures/rubric-cases.json) 里的共享用例保证两边结果一致。

```bash
python3 skills/launch-audit/scripts/audit.py OWNER/REPO                     # GitHub 上的当前版本
python3 skills/launch-audit/scripts/audit.py OWNER/REPO --readme README.md  # 本地草稿
```

## 一次发布是怎么跑的

```text
体检 ──▶ 定位 ──▶ README 首屏 ──▶ 各渠道文案 ──▶ 排期 ──▶（你亲自发）──▶ 复盘
 │        │          │               │            │                     │
audit.md brief.md  README.md      posts/*.md    plan.md             report.md
```

所有产出都放在仓库里的 `.megaphone/` 文件夹，你可以先看、再改、最后决定。`launch` 技能默认会把它加进 `.gitignore`：里面有还没发出去的草稿，之后还会存流量快照——这些数据 GitHub 本来只给有推送权限的人看。你的回答，以及你不在时 AI 做出的假设，都记在 `decisions.md` 里，后面的步骤不会再问一遍。Megaphone 永远不会替你发帖、投稿或发邮件。

## 它会运行什么、连接哪里

Megaphone 由 Markdown 写的技能和两个小 Python 脚本组成（只用标准库）。没有 hooks、没有 MCP 服务器、
不装任何依赖、不收集使用数据，也没有自己的服务器。

| 部分 | 什么时候运行 | 连接哪里 | 读取什么 | 写入什么 |
|---|---|---|---|---|
| 技能（`skills/*/SKILL.md`） | 你的 AI 助手按技能做事时 | 技能里写明的公开页面：`api.github.com`（查仓库信息）、`hn.algolia.com` 和 Reddit 搜索（查以前有没有发过）、手册里链接的各平台规则页 | 你仓库里的文件 | 你仓库里的 `.megaphone/`，并在 `.gitignore` 里加一行 `.megaphone/`；`README.md` 只在你同意时才改 |
| [`audit.py`](skills/launch-audit/scripts/audit.py) | 体检技能或你自己运行时 | `api.github.com`、`raw.githubusercontent.com` | 设置了的话读 `GITHUB_TOKEN` / `GH_TOKEN`，只发给 `api.github.com` | 打印报告 |
| [`stars.py`](skills/launch-review/scripts/stars.py) | 复盘技能或你自己运行时 | `api.github.com` | `GITHUB_TOKEN` / `GH_TOKEN`（看 star 用户和流量必须有；技能可能建议用 `gh auth token` 来设置），只发给 `api.github.com`；`.megaphone/log.csv` | `.megaphone/` 里的快照和报告 |
| 网页检测器（`docs/`） | 在你的浏览器里 | `api.github.com`、`raw.githubusercontent.com`、`img.shields.io` 的徽章图片 | 只有你粘贴了 token 才会用，只留在当前标签页 | 结果在你的浏览器里缓存一小时 |
| 维护者工具（`scripts/`、`tests/`） | 只在贡献者手动运行时；没有任何技能会调用 | `check_sources.py`：它 `SOURCES` 列表里的平台页面；`study.py`：`api.github.com` | `study.py`：`GITHUB_TOKEN` | 只写到你指定的位置 |

## 原则

- **你来发，AI 只负责写稿。** 平台会惩罚自动化行为，而且署的是你的名字。
- **帖子里绝不求赞、求 star。** 这违反 Hacker News、Product Hunt 和 Reddit 的规则，帖子会直接被降权。在自己的 README 或工具里轻轻提一句没问题；在帖子、私信里求，或者帮了别人之后要回报，都不行。
- **只说真话。** 不编数据、不编用户评价；不确定的地方标成 `[TODO]`。
- **绝不编造作者的话。** 「我做这个是因为……」只能是你自己的原话。没有你的原话，AI 会留一个 `[TODO]`，不会替你编一段缘起。
- **先想想曝光会不会惹麻烦。** 让项目「更响」之前，先看清发布会把什么暴露出来：非官方 API、受版权保护的内容、别人的数据、扛不住流量高峰的服务。任何草稿都不写「零风险」「完全合法」。
- **原生而不是翻译。** 中文渠道的文案直接用中文、按中文社区的习惯来写；也只用你能回复评论的语言来写。

## 常见问题

**用了就能涨 star 吗？** 它能让对的人、以他们愿意尝试的方式看到你的项目。至于会不会点 star，取决于项目本身。

**分数高就代表能火吗？** 不代表。分数衡量的是 README 的「样子」：访客能不能看出它是什么、长什么样、怎么试。阻断项衡量的是它对访客到底管不管用：一个 100 分的 README，如果快速开始展示不出核心功能，等级照样是「还需打磨」。至于大家想不想要这个项目，任何分数都说明不了。

**需要 GitHub token 吗？** 只有 `launch-review` 需要，而且要用维护者自己的：GitHub 只对登录请求开放 stargazers 列表，并且正在把它限制为仅仓库管理员和协作者可见（[文档](https://docs.github.com/en/rest/activity/starring)），流量数据还需要仓库的推送权限。其他功能都不需要；匿名额度用完时，网页检测器和 `audit.py` 也能用 token 提高额度。

**网页检测安全吗？** 完全在你的浏览器里运行，没有 Megaphone 自己的服务器。仓库数据直接来自 GitHub（公开 API 和 raw.githubusercontent.com）；徽章预览是一张 shields.io 图片，链接里只带分数。匿名 API 请求每个 IP 每小时 60 次，每次检测用 3–5 次，结果会在你的浏览器里缓存一小时。

**我的项目只有中文 / 只有英文，会扣很多分吗？** 不会。第二种语言只占 100 分里的 5 分，因为它能解锁更多渠道。如果你不打算用另一种语言发布，`launch-audit` 会把它记为「接受的取舍」，只按其余各项打分。

## 参与贡献

平台规则一直在变，手册的准确度取决于最近一次是谁核对的。发现过时的地方，欢迎[提交「渠道规则变了」的 issue](../../issues/new/choose) 或直接发 PR——每份手册都有「Last checked / 最近核对」日期，并写明信息来源。[`scripts/check_sources.py`](scripts/check_sources.py) 会重新读取手册里关键事实所依据的平台页面，标出上游已经变了的地方。新增渠道或修改评分标准，请看 [CONTRIBUTING.md](CONTRIBUTING.md)。

运行测试：

```bash
python3 -m unittest discover -s tests       # launch-review 脚本，以及用共享评分用例核对 audit.py
python3 -m http.server 8820                  # 然后打开 http://localhost:8820/tests/ 测检测器（同一套用例）
```

有问题、想分享你的发布经历，欢迎来 [Issues](../../issues)。如果 Megaphone 帮到了你，点个 ⭐ 能让更多开发者看到它。

## 开源协议

[MIT](LICENSE)
