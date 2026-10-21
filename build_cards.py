"""Generates the terminal-style SVG cards used in README.md (same look as banner.svg)."""
from html import escape
from pathlib import Path

OUT = Path(__file__).parent / "assets"
SANS = "Segoe UI, Inter, Helvetica, Arial, sans-serif"
MONO = "Menlo, Consolas, monospace"

# muted tints, one per card, so cards feel related but not identical
TINTS = {
    "slate": ("#334155", "#1E3A5F"),
    "indigo": ("#3B3F6B", "#334155"),
    "teal": ("#1F4E5A", "#334155"),
    "plum": ("#4A3B5C", "#1E3A5F"),
    "steel": ("#2E4A6B", "#3B3F6B"),
    "moss": ("#2F4A45", "#334155"),
}


def shell(w, h, tint, body, uid):
    a, b = TINTS[tint]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <clipPath id="c{uid}"><rect width="{w}" height="{h}" rx="18"/></clipPath>
    <filter id="b{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="45"/></filter>
    <pattern id="g{uid}" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#fff" stroke-opacity=".04"/></pattern>
  </defs>
  <g clip-path="url(#c{uid})">
    <rect width="{w}" height="{h}" fill="#0B1020"/>
    <g filter="url(#b{uid})" opacity=".6">
      <circle cx="{w*0.2:.0f}" cy="20" r="{min(w,h)*0.45:.0f}" fill="{a}">
        <animate attributeName="cx" values="{w*0.2:.0f};{w*0.4:.0f};{w*0.2:.0f}" dur="14s" repeatCount="indefinite"/></circle>
      <circle cx="{w*0.85:.0f}" cy="{h:.0f}" r="{min(w,h)*0.5:.0f}" fill="{b}">
        <animate attributeName="cx" values="{w*0.85:.0f};{w*0.65:.0f};{w*0.85:.0f}" dur="12s" repeatCount="indefinite"/></circle>
    </g>
    <rect width="{w}" height="{h}" fill="url(#g{uid})"/>
    <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="#fff" stroke-opacity=".12"/>
    <circle cx="28" cy="28" r="5" fill="#475569"/><circle cx="45" cy="28" r="5" fill="#475569"/><circle cx="62" cy="28" r="5" fill="#475569"/>
{body}
  </g>
</svg>
'''


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur]


def chips(tags, x, y, max_w):
    out, cx, cy = [], x, y
    for t in tags:
        w = len(t) * 7.4 + 18
        if cx + w > x + max_w:
            cx, cy = x, cy + 30
        out.append(f'    <rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="22" rx="6" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".14"/>'
                   f'<text x="{cx + w/2:.0f}" y="{cy + 15}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#CBD5E1">{escape(t)}</text>')
        cx += w + 8
    return "\n".join(out)


def project(slug, tint, path, title, kind, desc, tags):
    w, h = 490, 270
    lines = wrap(desc, 58)
    desc_svg = "\n".join(
        f'    <text x="28" y="{122 + i*21}" font-family="{SANS}" font-size="14.5" fill="#CBD5E1">{escape(l)}</text>'
        for i, l in enumerate(lines))
    body = f'''    <text x="{w-24}" y="33" text-anchor="end" font-family="{MONO}" font-size="12" fill="#94A3B8">{escape(path)}</text>
    <text x="28" y="72" font-family="{MONO}" font-size="12.5" fill="#94A3B8">{escape(kind)}</text>
    <text x="28" y="100" font-family="{SANS}" font-size="24" font-weight="700" fill="#F1F5F9">{escape(title)}</text>
{desc_svg}
{chips(tags, 28, h - 46 - (30 if sum(len(t)*7.4+26 for t in tags) > w - 56 else 0), w - 56)}'''
    (OUT / f"p-{slug}.svg").write_text(shell(w, h, tint, body, slug))


def section(slug, cmd, title):
    w, h = 1000, 64
    body = f'''    <text x="88" y="35" font-family="{MONO}" font-size="14" fill="#94A3B8">$ {escape(cmd)}</text>
    <text x="{88 + (len(cmd)+3)*8.6:.0f}" y="36" font-family="{SANS}" font-size="19" font-weight="700" fill="#F1F5F9">{escape(title)}</text>
    <rect x="{88 + (len(cmd)+3)*8.6 + len(title)*11.2 + 6:.0f}" y="22" width="9" height="17" fill="#A5B4FC">
      <animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>'''
    svg = shell(w, h, "slate", body, slug).replace('cy="28" r="5"', 'cy="32" r="5"')
    (OUT / f"s-{slug}.svg").write_text(svg)


def focus():
    w, h = 1000, 190
    cols = [
        ("ai / ml", "AI & ML", "RAG pipelines, local LLMs and ML", "models that predict real outcomes"),
        ("backend", "Backend", "REST APIs, relational databases,", "auth and Dockerised services"),
        ("web + mobile", "Web & Mobile", "Vue, Streamlit and Flutter interfaces", "on top of my own APIs"),
    ]
    parts = []
    for i, (tag, title, l1, l2) in enumerate(cols):
        x = 28 + i * 324
        if i:
            parts.append(f'    <rect x="{x-14}" y="64" width="1" height="100" fill="#fff" fill-opacity=".1"/>')
        parts.append(f'''    <text x="{x}" y="80" font-family="{MONO}" font-size="12.5" fill="#94A3B8">// {tag}</text>
    <text x="{x}" y="110" font-family="{SANS}" font-size="21" font-weight="700" fill="#F1F5F9">{escape(title)}</text>
    <text x="{x}" y="138" font-family="{SANS}" font-size="14" fill="#CBD5E1">{escape(l1)}</text>
    <text x="{x}" y="158" font-family="{SANS}" font-size="14" fill="#CBD5E1">{escape(l2)}</text>''')
    parts.insert(0, f'    <text x="{w-24}" y="33" text-anchor="end" font-family="{MONO}" font-size="12" fill="#94A3B8">what-i-do.md</text>')
    (OUT / "focus.svg").write_text(shell(w, h, "indigo", "\n".join(parts), "focus"))


def stack():
    rows = [
        ("ai / ml", ["LangChain", "ChromaDB", "HuggingFace", "Ollama", "Llama 3.2", "scikit-learn", "pandas", "Streamlit"]),
        ("backend", ["Python", "Java", "Node.js", "Express", "Prisma", "PostgreSQL", "REST APIs"]),
        ("frontend", ["Vue 3", "TypeScript", "JavaScript", "Tailwind CSS", "Flutter", "Dart"]),
        ("systems", ["C++", "OpenMP", "Docker", "Docker Compose", "Git", "Linux"]),
    ]
    w, h = 1000, 70 + len(rows) * 44
    parts = [f'    <text x="{w-24}" y="33" text-anchor="end" font-family="{MONO}" font-size="12" fill="#94A3B8">stack.json</text>']
    for i, (label, tags) in enumerate(rows):
        y = 62 + i * 44
        parts.append(f'    <text x="28" y="{y+15}" font-family="{MONO}" font-size="13" fill="#A5B4FC">{label}</text>')
        parts.append(chips(tags, 140, y, w - 170))
    (OUT / "stack.svg").write_text(shell(w, h, "steel", "\n".join(parts), "stack"))


def contact():
    w, h = 1000, 150
    body = f'''    <text x="{w-24}" y="33" text-anchor="end" font-family="{MONO}" font-size="12" fill="#94A3B8">contact.sh</text>
    <text x="28" y="74" font-family="{MONO}" font-size="13" fill="#94A3B8">$ echo $STATUS</text>
    <text x="28" y="104" font-family="{SANS}" font-size="22" font-weight="700" fill="#F1F5F9">Open to internships and collaboration.</text>
    <text x="28" y="128" font-family="{SANS}" font-size="14.5" fill="#CBD5E1">Currently going deeper into RAG evaluation and turning ML models into real products.</text>
    <g transform="translate(790 86)">
      <rect width="180" height="36" rx="18" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".18"/>
      <circle cx="22" cy="18" r="4" fill="#86EFAC"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></circle>
      <text x="36" y="23" font-family="{SANS}" font-size="13.5" font-weight="600" fill="#CBD5E1">Let's talk</text>
    </g>'''
    (OUT / "contact.svg").write_text(shell(w, h, "plum", body, "contact"))


if __name__ == "__main__":
    focus()
    stack()
    contact()
    for s, cmd, t in [("work", "ls ./projects", "Featured work"),
                      ("stack", "cat stack.json", "Tech stack"),
                      ("github", "git log --stat", "On GitHub")]:
        section(s, cmd, t)
    project("pharaoh", "indigo", "PharaohMind-RAG", "PharaohMind RAG", "AI · Retrieval-Augmented Generation",
            "A chatbot for Ancient Egypt history whose answers are grounded in a local knowledge base. It shows the passages it retrieved, so every answer can be checked.",
            ["LangChain", "ChromaDB", "HuggingFace", "Ollama", "Streamlit"])
    project("studor", "teal", "AI_SE04_StudyRiskPredictor", "Studor", "AI · Machine Learning",
            "Predicts a student's academic risk from attendance, study hours, deadlines and workload, then gives personalised study advice.",
            ["scikit-learn", "pandas", "Streamlit", "PostgreSQL", "Plotly"])
    project("clarivo", "steel", "clarivo", "Clarivo", "Mobile + Web · Fintech",
            "Stock tracker with demo prices, historical charts, portfolio tracking, market news and geolocation, with fallbacks when free API limits run out.",
            ["Flutter", "Dart", "REST APIs", "JavaScript"])
    project("ade", "moss", "ade-website", "ADE Website", "Full-stack · E-commerce",
            "Storefront with separate frontend and backend services: catalog, cart, checkout, auth and EN/DE localisation, started with one Docker Compose command.",
            ["Vue 3", "TypeScript", "Express", "Prisma", "PostgreSQL", "Docker"])
    project("pagerank", "slate", "pagerank", "Parallel PageRank", "Systems · Parallel computing",
            "Serial vs. OpenMP-parallel PageRank on a 4,500-node graph, measuring speedup and checking that both versions produce the same ranks.",
            ["C++", "OpenMP", "CMake"])
    project("chessy", "plum", "chessy", "Chessy", "Game · AI opponent",
            "Cyberpunk-themed chess game with a computer opponent, two-player mode, an openings learning section, sound and animations. Team project.",
            ["Python", "Pygame", "Game AI"])
