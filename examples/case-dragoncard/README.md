# DragonCard: 54 → 71 in one day · DragonCard：一天从 54 分到 71 分

[中文](#中文) · [English](#english)

[DragonCard](https://github.com/crazy-dragon/dragon_card) is a local-first flashcard tool by
[@crazy-dragon](https://github.com/crazy-dragon). Shared here with the author's permission
([dragon_card#6](https://github.com/crazy-dragon/dragon_card/issues/6)).

## 中文

2026-10-18，我们用 [Megaphone 检测器](https://2104178150-ai.github.io/megaphone/?repo=crazy-dragon/dragon_card)测了 DragonCard。报告里有 10 条可改的，我们给作者开了一个 issue，只提了 3 条：侧栏 Website 填上在线 Demo、首屏放一张截图、加几个 topics。第二天作者就改好了其中最快的两条：

| 检查项 | 改之前 | 改之后 | 分数 |
|---|---|---|---|
| 侧栏 Website 填在线 Demo | 空着（Demo 链接只在 README 正文里） | `https://dragoncard.top/` | +4 |
| 一步就能试 | 检测器没找到能直接试的地方 | 侧栏的 Demo 网站就算（同一处改动带来的） | +8 |
| 至少 3 个 topics | 没有 | 4 个，比如 `flashcards`、`local-first` | +5 |
| **总分** | **54 · 🔈 小声嘀咕** | **71 · 🔉 还需打磨** | **+17** |

**学到的：**

- **在线 Demo 要放进侧栏的 Website。** README 里已经有 Demo 链接，但 GitHub 侧栏和搜索结果里看不到，检测器也不把它算作「一步就能试」。填进 Website 一处，两项检查同时通过，一共 +12 分。
- **topics 是最便宜的分。** 加几个具体的词，不用改代码，话题页和搜索就能找到你。
- **只提 3 件事，不提 10 件。** issue 里只写了最值得做的 3 条，其中改起来最快的 2 条一天内就改好了。

**还能再涨的：** issue 里提过的首屏截图或 GIF（+8），以及发一个 Release（+4）。

## English

On 2026-10-18 we ran DragonCard through the
[Megaphone checker](https://2104178150-ai.github.io/megaphone/?repo=crazy-dragon/dragon_card). The report
listed ten fixes; we opened one issue with just three: put the live demo in the sidebar's Website field,
add a screenshot to the first screen, and add a few topics. The next day the author had made the two
quickest ones:

| Check | Before | After | Points |
|---|---|---|---|
| Demo in the About → Website field | Empty (the demo link was only in the README text) | `https://dragoncard.top/` | +4 |
| One step to try it | The checker found no way to try it directly | The demo site in the sidebar counts (same change) | +8 |
| At least 3 topics | None | 4, e.g. `flashcards`, `local-first` | +5 |
| **Score** | **54 · 🔈 Whispering** | **71 · 🔉 Needs polish** | **+17** |

**What it shows:**

- **Put the live demo in the Website field.** The README already linked the demo, but it didn't show in
  GitHub's sidebar or search results, and the checker didn't count it as a one-step try. One field passed
  two checks: +12 points.
- **Topics are the cheapest points.** A few specific words, no code, and topic pages and search can find you.
- **Ask for three things, not ten.** The issue named the three that mattered most; the two quickest were
  done within a day.

**Still open:** the screenshot or GIF from the issue (+8) and a first release (+4).
