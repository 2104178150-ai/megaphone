# 其他中文渠道：中国独立开发者项目列表、知乎、B 站、开源中国、少数派、Gitee

> **English summary:** Long-tail Chinese channels — slower than V2EX or 即刻, but content
> there keeps being found through search. List the project on 中国独立开发者项目列表
> (1c7/chinese-independent-developer, ~62k★) with a two-line entry via PR or issue: the main list takes only
> websites, apps and desktop apps that work on open, so CLIs, libraries and agent skills go to its 程序员版面; the
> one hard rule is that every link opens. Answer existing Zhihu questions honestly (and
> disclose you're the author), make demo videos for Bilibili (whether links in descriptions
> are clickable for new accounts is unverified), submit to OSChina's software library via
> 投递资讯 / 软件 (its 2023 guide's name for the entry; the current site may label it
> differently; review usually takes one working day), and write "why I built it / how I use
> it" pieces for sspai's Matrix community as the maker (sspai rejects developers posing as
> users or posting press releases). Gitee announced in May 2022 that public
> repositories are manually reviewed before they go public, so a mirror of a project that
> touches other platforms may be rejected; check the risks first.
>
> 最近核对：2026-10-16（中国独立开发者项目列表：2026-11-17，依据其 [README](https://github.com/1c7/chinese-independent-developer)、
> [程序员版面](https://github.com/1c7/chinese-independent-developer/blob/master/.github/pages/README-Programmer-Edition.md)
> 和 [提交说明](https://github.com/1c7/chinese-independent-developer/blob/master/.github/CONTRIBUTING.md)）。开源中国的投递流程依据其[帮助中心指南](https://www.oschina.net/help-center/oschina-guides/how-to-play-in-osc.html)（约 2023 年，入口名称以当前界面为准）；
> 少数派依据[开发者自荐指南](https://sspai.com/post/40262)（2017 年）和 [Matrix FAQ](https://sspai.com/post/65521)；
> Gitee 的审核依据 2022 年 5 月 Gitee 在知乎发布的声明（[The Register 报道](https://www.theregister.com/2022/05/20/gitee_code_review/)），
> 我们没在 Gitee 帮助文档里找到现行说明。其余是社区习惯，发布前看各平台当前规则。

## 适合什么项目

这些都是长尾渠道，见效比 V2EX 和即刻慢，但内容会被搜索持续找到。

| 平台 | 适合 | 形式 |
|---|---|---|
| 中国独立开发者项目列表 | 个人或小团队做的网站 / App / 桌面应用（主版面）；命令行工具、开源库、Agent Skill 等要写代码或敲命令才能用的（程序员版面） | 一行条目，发 PR 或 Issue |
| 知乎 | 有人在问「有没有好用的 XX 工具」的品类 | 回答已有问题、专栏文章 |
| B 站 | 能演示出效果的东西：网页 / 桌面应用、AI 工具、看得见输出的 CLI | 演示视频、教程 |
| 开源中国（OSChina） | 面向国内开发者和企业用户的开源项目 | 软件库收录、版本资讯 |
| 少数派（sspai） | 面向普通用户的应用和效率工具，不适合代码库 | 开发者自荐文章（以作者身份写「为什么做、我怎么用」） |
| Gitee | 已经有不少国内用户、需要国内下载地址的项目 | 仓库镜像 |

## 规则与习惯

- **中国独立开发者项目列表**：主版面的入选标准是「必须是网站或App，不能是开发者工具或论坛型网站」，
  收录「打开即用」的产品；用户是程序员、需要命令行（如 `npm install`）的项目放
  [程序员版面](https://github.com/1c7/chinese-independent-developer/blob/master/.github/pages/README-Programmer-Edition.md)。
  提交说明里唯一的硬性要求是**每个链接都能打开**（404、域名过期、跳到无关页面的不收；App Store 链接要能在国内区下载，
  只在海外区上架的注明「仅 XX 区」）。介绍语「先定性，再加分」：先说是什么，再说哪里不同；没有独特之处就写具体数字或
  限制（免费、无需注册、本地处理）。
- **知乎**：只回答你的项目确实能解决提问者问题的问题（例如「有哪些好用的开源 XXX 工具？」）。
  先认真回答问题本身，再提到你的项目，并**说明自己是作者**。不要在很多问题下贴同一段回答。
- **B 站**：视频简介里的外链对新账号是否可点、是否受限，**我们没有核实到**。简介里除了链接，
  再写一句「GitHub 搜 <名字>」作为备选，并把获取方式写在置顶评论里。
- **开源中国**：指南要求「不要从产品的角度来描述项目」，要多写开发者关注的特性、架构、逻辑原理。
  版本资讯要「有头有尾」，不要只贴 1、2、3 条变更。
- **少数派**：[Matrix 社区](https://sspai.com/matrix) 是用户写作区。2017 年的
  [开发者自荐指南](https://sspai.com/post/40262)里最重要的一条原则：不要假扮第三方或用户推荐、评测自己的产品，也不要
  发通稿。所以要以作者身份写：开头说明自己是开发者，再讲为什么做、自己怎么用，配真实截图。
  [Matrix FAQ](https://sspai.com/post/65521) 说有明显软文倾向、带不合规推广链接的文章可能被屏蔽。
- **Gitee**：Gitee 2022 年 5 月宣布，新的开源仓库要经人工审核才能公开，已公开的仓库先转为私有、
  审核后再恢复。项目如果调用其他平台的非官方接口、抓取数据或涉及版权内容，镜像**可能审核不过或
  被屏蔽**（推断，没有公开标准）。先看 `audit.md` 里的风险项再决定要不要镜像；镜像的话以 GitHub 仓库为准，
  两边 README 都写清楚。

## 怎么投稿（开源中国）

依据其[帮助中心指南](https://www.oschina.net/help-center/oschina-guides/how-to-play-in-osc.html)：

1. 登录开源中国，指南（约 2023 年）写的是从首页右上角点开个人信息，选 **「投递资讯 / 软件」**；新版界面里
   入口名称可能不同（例如「软件投递」），以当前界面为准。
2. 接收来自 GitHub、Gitee 等托管平台的开源项目。软件介绍写得越详细越好，从开发者关注的特性、架构、
   原理来写，不要写成产品宣传。
3. 指南说通常会在**一个工作日内**审核。收录后会有一个软件主页。
4. 以后发新版本：同一个入口选「投递资讯」，分类选「软件更新资讯」，填上关联的软件名，标题写名称 +
   版本号 + 亮点，出处填 release 链接。

## 怎么提交（中国独立开发者项目列表）

1. 先判断版面：打开网页、App 或桌面应用就能用 → 主版面（仓库根目录的 `README.md`）；要敲命令、`npm install`
   或写代码才能用 → 程序员版面（`.github/pages/README-Programmer-Edition.md`）；游戏另有游戏版面。
2. 按[提交说明](https://github.com/1c7/chinese-independent-developer/blob/master/.github/CONTRIBUTING.md)的格式写一条，
   加到列表最上面那个「YYYY 年 M 月 D 号添加」分组里，发 PR（我们的经历：加在最上面已有的日期分组里、没有新建分组，就被合并了）；
   README 说发 PR 或 Issue 都可以，不想改文件就开 Issue 贴这一条。
3. 发之前自己点一遍每个链接。（我们的经历）Megaphone 2026-10-18 发的 PR 加在程序员版面，不到两小时就合并了；
   这是一次经历，不代表平均速度。

## 格式

- **中国独立开发者项目列表**：一个 `####` 作者行 + 一个 `*` 条目行，状态用 `:white_check_mark:`（已上线）、
  `:clock8:`（开发中）、`:x:`（已关闭或缺乏维护）。城市、GitHub、博客、「更多介绍」都是可选项。
- **知乎回答**：先答问题 → 你的方案和截图 → 链接 + 作者声明。专栏文章写法和掘金文章类似：
  问题 → 思路 → 结果 → 链接。
- **B 站视频**：3–8 分钟的「从零用 <名字> 做 X」，或 1 分钟的快速演示。加上分段（章节）和
  封面大字标题，方便被搜索到。
- **开源中国**：软件介绍偏技术，版本资讯偏变更说明。
- **少数派**：以开发者身份写「我为什么做它、我自己怎么用它」+ 真实截图，开头写明自己是作者；不要写成
  第三方体验 / 评测或通稿。

## 时机

（经验）这些渠道见效慢，时间点不关键。适合放在主发布之后：先在 V2EX / 即刻拿到第一批反馈、修好问题，
再做 B 站视频和知乎回答，内容里可以写上真实的反馈和改进。开源中国的版本资讯在每次发版时投。

## 模板

中国独立开发者项目列表（[提交说明](https://github.com/1c7/chinese-independent-developer/blob/master/.github/CONTRIBUTING.md)的格式）：

```
#### <你的名字或 GitHub 用户名>(<城市，可选>) - [GitHub](https://github.com/<用户名>), [博客](<可选>)
* :white_check_mark: [<产品名称>](<网址或仓库地址>)：<是什么>，<哪里不同 / 具体数字 / 免费、本地处理等限制> - [更多介绍](<可选>)
```

知乎回答：

```
<先用两三段认真回答问题本身>

我自己做过一个相关的开源工具 <名字>（利益相关：我是作者），解决的是 <具体问题>：
<截图>
地址：<链接>。还不支持 <局限>，欢迎提意见。
```

B 站简介：

```
<一句话：这个视频演示什么>
<名字> 是开源的：<链接>（打不开的话 GitHub 搜「<名字>」）
00:00 效果 / 00:30 安装 / 01:30 <功能>
```

## 常见坑

- 把命令行工具或 Agent Skill 投到中国独立开发者项目列表的主版面 → 主版面只收打开即用的网站 / App / 桌面应用，应该投程序员版面。
- 所有平台发同一份文案 → 每个平台都有自己的格式，要改写。
- 回答里不说明作者身份 → 容易被举报为软广。
- 开源中国的软件介绍写成面向用户的产品介绍或广告词 → 指南明确要求不要从产品的角度描述，要从开发者
  关注的特性、架构、逻辑原理来写。
- 少数派文章写成第三方体验或评测、不说自己是开发者 → 自荐指南明确不允许。
- 不看风险就开 Gitee 镜像 → 可能审核不过，或者让项目多一个被投诉的入口。
