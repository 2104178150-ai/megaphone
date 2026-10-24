#!/usr/bin/env python3
"""Draw docs/demo.svg and docs/demo.zh-CN.svg: a looping, 14-second animation of the checker
(type a repo, the meter fills, the three fixes and the channels appear) for the README's first
screen. Plain SVG + CSS, no fonts or images to load, so GitHub renders it inline.

    python3 scripts/make_demo.py
"""

import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LOOP = 14.0  # seconds

INK, INK2, INK3 = "#141413", "#57544f", "#8b8780"
BG, SURFACE, SURFACE2, LINE = "#fafaf9", "#ffffff", "#f4f3f0", "#e9e7e2"
ACCENT, GOOD = "#e4531b", "#4d7c0f"
SANS = "system-ui, -apple-system, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

TEXT = {
    "en": dict(title="Megaphone checking a repo: type it in, get a 0–100 launch score, the three fixes that matter most and where to launch",
               tagline="Is your repo ready to launch?", check="Check", level="Almost there",
               say="Fix the top items first — they’re cheap.", out="out of 100",
               cats=["First impression", "Time to wow", "Trust", "Shareability"],
               fixk="FIX FIRST", fixes=[("Put a screenshot in the first screen", 8), ("Put the demo in the Website field", 4),
                                          ("Publish a first release", 4)],
               wherek="WHERE TO LAUNCH"),
    "zh": dict(title="Megaphone 给一个仓库打分：输入仓库，得到 0–100 的发布就绪分、最该先改的三件事和适合去哪里发",
               tagline="你的开源项目，准备好被看见了吗？", check="检测", level="就差一点",
               say="先改掉最前面几项，成本很低。", out="满分 100",
               cats=["第一印象", "上手速度", "可信度", "传播力"],
               fixk="先改", fixes=[("首屏放一张截图或动图", 8), ("侧栏 Website 填上演示链接", 4), ("发一个 Release", 4)],
               wherek="去哪发"),
}
SCORE = 84
CATS = [(27, 35), (25, 25), (16, 20), (16, 20)]
CHANNELS = ["Show HN", "r/golang", "V2EX", "HelloGitHub"]
REPO = "your-name/your-repo"


def pct(t):
    return "%.2f%%" % (100 * t / LOOP)


def appear(name, start, dur=0.45, dy=8):
    """Fade (and rise) in at `start` seconds, stay, fade out with everything at the end of the loop."""
    return ("@keyframes %s { 0%%, %s { opacity: 0; transform: translateY(%dpx); } %s, 88%% { opacity: 1; transform: none; }"
            " 95%%, 100%% { opacity: 0; transform: none; } }\n.%s { animation-name: %s; transform-box: fill-box; }"
            % (name, pct(start), dy, pct(start + dur), name, name))


def build(lang):
    T = TEXT[lang]
    css = []
    out = []
    add = out.append
    css.append("* { animation-duration: %ss; animation-iteration-count: infinite; animation-timing-function: cubic-bezier(.2,.8,.2,1); }" % LOOP)

    add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 640" width="1200" height="640" font-family="%s">' % SANS)
    add("<title>%s</title>" % T["title"])
    add('<rect width="1200" height="640" rx="28" fill="%s"/>' % BG)
    add('<rect x="1" y="1" width="1198" height="638" rx="27" fill="none" stroke="%s" stroke-width="2"/>' % LINE)

    # header
    add('<g transform="translate(40 30) scale(.32)"><path d="M14 38 70 16v64L14 58Z" fill="%s"/>'
        '<rect x="5" y="35" width="12" height="26" rx="4" fill="%s"/><path d="M34 64l6 18" stroke="%s" stroke-width="9" stroke-linecap="round"/>'
        '<path d="M82 37a15 15 0 0 1 0 22M93 28a28 28 0 0 1 0 40M104 19a41 41 0 0 1 0 58" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round"/></g>'
        % (ACCENT, INK, INK, ACCENT))
    add('<text x="88" y="54" font-size="20" font-weight="650" fill="%s">Megaphone</text>' % INK)
    add('<text x="1160" y="54" font-size="16" fill="%s" text-anchor="end">%s</text>' % (INK3, T["tagline"]))

    # search field: the repo is typed in, then the button is pressed
    add('<rect x="300" y="92" width="600" height="60" rx="16" fill="%s" stroke="#dcd9d3"/>' % SURFACE)
    add('<text x="326" y="129" font-family="%s" font-size="19" fill="%s">%s</text>' % (MONO, INK, REPO))
    n = len(REPO)
    css.append("@keyframes type { 0%%, %s { transform: translateX(0); } %s, 92%% { transform: translateX(%dpx); } 96%%, 100%% { transform: translateX(0); } }"
               % (pct(0.3), pct(1.7), 12 * n))
    css.append(".typing { animation-name: type; animation-timing-function: steps(%d, end); }" % n)
    add('<rect class="typing" x="322" y="106" width="%d" height="32" fill="%s"/>' % (12 * n + 8, SURFACE))
    css.append("@keyframes press { 0%%, %s { transform: scale(1); } %s { transform: scale(.94); } %s, 100%% { transform: scale(1); } }"
               % (pct(1.9), pct(2.05), pct(2.25)))
    css.append(".press { animation-name: press; transform-box: fill-box; transform-origin: center; }")
    add('<g class="press"><rect x="796" y="100" width="96" height="44" rx="11" fill="%s"/>'
        '<text x="844" y="128" font-size="16" font-weight="600" fill="#ffffff" text-anchor="middle">%s</text></g>' % (INK, T["check"]))

    # report card
    css.append(appear("card", 2.2, 0.5, 14))
    add('<g class="card">')
    add('<rect x="40" y="184" width="1120" height="420" rx="22" fill="%s" stroke="%s"/>' % (SURFACE, LINE))
    add('<line x1="770" y1="214" x2="770" y2="574" stroke="%s"/>' % LINE)

    # segmented meter
    cx, cy, r = 186, 360, 98
    c = 2 * math.pi * r
    add('<g transform="rotate(-90 %d %d)">' % (cx, cy))
    add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="20"/>' % (cx, cy, r, SURFACE2))
    css.append("@keyframes fill { 0%%, %s { stroke-dashoffset: %.1f; } %s, 88%% { stroke-dashoffset: %.1f; } 95%%, 100%% { stroke-dashoffset: %.1f; } }"
               % (pct(2.6), c, pct(4.2), c * (1 - SCORE / 100), c * (1 - SCORE / 100)))
    css.append(".meter { animation-name: fill; }")
    add('<circle class="meter" cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="20" stroke-dasharray="%.1f" stroke-dashoffset="%.1f"/>'
        % (cx, cy, r, GOOD, c, c * (1 - SCORE / 100)))
    add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="24" stroke-dasharray="3.4 %.2f"/>' % (cx, cy, r, SURFACE, c / 50 - 3.4))
    add('</g>')
    css.append(appear("num", 3.7, 0.4, 0))
    add('<g class="num"><text x="%d" y="%d" font-family="%s" font-size="60" font-weight="600" fill="%s" text-anchor="middle" letter-spacing="-3">%d</text>'
        '<text x="%d" y="%d" font-family="%s" font-size="13" fill="%s" text-anchor="middle">%s</text></g>'
        % (cx, cy + 16, MONO, GOOD, SCORE, cx, cy + 44, MONO, INK3, T["out"]))

    # verdict and the four categories
    x0 = 330
    add('<text x="%d" y="246" font-family="%s" font-size="14" fill="%s">%s</text>' % (x0, MONO, INK3, REPO))
    css.append(appear("lvl", 4.0))
    add('<g class="lvl"><g transform="translate(%d 262) scale(.3)" fill="%s"><path d="M14 38 70 16v64L14 58Z"/><rect x="5" y="35" width="12" height="26" rx="4"/>'
        '<path d="M82 37a15 15 0 0 1 0 22M93 28a28 28 0 0 1 0 40M104 19a41 41 0 0 1 0 58" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round"/></g>'
        '<text x="%d" y="290" font-size="30" font-weight="650" fill="%s" letter-spacing="-.5">%s</text>'
        '<text x="%d" y="322" font-size="16" fill="%s">%s</text></g>'
        % (x0, GOOD, GOOD, x0 + 50, GOOD, T["level"], x0, INK2, T["say"]))
    for i, ((got, mx), name) in enumerate(zip(CATS, T["cats"])):
        y = 368 + i * 40
        add('<text x="%d" y="%d" font-size="15" fill="%s">%s</text>' % (x0, y + 5, INK2, name))
        add('<rect x="%d" y="%d" width="230" height="6" rx="3" fill="%s"/>' % (x0 + 150, y - 3, SURFACE2))
        k = "bar%d" % i
        css.append("@keyframes %s { 0%%, %s { transform: scaleX(0); } %s, 88%% { transform: scaleX(1); } 95%%, 100%% { transform: scaleX(1); } }"
                   % (k, pct(4.3 + i * 0.12), pct(5.2 + i * 0.12)))
        css.append(".%s { animation-name: %s; transform-box: fill-box; transform-origin: left center; }" % (k, k))
        add('<rect class="%s" x="%d" y="%d" width="%.0f" height="6" rx="3" fill="%s"/>' % (k, x0 + 150, y - 3, 230 * got / mx, INK))
        add('<text x="%d" y="%d" font-family="%s" font-size="13" fill="%s" text-anchor="end">%d/%d</text>' % (x0 + 432, y + 5, MONO, INK3, got, mx))

    # the three fixes, then where to launch
    xr = 800
    add('<text x="%d" y="246" font-family="%s" font-size="12" letter-spacing="2" fill="%s">%s</text>' % (xr, MONO, INK3, T["fixk"]))
    for i, (fix, gain) in enumerate(T["fixes"]):
        y = 284 + i * 48
        css.append(appear("fix%d" % i, 5.6 + i * 0.6))
        add('<g class="fix%d">' % i)
        if i:
            add('<line x1="%d" y1="%d" x2="1128" y2="%d" stroke="%s"/>' % (xr, y - 28, y - 28, LINE))
        add('<text x="%d" y="%d" font-size="16" font-weight="600" fill="%s">%s</text>' % (xr, y, INK, fix))
        add('<rect x="1080" y="%d" width="48" height="24" rx="6" fill="%s"/>' % (y - 17, SURFACE2))
        add('<text x="1104" y="%d" font-family="%s" font-size="13" fill="%s" text-anchor="middle">+%d</text></g>' % (y, MONO, INK2, gain))
    add('<text x="%d" y="456" font-family="%s" font-size="12" letter-spacing="2" fill="%s">%s</text>' % (xr, MONO, INK3, T["wherek"]))
    x = xr
    for i, ch in enumerate(CHANNELS):
        w = 18 + 8.6 * len(ch)
        css.append(appear("ch%d" % i, 7.6 + i * 0.18, 0.35, 6))
        add('<g class="ch%d"><rect x="%.0f" y="474" width="%.0f" height="32" rx="7" fill="%s" stroke="%s"/>'
            '<text x="%.0f" y="495" font-size="14" fill="%s" text-anchor="middle">%s</text></g>' % (i, x, w, SURFACE, LINE, x + w / 2, INK2, ch))
        x += w + 8
    add('</g>')  # card

    add('<style>@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }\n%s</style>' % "\n".join(css))
    add('</svg>')
    return "\n".join(out) + "\n"


for lang, name in (("en", "demo.svg"), ("zh", "demo.zh-CN.svg")):
    with open(os.path.join(HERE, "..", "docs", name), "w", encoding="utf-8") as f:
        f.write(build(lang))
    print("wrote docs/%s" % name)
