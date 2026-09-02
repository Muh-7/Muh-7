#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import html
import json
import os
import urllib.request
from collections import Counter
from pathlib import Path

USER = os.getenv("PROFILE_USER", "Muh-7")
TOKEN = os.getenv("GH_TOKEN", "")
OUT = Path("dist")
OUT.mkdir(exist_ok=True)

PROJECTS = [
    {
        "repo": "dna-mutation-analyzer",
        "slug": "dna",
        "index": "01",
        "domain": "BIO-AI / GENOMICS",
        "title": "DNA Mutation Analyzer",
        "line1": "From a sequence variant to genomic context,",
        "line2": "expression, splicing and TF-motif effects.",
        "stack": "GENCODE · GRCh38 · AlphaGenome · JASPAR · FIMO",
        "motif": "dna",
    },
    {
        "repo": "Traffic-Speed-Analytics",
        "slug": "traffic",
        "index": "02",
        "domain": "REAL-TIME COMPUTER VISION",
        "title": "Traffic Speed Analytics",
        "line1": "Detection, tracking and speed estimation",
        "line2": "from video with generated traffic analytics.",
        "stack": "YOLOv8 · ByteTrack · OpenCV · Pandas",
        "motif": "traffic",
    },
    {
        "repo": "Sign_Language_Recognition",
        "slug": "sign",
        "index": "03",
        "domain": "VISION / EDGE INFERENCE",
        "title": "Sign Language Recognition",
        "line1": "Real-time gesture recognition built around",
        "line2": "a custom 11,000-image training dataset.",
        "stack": "TensorFlow · MobileNetV3 · OpenCV · NumPy",
        "motif": "signal",
    },
    {
        "repo": "Alsehoum-Neural-Network-FrameWork-From-Scratch",
        "slug": "nn",
        "index": "04",
        "domain": "ML CORE / FROM SCRATCH",
        "title": "AlsehoumMiniNN",
        "line1": "Dense layers, backpropagation, losses and",
        "line2": "optimizers implemented explicitly in NumPy.",
        "stack": "NumPy · SGD · Momentum · Adam · Backpropagation",
        "motif": "network",
    },
]

THEMES = {
    "dark": {
        "bg": "#080B10", "panel": "#0C1118", "fg": "#F4F7FB",
        "body": "#C1CAD6", "muted": "#7D8998", "line": "#222B37",
        "subtle": "#151C25", "accent": "#6EE7F9", "accent2": "#8B7CFF",
        "good": "#70E1A1",
    },
    "light": {
        "bg": "#F7F8FA", "panel": "#FFFFFF", "fg": "#11151B",
        "body": "#38414D", "muted": "#6E7885", "line": "#DCE1E7",
        "subtle": "#ECEFF3", "accent": "#008DA6", "accent2": "#6557E8",
        "good": "#14875A",
    },
}

STYLE = '<style>.ui{font-family:Inter,"Segoe UI",Arial,sans-serif}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}</style>'


def api(path: str):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "muh7-profile-engine",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def safe_api(path: str, fallback):
    try:
        return api(path)
    except Exception as exc:
        print(f"GitHub API warning for {path}: {exc}")
        return fallback


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def short_date(value: str | None) -> str:
    if not value:
        return "—"
    try:
        d = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return d.strftime("%d %b %Y").upper()
    except Exception:
        return "—"


def write(name: str, content: str):
    (OUT / name).write_text(content, encoding="utf-8")


def hero_svg(theme: dict, user: dict, repos: list[dict]) -> str:
    public_repos = user.get("public_repos", len(repos))
    followers = user.get("followers", 0)
    languages = Counter(r.get("language") for r in repos if r.get("language"))
    top_lang = languages.most_common(1)[0][0] if languages else "Python"
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420">
<defs>
  <linearGradient id="signal" x1="0" x2="1"><stop offset="0" stop-color="{theme['accent']}" stop-opacity="0"/><stop offset=".45" stop-color="{theme['accent']}"/><stop offset="1" stop-color="{theme['accent2']}" stop-opacity="0"/></linearGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
{STYLE}
<rect width="1200" height="420" rx="28" fill="{theme['bg']}"/>
<path d="M40 72 H1160 M40 350 H1160" stroke="{theme['subtle']}"/>
<path d="M760 72 V350" stroke="{theme['subtle']}"/>

<text x="46" y="58" class="mono" fill="{theme['muted']}" font-size="11" letter-spacing="2.3">MUH-7 / AI SYSTEMS</text>
<circle cx="1128" cy="54" r="5" fill="{theme['good']}"><animate attributeName="opacity" values=".3;1;.3" dur="2.2s" repeatCount="indefinite"/></circle>
<text x="1114" y="59" text-anchor="end" class="mono" fill="{theme['muted']}" font-size="10">LIVE</text>

<text x="46" y="142" class="ui" fill="{theme['fg']}" font-size="49" font-weight="800" letter-spacing="-1.6">Muhammad Alsehoum</text>
<text x="46" y="196" class="ui" fill="{theme['fg']}" font-size="31" font-weight="700">AI Engineer building the system around the model.</text>
<text x="46" y="239" class="ui" fill="{theme['body']}" font-size="16">Computer Vision · Machine Learning · Bio-AI · MLOps</text>

<g transform="translate(46,293)">
  <text x="0" y="0" class="mono" fill="{theme['muted']}" font-size="10">PUBLIC REPOS</text><text x="0" y="27" class="ui" fill="{theme['fg']}" font-size="20" font-weight="700">{public_repos}</text>
  <text x="132" y="0" class="mono" fill="{theme['muted']}" font-size="10">FOLLOWERS</text><text x="132" y="27" class="ui" fill="{theme['fg']}" font-size="20" font-weight="700">{followers}</text>
  <text x="258" y="0" class="mono" fill="{theme['muted']}" font-size="10">PRIMARY</text><text x="258" y="27" class="ui" fill="{theme['fg']}" font-size="20" font-weight="700">{esc(top_lang)}</text>
  <text x="395" y="0" class="mono" fill="{theme['muted']}" font-size="10">RENDER</text><text x="395" y="27" class="ui" fill="{theme['fg']}" font-size="20" font-weight="700">{now}</text>
</g>

<g transform="translate(805,105)">
  <text x="0" y="0" class="mono" fill="{theme['muted']}" font-size="10" letter-spacing="1.7">ML LIFECYCLE / SIGNAL PATH</text>
  <path d="M24 72 H258 V158 H80 V236 H290" fill="none" stroke="{theme['line']}" stroke-width="2"/>
  <g class="mono" font-size="10">
    <circle cx="24" cy="72" r="7" fill="{theme['panel']}" stroke="{theme['accent']}" stroke-width="2"/><text x="24" y="51" text-anchor="middle" fill="{theme['muted']}">DATA</text>
    <circle cx="144" cy="72" r="7" fill="{theme['panel']}" stroke="{theme['accent']}" stroke-width="2"/><text x="144" y="51" text-anchor="middle" fill="{theme['muted']}">TRAIN</text>
    <circle cx="258" cy="72" r="7" fill="{theme['panel']}" stroke="{theme['accent']}" stroke-width="2"/><text x="258" y="51" text-anchor="middle" fill="{theme['muted']}">EVAL</text>
    <circle cx="258" cy="158" r="7" fill="{theme['panel']}" stroke="{theme['accent2']}" stroke-width="2"/><text x="278" y="162" fill="{theme['muted']}">SERVE</text>
    <circle cx="80" cy="158" r="7" fill="{theme['panel']}" stroke="{theme['accent2']}" stroke-width="2"/><text x="80" y="139" text-anchor="middle" fill="{theme['muted']}">SHIP</text>
    <circle cx="80" cy="236" r="7" fill="{theme['panel']}" stroke="{theme['good']}" stroke-width="2"/><text x="80" y="260" text-anchor="middle" fill="{theme['muted']}">OBSERVE</text>
    <circle cx="290" cy="236" r="7" fill="{theme['panel']}" stroke="{theme['good']}" stroke-width="2"/><text x="290" y="260" text-anchor="middle" fill="{theme['muted']}">ITERATE</text>
  </g>
  <circle r="5" fill="{theme['accent']}" filter="url(#glow)"><animateMotion dur="7s" repeatCount="indefinite" path="M24 72 H258 V158 H80 V236 H290"/></circle>
</g>

<rect x="-180" y="348" width="220" height="3" rx="2" fill="url(#signal)"><animate attributeName="x" values="-180;1200" dur="6.5s" repeatCount="indefinite"/></rect>
</svg>'''


def motif(kind: str, theme: dict) -> str:
    a, b, line = theme["accent"], theme["accent2"], theme["line"]
    if kind == "dna":
        return f'''<g transform="translate(417,90)"><path d="M0 6 C58 26 58 105 0 126 M108 6 C50 26 50 105 108 126" fill="none" stroke="{b}" stroke-width="2.2"/><g stroke="{a}" opacity=".75"><line x1="17" y1="25" x2="91" y2="25"/><line x1="5" y1="54" x2="103" y2="54"/><line x1="5" y1="83" x2="103" y2="83"/><line x1="17" y1="111" x2="91" y2="111"/></g><circle cx="54" cy="54" r="5" fill="{a}"><animate attributeName="r" values="4;7;4" dur="2.1s" repeatCount="indefinite"/></circle></g>'''
    if kind == "traffic":
        return f'''<g transform="translate(400,95)" fill="none"><rect x="0" y="16" width="75" height="46" rx="4" stroke="{a}" stroke-width="2"/><rect x="72" y="68" width="103" height="60" rx="4" stroke="{b}" stroke-width="2"/><path d="M7 39H68 M80 98H168" stroke="{line}" stroke-dasharray="5 5"/><circle cx="38" cy="39" r="3" fill="{a}"><animate attributeName="opacity" values=".25;1;.25" dur="1.7s" repeatCount="indefinite"/></circle></g>'''
    if kind == "signal":
        return f'''<g transform="translate(392,122)"><path d="M0 52 H28 L43 31 L60 77 L80 7 L101 52 H178" fill="none" stroke="{a}" stroke-width="2.4"/><circle cx="0" cy="52" r="4" fill="{b}"><animateMotion dur="3.4s" repeatCount="indefinite" path="M0 52 H28 L43 31 L60 77 L80 7 L101 52 H178"/></circle></g>'''
    return f'''<g transform="translate(398,92)" stroke="{b}" stroke-width="1.3" fill="{theme['panel']}"><circle cx="5" cy="20" r="6"/><circle cx="5" cy="63" r="6"/><circle cx="5" cy="106" r="6"/><circle cx="77" cy="7" r="6"/><circle cx="77" cy="40" r="6"/><circle cx="77" cy="73" r="6"/><circle cx="77" cy="106" r="6"/><circle cx="150" cy="34" r="6"/><circle cx="150" cy="81" r="6"/><g fill="none" opacity=".55"><path d="M11 20L71 7M11 20L71 40M11 63L71 40M11 63L71 73M11 106L71 73M83 7L144 34M83 40L144 34M83 73L144 81M83 106L144 81"/></g><circle cx="150" cy="34" r="4" fill="{a}" stroke="none"><animate attributeName="opacity" values=".2;1;.2" dur="1.8s" repeatCount="indefinite"/></circle></g>'''


def project_svg(theme: dict, cfg: dict, repo: dict) -> str:
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    language = repo.get("language") or "Python"
    updated = short_date(repo.get("pushed_at"))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="580" height="286" viewBox="0 0 580 286">
{STYLE}
<rect x=".7" y=".7" width="578.6" height="284.6" rx="23" fill="{theme['panel']}" stroke="{theme['line']}" stroke-width="1.4"/>
<text x="30" y="37" class="mono" fill="{theme['accent']}" font-size="11" font-weight="700">{cfg['index']}</text>
<text x="69" y="37" class="mono" fill="{theme['muted']}" font-size="10" letter-spacing="1.4">{esc(cfg['domain'])}</text>
<text x="30" y="88" class="ui" fill="{theme['fg']}" font-size="25" font-weight="800">{esc(cfg['title'])}</text>
<text x="30" y="126" class="ui" fill="{theme['body']}" font-size="14">{esc(cfg['line1'])}</text>
<text x="30" y="148" class="ui" fill="{theme['body']}" font-size="14">{esc(cfg['line2'])}</text>
<text x="30" y="190" class="mono" fill="{theme['muted']}" font-size="9">{esc(cfg['stack'])}</text>
<path d="M30 215 H550" stroke="{theme['line']}"/>
<g transform="translate(30,242)" class="mono" font-size="9">
  <text x="0" y="0" fill="{theme['muted']}">LANG</text><text x="34" y="0" fill="{theme['fg']}">{esc(language)}</text>
  <text x="130" y="0" fill="{theme['muted']}">STARS</text><text x="169" y="0" fill="{theme['fg']}">{stars}</text>
  <text x="218" y="0" fill="{theme['muted']}">FORKS</text><text x="256" y="0" fill="{theme['fg']}">{forks}</text>
  <text x="318" y="0" fill="{theme['muted']}">UPDATED</text><text x="373" y="0" fill="{theme['fg']}">{updated}</text>
</g>
{motif(cfg['motif'], theme)}
</svg>'''


def system_svg(theme: dict) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="255" viewBox="0 0 1200 255">
{STYLE}
<rect width="1200" height="255" rx="26" fill="{theme['panel']}" stroke="{theme['line']}"/>
<text x="38" y="43" class="mono" fill="{theme['muted']}" font-size="10" letter-spacing="1.7">ENGINEERING SYSTEM</text>
<text x="38" y="83" class="ui" fill="{theme['fg']}" font-size="26" font-weight="800">From model quality to system reliability.</text>
<text x="38" y="113" class="ui" fill="{theme['body']}" font-size="14">Current direction: reproducible ML workflows, deployment, CI/CD, monitoring and model lifecycle.</text>
<g transform="translate(38,169)">
  <path d="M0 0 H1095" stroke="{theme['line']}" stroke-width="2"/>
  <g class="mono" font-size="9">
    <circle cx="0" cy="0" r="6" fill="{theme['accent']}"/><text x="0" y="30" text-anchor="middle" fill="{theme['muted']}">DATA</text>
    <circle cx="219" cy="0" r="6" fill="{theme['accent']}"/><text x="219" y="30" text-anchor="middle" fill="{theme['muted']}">TRAIN</text>
    <circle cx="438" cy="0" r="6" fill="{theme['accent2']}"/><text x="438" y="30" text-anchor="middle" fill="{theme['muted']}">PACKAGE</text>
    <circle cx="657" cy="0" r="6" fill="{theme['accent2']}"/><text x="657" y="30" text-anchor="middle" fill="{theme['muted']}">DEPLOY</text>
    <circle cx="876" cy="0" r="6" fill="{theme['good']}"/><text x="876" y="30" text-anchor="middle" fill="{theme['muted']}">MONITOR</text>
    <circle cx="1095" cy="0" r="6" fill="{theme['good']}"><animate attributeName="r" values="5;9;5" dur="2s" repeatCount="indefinite"/></circle><text x="1095" y="30" text-anchor="middle" fill="{theme['muted']}">IMPROVE</text>
  </g>
  <circle r="4.5" fill="{theme['accent']}"><animateMotion dur="5.8s" repeatCount="indefinite" path="M0 0 H1095"/></circle>
</g>
<g transform="translate(835,35)" class="mono" font-size="10">
  <rect x="0" y="0" width="116" height="28" rx="14" fill="{theme['bg']}" stroke="{theme['line']}"/><text x="58" y="18" text-anchor="middle" fill="{theme['muted']}">PYTHON</text>
  <rect x="126" y="0" width="116" height="28" rx="14" fill="{theme['bg']}" stroke="{theme['line']}"/><text x="184" y="18" text-anchor="middle" fill="{theme['muted']}">TENSORFLOW</text>
  <rect x="252" y="0" width="78" height="28" rx="14" fill="{theme['bg']}" stroke="{theme['line']}"/><text x="291" y="18" text-anchor="middle" fill="{theme['muted']}">DOCKER</text>
</g>
</svg>'''


def main():
    user = safe_api(f"/users/{USER}", {"public_repos": 0, "followers": 0, "login": USER})
    repos = safe_api(f"/users/{USER}/repos?per_page=100&sort=updated&type=owner", [])
    repo_map = {r.get("name"): r for r in repos}

    for theme_name, theme in THEMES.items():
        write(f"hero-{theme_name}.svg", hero_svg(theme, user, repos))
        write(f"system-{theme_name}.svg", system_svg(theme))
        for cfg in PROJECTS:
            write(
                f"project-{cfg['slug']}-{theme_name}.svg",
                project_svg(theme, cfg, repo_map.get(cfg["repo"], {})),
            )

    print(f"Rendered {len(list(OUT.glob('*.svg')))} SVG files into {OUT}/")


if __name__ == "__main__":
    main()
