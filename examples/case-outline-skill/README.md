# outline-skill: 58 → 78 · outline-skill：从 58 分到 78 分

[中文](#中文) · [English](#english)

[outline-skill](https://github.com/huangy7/outline-skill) is an Agent Skill and CLI for writing and
formatting documents in the [Outline](https://www.getoutline.com/) knowledge base, by
[@huangy7](https://github.com/huangy7). Shared here with the author's permission
([outline-skill#3](https://github.com/huangy7/outline-skill/issues/3)).

> 「Megaphone 我也看了下，挺好用的，已经 star 了。」 — [@huangy7](https://github.com/huangy7/outline-skill/issues/3)

## 中文

2026-10-18，我们用 [Megaphone 检测器](https://2104178150-ai.github.io/megaphone/?repo=huangy7/outline-skill)测了 outline-skill：58 分，报告里有 10 条可改的。我们开了一个 issue，只提了 3 条：首屏放一个演示、加一份中文 README、打一个 v0.1.0 Release。作者改了前两条，还顺手补了两项，自己用 Megaphone 的 audit 脚本重新打分：

| 检查项 | 改之前 | 改之后 | 分数 |
|---|---|---|---|
| 首屏有截图、GIF 或视频 | 前 60 行没有图 | 一张工作流演示图（`assets/demo.svg`） | +8 |
| 中英双语 | 只有一种语言 | 加了 `README.zh-CN.md`，开头可以切换语言 | +5 |
| 有「为什么 / 对比」章节 | 没有 | 有 | +4 |
| 徽章 | 0 个 | 标题下一行徽章 | +3 |
| **总分** | **58 · 🔉 还需打磨** | **78 · 🔊 就差一点** | **+20** |

我们 2026-10-24 用 `audit.py` 复测，同样是 78 分。作者还在 README 的致谢里加了 Megaphone 的链接。

**学到的：**

- **Skill 类项目最需要一张演示图。** 一个「让 AI 帮你写文档」的工具，光看文字很难想象效果；首屏一张图就是 +8，是整个评分里最大的单项之一。
- **在中文渠道被发现的项目，值得有一份中文 README。** outline-skill 是在「中国独立开发者项目列表」里被我们看到的，有了中文版，V2EX、掘金这些渠道就都能用了。
- **只提 3 件事。** 作者改完那 2 条之后，自己又往下做了两项——建议少，反而更容易被接着做下去。

**还能再涨的：** issue 里提过的 Release（+4），以及侧栏 Website 填上文档或演示地址（+4）。

## English

On 2026-10-18 we ran outline-skill through the
[Megaphone checker](https://2104178150-ai.github.io/megaphone/?repo=huangy7/outline-skill): 58, with ten
fixes listed. We opened one issue with just three: show a demo in the first screen, add a Chinese README,
and tag a v0.1.0 release. The author did the first two, added two more on their own, and re-scored the
repo with Megaphone's audit script:

| Check | Before | After | Points |
|---|---|---|---|
| Screenshot, GIF or video in the first screen | No image in the first 60 lines | A workflow demo image (`assets/demo.svg`) | +8 |
| Two languages | One language only | `README.zh-CN.md`, with a language switch at the top | +5 |
| "Why" or comparison section | None | Added | +4 |
| Badges | 0 | A row under the title | +3 |
| **Score** | **58 · 🔉 Needs polish** | **78 · 🔊 Almost there** | **+20** |

Our own re-run of `audit.py` on 2026-10-24 also gives 78. The author also linked Megaphone in the
README's acknowledgements.

**What it shows:**

- **A skill needs a picture most of all.** "AI writes your docs for you" is hard to imagine from text;
  one image in the first screen is +8, one of the biggest single checks.
- **Found through a Chinese channel? Have a Chinese README.** We found outline-skill in a list of Chinese
  indie projects; with a Chinese README, channels like V2EX and 掘金 open up.
- **Ask for three things.** After the two from the issue, the author kept going on their own — a short
  list is easier to carry on with.

**Still open:** the release from the issue (+4), and a docs or demo link in the sidebar's Website field (+4).
