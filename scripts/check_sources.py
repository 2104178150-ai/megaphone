#!/usr/bin/env python3
"""Check that the facts our channel playbooks rely on still appear on their sources.

Each entry pairs a playbook with a phrase from the platform's own page. If the phrase
disappears, the rule may have changed and the playbook needs a human (or agent) to
re-read the source. Standard library only.

    python3 scripts/check_sources.py            # human-readable
    python3 scripts/check_sources.py --json     # machine-readable

Exit code: 0 all found, 1 something missing or unreachable.
"""

import gzip
import html
import http.client
import json
import re
import sys
import urllib.error
import urllib.request
import zlib

# (playbook, url, phrase that should still be on the page)
SOURCES = [
    ("awesome-lists.md", "https://raw.githubusercontent.com/avelino/awesome-go/main/CONTRIBUTING.md", "at least 5 months of history"),
    ("awesome-lists.md", "https://raw.githubusercontent.com/awesome-selfhosted/awesome-selfhosted-data/master/.github/PULL_REQUEST_TEMPLATE.md", "The submission was done by a human, not a machine/LLM."),
    ("awesome-lists.md", "https://raw.githubusercontent.com/awesome-selfhosted/awesome-selfhosted-data/master/CONTRIBUTING.md", "first release more than four months old"),
    ("awesome-lists.md", "https://raw.githubusercontent.com/awesome-selfhosted/awesome-selfhosted-data/master/CONTRIBUTING.md", "will result in a ban"),
    ("channels/README.md", "https://help.qiita.com/ja/articles/qiita-community-guideline", "宣伝や販売を主目的とした記事は投稿しない"),
    ("china-other.md", "https://www.oschina.net/help-center/oschina-guides/how-to-play-in-osc.html", "一个工作日内"),
    ("china-other.md", "https://www.oschina.net/help-center/oschina-guides/how-to-play-in-osc.html", "投递资讯 / 软件"),
    ("china-other.md", "https://www.theregister.com/2022/05/20/gitee_code_review/", "manually reviewed"),
    ("dev-blogs.md", "https://dev.to/guidelines-for-ai-assisted-articles-on-dev", "(including your own)"),
    ("dev-blogs.md", "https://dev.to/p/editor_guide", "max of four tags"),
    ("dev-blogs.md", "https://dev.to/terms", "not designed primarily for the purposes of promotion or creating backlinks"),
    ("ecosystems.md", "https://code.visualstudio.com/api/working-with-extensions/publishing-extension", "allow an extension package to have more than 30"),
    ("ecosystems.md", "https://code.visualstudio.com/api/working-with-extensions/publishing-extension", "global Personal Access Tokens (PATs) in Azure DevOps are retired"),
    ("ecosystems.md", "https://developer.chrome.com/docs/webstore/register", "one-time registration fee"),
    ("ecosystems.md", "https://claude.com/docs/directory/publish", "Free accounts can’t submit"),
    ("research", "https://raw.githubusercontent.com/github/docs/main/content/site-policy/acceptable-use-policies/github-acceptable-use-policies.md", "rank abuse, such as automated starring or following"),
    ("ecosystems.md", "https://claude.com/docs/directory/publish", "Skills aren’t a submission type on their own"),
    ("ecosystems.md", "https://claude.com/docs/plugins/pre-submission-checklist", "README of at least 40 words"),
    ("ecosystems.md", "https://www.skills.sh/docs", "anonymous telemetry data collected from the"),
    ("ecosystems.md", "https://skillsmp.com/about", "Skills are sourced from public GitHub repositories"),
    ("ecosystems.md", "https://raw.githubusercontent.com/hesreallyhim/awesome-claude-code/main/CONTRIBUTING.md", "resource recommendations must be created by human beings"),
    ("ecosystems.md", "https://raw.githubusercontent.com/heilcheng/awesome-agent-skills/main/README.md", "at least 20 stars and is older than 14 days"),
    ("ecosystems.md", "https://raw.githubusercontent.com/heilcheng/awesome-agent-skills/main/AGENTS.md", "If you are an AI agent, say so"),
    ("ecosystems.md", "https://raw.githubusercontent.com/hesreallyhim/awesome-claude-code/main/CONTRIBUTING.md", "Recommendations are reviewed in a best-effort way"),
    ("ecosystems.md", "https://developers.raycast.com/basics/prepare-an-extension-for-store", "maximum of six screenshots"),
    ("ecosystems.md", "https://developers.raycast.com/basics/publish-an-extension", "automatically open a pull request in our"),
    ("ecosystems.md", "https://docs.brew.sh/Package-Acceptance-Policy", "are not editorial curation or recommendation services"),
    ("ecosystems.md", "https://docs.brew.sh/Package-Acceptance-Policy", "at least 90 forks, 90 watchers or 225 stars"),
    ("ecosystems.md", "https://extensionworkshop.com/documentation/publish/submitting-an-add-on/", "On this site"),
    ("ecosystems.md", "https://github.com/eclipse-openvsx/openvsx/wiki/Publishing-Extensions", "Publisher Agreement"),
    ("ecosystems.md", "https://plugins.jetbrains.com/docs/marketplace/uploading-a-new-plugin.html", "Upload plugin"),
    ("ecosystems.md", "https://publish-01.obsidian.md/access/caa27d6312fe5c26ebc657cc609543be/Plugins/Releasing/Submit%20your%20plugin.md", "Obsidian Community directory"),
    ("ecosystems.md", "https://raw.githubusercontent.com/maotoumao/MusicFree/master/readme.md", "请不要以 VIP/破解版为噱头进行宣传"),
    ("ecosystems.md", "https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/README.md", "does not accept issues"),
    ("ecosystems.md", "https://raw.githubusercontent.com/siyuan-note/bazaar/main/README.md", "plugins.txt"),
    ("github-native.md", "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics", "Add no more than 20 topics"),
    ("github-native.md", "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview", "1280 by 640 pixels for best display"),
    ("github-native.md", "https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository", "Anyone with push access to a repository can view its traffic"),
    ("github-native.md", "https://docs.github.com/en/rest/activity/starring", "application/vnd.github.star+json"),
    ("github-native.md", "https://docs.github.com/en/rest/metrics/traffic", "for the last 14 days"),
    ("github-native.md", "https://docs.github.com/en/rest/metrics/traffic", "last 14 days"),
    ("hacker-news.md", "https://news.ycombinator.com/item?id=22336638", "Either way is fine"),
    ("hacker-news.md", "https://news.ycombinator.com/item?id=22336638", "Write your text by hand"),
    ("hacker-news.md", "https://news.ycombinator.com/item?id=48210728", "80 char limit"),
    ("hacker-news.md", "https://news.ycombinator.com/newsfaq.html", "a small number of reposts is ok"),
    ("hacker-news.md", "https://news.ycombinator.com/newsguidelines.html", "Please don't put generated text in HN posts."),
    ("hacker-news.md", "https://news.ycombinator.com/showhn.html", "Don't post quickly-generated"),
    ("hacker-news.md", "https://news.ycombinator.com/showhn.html", "ask friends to upvote"),
    ("hacker-news.md", "https://news.ycombinator.com/showhn.html", "barriers such as signups or emails"),
    ("hacker-news.md", "https://news.ycombinator.com/showhn.html", "something you've made"),
    ("hellogithub.md", "https://raw.githubusercontent.com/521xueweihan/HelloGitHub/master/README.md", "推荐或自荐"),
    ("hellogithub.md", "https://raw.githubusercontent.com/521xueweihan/HelloGitHub/master/README.md", "每月 28 号"),
    ("jike.md", "https://post.okjike.com/jike-agreement/", "过度营销信息"),
    ("launch-review/SKILL.md", "https://docs.github.com/en/rest/activity/starring", "limited to admins and collaborators"),
    ("launch-review/SKILL.md", "https://docs.github.com/en/rest/metrics/traffic", "aligned to UTC midnight"),
    ("launch-review/SKILL.md", "https://docs.github.com/en/rest/metrics/traffic", "top 10 referrers over the last 14 days"),
    ("launch-review/SKILL.md", "https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api", "in UTC epoch seconds"),
    ("lobsters.md", "https://lobste.rs/about", "for their first 70 days"),
    ("lobsters.md", "https://lobste.rs/about", "less than a quarter"),
    ("lobsters.md", "https://lobste.rs/about", "without meaningful human authorship"),
    ("lobsters.md", "https://raw.githubusercontent.com/lobsters/lobsters/main/app/views/stories/_form.html.erb", "the author of the story at this URL (or this text)"),
    ("newsletters.md", "https://changelog.com/news/submit", "Submitting your own work is also encouraged."),
    ("newsletters.md", "https://console.dev/selection-criteria", "Any GA or stable releases are not eligible."),
    ("newsletters.md", "https://console.dev/selection-criteria", "Is there a self-service signup?"),
    ("newsletters.md", "https://console.dev/selection-criteria", "The more of these questions we can answer positively"),
    ("newsletters.md", "https://console.dev/selection-criteria", "hello@console.dev"),
    ("newsletters.md", "https://cooperpress.com/contact", "editor@cooperpress.com"),
    ("newsletters.md", "https://pycoders.com/submissions", "Submit Your Link"),
    ("newsletters.md", "https://pycoders.com/submissions", "projects you are working on"),
    ("newsletters.md", "https://raw.githubusercontent.com/rust-lang/this-week-in-rust/master/README.md", "no longer accepting pull request submissions for the Project/Tooling Updates section"),
    ("newsletters.md", "https://raw.githubusercontent.com/rust-lang/this-week-in-rust/master/README.md", "We don't accept articles written by LLMs"),
    ("newsletters.md", "https://raw.githubusercontent.com/rust-lang/this-week-in-rust/master/README.md", "drafts"),
    ("product-hunt.md", "https://help.producthunt.com/en/articles/3615694-community-guidelines", "asking for upvotes"),
    ("product-hunt.md", "https://www.producthunt.com/launch", "12:01"),
    ("product-hunt.md", "https://www.producthunt.com/launch", "Company accounts are prohibited"),
    ("product-hunt.md", "https://www.producthunt.com/launch", "no discernible advantage"),
    ("product-hunt.md", "https://www.producthunt.com/launch/preparing-for-launch", "1270x760"),
    ("product-hunt.md", "https://www.producthunt.com/launch/preparing-for-launch", "15% more"),
    ("product-hunt.md", "https://www.producthunt.com/launch/preparing-for-launch", "max 60 characters"),
    ("reddit.md", "https://redditinc.com/policies/reddit-rules", "Participate authentically in communities where you have a personal interest"),
    ("reddit.md", "https://support.reddithelp.com/api/v2/help_center/en-us/articles/360043504051.json", "generative AI tools"),
    ("ruanyf-weekly.md", "https://raw.githubusercontent.com/ruanyf/weekly/master/README.md", "周五发布"),
    ("ruanyf-weekly.md", "https://raw.githubusercontent.com/ruanyf/weekly/master/README.md", "提交 issue"),
    ("ruanyf-weekly.md", "https://raw.githubusercontent.com/ruanyf/weekly/master/README.md", "欢迎投稿文章/软件/资源"),
    ("v2ex.md", "https://www.v2ex.com/go/create", "爱意满满的作品展示区"),
    ("v2ex.md", "https://www.v2ex.com/help/currency", "创建新主题会消耗至少 20 铜币"),
    ("v2ex.md", "https://www.v2ex.com/help/currency", "附言"),
    ("v2ex.md", "https://www.v2ex.com/help/i", "付费使用的图片存储和分享服务"),
    ("v2ex.md", "https://www.v2ex.com/signup", "invite code"),
    ("v2ex.md", "https://www.v2ex.com/signup", "require an invite code to activate"),
    ("v2ex.md", "https://www.v2ex.com/help/anti-flood", "请不要在主题内容或者回复中使用来自 AI 生成的文本"),
    ("v2ex.md", "https://www.v2ex.com/help/anti-flood", "259200"),
    ("v2ex.md", "https://www.v2ex.com/help/node", "请把你们公司的任何营销内容发到这个节点"),
    ("v2ex.md", "https://www.v2ex.com/help/markdown", "imgur.com 和 i.v2ex.co"),
    ("v2ex.md", "https://www.v2ex.com/help/solana", "不需要使用邀请码激活"),
    ("x-twitter.md", "https://bsky.social/about/support/community-guidelines", "Do not send spam or repeatedly post content"),
    ("x-twitter.md", "https://github.com/xai-org/x-algorithm", "For You feed"),
    ("xiaohongshu.md", "https://cn.chinadaily.com.cn/a/202601/20/WS696eef27a310942cc499bf9f.html", "请主动标明"),
    ("xiaohongshu.md", "https://www.thepaper.cn/newsDetail_forward_32599956", "对未主动标识的AI生成合成内容限制分发"),
    ("xiaohongshu.md", "https://www.stdaily.com/web/gdxw/2026-04/27/content_508976.html", "所有AI参与创作的内容均需主动标识"),
    ("xiaohongshu.md", "https://m.gmw.cn/2025-03/12/content_1303989067.htm", "交易导流违规管理细则"),
    ("china-other.md", "https://sspai.com/post/40262", "不要假扮第三方或用户推荐、评测自己的产品"),
    ("china-other.md", "https://sspai.com/post/65521", "明显软文倾向"),
    ("china-other.md", "https://www.oschina.net/help-center/oschina-guides/how-to-play-in-osc.html", "不要从产品的角度来描述项目"),
]

UA = "Mozilla/5.0 (Macintosh; megaphone source check)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read()
    # Some servers gzip the page even when the request doesn't ask for it.
    if body[:2] == b"\x1f\x8b":
        body = gzip.decompress(body)
    # Pages escape quotes and apostrophes (&#x27;), so compare against the unescaped text.
    return html.unescape(body.decode("utf-8", errors="replace"))


def normalize(text):
    """Collapse markup and whitespace (incl. NBSP) so rewrapped or re-tagged text still matches."""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def found(phrase, page):
    return phrase in page or normalize(phrase) in normalize(page)


def utf8_output():
    """Print UTF-8 even where the console or pipe defaults to cp1252 or GBK (Windows)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def main():
    utf8_output()
    as_json = "--json" in sys.argv
    pages = {}
    results = []
    for playbook, url, phrase in SOURCES:
        if url not in pages:
            try:
                pages[url] = fetch(url)
            except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError, EOFError, zlib.error) as e:
                pages[url] = e
        page = pages[url]
        if isinstance(page, Exception):
            status = "unreachable"
            detail = str(page)
        else:
            status = "ok" if found(phrase, page) else "missing"
            detail = ""
        results.append({"playbook": playbook, "url": url, "phrase": phrase, "status": status, "detail": detail})

    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            mark = {"ok": "✓", "missing": "✗", "unreachable": "?"}[r["status"]]
            print("%s %-22s %-40s %s %s" % (mark, r["playbook"], r["phrase"][:40], r["url"], r["detail"]))
        bad = [r for r in results if r["status"] != "ok"]
        print("\n%d/%d sources still match." % (len(results) - len(bad), len(results)))
    sys.exit(0 if all(r["status"] == "ok" for r in results) else 1)


if __name__ == "__main__":
    main()
