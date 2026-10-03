"""Render the profile banner and the AI Factory animation as day/night SVGs.

Stdlib only, so the GitHub Action needs nothing but Python.

    python profile_gen/render.py --user wcr2000 --out dist
    python profile_gen/render.py --user wcr2000 --out dist --fixture sample.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.request
from html import escape
from pathlib import Path

PALETTES = {
    "day": {
        "bg": "#f7f3ec", "bg2": "#efe7da", "ink": "#1f2430", "muted": "#7b7f8a",
        "accent": "#e8743b", "accent_soft": "#f6c6a6", "teal": "#2f6f73",
        "teal_soft": "#bcd9d6", "line": "#d9cfbf", "metal": "#a7adb7", "glow": "#ffd9a8",
    },
    "night": {
        "bg": "#0f1420", "bg2": "#171e2e", "ink": "#e7eaf0", "muted": "#7f8799",
        "accent": "#f39a5b", "accent_soft": "#6b3d22", "teal": "#5fb3b3",
        "teal_soft": "#1f3c40", "line": "#283147", "metal": "#4b5468", "glow": "#f39a5b",
    },
}

FONT = "ui-sans-serif, -apple-system, 'Segoe UI', 'Noto Sans Thai', Roboto, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

QUERY = """
query($login: String!) {
  user(login: $login) {
    name
    followers { totalCount }
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


# ---------------------------------------------------------------- data

def fetch(login: str, token: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-gen"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def summarise(user: dict) -> dict:
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    today = dt.date.today().isoformat()
    days = [d for d in days if d["date"] <= today]

    # A streak survives an empty "today" because the day isn't over yet.
    streak = 0
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"] > 0:
            streak += 1
        elif i == 0:
            continue
        else:
            break

    return {
        "total_year": cal["totalContributions"],
        "streak": streak,
        "public_repos": user["repositories"]["totalCount"],
        "followers": user["followers"]["totalCount"],
        "last14": [d["contributionCount"] for d in days[-14:]],
        "last14_dates": [d["date"] for d in days[-14:]],
        "updated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


# ---------------------------------------------------------------- banner

def banner(stats: dict, mode: str) -> str:
    p = PALETTES[mode]
    w, h = 1200, 300

    # Neural-net doodle on the right: three layers, edges pulse in sequence.
    layers = [[70, 150, 230], [50, 110, 170, 230 + 20], [100, 200]]
    xs = [820, 950, 1080]
    nodes, edges = [], []
    k = 0
    for li in range(len(layers) - 1):
        for y1 in layers[li]:
            for y2 in layers[li + 1]:
                delay = (k * 0.23) % 4
                edges.append(
                    f'<line x1="{xs[li]}" y1="{y1}" x2="{xs[li+1]}" y2="{y2}" stroke="{p["line"]}" stroke-width="1.2"/>'
                    f'<line x1="{xs[li]}" y1="{y1}" x2="{xs[li+1]}" y2="{y2}" '
                    f'stroke="{p["teal"]}" stroke-width="1.4" class="edge" '
                    f'style="animation-delay:{delay:.2f}s"/>'
                )
                k += 1
    for li, ys in enumerate(layers):
        for j, y in enumerate(ys):
            fill = p["accent"] if (li + j) % 3 == 0 else p["teal"]
            nodes.append(
                f'<circle cx="{xs[li]}" cy="{y}" r="9" fill="{p["bg"]}" stroke="{fill}" stroke-width="3"/>'
                f'<circle cx="{xs[li]}" cy="{y}" r="4" fill="{fill}" class="node" '
                f'style="animation-delay:{(li * 0.7 + j * 0.31):.2f}s"/>'
            )

    chips = [
        (f'{stats["total_year"]:,}', "contributions / year"),
        (f'{stats["streak"]}', "day streak"),
        (f'{stats["public_repos"]}', "public repos"),
    ]
    chip_svg = []
    x = 64
    for value, label in chips:
        cw = 46 + 9.2 * len(value) + 6.6 * len(label)
        chip_svg.append(
            f'<g transform="translate({x:.0f},214)">'
            f'<rect width="{cw:.0f}" height="38" rx="19" fill="{p["bg2"]}" stroke="{p["line"]}"/>'
            f'<circle cx="20" cy="19" r="5" fill="{p["accent"]}"/>'
            f'<text x="34" y="25" font-family="{MONO}" font-size="16" font-weight="700" fill="{p["ink"]}">{escape(value)}'
            f'<tspan font-family="{FONT}" font-size="13" font-weight="400" fill="{p["muted"]}" dx="7">{escape(label)}</tspan></text>'
            f"</g>"
        )
        x += cw + 12

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Watchara, AI engineer and automation builder">
<style>
  .edge {{ stroke-dasharray: 14 200; animation: flow 4s linear infinite; opacity:.9 }}
  .node {{ animation: pulse 2.6s ease-in-out infinite; transform-box: fill-box; transform-origin: center }}
  .cursor {{ animation: blink 1.1s steps(1) infinite }}
  @keyframes flow {{ from {{ stroke-dashoffset: 206 }} to {{ stroke-dashoffset: 0 }} }}
  @keyframes pulse {{ 0%,100% {{ transform: scale(1) }} 50% {{ transform: scale(1.6) }} }}
  @keyframes blink {{ 50% {{ opacity: 0 }} }}
</style>
<rect width="{w}" height="{h}" rx="22" fill="{p["bg"]}"/>
<g opacity=".5">{''.join(f'<circle cx="{cx}" cy="{cy}" r="1.3" fill="{p["line"]}"/>' for cx in range(700, 1180, 24) for cy in range(24, 290, 24))}</g>
{''.join(edges)}
{''.join(nodes)}
<text x="64" y="74" font-family="{MONO}" font-size="15" fill="{p["accent"]}">~/watchara $ whoami<tspan class="cursor">▍</tspan></text>
<text x="62" y="134" font-family="{FONT}" font-size="54" font-weight="800" fill="{p["ink"]}">Watchara <tspan fill="{p["accent"]}">“First”</tspan></text>
<text x="64" y="176" font-family="{FONT}" font-size="20" fill="{p["muted"]}">AI engineer · automation builder · AI teacher at <tspan fill="{p["teal"]}" font-weight="700">AI พารวย</tspan></text>
{''.join(chip_svg)}
<text x="1136" y="284" text-anchor="end" font-family="{MONO}" font-size="10" fill="{p["muted"]}">updated {escape(stats["updated"])}</text>
</svg>
"""


# ---------------------------------------------------------------- factory

def factory(stats: dict, mode: str) -> str:
    p = PALETTES[mode]
    w, h = 1200, 380
    belt_y = 290
    counts = stats["last14"] or [0] * 14
    dates = stats["last14_dates"] or [""] * len(counts)
    peak = max(max(counts), 1)
    cycle = 28  # seconds for one crate to cross the belt

    crates = []
    for i, (n, date) in enumerate(zip(counts, dates)):
        if n == 0:
            ch, fill, stroke = 14, "none", p["line"]
        else:
            ch = 22 + 58 * (n / peak)
            fill, stroke = (p["accent"] if n >= peak * 0.6 else p["accent_soft"]), p["accent"]
        cw = 46
        label = dt.date.fromisoformat(date).strftime("%d") if date else ""
        delay = -i * (cycle / len(counts))
        dash = 'stroke-dasharray="4 3"' if n == 0 else ""
        strong = n >= peak * 0.6
        date_ink = p["muted"] if n == 0 else (p["bg"] if strong else p["ink"])
        crates.append(
            f'<g class="crate" style="animation-delay:{delay:.2f}s">'
            f'<rect x="0" y="{belt_y - ch:.1f}" width="{cw}" height="{ch:.1f}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="2" '
            f'{dash}/>'
            f'<text x="{cw/2}" y="{belt_y - ch - 7:.1f}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{p["ink"]}">{n}</text>'
            f'<text x="{cw/2}" y="{belt_y - 6:.1f}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{date_ink}">{label}</text>'
            f"</g>"
        )

    rollers = "".join(
        f'<g transform="translate({x},{belt_y + 14})"><circle r="10" fill="{p["bg2"]}" stroke="{p["metal"]}" stroke-width="2"/>'
        f'<line x1="-7" y1="0" x2="7" y2="0" stroke="{p["metal"]}" stroke-width="2" class="spin"/></g>'
        for x in range(80, 1130, 50)
    )

    def arm(x: int, delay: float, tint: str) -> str:
        return (
            f'<g transform="translate({x},0)">'
            f'<rect x="-34" y="40" width="68" height="16" rx="4" fill="{p["metal"]}"/>'
            f'<g class="arm" style="animation-delay:{delay}s">'
            f'<rect x="-5" y="56" width="10" height="120" fill="{p["metal"]}"/>'
            f'<rect x="-22" y="170" width="44" height="18" rx="5" fill="{tint}"/>'
            f'<circle cx="0" cy="66" r="7" fill="{p["bg2"]}" stroke="{tint}" stroke-width="3" class="led" style="animation-delay:{delay}s"/>'
            f"</g></g>"
        )

    # Streak gauge: needle angle maps 0..30 days to -90..90 degrees.
    streak = stats["streak"]
    angle = -90 + 180 * min(streak, 30) / 30

    total14 = sum(counts)
    busiest = max(counts) if counts else 0

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="AI Factory: the last 14 days of contributions ride a conveyor belt">
<style>
  .crate {{ animation: ride {cycle}s linear infinite; }}
  @keyframes ride {{ from {{ transform: translateX(-80px) }} to {{ transform: translateX(1220px) }} }}
  .spin {{ animation: spin 1.2s linear infinite; transform-origin: 0 0 }}
  @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
  .arm {{ animation: stamp 3.5s ease-in-out infinite }}
  @keyframes stamp {{ 0%,60%,100% {{ transform: translateY(0) }} 70% {{ transform: translateY(32px) }} 80% {{ transform: translateY(26px) }} }}
  .led {{ animation: led 3.5s ease-in-out infinite }}
  @keyframes led {{ 0%,60%,100% {{ fill: {p["bg2"]} }} 70%,80% {{ fill: {p["glow"]} }} }}
  .smoke {{ animation: smoke 5s ease-out infinite; opacity: 0 }}
  @keyframes smoke {{ 0% {{ transform: translate(0,0) scale(.6); opacity: 0 }} 20% {{ opacity: .55 }} 100% {{ transform: translate(-30px,-60px) scale(1.8); opacity: 0 }} }}
  .screen {{ animation: flicker 6s steps(1) infinite }}
  @keyframes flicker {{ 0%,100% {{ opacity: 1 }} 92% {{ opacity: .75 }} }}
</style>
<rect width="{w}" height="{h}" rx="22" fill="{p["bg"]}"/>
<rect x="0" y="{belt_y + 30}" width="{w}" height="{h - belt_y - 30}" fill="{p["bg2"]}"/>

<!-- chimney + smoke -->
<rect x="1080" y="12" width="40" height="80" fill="{p["metal"]}"/>
<circle cx="1100" cy="10" r="12" fill="{p["muted"]}" class="smoke"/>
<circle cx="1100" cy="10" r="12" fill="{p["muted"]}" class="smoke" style="animation-delay:1.7s"/>
<circle cx="1100" cy="10" r="12" fill="{p["muted"]}" class="smoke" style="animation-delay:3.4s"/>

<!-- shift monitor -->
<g transform="translate(40,28)" class="screen">
  <rect width="330" height="128" rx="12" fill="{p["bg2"]}" stroke="{p["line"]}" stroke-width="2"/>
  <text x="20" y="32" font-family="{MONO}" font-size="13" fill="{p["accent"]}">AI FACTORY · shift report</text>
  <text x="20" y="64" font-family="{MONO}" font-size="14" fill="{p["ink"]}">last 14 days  <tspan font-weight="700">{total14}</tspan> contributions</text>
  <text x="20" y="88" font-family="{MONO}" font-size="14" fill="{p["ink"]}">busiest day   <tspan font-weight="700">{busiest}</tspan></text>
  <text x="20" y="112" font-family="{MONO}" font-size="14" fill="{p["ink"]}">this year     <tspan font-weight="700">{stats["total_year"]:,}</tspan></text>
</g>

<!-- streak gauge -->
<g transform="translate(560,128)">
  <path d="M-80 0 A80 80 0 0 1 80 0" fill="none" stroke="{p["line"]}" stroke-width="14" stroke-linecap="round"/>
  <path d="M-80 0 A80 80 0 0 1 80 0" fill="none" stroke="{p["accent"]}" stroke-width="14" stroke-linecap="round"
        pathLength="100" stroke-dasharray="{min(streak, 30) / 30 * 100:.1f} 100"/>
  <g transform="rotate({angle:.1f})"><line x1="0" y1="0" x2="0" y2="-64" stroke="{p["ink"]}" stroke-width="4" stroke-linecap="round"/></g>
  <circle r="9" fill="{p["ink"]}"/>
  <text y="34" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="800" fill="{p["ink"]}">{streak} day{"s" if streak != 1 else ""}</text>
  <text y="54" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{p["muted"]}">contribution streak</text>
</g>

{arm(800, 0.0, p["teal"])}
{arm(960, 1.2, p["accent"])}

<!-- belt -->
{''.join(crates)}
<rect x="40" y="{belt_y}" width="{w - 80}" height="8" rx="4" fill="{p["ink"]}" opacity=".85"/>
{rollers}
<text x="40" y="{h - 16}" font-family="{FONT}" font-size="12" fill="{p["muted"]}">Each crate is one day. Height = contributions that day. Dashed = a rest day.</text>
<text x="{w - 40}" y="{h - 16}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{p["muted"]}">updated {escape(stats["updated"])}</text>
</svg>
"""


# ---------------------------------------------------------------- cli

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", default="dist")
    ap.add_argument("--fixture", help="read summarised stats from JSON instead of the API")
    args = ap.parse_args()

    if args.fixture:
        stats = json.loads(Path(args.fixture).read_text())
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("GITHUB_TOKEN is required")
        stats = summarise(fetch(args.user, token))

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for mode in PALETTES:
        (out / f"banner-{mode}.svg").write_text(banner(stats, mode))
        (out / f"factory-{mode}.svg").write_text(factory(stats, mode))
    (out / "stats.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps({k: v for k, v in stats.items() if not k.startswith("last14")}))


if __name__ == "__main__":
    main()
