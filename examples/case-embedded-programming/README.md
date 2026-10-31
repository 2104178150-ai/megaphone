# Embedded-programming: 49 → 90 · Embedded-programming：从 49 分到 90 分

[中文](#中文) · [English](#english)

[Embedded-programming](https://github.com/wdcjx/Embedded-programming) (`embed`) is an agent skill that
lets Claude Code, Codex and other coding agents write simple STM32 projects (SPL or HAL, bare-metal or
FreeRTOS), with pin tables, wiring tables and a static checker for the generated code, by
[@wdcjx](https://github.com/wdcjx). Shared here with the author's permission
([Embedded-programming#1](https://github.com/wdcjx/Embedded-programming/issues/1)).

## 中文

2026-10-27，我们用 [Megaphone 检测器](https://2104178150-ai.github.io/megaphone/?repo=wdcjx/Embedded-programming)测了 Embedded-programming：49 分。技能本身很扎实（四条轨、静态检查脚本、48 条实测坑，每条都有症状 / 原因 / 修法），但第一次来的人看不出来。我们开了一个 issue，只提了 3 条：补上 LICENSE 文件、加一行 `npx skills add` 安装、首屏放一个真实的生成结果，代替一大段文件树。

**第一轮（不到 14 小时）：** 三条全做了，49 → 71。

| 检查项 | 改之前 | 改之后 | 分数 |
|---|---|---|---|
| 协议 | README 末尾写着「许可：MIT」，但仓库里没有 LICENSE 文件，GitHub 显示没有协议 | 补上 MIT 全文 | +6 |
| 一步试用 | 先 clone，再手动复制到 `~/.claude/skills/embed`，还要注意目录名 | 「安装」第一行是 `npx skills add wdcjx/Embedded-programming`，作者实测后写明：自动识别技能名 `embed`，`references/`、`scripts/`、`templates/` 都会带上 | +8 |
| 首屏截图 | 开头是一大段文件树 | 新的「生成结果长什么样」：一个用户用这个技能做出来的大棚环境监控节点，硬件实物、OLED 运行实拍、Keil 编译 0 Error 0 Warning 三张图，下面是一次简单需求的交付格式；文件树折叠到了最后 | +8 |
| **总分** | **49 · 🔈 小声嘀咕** | **71 · 🔉 还需打磨** | **+22** |

**第二轮（到 10-28 我们复测时）：** issue 里没提的，作者自己接着做了。

| 检查项 | 做了什么 | 分数 |
|---|---|---|
| 仓库简介 | 275 个字符的英文长句（检测器建议 20–160 个字符）改成了一句中文 | +4 |
| 至少一个 Release | [v0.9.1「首个公开版本」](https://github.com/wdcjx/Embedded-programming/releases/tag/v0.9.1)；10-30 又发了 v0.10.0 | +4 |
| 贡献指南 | `CONTRIBUTING.md`：提问前先查实测坑和症状反查表；新坑、新文档、validator 规则怎么贡献 | +3 |
| Issue 模板 | 两个：问题反馈、工程沉淀建议 | +3 |
| 社区入口 | 开了 Discussions，README 新增「反馈与社区」一节 | +5 |
| **总分** | **71 → 90 · 📣 准备好喊出来了** | **+19** |

我们 2026-10-28 用 `audit.py` 复测：90 分。作者之后又加了徽章，10-31 再测是 93 分。

**有一项是我们的误判。** 两栏里都有「为什么 / 对比」的 4 分，来自常见问题里的一个标题「模板在 VS Code 里报……」：检测器把「VS Code」里的 VS 当成了对比用的「vs」。这个仓库其实还没有对比章节。去掉这 4 分，是 45 → 86，涨幅一样（+41）。规则已在 2026-10-31 修好（[9c54990](https://github.com/2104178150-ai/megaphone/commit/9c54990)）：「VS Code」「VS 2022」这类写法不再算作对比，用修好的规则重测，今天是 89 分。

**学到的：**

- **「README 写了 MIT，却没有 LICENSE 文件」又出现了。** 和 [token-pilot](../case-token-pilot/) 一模一样：没有任何东西会报错，GitHub 只是安静地显示「没有协议」。这是最值得先查的一条。
- **真实产出比文件树更有说服力。** 我们在 issue 里举的是「串口回显」的例子，作者放的是一个用户真做出来的项目：实物、屏幕实拍、0 Error 截图。有了这个案例，作者还把 README 里「早期版本」的声明删掉了。
- **把建议写成可以验证的样子。** 我们说 `npx skills add` 应该能装好，请作者先试一下目录名对不对；作者实测后把结果写进了 README。作者自己验证过的安装说明，比我们说「应该可以」可信得多。
- **3 条是起点，不是上限。** issue 只提了 3 条，第二轮的 5 项是作者自己做的，第一个公开版本也是这时候发的。

**还能再涨的：** 侧栏 Website 填一个文档或演示页（+4）、行为准则（+3）。

## English

On 2026-10-27 we ran Embedded-programming through the
[Megaphone checker](https://2104178150-ai.github.io/megaphone/?repo=wdcjx/Embedded-programming): 49. The
skill itself is solid (four tracks, a static checker script, 48 pitfalls each written up as symptom, cause
and fix), but a first-time visitor couldn't see that. We opened one issue with just three suggestions: add
the LICENSE file, add a one-line `npx skills add` install, and open the README with a real generated result
instead of a long file tree.

**Round one (under 14 hours later):** all three done, 49 → 71.

| Check | Before | After | Points |
|---|---|---|---|
| License | The README ended with "License: MIT", but there was no LICENSE file, so GitHub showed no license | The full MIT text added | +6 |
| One step to try it | Clone, then copy by hand into `~/.claude/skills/embed`, minding the folder name | `npx skills add wdcjx/Embedded-programming` as the first install line; the author tested it and noted that it picks up the skill name `embed` and brings `references/`, `scripts/` and `templates/` along | +8 |
| Screenshot in the first screen | A long file tree | A new "what the output looks like" section: a greenhouse monitoring node a user built with the skill, shown as three photos (the hardware, the OLED running, Keil reporting 0 errors and 0 warnings), then the delivery format for one simple request; the file tree folded away at the end | +8 |
| **Score** | **49 · 🔈 Whispering** | **71 · 🔉 Needs polish** | **+22** |

**Round two (by our re-check on 10-28):** things the issue didn't mention, which the author did anyway.

| Check | What they did | Points |
|---|---|---|
| Description | A 275-character English sentence (the checker asks for 20–160) became one short Chinese sentence | +4 |
| At least one release | [v0.9.1, "first public release"](https://github.com/wdcjx/Embedded-programming/releases/tag/v0.9.1); v0.10.0 followed on 10-30 | +4 |
| Contributing guide | `CONTRIBUTING.md`: check the pitfalls list and symptom table before asking; how to contribute new pitfalls, new docs and validator rules | +3 |
| Issue templates | Two: report a problem, and suggest a tested project to write up | +3 |
| Community channel | Discussions turned on, plus a new "feedback and community" section in the README | +5 |
| **Score** | **71 → 90 · 📣 Ready to launch** | **+19** |

Our own re-run of `audit.py` on 2026-10-28 gives 90. The author has since added badges; on 10-31 it scores 93.

**One check was our mistake.** Both columns get 4 points for a "why / comparison" section, and both come
from an FAQ heading about an error in "VS Code": the checker read the "VS" as "vs". The repo doesn't have a
comparison section yet. Without those 4 points it's 45 → 86, the same +41. The rule was fixed on 2026-10-31
([9c54990](https://github.com/2104178150-ai/megaphone/commit/9c54990)): "VS Code" and "VS 2022" no longer count as a
comparison, and with the fixed rule the repo scores 89 today.

**What it shows:**

- **"MIT in the README, no LICENSE file" again.** Exactly as with [token-pilot](../case-token-pilot/):
  nothing ever flags it, and GitHub just quietly shows no license. It's the first thing worth checking.
- **A real result beats a file tree.** Our issue suggested a "serial echo" example; the author showed a
  project a user actually built, with photos of the board and screen and the 0-error build. With that in
  place, the author also removed the README's "early version" notice.
- **Write advice the author can verify.** We said `npx skills add` should work and asked the author to
  check the folder name first; they tested it and wrote the result into the README. Install notes the
  author has checked are worth more than our "it should work".
- **Three fixes are a start, not a ceiling.** The issue asked for three; the five in round two were the
  author's own, along with their first public release.

**Still open:** a docs or demo page in the Website field (+4) and a code of conduct (+3).
