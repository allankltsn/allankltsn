"""Gera os SVGs animados dos tópicos do README: títulos de seção, um card por
repositório (ilustração + descrição) e o painel "Código em números".

Uso: python tools/gen_cards.py assets [stats.json]
Só biblioteca padrão. SMIL puro (o GitHub preserva a animação em <img>).
"""
import json
import math
import sys
import textwrap
from collections import Counter
from pathlib import Path

OUT = Path(sys.argv[1])
STATS = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")) if len(sys.argv) > 2 else None
(OUT / "cards").mkdir(parents=True, exist_ok=True)
(OUT / "sections").mkdir(parents=True, exist_ok=True)

BG, CARD, LINE, NODE = "#0b0f17", "#111827", "#1f2937", "#0d1117"
TXT, MUTED, DIM = "#e6edf3", "#8b96a8", "#4b5563"
TEAL, BLUE, PURPLE, AMBER, GREEN, PINK, RED = "#2dd4bf", "#3b82f6", "#a78bfa", "#f59e0b", "#4ade80", "#f472b6", "#ef4444"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
LANG_COLOR = {"Python": "#3776ab", "TypeScript": "#3178c6", "JavaScript": "#f7df1e", "C++": "#f34b7d", "C": "#a8b9cc",
              "Jupyter Notebook": "#f37726", "HTML": "#e34c26", "Shell": "#89e051", "Java": "#ed8b00", "CSS": "#9b6bdf"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fade(b, d=0.5):
    return f'<animate attributeName="opacity" to="1" begin="{b}s" dur="{d}s" fill="freeze"/>'


def loop(vals, kt, dur, attr="opacity", begin=0):
    return (f'<animate attributeName="{attr}" values="{vals}" keyTimes="{kt}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>')


def pulse(attr, vals, dur, begin=0):
    return f'<animate attributeName="{attr}" values="{vals}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'


def T(x, y, s, size=12, fill=MUTED, anchor="start", mono=False, weight=None, extra=""):
    f = f' font-family="{MONO}"' if mono else ""
    w = f' font-weight="{weight}"' if weight else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{f}{w} {extra}>{esc(s)}</text>'


def R(x, y, w, h, rx=4, fill="none", stroke=None, sw=1, extra="", inner=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st} {extra}>{inner}</rect>'


def C(x, y, r, fill, extra="", inner=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}>{inner}</circle>'


def L(x1, y1, x2, y2, stroke=LINE, sw=1.5, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def packet(x1, y1, x2, y2, color, dur=2.2, begin=0, r=3.5):
    return C(x1, y1, r, color, 'opacity="0"',
             pulse("cx", f"{x1};{x2}", dur, begin) + pulse("cy", f"{y1};{y2}", dur, begin) +
             f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>')


# ------------------------------------------------------------------ ilustrações (600x150)
def m_agents(a):
    cx, cy = 300, 78
    spec = [(150, 38, TEAL), (150, 118, BLUE), (255, 20, PURPLE), (345, 136, AMBER), (450, 38, PINK), (450, 118, GREEN)]
    o = []
    for i, (x, y, c) in enumerate(spec):
        o.append(L(cx, cy, x, y, LINE))
        o.append(packet(cx, cy, x, y, c, 2.0 + i * 0.2, i * 0.35))
        o.append(R(x - 24, y - 11, 48, 22, 11, NODE, c, 1.2, inner=pulse("stroke-opacity", "0.4;1;0.4", 2.4, i * 0.3)))
        o.append(T(x, y + 4, ["back", "front", "qa", "sec", "ux", "sre"][i], 10, c, "middle", True))
    o.append(C(cx, cy, 24, NODE, f'stroke="{a}" stroke-width="2"', pulse("r", "24;27;24", 2.5)))
    o.append(T(cx, cy + 4, "gestor", 11, TXT, "middle", True, 700))
    return "".join(o)


def m_avatar(a):
    o = []
    for i in range(9):
        h = 14 + (i * 7) % 26
        o.append(R(52 + i * 11, 75 - h / 2, 6, h, 3, a, extra=f'opacity="0.8"',
                   inner=pulse("height", f"{h};{h*0.35:.0f};{h}", 0.9 + i * 0.07) + pulse("y", f"{75-h/2};{75-h*0.175:.0f};{75-h/2}", 0.9 + i * 0.07)))
    o.append(T(100, 128, "fala", 10, DIM, "middle", True))
    o.append(L(165, 75, 205, 75, LINE)); o.append(packet(165, 75, 205, 75, a, 1.6))
    for i, g in enumerate(["OLÁ", "TUDO", "BEM"]):
        o.append(f'<g opacity="0">{loop("0;0;1;1;0", f"0;{0.1+i*0.15:.2f};{0.2+i*0.15:.2f};0.9;1", 4.5)}'
                 + R(215 + i * 62, 60, 54, 30, 8, NODE, a, 1) + T(242 + i * 62, 80, g, 11, a, "middle", True) + '</g>')
    o.append(T(300, 128, "glosas", 10, DIM, "middle", True))
    o.append(L(405, 75, 440, 75, LINE)); o.append(packet(405, 75, 440, 75, PURPLE, 1.6, 0.4))
    # avatar
    o.append(C(500, 48, 14, "#1e293b", f'stroke="{PURPLE}" stroke-width="2"'))
    o.append(f'<path d="M476 118 Q476 82 500 82 Q524 82 524 118 Z" fill="#1e293b" stroke="{PURPLE}" stroke-width="2"/>')
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="0 524 92;-28 524 92;8 524 92;-28 524 92;0 524 92" dur="2.4s" repeatCount="indefinite"/>'
             + f'<path d="M524 92 L552 70" stroke="{PURPLE}" stroke-width="5" stroke-linecap="round"/>' + C(554, 66, 6, PURPLE) + '</g>')
    o.append(T(500, 138, "avatar 3D", 10, DIM, "middle", True))
    return "".join(o)


def m_panel(a):
    o = [R(165, 10, 270, 132, 8, NODE, LINE), R(177, 20, 246, 20, 6, "none", LINE), T(190, 34, "buscar ferramentas…", 10, DIM)]
    groups = [(TEAL, "Qualidade e testes", ["Problemas", "Testes"]), (PURPLE, "Git", ["Branches"])]
    y = 48
    for i, (c, name, items) in enumerate(groups):
        o.append(R(177, y, 3, 14, 1.5, c) + T(188, y + 11, "▾ " + name, 11, TXT, weight=600))
        y += 18
        for it in items:
            o.append(T(200, y + 9, it, 10, MUTED)); y += 14
        y += 4
    o.append(R(182, 66, 236, 15, 4, "none", a, 1.2, inner=pulse("stroke-opacity", "0;1;0", 3) + pulse("y", "66;80;94;66", 6)))
    o.append(R(445, 118, 110, 22, 11, NODE, a, 1.2) + C(461, 129, 4, a, inner=pulse("opacity", "0.3;1;0.3", 1.6)) + T(474, 133, "fixado · 4", 10, a, mono=True))
    o.append(L(435, 129, 445, 129, a, 1))
    return "".join(o)


def m_hooks(a):
    rows = ["lint ao salvar", "protege a main", "bloqueia segredos", "commitlint"]
    o = [R(150, 10, 300, 132, 10, NODE, LINE), T(166, 30, "hooks · pre-commit", 10, DIM, mono=True)]
    for i, r in enumerate(rows):
        y = 48 + i * 23
        o.append(R(166, y, 268, 18, 5, "#0b1220", LINE))
        o.append(T(176, y + 13, r, 11, MUTED))
        t0 = 0.12 + i * 0.18
        o.append(f'<g opacity="0">{loop("0;0;1;1;0", f"0;{t0:.2f};{t0+0.05:.2f};0.92;1", 5.5)}'
                 + f'<path d="M408 {y+9} l5 5 l10 -11" stroke="{GREEN}" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    o.append(C(500, 76, 26, NODE, f'stroke="{a}" stroke-width="2"', pulse("r", "26;29;26", 2.2)))
    o.append(f'<path d="M500 62 L514 67 V78 Q514 88 500 93 Q486 88 486 78 V67 Z" fill="none" stroke="{a}" stroke-width="2"/>')
    return "".join(o)


def m_satellite(a):
    cx, cy = 300, 76
    o = [C(cx, cy, 70, "none", f'stroke="{LINE}" stroke-dasharray="3 5"'), C(cx, cy, 38, "none", f'stroke="{LINE}" stroke-dasharray="3 5"')]
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="14s" repeatCount="indefinite"/>')
    for i, (r, c, n) in enumerate([(70, TEAL, "app"), (70, BLUE, "api"), (38, PURPLE, "ui"), (38, AMBER, "ia")]):
        ang = i * 90 + (0 if r == 70 else 45)
        x, y = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
        o.append(L(cx, cy, f"{x:.1f}", f"{y:.1f}", LINE, 1))
        o.append(C(f"{x:.1f}", f"{y:.1f}", 11, NODE, f'stroke="{c}" stroke-width="2"'))
    o.append('</g>')
    o.append(C(cx, cy, 20, NODE, f'stroke="{a}" stroke-width="2.4"', pulse("r", "20;23;20", 2.4)) + T(cx, cy + 4, "hub", 11, TXT, "middle", True, 700))
    o.append(T(120, 80, "configs", 10, DIM, "middle", True) + T(480, 80, "satélites", 10, DIM, "middle", True))
    return "".join(o)


def m_gateway(a):
    o = [R(40, 56, 92, 40, 8, NODE, BLUE, 1.5) + T(86, 80, "cliente", 12, BLUE, "middle", True),
         R(246, 40, 108, 72, 10, NODE, a, 2, inner=pulse("stroke-opacity", "0.4;1;0.4", 2.4)),
         T(300, 66, "API Gateway", 11, TXT, "middle", weight=700),
         f'<rect x="288" y="78" width="24" height="18" rx="3" fill="none" stroke="{a}" stroke-width="2"/><path d="M293 78 v-5 a7 7 0 0 1 14 0 v5" fill="none" stroke="{a}" stroke-width="2"/>',
         R(468, 56, 92, 40, 8, NODE, GREEN, 1.5) + T(514, 80, "serviço", 12, GREEN, "middle", True),
         L(132, 76, 246, 76, LINE), L(354, 76, 468, 76, LINE), packet(132, 76, 246, 76, BLUE, 1.8), packet(354, 76, 468, 76, GREEN, 1.8, 0.9)]
    o.append(f'<path d="M300 112 V134" stroke="{LINE}" stroke-width="1.5"/>')
    o.append(f'<ellipse cx="300" cy="140" rx="22" ry="6" fill="{NODE}" stroke="{AMBER}"/>' + T(336, 143, "DynamoDB · métricas", 10, AMBER, mono=True))
    return "".join(o)


def m_observ(a):
    o = []
    for i, (title, c) in enumerate([("logs", BLUE), ("métricas", a), ("traces", PURPLE)]):
        x = 28 + i * 188
        o.append(R(x, 14, 172, 122, 8, NODE, LINE) + T(x + 12, 32, title, 11, c, mono=True))
        if i == 0:
            for j in range(5):
                w = 70 + (j * 37) % 70
                o.append(R(x + 12, 46 + j * 17, w, 7, 3, c, extra='opacity="0"', inner=fade(0.3 + j * 0.25, 0.4)))
        elif i == 1:
            pts = " ".join(f"{x+12+k*8:.0f},{96+math.sin(k/2.3)*22:.0f}" for k in range(20))
            o.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2.2" stroke-dasharray="260" stroke-dashoffset="260">'
                     f'<animate attributeName="stroke-dashoffset" values="260;0;0;260" keyTimes="0;0.5;0.9;1" dur="4s" repeatCount="indefinite"/></polyline>')
        else:
            for j, (s, w) in enumerate([(0, 120), (14, 70), (30, 50), (50, 40), (20, 30)]):
                o.append(R(x + 12 + s, 46 + j * 17, w, 9, 3, c, extra='opacity="0.85"', inner=pulse("width", f"0;{w}", 3.5, j * 0.2)))
    return "".join(o)


def m_login(a):
    o = [R(90, 10, 250, 132, 10, NODE, LINE), T(108, 32, "login", 11, DIM, mono=True),
         R(108, 42, 214, 20, 5, "none", LINE) + T(118, 56, "usuário@empresa.com", 10, MUTED),
         R(108, 68, 214, 20, 5, "none", LINE) + T(118, 82, "••••••••••", 11, MUTED),
         R(108, 96, 120, 30, 5, "none", LINE), R(114, 104, 14, 14, 3, "none", MUTED)]
    o.append(f'<path d="M117 111 l4 4 l8 -9" stroke="{GREEN}" stroke-width="2.2" fill="none" stroke-linecap="round" opacity="0">{loop("0;0;1;1;0","0;0.15;0.2;0.9;1",5)}</path>')
    o.append(T(136, 115, "não sou um robô", 10, MUTED))
    for i in range(6):
        o.append(R(366 + i * 32, 54, 26, 34, 6, NODE, a, 1.2) + f'<text x="{379+i*32}" y="78" font-size="16" fill="{TXT}" text-anchor="middle" font-family="{MONO}" opacity="0">'
                 + loop("0;0;1;1;0", f"0;{0.3+i*0.07:.2f};{0.35+i*0.07:.2f};0.9;1", 5) + ["4", "8", "2", "7", "1", "9"][i] + '</text>')
    o.append(T(462, 110, "código MFA", 10, DIM, "middle", True))
    o.append(f'<g opacity="0">{loop("0;0;0;1;1;0","0;0.7;0.74;0.78;0.95;1",5)}' + C(462, 130, 0, "none") + T(462, 132, "✓ autenticado", 11, GREEN, "middle", True) + '</g>')
    return "".join(o)


def m_dynamo(a):
    o = [R(130, 12, 340, 126, 8, NODE, LINE), R(130, 12, 340, 24, 8, "#0b1220", LINE),
         T(148, 29, "pk", 11, a, mono=True), T(250, 29, "sk", 11, a, mono=True), T(360, 29, "atributos", 11, a, mono=True)]
    for i in range(4):
        y = 46 + i * 22
        o.append(T(148, y + 14, f"USER#{100+i*7}", 11, MUTED, mono=True) + T(250, y + 14, f"PROFILE", 11, MUTED, mono=True) + T(360, y + 14, "{ nome, e-mail }", 11, DIM, mono=True))
        o.append(L(136, y + 20, 464, y + 20, LINE, 1))
    o.append(R(134, 44, 332, 22, 4, a, extra='opacity="0.16"', inner=pulse("y", "44;66;88;110;44", 5)))
    o.append(R(134, 44, 332, 22, 4, "none", a, 1.4, inner=pulse("y", "44;66;88;110;44", 5)))
    return "".join(o)


def m_sentiment(a):
    o = []
    for i in range(5):
        y = 20 + i * 24
        pos = [0.62, 0.35, 0.5, 0.7, 0.28][i]
        o.append(R(60, y, 330, 14, 7, "#0b1220", LINE))
        o.append(R(60, y, 330 * pos, 14, 7, GREEN, extra='opacity="0.85"', inner=pulse("width", f"0;{330*pos:.0f};{330*pos:.0f};0", 5, i * 0.25) ))
        o.append(R(60 + 330 * pos, y, 330 * (1 - pos), 14, 0, RED, extra='opacity="0.7"', inner=pulse("x", f"60;{60+330*pos:.0f};{60+330*pos:.0f};60", 5, i * 0.25)))
    o.append(T(60, 144, "positivo", 10, GREEN, mono=True) + T(390, 144, "negativo", 10, RED, "end", True))
    for i, (x, y) in enumerate([(430, 26), (470, 70), (440, 112)]):
        o.append(f'<g opacity="0">{loop("0;0;1;1;0", f"0;{0.1+i*0.2:.2f};{0.2+i*0.2:.2f};0.85;1", 5)}'
                 + R(x, y, 100, 28, 10, NODE, BLUE, 1.2) + R(x + 10, y + 9, 60, 4, 2, MUTED) + R(x + 10, y + 17, 40, 4, 2, DIM) + '</g>')
    o.append(T(500, 144, "tweets", 10, BLUE, "middle", True))
    return "".join(o)


def m_mlaas(a):
    nodes = [("dados", 40, BLUE), ("pré", 150, TEAL), ("treino", 270, a), ("avalia", 390, AMBER)]
    o = []
    for i, (n, x, c) in enumerate(nodes):
        o.append(R(x, 34, 82, 38, 8, NODE, c, 1.5, inner=pulse("stroke-opacity", "0.4;1;0.4", 2.6, i * 0.4)) + T(x + 41, 58, n, 12, c, "middle", True))
        if i < 3:
            o.append(L(x + 82, 53, nodes[i + 1][1], 53, LINE) + packet(x + 82, 53, nodes[i + 1][1], 53, c, 1.4, i * 0.5, 3))
    for i, m in enumerate(["KNN", "NB", "SVM"]):
        o.append(R(270 + i * 42, 90, 36, 20, 6, NODE, a, 1) + T(288 + i * 42, 104, m, 10, a, "middle", True))
    o.append(L(311, 72, 311, 90, LINE, 1))
    o.append(R(490, 22, 84, 84, 8, NODE, LINE) + T(532, 18, "matriz de confusão", 9, DIM, "middle", True))
    for i in range(4):
        d = i in (0, 3)
        o.append(R(498 + (i % 2) * 38, 30 + (i // 2) * 38, 34, 34, 4, GREEN if d else RED, extra=f'opacity="{0.55 if d else 0.22}"', inner=pulse("opacity", "0.25;0.7;0.25" if d else "0.1;0.3;0.1", 3, i * 0.3)))
    o.append(R(40, 120, 420, 20, 10, NODE, LINE) + T(250, 134, "POST /treinar · GET /prever   (API em container)", 10, DIM, "middle", True))
    return "".join(o)


def m_text(a):
    o = [T(60, 30, "texto bruto", 10, DIM, mono=True), T(250, 30, "tokens + stemming", 10, DIM, mono=True), T(470, 30, "vetor", 10, DIM, mono=True)]
    words = [("Os", None), ("candidatos", "candid"), ("debatendo", "debat"), ("ontem", "ont")]
    for i, (w, s) in enumerate(words):
        y = 52 + i * 24
        o.append(R(40, y - 13, 150, 20, 5, NODE, LINE) + T(52, y + 1, w, 12, MUTED, mono=True))
        o.append(L(190, y - 3, 238, y - 3, LINE, 1) + packet(190, y - 3, 238, y - 3, a, 1.5, i * 0.3, 2.5))
        if s:
            o.append(R(240, y - 13, 150, 20, 5, NODE, a, 1) + T(252, y + 1, s, 12, a, mono=True))
        else:
            o.append(R(240, y - 13, 150, 20, 5, NODE, LINE) + T(252, y + 1, w, 12, DIM, mono=True) + L(250, y - 3, 280, y - 3, RED, 1.5))
        h = [14, 38, 26, 44][i]
        o.append(R(430 + i * 30, 130 - h, 22, h, 4, [PURPLE, BLUE, TEAL, AMBER][i], extra='opacity="0.85"', inner=pulse("height", f"4;{h}", 2.6, i * 0.2) + pulse("y", f"126;{130-h}", 2.6, i * 0.2)))
    return "".join(o)


def m_prouni(a):
    o = [L(60, 126, 540, 126, LINE)]
    def bars(x0, label, v1, v2, cap):
        s = R(x0, 126 - v1, 56, v1, 5, BLUE, extra='opacity="0.9"', inner=pulse("height", f"{v1};{cap};{v1}", 5) + pulse("y", f"{126-v1};{126-cap};{126-v1}", 5))
        s += R(x0 + 72, 126 - v2, 56, v2, 5, a, extra='opacity="0.9"', inner=pulse("height", f"{v2};{cap};{v2}", 5) + pulse("y", f"{126-v2};{126-cap};{126-v2}", 5))
        return s
    o.append(bars(130, "", 100, 22, 60))
    o.append(T(194, 144, "classes desbalanceadas  →  reamostragem", 10, DIM, "middle", True, extra=""))
    o.append(f'<path d="M290 70 H330" stroke="{MUTED}" stroke-width="2" marker-end="url(#ah)"/>')
    for i, c in enumerate([BLUE, GREEN, AMBER, PINK]):
        o.append(R(370 + i * 44, 126 - 36 - i * 8, 34, 36 + i * 8, 5, c, extra='opacity="0.85"', inner=pulse("opacity", "0.5;1;0.5", 3, i * 0.3)))
    o.append(T(440, 144, "KNN · NB · SVM", 10, DIM, "middle", True))
    return "<defs><marker id=\"ah\" markerWidth=\"8\" markerHeight=\"7\" refX=\"7\" refY=\"3.5\" orient=\"auto\"><path d=\"M0 0 L8 3.5 L0 7 Z\" fill=\"" + MUTED + "\"/></marker></defs>" + "".join(o)


def m_vision(a, kind="tree", label="árvore"):
    o = [R(170, 8, 260, 134, 8, NODE, LINE)]
    if kind == "tree":
        o.append(f'<rect x="293" y="100" width="14" height="30" fill="#7c4a1e"/>' + C(300, 70, 30, "#166534") + C(278, 88, 20, "#15803d") + C(322, 88, 20, "#15803d"))
        box = (255, 36, 90, 96)
    else:
        o.append(C(300, 44, 12, "#475569") + f'<path d="M280 124 Q280 66 300 66 Q320 66 320 124 Z" fill="#475569"/>' + L(300, 66, 300, 124, "#334155", 1))
        box = (268, 26, 64, 102)
    x, y, w, h = box
    o.append(f'<g opacity="0">{loop("0;0;1;1;0","0;0.3;0.38;0.9;1",4)}' + R(x, y, w, h, 4, "none", a, 2) + R(x, y - 16, 70, 15, 3, a) + T(x + 6, y - 5, label, 10, "#04110f", mono=True, weight=700) + '</g>')
    o.append(R(172, 8, 256, 3, 1, a, extra='opacity="0.8"', inner=pulse("y", "10;138;10", 4)))
    return "".join(o)


def m_course(a):
    o = []
    for i, (code, c) in enumerate([("import pandas as pd", BLUE), ("df.describe()", TEAL), ("KNeighborsClassifier().fit(X, y)", a)]):
        y = 12 + i * 44
        o.append(R(110, y, 380, 36, 6, NODE, c, 1.2, inner=pulse("stroke-opacity", "0.25;1;0.25", 4.5, i * 1.4)))
        o.append(T(124, y + 15, f"In [{i+1}]:", 10, DIM, mono=True) + T(180, y + 15, code, 11, c, mono=True))
        o.append(R(180, y + 22, 180 if i == 2 else 120, 5, 2, MUTED, extra='opacity="0.4"'))
    return "".join(o)


def m_sensors(a):
    pts = [(120, 40), (210, 100), (300, 30), (390, 96), (480, 42), (160, 112), (440, 120), (300, 110)]
    o = []
    for i, (x, y) in enumerate(pts):
        o.append(C(x, y, 34, a, 'opacity="0"', f'<animate attributeName="opacity" values="0;0.12;0" dur="3s" begin="{i*0.35}s" repeatCount="indefinite"/>'))
        o.append(L(x, y, 300, 76, LINE, 1, 'stroke-dasharray="2 4"'))
    for i, (x, y) in enumerate(pts):
        c = a if i != 4 else RED
        o.append(C(x, y, 5, c, inner=pulse("opacity", "1;0.35;1", 2.2, i * 0.3)))
    o.append(C(300, 76, 11, NODE, f'stroke="{AMBER}" stroke-width="2.4"') + T(300, 80, "S", 11, AMBER, "middle", True, 700))
    o.append(f'<g>' + T(480, 62, "falha", 9, RED, "middle", True) + '</g>')
    return "".join(o)


def m_parallel(a):
    o = [T(30, 28, "thread", 10, DIM, mono=True)]
    for i in range(4):
        y = 22 + i * 28
        o.append(R(90, y, 420, 18, 4, "#0b1220", LINE))
        w = 120 + (i * 53) % 130
        o.append(R(90, y, w, 18, 4, [BLUE, TEAL, a, AMBER][i], extra='opacity="0.8"', inner=pulse("width", f"0;{w};{w};0", 4.5, i * 0.25)))
        o.append(T(70, y + 13, f"t{i}", 10, MUTED, "end", True))
    o.append(R(90, 132, 420, 4, 2, GREEN, extra='opacity="0.7"', inner=pulse("width", "0;420;420;0", 4.5)))
    o.append(T(300, 148, "join: soma parcial → resultado", 10, GREEN, "middle", True))
    return "".join(o)


def m_graph(a):
    nodes = [(80, 108), (170, 40), (200, 112), (300, 70), (390, 28), (410, 118), (510, 70)]
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (1, 4)]
    o = [L(*nodes[x], *nodes[y], LINE, 1.5) if False else L(nodes[x][0], nodes[x][1], nodes[y][0], nodes[y][1], LINE, 1.5) for x, y in edges]
    path = [0, 2, 3, 5, 6]
    d = "M" + " L".join(f"{nodes[i][0]},{nodes[i][1]}" for i in path)
    o.append(f'<path d="{d}" fill="none" stroke="{a}" stroke-width="3" stroke-linecap="round" stroke-dasharray="520" stroke-dashoffset="520">'
             f'<animate attributeName="stroke-dashoffset" values="520;0;0;520" keyTimes="0;0.45;0.9;1" dur="5s" repeatCount="indefinite"/></path>')
    for i, (x, y) in enumerate(nodes):
        on = i in path
        o.append(C(x, y, 9, NODE, f'stroke="{a if on else MUTED}" stroke-width="2"'))
    o.append(T(80, 132, "origem", 10, a, "middle", True) + T(510, 92, "profissional", 10, a, "middle", True))
    return "".join(o)


def m_code(a):
    o = []
    for r in range(4):
        for c in range(14):
            k = r * 14 + c
            on = (k * 7) % 5 != 0
            col = GREEN if on else LINE
            o.append(R(60 + c * 33, 18 + r * 30, 26, 22, 4, col, extra=f'opacity="{0.25 if on else 1}"',
                       inner=(pulse("opacity", "0.15;0.9;0.45", 6, (k % 14) * 0.08 + r * 0.2) if on else "")))
    o.append(T(300, 146, "AC · AC · AC · WA · AC …", 10, DIM, "middle", True))
    return "".join(o)


def m_agentloop(a):
    cx, cy, r = 300, 76, 50
    o = [C(cx, cy, r, "none", f'stroke="{LINE}" stroke-width="2"')]
    pts = [("pensa", -90, a), ("ferramenta", 30, AMBER), ("resposta", 150, GREEN)]
    for n, ang, c in pts:
        x, y = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
        o.append(R(x - 42, y - 13, 84, 26, 13, NODE, c, 1.6) + T(x, y + 4, n, 11, c, "middle", True))
    o.append(C(cx + r, cy, 5, a, inner=f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="4s" repeatCount="indefinite"/>'))
    for i, s in enumerate(["skills", "hooks", "memória"]):
        o.append(R(40 + i * 0, 28 + i * 34, 76, 22, 11, NODE, LINE) + T(78, 43 + i * 34, s, 10, MUTED, "middle", True))
    for i, s in enumerate(["AWS", "eval", "deploy"]):
        o.append(R(484, 28 + i * 34, 76, 22, 11, NODE, LINE) + T(522, 43 + i * 34, s, 10, MUTED, "middle", True))
    return "".join(o)


MOTIFS = {
    "agents": m_agents, "avatar": m_avatar, "panel": m_panel, "hooks": m_hooks, "satellite": m_satellite,
    "gateway": m_gateway, "observ": m_observ, "login": m_login, "dynamo": m_dynamo, "sentiment": m_sentiment,
    "mlaas": m_mlaas, "text": m_text, "prouni": m_prouni, "course": m_course, "sensors": m_sensors,
    "parallel": m_parallel, "graph": m_graph, "code": m_code, "agentloop": m_agentloop,
    "tree": lambda a: m_vision(a, "tree", "árvore 0.94"), "person": lambda a: m_vision(a, "person", "pessoa 0.88"),
}

# ------------------------------------------------------------------ card
W, H, IH = 600, 340, 150


def year_of(name):
    if not STATS:
        return ""
    for acc in STATS.values():
        for r in acc["repos"]:
            if r["name"] == name:
                return r["created_at"][:4]
    return ""


def card(slug, repo, desc, tags, accent, motif, lang, order=0):
    uid = slug.replace("_", "-")
    lines = textwrap.wrap(desc, 66)[:4]
    year = year_of(repo.split("/")[1])
    lc = LANG_COLOR.get(lang, MUTED)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}" role="img" '
         f'aria-label="{esc(repo)}: {esc(desc)}">',
         f'<defs><linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{accent}" stop-opacity="0.16"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="cl{uid}"><rect width="{W}" height="{IH}" rx="14"/></clipPath>'
         f'<pattern id="dt{uid}" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="{LINE}"/></pattern></defs>',
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{CARD}" stroke="{LINE}"/>',
         f'<g opacity="0">{fade(0.05 + order*0.1, 0.5)}',
         f'<g clip-path="url(#cl{uid})"><rect width="{W}" height="{IH}" fill="{NODE}"/><rect width="{W}" height="{IH}" fill="url(#dt{uid})" opacity="0.7"/><rect width="{W}" height="{IH}" fill="url(#bg{uid})"/>',
         f'<g>{MOTIFS[motif](accent)}</g></g>',
         f'<path d="M0 {IH} H{W}" stroke="{LINE}"/>',
         T(24, IH + 34, repo, 18, TXT, weight=700),
         ]
    for i, ln in enumerate(lines):
        p.append(T(24, IH + 62 + i * 20, ln, 13.5, MUTED))
    # chips
    x = 24
    for t in tags[:4]:
        w = len(t) * 6.9 + 22
        p.append(R(x, H - 56, w, 22, 11, "none", LINE) + T(x + w / 2, H - 41, t, 11, accent, "middle", True))
        x += w + 8
    p.append(L(24, H - 30, W - 24, H - 30, LINE, 1))
    p.append(C(32, H - 14, 5, lc) + T(44, H - 10, lang, 11.5, MUTED) + (T(W - 24, H - 10, year, 11.5, DIM, "end", True) if year else ""))
    p.append('</g></svg>')
    (OUT / "cards" / f"{slug}.svg").write_text("\n".join(p), encoding="utf-8")


# ------------------------------------------------------------------ títulos de seção
def section(slug, num, title, sub, accent, count):
    W2, H2 = 1200, 96
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" font-family="{SANS}" role="img" aria-label="{num} — {esc(title)}">',
         f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient></defs>',
         f'<rect width="{W2}" height="{H2}" rx="14" fill="{BG}"/>',
         f'<g opacity="0">{fade(0.1)}' + T(40, 60, num, 30, accent, mono=True, weight=700) + '</g>',
         f'<g opacity="0">{fade(0.3)}' + T(104, 52, title, 30, TXT, weight=700) + T(104, 76, sub, 14, MUTED) + '</g>',
         f'<g opacity="0">{fade(0.6)}' + R(W2 - 40 - 150, 30, 150, 34, 17, "none", accent, 1.2) + T(W2 - 40 - 75, 52, count, 13, accent, "middle", True) + '</g>',
         f'<rect x="0" y="{H2-4}" width="0" height="3" rx="1.5" fill="url(#g)"><animate attributeName="width" to="{W2}" begin="0.3s" dur="1.2s" fill="freeze"/></rect>',
         f'<circle cx="0" cy="{H2-2.5}" r="4" fill="{accent}" opacity="0"><animate attributeName="cx" values="0;{W2}" dur="4s" begin="1.5s" repeatCount="indefinite"/>'
         f'<animate attributeName="opacity" values="0;1;1;0" dur="4s" begin="1.5s" repeatCount="indefinite"/></circle>',
         '</svg>']
    (OUT / "sections" / f"{slug}.svg").write_text("\n".join(p), encoding="utf-8")


# ------------------------------------------------------------------ conteúdo
CARDS = {
    "01-destaques": [
        ("guilda", "allankltsn/guilda", "Time de engenharia de IA para Claude Code e Codex, instalado com um comando: 28 papéis, 10 perfis e um agente gestor que escreve histórias, escolhe especialistas e cobra evidências.", ["Claude Code", "Codex", "multiagente"], TEAL, "agents", "Python"),
        ("genai-libras", "allankltsn/genai-libras-translations", "Prova de conceito: fala ou texto vira glosas de Libras, que viram sinais num avatar 3D (VRM). API em FastAPI com LLM. Sinais ainda não validados por intérpretes.", ["FastAPI", "LLM", "three.js · VRM"], PURPLE, "avatar", "TypeScript"),
        ("group-tools", "allankltsn/vscode-grouped-tools-extension", "Extensão do VS Code que reúne os painéis de outras extensões num só lugar: busca, grupos coloridos, favoritos por workspace e fixação na barra de status.", ["VS Code API", "demo ao vivo"], BLUE, "panel", "JavaScript"),
        ("setup-kiro", "allankltsn/setup_kiro", "Kit de hooks, steering e skills do Kiro com postura de arquiteto sênior: lint ao salvar, proteção da main, bloqueio de segredos no commit e commitlint.", ["Kiro", "hooks", "steering"], AMBER, "hooks", "HTML"),
        ("agno-study", "allankltsn/agno_study", "Estudo de agentes com Agno, da criação ao deploy na AWS, apoiado por skills do Agno (agentes básicos, AgentOS, avaliação, qualidade) e pelo kit setup_kiro.", ["Agno", "AWS", "skills"], GREEN, "agentloop", "Python"),
        ("vibecoder", "allankltsn/vibecoder-template", "Hub de desenvolvimento assistido por IA: cada projeto nasce como satélite e herda agentes, templates e workflows do hub.", ["Claude Code", "templates"], PINK, "satellite", "Python"),
    ],
    "02-backend-cloud": [
        ("apigateway-auth", "AllanKT/aws_apigateway_authenticator", "Autenticador no API Gateway que protege um serviço REST sem alterar o código dele, com contagem de acessos no DynamoDB.", ["API Gateway", "Lambda", "DynamoDB"], AMBER, "gateway", "Python"),
        ("fastapi-otel", "AllanKT/fastapi-observability-opentelemetry", "Os três pilares de observabilidade (logs, métricas e traces) de uma API FastAPI, reunidos no Grafana.", ["OpenTelemetry", "Grafana", "FastAPI"], TEAL, "observ", "Python"),
        ("cypress-mfa", "AllanKT/cypress_login_captcha_mfa", "Testes E2E de login em sistema com reCAPTCHA e MFA, cobrindo o fluxo completo de autenticação.", ["Cypress", "E2E", "MFA"], PINK, "login", "TypeScript"),
        ("python-dynamo", "AllanKT/python-dynamo", "Acesso ao DynamoDB em Python: modelagem de chaves e operações de leitura e escrita.", ["DynamoDB", "boto3"], BLUE, "dynamo", "Python"),
    ],
    "03-ml-nlp": [
        ("sentimental", "AllanKT/SentimentalClassifierPoliticosBrasil2018", "Coleta de tweets sobre os candidatos à Presidência em 2018 e classificação do sentimento de cada um com embeddings e rede neural.", ["Tweepy", "Word2Vec", "Keras"], GREEN, "sentiment", "Jupyter Notebook"),
        ("mlaas", "AllanKT/MachineLearningAsAService", "TCC: serviço em container que pré-processa dados, treina e avalia modelos e gera os gráficos de cada um.", ["KNN", "Naive Bayes", "SVM", "Docker"], AMBER, "mlaas", "Python"),
        ("text-mining", "AllanKT/Text-Mining-and-NLP", "Pipeline de mineração de texto: limpeza, stemming e vetorização de documentos.", ["NLTK", "TextBlob", "scikit-learn"], PURPLE, "text", "Jupyter Notebook"),
        ("prouni", "AllanKT/Prouni-Data-Classification", "Classificação sobre os dados abertos do Prouni 2016, com reamostragem para classes desbalanceadas.", ["KNN", "NB", "SVM"], BLUE, "prouni", "Jupyter Notebook"),
        ("alpharead", "AllanKT/AlphaReadMicroservice", "Microsserviço de classificação de imagens para o aplicativo Android AlphaRead.", ["visão computacional", "Python"], TEAL, "tree", "Python"),
        ("human-classifier", "AllanKT/HumanClassifier", "Detecção de pessoas em imagens com descritor HOG e SVM.", ["OpenCV", "HOG", "imutils"], PINK, "person", "Jupyter Notebook"),
        ("curso-ml", "AllanKT/CursoMachineLearning", "Material de curso em aulas: Python, NumPy, Pandas, Matplotlib e os principais classificadores, com exercícios.", ["KNN", "SVM", "árvores"], AMBER, "course", "Jupyter Notebook"),
    ],
    "04-fundamentos": [
        ("genetic", "AllanKT/Algoritimo_Genetico", "Iniciação científica: simulador que posiciona nós de uma rede de sensores sem fio com heurística, otimizando cobertura.", ["C++", "heurística", "RSSF"], GREEN, "sensors", "C++"),
        ("parallel", "AllanKT/Programacao-Paralela", "Integrais numéricas, crivo de primos e soma de vetores em C paralelo, executados num ambiente Docker.", ["C", "paralelismo", "Docker"], BLUE, "parallel", "C"),
        ("graph", "AllanKT/Graph-Project-Finder", "Grafo de profissionais com geolocalização: acha o mais próximo disponível para cada função por menor caminho.", ["Python", "grafos", "Dijkstra"], PURPLE, "graph", "Python"),
        ("competitive", "AllanKT/competitive_programming", "Mais de 100 problemas resolvidos no URI, Codeforces e CodCad, em C, C++ e Python.", ["C++", "algoritmos"], AMBER, "code", "C++"),
    ],
}
SECTIONS = {
    "01-destaques": ("05", "Projetos em destaque", "IA aplicada, agentes e ferramentas de desenvolvimento · conta @allankltsn", TEAL),
    "02-backend-cloud": ("06", "Back-end e cloud", "APIs, AWS, observabilidade e testes · conta @AllanKT", BLUE),
    "03-ml-nlp": ("07", "Laboratório de ML e NLP", "Estudos e pesquisas de 2018 a 2022 · conta @AllanKT", GREEN),
    "04-fundamentos": ("08", "Fundamentos de computação", "Algoritmos, paralelismo e grafos · conta @AllanKT", AMBER),
}

for key, items in CARDS.items():
    num, title, sub, acc = SECTIONS[key]
    section(key, num, title, sub, acc, f"{len(items)} repositórios")
    for i, (slug, repo, desc, tags, accent, motif, lang) in enumerate(items):
        card(slug, repo, desc, tags, accent, motif, lang, i)
    print("ok", key, len(items))


# ------------------------------------------------------------------ Código em números
def numbers():
    if not STATS:
        return
    repos = [dict(r, acc=u) for u, d in STATS.items() for r in d["repos"]]
    n = len(repos)
    langs = Counter(r["language"] for r in repos if r["language"])
    years = Counter(r["created_at"][:4] for r in repos)
    stars = sum(r["stargazers_count"] for r in repos)
    since = min(years)
    W2, H2 = 1200, 470
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" font-family="{SANS}" role="img" '
         f'aria-label="Código em números: {n} repositórios próprios em duas contas desde {since}, {len(langs)} linguagens principais">',
         f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient></defs>',
         f'<rect width="{W2}" height="{H2}" rx="14" fill="{BG}"/>']
    # tiles
    tiles = [(str(n), "repositórios próprios", TEAL), (str(len(langs)), "linguagens principais", BLUE),
             (since, "ano do primeiro repositório", PURPLE), ("2", "contas: @allankltsn e @AllanKT", AMBER)]
    for i, (v, l, c) in enumerate(tiles):
        x = 40 + i * 286
        p.append(f'<g opacity="0">{fade(0.1+i*0.15)}' + R(x, 30, 268, 92, 12, CARD, LINE) + R(x, 30, 4, 92, 2, c)
                 + T(x + 24, 84, v, 44, TXT, weight=700) + T(x + 24, 108, l, 13, MUTED) + '</g>')
    # linguagens (barras horizontais por nº de repos)
    top = langs.most_common(7)
    mx = top[0][1]
    p.append(f'<g opacity="0">{fade(0.7)}' + T(40, 166, "Linguagem principal por repositório", 14, TXT, weight=600) + '</g>')
    for i, (lg, v) in enumerate(top):
        y = 186 + i * 36
        c = LANG_COLOR.get(lg, MUTED)
        wmax = 400
        p.append(f'<g opacity="0">{fade(0.8+i*0.1,0.4)}' + T(40, y + 16, lg, 13, MUTED) + R(180, y + 2, wmax, 16, 8, "#0b1220", LINE) + '</g>')
        p.append(R(180, y + 2, 0, 16, 8, c, inner=f'<animate attributeName="width" to="{wmax*v/mx:.0f}" begin="{1.0+i*0.12}s" dur="0.9s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0 0.2 1"/>'))
        p.append(f'<g opacity="0">{fade(1.5+i*0.12,0.4)}' + T(190 + wmax * v / mx + 0, y + 16, str(v), 12, TXT, mono=True) + '</g>')
    # repositórios criados por ano
    ys = sorted(years)
    x0, base, bh = 660, 400, 190
    pk = max(years.values())
    p.append(f'<g opacity="0">{fade(0.7)}' + T(x0, 166, "Repositórios criados por ano", 14, TXT, weight=600) + '</g>')
    p.append(L(x0, base, 1160, base, LINE))
    bw = min(40, 480 / len(ys) - 14)
    gap = 480 / len(ys)
    for i, y in enumerate(ys):
        v = years[y]
        h = bh * v / pk
        x = x0 + i * gap + (gap - bw) / 2
        col = TEAL if y == max(ys) else (BLUE if int(y) >= 2024 else PURPLE)
        p.append(R(f"{x:.0f}", base, bw, 0, 5, col, extra='opacity="0.9"', inner=f'<animate attributeName="height" to="{h:.0f}" begin="{1.0+i*0.1}s" dur="0.8s" fill="freeze"/><animate attributeName="y" to="{base-h:.0f}" begin="{1.0+i*0.1}s" dur="0.8s" fill="freeze"/>'))
        p.append(f'<g opacity="0">{fade(1.6+i*0.1,0.4)}' + T(f"{x+bw/2:.0f}", f"{base-h-8:.0f}", str(v), 12, TXT, "middle", True) + '</g>')
        p.append(T(f"{x+bw/2:.0f}", base + 20, y, 12, MUTED, "middle", True))
    p.append(f'<g opacity="0">{fade(2.2)}' + T(40, H2 - 22, "Fonte: API pública do GitHub, repositórios próprios (sem forks) das duas contas. Linguagem por repositório, não por bytes, para não contar bibliotecas versionadas.", 11.5, DIM) + '</g>')
    p.append('</svg>')
    (OUT / "sections" / "05-numeros.svg").write_text("\n".join(p), encoding="utf-8")
    section("05-numeros-titulo", "02", "Código em números", "Panorama dos repositórios das duas contas", BLUE, f"{n} repositórios")
    print("ok numbers", n, dict(langs), dict(years), "stars", stars)


numbers()

section("00-fluxo", "04", "Como trabalho com agentes de IA", "Spec-driven e multiagente, do pedido à entrega", PINK, "6 etapas")
section("06-stack", "01", "Stack", "Ferramentas do dia a dia, agrupadas por área", TEAL, "7 áreas")
section("07-trajetoria", "03", "Trajetória", "De 2018 até hoje: pesquisa, liderança técnica e IA aplicada", PURPLE, "2018 → 2026")
