"""Build assets/whoami.svg from assets/whoami.template.svg by embedding stack icons.

SVGs shown via <img> on GitHub cannot load external images, so each icon is
downloaded and embedded as a base64 data URI.
"""
import base64, re, urllib.request

SKILL = "https://skillicons.dev/icons?theme=dark&i={}"
ROWS = [
    ("Frontend", ["vue", "react", "tailwind", "bootstrap", "vite"]),
    ("Backend", ["laravel", "php", "fastapi", "python", "spring", "nginx"]),
    ("Database", ["mysql", "postgres", "redis",
                  "https://go-skill-icons.vercel.app/api/icons?theme=dark&i=sqlserver"]),
    ("Tools", ["git", "github", "docker", "linux", "vscode", "postman",
               "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jetbrains/jetbrains-original.svg"]),
]
SIZE, GAP, PITCH, LABEL_W = 28, 8, 36, 100


def fetch(src):
    url = src if src.startswith("http") else SKILL.format(src)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=30).read()
    return "data:image/svg+xml;base64," + base64.b64encode(data).decode()


tpl = open("assets/whoami.template.svg", encoding="utf-8").read()
m = re.search(r"<!--STACK x=([\d.]+) y=([\d.]+)-->", tpl)
x0, y0 = float(m.group(1)), float(m.group(2))
out = []
for r, (label, icons) in enumerate(ROWS):
    top = y0 + r * PITCH
    out.append(f'<text x="{x0}" y="{top + SIZE / 2 + 5}" class="k">{label}</text>')
    for i, src in enumerate(icons):
        x = x0 + LABEL_W + i * (SIZE + GAP)
        out.append(f'<image x="{x}" y="{top}" width="{SIZE}" height="{SIZE}" href="{fetch(src)}"/>')
svg = tpl.replace(m.group(0), "\n".join(out))
open("assets/whoami.svg", "w", encoding="utf-8").write(svg)
print("built assets/whoami.svg")
