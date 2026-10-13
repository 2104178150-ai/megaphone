# Channel map

Every playbook in this folder has the same sections: **Fit, Rules, Format, Timing,
Template, Pitfalls**. Playbooks for Chinese channels are written in Chinese with an
English summary at the top; the rest are in English. Each file says when its rules were last checked and links to the
platform's own rules where they exist. Platforms change their rules; when a playbook
and the platform disagree, the platform wins. Please open a PR when you notice drift.

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

## Chinese developer channels

| Channel | Best for | Effort | Risk if done wrong | Playbook |
|---|---|---|---|---|
| V2EX 分享创造 | Tools and side projects, honest feedback | Low | Downvoted, "推广" backlash | [v2ex.md](v2ex.md) |
| HelloGitHub 月刊 | Interesting, beginner-friendly open source | Low | Not selected | [hellogithub.md](hellogithub.md) |
| 阮一峰《科技爱好者周刊》 | Useful tools, broad tech audience | Low | Not selected | [ruanyf-weekly.md](ruanyf-weekly.md) |
| 即刻 | Indie developers, AI/product people, personal stories | Low | Low | [jike.md](jike.md) |
| 小红书 | Visual, benefit-led tools; AI tools; students | Medium | Ignored without a good cover | [xiaohongshu.md](xiaohongshu.md) |
| 掘金 | Technical write-ups for Chinese engineers | Medium | Low | [juejin.md](juejin.md) |
| 知乎, B 站, 开源中国, 少数派 | Long-tail answers, video demos, app-style tools | Varies | Low | [china-other.md](china-other.md) |

## Quick picks by project type

| If your project is… | Start with |
|---|---|
| A CLI or developer library | GitHub topics → awesome list → Show HN → language subreddit (r/rust, r/golang, r/Python…) → language newsletter |
| Self-hostable software | r/selfhosted → Show HN → awesome-selfhosted |
| An AI / LLM tool | X demo video → Show HN → r/LocalLLaMA (if it runs local models) → 即刻 → 小红书 |
| A web app anyone can use | Show HN (no sign-up demo) → Product Hunt → r/SideProject → 小红书 |
| A learning resource or list | HelloGitHub → 阮一峰周刊 → V2EX → submit as a regular HN story (not Show HN) |
| Bilingual (EN + 中文) | Run the global and Chinese tracks on different days so you can answer comments in both |

## Sequencing in one line

Fix the repo → seed the compounding channels (topics, awesome lists, newsletters) →
one "big" channel per day, never two on the same day → answer every comment for the
first few hours → log everything.
