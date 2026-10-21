"""Generates the SVG pieces used in README.md.

Only the banner (assets/banner.svg, hand-written) is a full dark terminal card.
Everything else uses a different form on purpose: a light paper card, two
feature cards with their own tint, a file-listing card, and a warm contact strip.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).parent / "assets"
SANS = "Segoe UI, Inter, Helvetica, Arial, sans-serif"
MONO = "Menlo, Consolas, monospace"
SERIF = "Georgia, 'Times New Roman', serif"


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'


PAD = 14


def padded(w, h, body):
    """Card with transparent margin so cards placed side by side never touch."""
    return svg(w + 2 * PAD, h + 2 * PAD, f'<g transform="translate({PAD} {PAD})">\n{body}\n</g>')


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur]


def chips(tags, x, y, max_w, fg, bg, stroke):
    out, cx, cy = [], x, y
    for t in tags:
        w = len(t) * 7.4 + 18
        if cx + w > x + max_w:
            cx, cy = x, cy + 30
        out.append(f'  <rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="22" rx="11" fill="{bg}" stroke="{stroke}"/>'
                   f'<text x="{cx + w/2:.0f}" y="{cy + 15}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{fg}">{escape(t)}</text>')
        cx += w + 8
    return "\n".join(out)


# 1. light "paper" card: what I do -------------------------------------------
def focus():
    w, h = 1000, 156
    accents = ["#8FA6FF", "#6FD6AE", "#F2B880"]  # dusty blue, sage, sand
    cols = [
        ("01", "AI & ML", ["RAG pipelines, local LLMs and", "ML models that predict outcomes"]),
        ("02", "Backend", ["REST APIs, relational databases,", "auth and Dockerised services"]),
        ("03", "Web & Mobile", ["Vue, Streamlit and Flutter", "interfaces on my own APIs"]),
    ]
    parts = [f'  <rect width="{w}" height="{h}" rx="20" fill="#1B1530"/>',
             f'  <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="20" fill="none" stroke="#2E2836"/>',
             f'  <text x="40" y="40" font-family="{SERIF}" font-size="15" font-style="italic" fill="#A89BB5">What I work on</text>']
    for i, (num, title, lines) in enumerate(cols):
        x = 40 + i * 315
        a = accents[i]
        parts.append(f'''  <circle cx="{x+18}" cy="74" r="16" fill="{a}" fill-opacity=".18"/>
  <circle cx="{x+18}" cy="74" r="6" fill="{a}"><animate attributeName="r" values="6;8;6" dur="{3+i}s" repeatCount="indefinite"/></circle>
  <text x="{x+50}" y="81" font-family="{SANS}" font-size="19" font-weight="700" fill="#EDE7F2">{escape(title)}</text>
  <text x="{x}" y="114" font-family="{SANS}" font-size="14" fill="#B8AFC2">{escape(lines[0])}</text>
  <text x="{x}" y="133" font-family="{SANS}" font-size="14" fill="#B8AFC2">{escape(lines[1])}</text>''')
    (OUT / "focus-v4.svg").write_text(svg(w, h, "\n".join(parts)))


# 2. two feature cards, each with its own tint --------------------------------
def feature(slug, bg, glow, accent, label, title, desc, tags, number):
    w, h = 490, 300
    lines = wrap(desc, 54)
    desc_svg = "\n".join(f'  <text x="32" y="{150 + i*22}" font-family="{SANS}" font-size="15" fill="#D9DEE6">{escape(l)}</text>'
                         for i, l in enumerate(lines))
    body = f'''  <defs>
    <clipPath id="c{slug}"><rect width="{w}" height="{h}" rx="24"/></clipPath>
    <radialGradient id="r{slug}" cx="85%" cy="15%" r="70%"><stop offset="0" stop-color="{glow}" stop-opacity=".75"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
  </defs>
  <g clip-path="url(#c{slug})">
    <rect width="{w}" height="{h}" fill="{bg}"/>
    <rect width="{w}" height="{h}" fill="url(#r{slug})">
      <animate attributeName="opacity" values=".7;1;.7" dur="6s" repeatCount="indefinite"/></rect>
    <text x="{w-28}" y="96" text-anchor="end" font-family="{SERIF}" font-size="96" font-weight="700" fill="#fff" fill-opacity=".06">{number}</text>
    <rect x="32" y="36" width="{len(label)*7.3+24:.0f}" height="24" rx="12" fill="{accent}" fill-opacity=".16"/>
    <text x="44" y="52" font-family="{MONO}" font-size="12" fill="{accent}">{escape(label)}</text>
    <text x="32" y="112" font-family="{SANS}" font-size="28" font-weight="800" fill="#E8ECF4">{escape(title)}</text>
    <rect x="32" y="124" width="36" height="3" rx="1.5" fill="{accent}">
      <animate attributeName="width" values="36;64;36" dur="4s" repeatCount="indefinite"/></rect>
{desc_svg}
{chips(tags, 32, h - 72, w - 160, "#E7EBF0", "#ffffff14", "#ffffff22")}
    <text x="{w-28}" y="{h-56}" text-anchor="end" font-family="{SANS}" font-size="13" font-weight="600" fill="{accent}">View repo →</text>
  </g>'''
    (OUT / f"feat-{slug}.svg").write_text(padded(w, h, body))


# 3. "ls -la" listing for the smaller projects --------------------------------
def listing():
    rows = [
        ("clarivo/", "Flutter stock tracker: prices, charts, portfolio, news", "Flutter · Dart", "#5CC4E6"),
        ("ade-website/", "Full-stack storefront with Docker Compose, EN/DE", "Vue · Express · Prisma", "#8FD18B"),
        ("pagerank/", "Serial vs OpenMP-parallel PageRank, speedup tests", "C++ · OpenMP", "#F08FB0"),
        ("chessy/", "Chess game with AI opponent and openings trainer", "Python · Pygame", "#F2B880"),
    ]
    w, h = 1000, 70 + len(rows) * 46
    parts = [f'  <rect width="{w}" height="{h}" rx="16" fill="#111418"/>',
             f'  <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="#2A2F36"/>',
             f'  <text x="32" y="42" font-family="{MONO}" font-size="14" fill="#7D8590"><tspan fill="#8FD18B">azra@github</tspan>:<tspan fill="#5CC4E6">~/more-projects</tspan>$ ls -la</text>']
    for i, (name, desc, stack, color) in enumerate(rows):
        y = 84 + i * 46
        parts.append(f'''  <rect x="20" y="{y-24}" width="{w-40}" height="38" rx="8" fill="#ffffff" fill-opacity="0">
    <animate attributeName="fill-opacity" values="0;.045;0" dur="8s" begin="{i*2}s" repeatCount="indefinite"/></rect>
  <text x="32" y="{y}" font-family="{MONO}" font-size="12.5" fill="#545D68">drwxr-xr-x</text>
  <text x="140" y="{y}" font-family="{MONO}" font-size="14.5" font-weight="700" fill="{color}">{escape(name)}</text>
  <text x="300" y="{y}" font-family="{SANS}" font-size="14.5" fill="#C9D1D9">{escape(desc)}</text>
  <text x="{w-32}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="#7D8590">{escape(stack)}</text>''')
    (OUT / "more.svg").write_text(svg(w, h, "\n".join(parts)))


# 3b. smaller clickable cards for the other repos ---------------------------
def mini(slug, bg, accent, label, title, desc, stack):
    w, h = 490, 190
    lines = wrap(desc, 56)
    desc_svg = "\n".join(f'  <text x="28" y="{108 + i*21}" font-family="{SANS}" font-size="14" fill="#C3CAD6">{escape(l)}</text>'
                         for i, l in enumerate(lines))
    body = f'''  <rect width="{w}" height="{h}" rx="18" fill="{bg}"/>
  <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{accent}" stroke-opacity=".4"/>
  <rect x="0" y="28" width="4" height="40" rx="2" fill="{accent}">
    <animate attributeName="height" values="40;64;40" dur="5s" repeatCount="indefinite"/></rect>
  <text x="28" y="48" font-family="{MONO}" font-size="12" fill="{accent}">{escape(label)}</text>
  <text x="28" y="80" font-family="{SANS}" font-size="22" font-weight="700" fill="#E3E7EE">{escape(title)}</text>
  <text x="{w-24}" y="48" text-anchor="end" font-family="{SANS}" font-size="16" fill="{accent}">↗</text>
{desc_svg}
  <text x="28" y="{h-24}" font-family="{MONO}" font-size="12" fill="#8A93A3">{escape(stack)}</text>'''
    (OUT / f"card-{slug}.svg").write_text(padded(w, h, body))


# 3c. large contact buttons under the banner ---------------------------------
def link_button(slug, label, value, accent):
    w, h = 310, 76
    body = f'''  <rect width="{w}" height="{h}" rx="38" fill="#141A26"/>
  <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="38" fill="none" stroke="{accent}" stroke-opacity=".35"/>
  <circle cx="36" cy="38" r="16" fill="{accent}" fill-opacity=".18"/>
  <circle cx="36" cy="38" r="6" fill="{accent}"/>
  <text x="64" y="30" font-family="{SANS}" font-size="14.5" fill="{accent}">{escape(label)}</text>
  <text x="64" y="56" font-family="{SANS}" font-size="17" font-weight="600" fill="#E3E7EE">{escape(value)}</text>'''
    (OUT / f"btn-{slug}.svg").write_text(padded(w, h, body))


# 4. warm contact strip -------------------------------------------------------
def contact():
    w, h = 1000, 130
    body = f'''  <defs><linearGradient id="k" x1="0" x2="1"><stop offset="0" stop-color="#2A211C"/><stop offset="1" stop-color="#1C1A22"/></linearGradient></defs>
  <rect width="{w}" height="{h}" rx="65" fill="url(#k)"/>
  <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="65" fill="none" stroke="#4A3D33"/>
  <circle cx="72" cy="65" r="26" fill="#F2B880" fill-opacity=".15"/>
  <circle cx="72" cy="65" r="9" fill="#F2B880"><animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>
  <text x="120" y="58" font-family="{SERIF}" font-size="24" font-style="italic" fill="#F3E9DC">Open to internships and collaboration.</text>
  <text x="120" y="86" font-family="{SANS}" font-size="14.5" fill="#BFB2A3">Currently exploring RAG evaluation and turning ML models into real products.</text>
  <rect x="{w-210}" y="43" width="160" height="44" rx="22" fill="#F2B880"/>
  <text x="{w-130}" y="71" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="#2A211C">Say hello →</text>'''
    (OUT / "contact-v3.svg").write_text(svg(w, h, body))


if __name__ == "__main__":
    focus()
    feature("pharaoh", "#131B3A", "#4F6BE0", "#9FB4FF", "AI · RAG", "PharaohMind RAG",
            "A chatbot for Ancient Egypt history whose answers are grounded in a local knowledge base. It shows the passages it retrieved, so every answer can be checked.",
            ["LangChain", "ChromaDB", "Ollama", "Streamlit"], "01")
    feature("ade-website", "#261C10", "#C98A3E", "#F5C98A", "Full-stack · E-commerce", "ADE Website",
            "Storefront with separate frontend and backend: catalog, cart, checkout, auth and EN/DE. The whole stack runs with one Docker Compose command.",
            ["Vue 3", "TypeScript", "Express", "Prisma", "PostgreSQL", "Docker"], "02")
    mini("studor", "#10261F", "#6FD6AE", "AI · Machine Learning", "Studor",
         "Predicts a student's academic risk from attendance, study hours and workload, then gives study advice.",
         "scikit-learn · pandas · Streamlit · PostgreSQL")
    mini("clarivo", "#0F2433", "#5CC4E6", "Mobile · Fintech", "Clarivo",
         "Flutter stock tracker with demo prices, historical charts, portfolio tracking and market news.",
         "Flutter · Dart · REST APIs")
    mini("clarivoweb", "#1C1A33", "#A99BFF", "Web · Fintech", "Clarivo Web",
         "Web version of Clarivo: market, portfolio, news and stock detail pages with Chart.js charts.",
         "JavaScript · HTML · CSS")
    mini("pagerank", "#2B1724", "#F08FB0", "Systems · Parallel", "Parallel PageRank",
         "Serial vs OpenMP-parallel PageRank on a 4,500-node graph, with speedup and correctness checks.",
         "C++ · OpenMP · CMake")
    mini("chessy", "#2B2113", "#F2B880", "Game · AI opponent", "Chessy",
         "Cyberpunk chess game with a computer opponent, two-player mode and an openings trainer.",
         "Python · Pygame")
    mini("calc", "#12272A", "#6CCFC4", "Desktop · Java", "Scientific Calculator",
         "Java Swing scientific calculator with memory and calculation history.",
         "Java · Swing")
    contact()
    link_button("linkedin", "LinkedIn", "in/azra-ozdas", "#8FA6FF")
    link_button("email", "Email", "azraozdas.main@gmail.com", "#F2B880")
    link_button("github", "GitHub", "10+ projects", "#6FD6AE")
