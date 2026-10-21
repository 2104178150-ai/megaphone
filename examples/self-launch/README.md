# Megaphone launching itself · Megaphone 给自己做的发布

[中文](#中文) · [English](#english)

## 中文

这个文件夹里是 Megaphone 的技能为它自己准备、并且真的发出去了的东西：

| 渠道 | 准备了什么 | 为什么这样做 |
|---|---|---|
| 小红书 | 5 张 3:4 配图（`xiaohongshu-1.jpg` … `5.jpg`）+ 文案和话题（[xiaohongshu.md](xiaohongshu.md)） | 小红书要求发布时声明 AI 辅助，图片和正文里也不能放站外链接，所以只写「GitHub 搜……」 |
| V2EX | 只有事实清单和提纲（[v2ex.md](v2ex.md)），没有现成正文 | V2EX 规定主题和回复都不能用 AI 生成的文字，正文要作者本人写 |
| 掘金沸点 | 作者回答 4 个问题，用自己的话写成；[发出的沸点](https://juejin.cn/pin/7697470958782169088) | 掘金把直接发布 AI 生成的技术内容算作抄袭类违规 |
| 中国独立开发者项目列表 | 按它的格式写好的一行介绍；[已收录](https://github.com/1c7/chinese-independent-developer/pull/1599) | 程序员版收命令行和开源项目，主版面只收网站和 App |

<p>
  <img src="xiaohongshu-1.jpg" width="240" alt="小红书封面：开源项目没人看？先给它做个体检">
  <img src="xiaohongshu-3.jpg" width="240" alt="小红书第 3 张：一个真实项目的检测结果">
</p>

## 我们做错了什么、后来怎么改的

如实记录，这些教训已经写回了 Megaphone 的技能里：

| 做错的 | 后果 | 现在的做法 |
|---|---|---|
| 项目刚上线就投了 HelloGitHub | 每个仓库只能投一次，如果这次没选上，就没有第二次了；我们交的是最早、最粗糙的版本 | 只有一次机会的渠道，等首页和案例都准备好再用 |
| 推广引来的几乎都是中文访客，落地的却是英文首页 | 只有 3 个人点进了中文版；推广开始后两天没有新 star | 先按每个渠道访客的语言检查首页；英文 README 标语下加一行中文 |
| 掘金沸点发在北京时间凌晨 3 点半 | 发出去时大多数读者在睡觉（仍带来 5 个访客，白天发会多多少不知道） | 不在窗口期就定时或等，不因为「写好了」就发 |
| 一天开了五个渠道 | 除了掘金，分不清访客从哪来 | 早期一次开一个小渠道，间隔 2–3 天，对照基线看效果 |
| 小红书第一篇是产品介绍、新号没养号、正文写了「GitHub 搜」 | 两天 5–6 次浏览、0 互动 | 第二篇改成干货清单 + 评论区免费体检，不提去哪找工具 |

## English

What Megaphone's own skills prepared for its launch, and what actually went out:

| Channel | What was prepared | Why |
|---|---|---|
| 小红书 (Xiaohongshu) | Five 3:4 images and the note text with topics ([xiaohongshu.md](xiaohongshu.md)) | The platform requires declaring AI help at publish time and bans off-platform links, so the post says what to search for instead |
| V2EX | A fact sheet and outline only ([v2ex.md](v2ex.md)) | V2EX's rules ban AI-generated text in topics and replies; the author writes the post |
| 掘金 (Juejin) | The author's own answers to four questions; [the published post](https://juejin.cn/pin/7697470958782169088) | Juejin treats AI-generated technical content posted directly as plagiarism |
| Chinese Independent Developer list | One line in the list's format; [merged](https://github.com/1c7/chinese-independent-developer/pull/1599) | Its programmer edition takes CLI and open-source projects |

### What we got wrong, and what changed

Recorded honestly; each lesson is now part of Megaphone's skills.

| Mistake | Effect | What we do now |
|---|---|---|
| Submitted to HelloGitHub on day one | It takes each repo once; if this one isn't picked, there's no second try, and we sent the earliest, roughest version | Hold one-shot channels until the landing page and a case study are ready |
| Traffic came from Chinese channels, but landed on an English README | Only 3 people opened the Chinese one; no new stars in the two days after promotion began | Check the landing page in each channel's language; one Chinese line under the English tagline |
| Posted on 掘金 at 03:30 Beijing time | Most readers were asleep (it still sent 5 visitors; how many more a daytime post would have sent, we don't know) | Outside the window, schedule or wait — "ready" isn't a reason to post |
| Opened five channels on one day | Apart from 掘金, no way to tell who brought whom | Early on, one small channel at a time, 2–3 days apart, against a baseline |
| First 小红书 note: a product intro, from a cold account, with "search GitHub for …" | 5–6 views and no interactions in two days | The next note leads with a checklist and offers free checks in the comments, with no pointer elsewhere |
