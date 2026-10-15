# Host ecosystems: stores, plugin directories, package registries

> Last checked: 2026-10-15 against each host's own docs, linked in the table below. Store
> rules and review processes change; when this file and the host's docs disagree, the
> host wins. Anything not confirmed on the host's own page is marked *(unverified)* or
> *(heuristic)*.

## Fit

If the project lives inside another app — an editor extension, a browser extension, a
note-app plugin, a launcher command, a plugin for an app like 思源笔记 or MusicFree — or is
installed through a package manager, the host's own directory is often the best channel
you have. People browse it when they already use the host and have the problem, there's an
install button next to your description, and a listing keeps working for years, like an
awesome-list entry. For libraries, the registry's search (npm, PyPI) plays the same role.

A listing is not a launch, though: new listings rarely get much exposure on their own
*(heuristic)*. List first, then announce — in the host's showcase space and in the general
channels where its users are.

## Rules

### Etiquette that applies to every host

- **Read the host's developer policy or store guidelines before you submit.** Obsidian,
  Raycast, JetBrains, Chrome and Firefox each link theirs from the pages in the table.
- **Ask before posting in the host's community.** Before announcing in the host's forum,
  Discord, Slack, subreddit or WeChat group, look for a showcase channel or thread. If there
  isn't one, ask a maintainer or moderator first (template below). It's their space, not
  your launch venue.
- **Never use the host's issue tracker to announce.** Issues are for bugs in the host.
  Obsidian's releases repo, for example, says it doesn't accept issues and sends plugin
  questions to each plugin's own repo.
- **Follow the host's wishes about how it's described.** MusicFree's README asks people not
  to promote it as a "VIP / 破解版", to describe it truthfully, to blur plugin sources in
  articles, and says the author only announces it in the Git repo and their WeChat account.
  If the host says something like this, your posts follow it.
- **Don't imply endorsement.** Say "for <host>" or "<host> plugin", add "unofficial / not
  affiliated" if a reader could think otherwise, and don't use the host's logo as your icon.
  This is our advice; check the host's trademark or branding rules where it has them.
- **One listing, honest keywords.** No duplicate listings and no keyword stuffing.

### Where and how to list

| Host | How to get listed | Notes from the host's docs |
|---|---|---|
| **VS Code Marketplace** | Register a publisher, then `vsce publish` ([docs](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)) | At most 30 `keywords` in `package.json`. README and CHANGELOG images must be https; SVGs only from trusted badge providers. Global Azure DevOps personal access tokens are retired on 2026-12-01; the docs say to publish with Microsoft Entra ID instead. |
| **Open VSX** | Eclipse account + Publisher Agreement, create a namespace, then `npx ovsx publish` ([wiki](https://github.com/eclipse-openvsx/openvsx/wiki/Publishing-Extensions)) | VS Code forks such as VSCodium can't use Microsoft's Marketplace and install from Open VSX ([VSCodium docs](https://github.com/VSCodium/vscodium/blob/master/docs/extensions.md)). Publish to both. |
| **JetBrains Marketplace** | Log in, then account menu → **Upload plugin**; first time, accept the Developer Agreement and create a Vendor profile ([docs](https://plugins.jetbrains.com/docs/marketplace/uploading-a-new-plugin.html)) | Must meet the approval criteria. Tags are search filters, so pick the right ones. An open-source licence needs a link to the source. Use a custom release channel for alpha/beta builds. |
| **Chrome Web Store** | Register as a developer (one-time registration fee), then submit from the developer dashboard; new items go through review ([register](https://developer.chrome.com/docs/webstore/register), [publish](https://developer.chrome.com/docs/webstore/publish)) | Fill in the privacy fields. The developer email can't be changed later, so pick it with care. |
| **Firefox Add-ons (AMO)** | Developer Hub → Submit a New Add-on → **On this site** to be listed ([docs](https://extensionworkshop.com/documentation/publish/submitting-an-add-on/)) | An automatic validator runs on upload. Up to 2 categories. A privacy policy is required if any data leaves the user's device. Flagging the add-on "experimental" lists it with reduced visibility. |
| **Obsidian community plugins** | Sign in at [community.obsidian.md](https://community.obsidian.md), link GitHub, add the plugin; review is automated ([docs](https://docs.obsidian.md/Plugins/Releasing/Submit+your+plugin)) | Repo root needs `README.md`, `LICENSE`, `manifest.json`; a GitHub release whose tag equals the manifest `version`, with `main.js`, `manifest.json` (and `styles.css`) attached. The `id` must be unique and can't contain `obsidian`. Older guides describe a PR to `obsidianmd/obsidian-releases`; the current docs send you to the directory. After listing, the docs suggest announcing in the forum's Share & showcase and Discord `#updates` (needs the developer role). |
| **Raycast Store** | `npm run publish` opens a PR in `raycast/extensions`; the Raycast team reviews and merging publishes it ([publish](https://developers.raycast.com/basics/publish-an-extension), [prepare](https://developers.raycast.com/basics/prepare-an-extension-for-store)) | Store prep: `license` must be MIT, `author` your Raycast username, at least one category, up to six screenshots (three or more recommended). |
| **Homebrew** | Your own tap: `brew tap-new <user>/homebrew-tap`, then users run `brew install <user>/tap/<name>` ([taps](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap)). `homebrew/core`: a pull request that meets the acceptance policy; search earlier PRs for your project first ([adding software](https://docs.brew.sh/Adding-Software-to-Homebrew), [policy](https://docs.brew.sh/Package-Acceptance-Policy), [formulae](https://docs.brew.sh/Acceptable-Formulae)) | Core needs public interest beyond the author: normally 30 forks, 30 watchers or 75 stars, and **90 / 90 / 225 if the repo owner submits it**; repos under 30 days old are normally not eligible; a stable tagged release; a DFSG-compatible licence; builds from source. Homebrew says its official repos "are not editorial curation or recommendation services": core is an install path, not a discovery channel. Start with a tap. |
| **npm** | `npm publish` | `description` and `keywords` in `package.json` are what `npm search` lists ([docs](https://docs.npmjs.com/cli/configuring-npm/package-json)). |
| **PyPI** | Upload a built package | `keywords` help PyPI's search suggest your project; `classifiers` describe maturity and audience; `readme` becomes the project page; `[project.urls]` show in the sidebar ([guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)). |
| **思源笔记集市** (SiYuan bazaar) | Fork [siyuan-note/bazaar](https://github.com/siyuan-note/bazaar), add `owner/repo` to `plugins.txt` (or `themes.txt`, `icons.txt`, `templates.txt`, `widgets.txt`), open a PR to `main` | One new package per PR. A PR Check workflow and the maintainers review it; the repo needs a Latest Release with `package.zip`. Later versions are picked up from your releases, with no new PR. |
| **MusicFree plugins** | No central store: users install a plugin from a file or a URL (`.js` or `.json`) under 设置 → 插件设置 ([README](https://github.com/maotoumao/MusicFree)) | Your README and install URL are the listing. Respect the host's wording rules above. |

For any other host, search its docs for "submit", "publish", "marketplace" or "community
plugins", look for an `awesome-<host>` list, and check which GitHub topic its plugins use
(e.g. `<host>-plugin`).

## Format

- **The listing is the post.** Name, a one-line description in the host's vocabulary (what
  it does *inside the host*), an icon, screenshots or a GIF of it working in the host's own
  UI, and a README that starts with install and usage.
- **Keywords and tags**: the words users type into the store's search box. Specific beats
  generic.
- **Say what it touches.** Required host version, permissions, and what data leaves the
  device. Browser stores ask for this in their privacy fields and policies; users read it
  before installing.
- **Store link first.** In every announcement, link the listing (one-click install), with
  the repo as the source link.
- **Showcase post** in the host's community: what it does, a GIF, the store link, that
  you're the author, what it doesn't do yet, and the feedback you want.

## Timing

- **Submit before launch week.** Review ranges from automated (Obsidian) to a PR review
  (Raycast, SiYuan, Homebrew) to store review (Chrome, Firefox, JetBrains); none of the docs
  we read promise a turnaround.
- **Announce only after the listing is live**, so every post can link to the install
  button.
- **Host moments** *(heuristic)*: a host release that your plugin supports or relies on is a
  natural time for an update post in the host's showcase space.

## Template

Asking the host's maintainer before posting in their community:

```
Hi <name>, I made <plugin>, an unofficial <host> plugin that <does X>. It's <licence>;
source: <repo>. Before I mention it in <forum / Discord / subreddit>, is there a right
place for this (a showcase channel or thread), or would you rather I didn't post it?
Thanks for building <host>.
```

The same request in Chinese, for Chinese hosts:

```
你好，我做了一个 <宿主> 的非官方插件 <名字>，可以 <做什么>，<协议> 开源：<仓库>。
想在 <交流群 / 论坛> 里介绍一下，请问有专门发插件的地方吗？如果不方便发，我就不发了。谢谢！
```

Store description:

```
<Name> — <what it does inside the host, in the host's words>.
- <benefit> (<how>)
- <benefit> (<how>)
Works with <host> <version>+. <Permissions / data it touches, or "No data leaves your device.">
Not affiliated with <host>. Source and issues: <repo>
```

## Pitfalls

- Announcing in the host's issue tracker → closed, and the host's maintainers remember.
- Posting in the host's community before asking, or in every channel at once → reads as spam
  in someone else's house.
- Implying endorsement (the host's logo as your icon, "official") → risks rejection and
  trademark complaints.
- Submitting before it's ready → early reviews and ratings stick to the listing *(heuristic)*.
- Different listings for the same thing (marketplace + Open VSX + a fork's store) with
  different descriptions → keep one source of truth (the README) and copy from it.
- A plugin in a grey area (unofficial APIs, media sources) → the host may object or remove
  it; check the brief's "Claims we won't make" before you post in the host's spaces.
