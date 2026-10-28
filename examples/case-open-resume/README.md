# Open Resume: 70 → 79 · Open Resume：从 70 分到 79 分

[中文](#中文) · [English](#english)

[Open Resume](https://github.com/AniChikage/open-resume) is a free, self-hosted resume builder with all
templates, unlimited resumes, local SQLite storage and Docker support, by
[@AniChikage](https://github.com/AniChikage). Shared here with the author's permission
([open-resume#1](https://github.com/AniChikage/open-resume/issues/1)).

## 中文

2026-10-24，我们用 [Megaphone 检测器](https://2104178150-ai.github.io/megaphone/?repo=AniChikage/open-resume)测了 Open Resume：70 分。项目本身已经很完整（演示 GIF、安装命令、双语 README 都有），所以 issue 里只提了 2 条：加 topics、打一个 v1.0.0 Release。不到三天，作者两条都做了：

| 检查项 | 改之前 | 改之后 | 分数 |
|---|---|---|---|
| topics | 0 个 | 7 个：`resume-builder`、`cv`、`self-hosted`、`resume-template`、`docker`、`typescript`、`react` | +5 |
| 至少一个 Release | 没有 Release 和 tag | [v1.0.0](https://github.com/AniChikage/open-resume/releases/tag/v1.0.0)，中英文 README 都加了固定到这个 tag 的安装命令 | +4 |
| **总分** | **70 · 🔉 还需打磨** | **79 · 🔊 就差一点** | **+9** |

我们 2026-10-28 用 `audit.py` 复测，同样是 79 分。

**分数之外更重要的一件事：** 作者在准备 v1.0.0 时发现，Docker 运行镜像少了历史版本模块，容器根本起不来，于是先修好了这个 bug，再跑完 72 项测试、类型检查和 CI，并实际验证了登录、保存、重启后数据保留和历史版本恢复。我们只建议了「打个 Release」，可正是这一步，让作者把整条部署链路从头走了一遍。

**学到的：**

- **项目已经很好时，就少提几条。** 这次只提了 2 条，两条都被做了；硬凑到 3 条只会让真正有用的那两条被稀释。
- **讲清楚为什么，作者会做得比建议更多。** 我们说的是「自托管的人看重能锁定的稳定版本」，作者就顺手把 README 里的安装命令固定到了 v1.0.0，我们没想到这一步。
- **Release 是一次「发布前检查」。** 打版本会逼着人把部署流程完整跑一遍，这比 4 分本身更有价值。

**还能再涨的：** 「为什么 / 对比」章节（+4）、社区入口如 Discussions（+5）、标题下一行徽章（+3），以及贡献指南、Issue 模板、行为准则（各 +3）。

## English

On 2026-10-24 we ran Open Resume through the
[Megaphone checker](https://2104178150-ai.github.io/megaphone/?repo=AniChikage/open-resume): 70. The
project was already in good shape (a demo GIF, an install command, a README in two languages), so the
issue asked for only two things: add topics, and tag a v1.0.0 release. Within three days the author did
both:

| Check | Before | After | Points |
|---|---|---|---|
| Topics | 0 | 7: `resume-builder`, `cv`, `self-hosted`, `resume-template`, `docker`, `typescript`, `react` | +5 |
| At least one release | No releases or tags | [v1.0.0](https://github.com/AniChikage/open-resume/releases/tag/v1.0.0), with install commands pinned to that tag in both READMEs | +4 |
| **Score** | **70 · 🔉 Needs polish** | **79 · 🔊 Almost there** | **+9** |

Our own re-run of `audit.py` on 2026-10-28 also gives 79.

**What mattered more than the score:** while preparing v1.0.0, the author found that the Docker runtime
image was missing the version-history module, so the container wouldn't start. They fixed it first, then
ran the 72 tests, type checks and CI, and checked by hand that login, saving, data surviving a restart and
restoring old versions all worked. We only suggested "tag a release", but that step made the author walk
the whole deployment path from start to finish.

**What it shows:**

- **When a project is already good, ask for less.** Two suggestions, both done; padding the list to three
  would only have diluted the two that mattered.
- **Explain why, and authors go further than the advice.** We said self-hosters value a stable version they
  can pin; the author pinned the README's install commands to v1.0.0, which we hadn't thought of.
- **A release works as a pre-launch check.** Cutting a version forces you to run the whole deployment once,
  which is worth more than its 4 points.

**Still open:** a "why" or comparison section (+4), a community channel such as Discussions (+5), badges
under the title (+3), and a contributing guide, issue templates and a code of conduct (+3 each).
