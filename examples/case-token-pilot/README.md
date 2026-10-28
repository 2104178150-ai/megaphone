# token-pilot: 54 → 100 · token-pilot：从 54 分到 100 分

[中文](#中文) · [English](#english)

[token-pilot](https://github.com/anthonyhann/token-pilot) is a local bill for every AI coding tool
(Claude Code, Codex, Kimi Code and more), shown in the menu bar, by
[@anthonyhann](https://github.com/anthonyhann). Shared here with the author's permission
([token-pilot#1](https://github.com/anthonyhann/token-pilot/issues/1)).

> 「LICENSE 在不在，没有任何东西会报错。……这类问题靠自己的流程永远发现不了，只能靠外部体检。」
> — [@anthonyhann](https://github.com/anthonyhann/token-pilot/issues/1)

## 中文

2026-10-24，我们用 [Megaphone 检测器](https://2104178150-ai.github.io/megaphone/?repo=anthonyhann/token-pilot)测了 token-pilot：54 分，报告里有 10 条可改的。我们开了一个 issue，只提了 3 条：补上 LICENSE 文件、填仓库简介、加 topics。

**第一轮（10-26）：** 三条全做了，54 → 73。

| 检查项 | 改之前 | 改之后 | 分数 |
|---|---|---|---|
| 协议 | README 写着 MIT、徽章也链到 `LICENSE`，但文件不存在（点进去 404） | 补上 MIT 全文，GitHub 正确显示 MIT License | +6 |
| 仓库简介 | 空 | 「所有 AI 工具的本地账单，一抬头就看见 —— 只读本地日志，数据不出本机」 | +8 |
| topics | 0 个 | 8 个（我们建议的 5 个，加上 `llm-cost`、`ai-coding`、`tui`） | +5 |
| **总分** | **54 · 🔈 小声嘀咕** | **73 · 🔉 还需打磨** | **+19** |

**第二轮（10-27 → 10-28）：** 作者没等我们再提，自己照着完整报告把剩下的 7 项也做完了。

| 检查项 | 做了什么 | 分数 |
|---|---|---|
| 「为什么 / 对比」章节 | 和 ccusage、各工具自带用量页、商业代理工具横向对比 | +4 |
| 贡献指南 | `CONTRIBUTING.md`，重点写怎么报「数据不准」的 bug | +3 |
| 官网 / 演示链接 | 侧栏 Website 填上 GitHub Pages 展示页 | +4 |
| 社区入口 | 开了 Discussions | +5 |
| Issue 模板 | 加了 | +3 |
| 行为准则 | 加了 | +3 |
| 展示功能 | 只把标题「✨ 它能做什么」改成「✨ 功能清单：它能做什么」，内容一字没动 | +5 |
| **总分** | **73 → 100 · 📣 准备好喊出来了** | **+27** |

我们 2026-10-28 用 `audit.py` 复测：100 分。

**最后一行是我们的错。** 那一节本来就是功能介绍，是检测器只认「功能 / 特性 / 示例」这些词，不认「它能做什么」，作者为了让它识别才改了标题。作者在 issue 里指出：「内容达标、措辞不匹配」的漏判，提交者很难自查。我们当天就把「能做什么」「用法」「怎么用」「工作原理」「亮点」等中文说法加进了检测规则（[269b583](https://github.com/2104178150-ai/megaphone/commit/269b583)），现在原标题也能拿到这 5 分。

**学到的：**

- **最值得提醒的，是不会报错的问题。** 作者每天跑测试、看 CI，有反馈的错误都能抓住；而「LICENSE 文件在不在」没有任何机制会提醒。外部体检最有用的地方就在这里。
- **作者的改法常常比建议更好。** 我们建议的简介只有前半句，作者补了「数据不出本机」：账单类工具最容易被误解成云端统计，这半句在搜索结果里就把顾虑说清楚了。写对比章节时，作者还发现了一个之前没写进 README 的真实卖点：没有别的方案把国产模型和海外模型放在同一张账单里。
- **3 条建议是起点，不是上限。** issue 只提了 3 条；剩下 7 条是作者自己从完整报告里挑出来做的。所以报告要完整，issue 要简短。
- **用户发现的漏判，当天就修。** 关键词表是我们的实现细节，不该变成作者的负担。

## English

On 2026-10-24 we ran token-pilot through the
[Megaphone checker](https://2104178150-ai.github.io/megaphone/?repo=anthonyhann/token-pilot): 54, with
ten fixes listed. We opened one issue with just three: add the LICENSE file, fill in the About
description, and add topics.

**Round one (10-26):** all three done, 54 → 73.

| Check | Before | After | Points |
|---|---|---|---|
| License | README said MIT and the badge linked to `LICENSE`, but the file didn't exist (404) | Full MIT text added; GitHub now shows MIT License | +6 |
| Description | Empty | "A local bill for all your AI tools, at a glance. Reads local logs only; no data leaves your machine." (in Chinese) | +8 |
| Topics | 0 | 8 (the five we suggested, plus `llm-cost`, `ai-coding`, `tui`) | +5 |
| **Score** | **54 · 🔈 Whispering** | **73 · 🔉 Needs polish** | **+19** |

**Round two (10-27 → 10-28):** without being asked, the author worked through the other seven items in the
full report.

| Check | What they did | Points |
|---|---|---|
| "Why" or comparison section | Compared it with ccusage, each tool's own usage page, and commercial proxies | +4 |
| Contributing guide | `CONTRIBUTING.md`, focused on how to report "the numbers are wrong" bugs | +3 |
| Demo or website link | A GitHub Pages showcase in the Website field | +4 |
| Community channel | Turned on Discussions | +5 |
| Issue templates | Added | +3 |
| Code of conduct | Added | +3 |
| Shows what it does | Renamed the heading 「✨ 它能做什么」 ("What it does") to 「✨ 功能清单：它能做什么」 ("Features: what it does"); content unchanged | +5 |
| **Score** | **73 → 100 · 📣 Ready to launch** | **+27** |

Our own re-run of `audit.py` on 2026-10-28 gives 100.

**That last row was our mistake.** The section was already a feature list; the checker only knew Chinese
words like 功能 ("features") and 示例 ("examples"), not 能做什么 ("what it does"), so the author renamed
the heading to get it recognised. In the issue the author pointed out that a miss like this, where the content is
fine but the wording doesn't match, is hard for anyone to find on their own. The same day we added
能做什么, 用法 ("usage"), 怎么用 ("how to use"), 工作原理 ("how it works"), 亮点 ("highlights") and a few
more to the rule ([269b583](https://github.com/2104178150-ai/megaphone/commit/269b583)), so the original
heading now gets the 5 points too.

**What it shows:**

- **The most useful reminders are about things that never fail loudly.** The author runs tests and watches
  CI every day, so errors with feedback get caught; nothing ever tells you the LICENSE file is missing.
  That is where an outside check helps most.
- **Authors often improve on the advice.** We suggested the first half of the description; the author
  added "no data leaves your machine", which answers the first worry people have about a billing tool
  right in the search results. Writing the comparison section, the author also found a real selling point the
  README had never stated: no other tool puts Chinese and overseas models on the same bill.
- **Three suggestions are a starting point, not a ceiling.** The issue named three; the author picked the
  other seven from the full report. Keep the report complete and the issue short.
- **Fix a false negative the day a user finds it.** Our keyword list is an implementation detail; it
  shouldn't become the author's problem.
