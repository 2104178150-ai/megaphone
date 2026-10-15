# Channel map

The playbooks in this folder are built around the same sections: **Fit, Rules, Format,
Timing, Template, Pitfalls**. The Chinese ones use **适合什么项目 / 规则与习惯 / 格式 / 时机 /
模板 / 常见坑**, are written in Chinese, and start with an English summary; the rest are in
English. Some add channel-specific sections (how to submit, account setup, day of), and not
every channel has reliable timing data: where a playbook has no Timing section,
`launch-posts` writes "no data" instead of guessing. Each file says when it was last checked
and links to the platform's own rules where we found a public page; where the rules live
only in the app, it says so. Platforms change their rules; when a playbook and the platform
disagree, the platform wins. Please open a PR when you notice drift.

## Global

| Channel | Best for | Effort | Risk if done wrong | Playbook |
|---|---|---|---|---|
| Hacker News (Show HN) | Anything runnable that's technically interesting | Medium | Flagged / ignored | [hacker-news.md](hacker-news.md) |
| Reddit | Niche audiences via the right subreddit | Medium | Removal, ban | [reddit.md](reddit.md) |
| Product Hunt | Polished tools with a web presence | High | Wasted launch day | [product-hunt.md](product-hunt.md) |
| X / Bluesky | Build-in-public, demos, devs who follow you | Low–Medium | Low | [x-twitter.md](x-twitter.md) |
| DEV, Hashnode, Medium | "How I built it" articles | Medium | Low | [dev-blogs.md](dev-blogs.md) |
| Lobsters | Deeply technical projects (invite-only) | Low | Self-promo backlash | [lobsters.md](lobsters.md) |
| Awesome lists | Long-tail discovery that compounds | Low | PR rejected | [awesome-lists.md](awesome-lists.md) |
| Newsletters | Curated reach without needing an audience | Low | None | [newsletters.md](newsletters.md) |
| GitHub itself | Topics, Trending, social preview, releases | Low | None | [github-native.md](github-native.md) |
| Host ecosystems | Plugins, extensions and packages: VS Code, JetBrains, browser stores, Obsidian, Raycast, Homebrew, npm / PyPI, app plugin directories | Low–Medium | Listing rejected, annoyed host maintainers | [ecosystems.md](ecosystems.md) |

## Chinese channels

| Channel | Best for | Effort | Risk if done wrong | Playbook |
|---|---|---|---|---|
| V2EX 分享创造 | Tools and side projects, honest feedback | Low | Downvoted, "推广" backlash | [v2ex.md](v2ex.md) |
| HelloGitHub 月刊 | Interesting, beginner-friendly open source | Low | Not selected | [hellogithub.md](hellogithub.md) |
| 阮一峰《科技爱好者周刊》 | Useful tools, broad tech audience | Low | Not selected | [ruanyf-weekly.md](ruanyf-weekly.md) |
| 即刻 | Indie developers, AI/product people, personal stories | Low | Low | [jike.md](jike.md) |
| 小红书 | Consumer, AI and productivity tools with a visible result; students | Medium | Ignored without a good cover; throttled for 引流 | [xiaohongshu.md](xiaohongshu.md) |
| 掘金 | Technical write-ups for Chinese engineers | Medium | Low | [juejin.md](juejin.md) |
| 知乎, B 站, 开源中国, 少数派, Gitee | Long-tail answers, video demos, software directory, app-style tools, a mirror | Varies | Low (Gitee: mirror may fail review) | [china-other.md](china-other.md) |

## Quick picks by project type

| If your project is… | Start with |
|---|---|
| A CLI or developer library | GitHub topics → awesome list → r/commandline → Show HN → language subreddit (r/rust, r/golang, r/Python…) → language newsletter |
| Self-hostable software | r/selfhosted → Show HN → awesome-selfhosted |
| An AI / LLM tool | X demo video → Show HN → r/LocalLLaMA (if it runs local models) → 即刻 → 小红书 |
| A web app anyone can use | Show HN (no sign-up demo) → Product Hunt → r/SideProject → 小红书 |
| A consumer tool for Chinese users | 小红书 → V2EX 分享创造 → B 站 demo → HelloGitHub / 阮一峰周刊 → 即刻 |
| A plugin or integration for another app | The host's store or plugin directory ([ecosystems.md](ecosystems.md)) → the host's showcase space (ask its maintainers first) → the channels where the host's users already are |
| A learning resource or list | HelloGitHub → 阮一峰周刊 → V2EX → submit as a regular HN story (not Show HN) |
| Bilingual (EN + 中文) | Run the global and Chinese tracks on different days so you can answer comments in both |

## Other regions

We have no playbooks for these yet. They are well-known developer channels in their
regions; read each site's own guidelines before posting. Contributions welcome — see
[CONTRIBUTING.md](../../../CONTRIBUTING.md).

| Region | Channel | What it is |
|---|---|---|
| Japan | [Zenn](https://zenn.dev) | Articles and books by engineers |
| Japan | [Qiita](https://qiita.com) | Technical articles; its [community guidelines](https://help.qiita.com/ja/articles/qiita-community-guideline) say not to post articles mainly meant to advertise or sell, but technical write-ups of your own work don't count as advertising |
| Japan | [Hatena Bookmark](https://b.hatena.ne.jp) | Social bookmarking, with a テクノロジー (technology) category of trending entries |
| Korea | [GeekNews](https://news.hada.io) | Developer and tech news; makers post their own projects as "Show GN" |
| Russian-speaking | [Habr](https://habr.com) | Technical articles and news |

## Sequencing in one line

Fix the repo → seed the compounding channels (topics, awesome lists, newsletters, store
listings) → one "big" channel per day, never two on the same day → answer every comment
for the first few hours → log everything.
