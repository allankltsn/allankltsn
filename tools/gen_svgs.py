"""Gera os SVGs animados do README de perfil (allankltsn)."""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BG, CARD, LINE = "#0b0f17", "#111827", "#1f2937"
TXT, MUTED = "#e6edf3", "#8b96a8"
TEAL, BLUE, PURPLE = "#2dd4bf", "#60a5fa", "#a78bfa"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fade(begin, dur=0.5):
    return f'<animate attributeName="opacity" to="1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1200, 296
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'font-family="{SANS}" role="img" aria-label="Allan Kleitson Teotonio, engenheiro de software sênior: IA aplicada, cloud e back-end">')
    p.append('<defs>'
             f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
             f'<radialGradient id="glow"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.9"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>'
             '<clipPath id="sub"><rect x="64" y="150" width="0" height="34"><animate attributeName="width" values="0;660" keyTimes="0;1" begin="1.0s" dur="1.1s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.2 1"/></rect></clipPath>'
             '</defs>')
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')

    # fundo: pequena rede neural esmaecida
    nodes = [(560, 40), (620, 70), (600, 120), (680, 40), (700, 100), (650, 150), (740, 60)]
    edges = [(0, 1), (1, 2), (1, 3), (3, 4), (2, 5), (4, 5), (4, 6), (3, 6)]
    p.append('<g opacity="0.35">')
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LINE}" stroke-width="1"/>')
    for i, (x, y) in enumerate(nodes):
        p.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{TEAL}"><animate attributeName="opacity" values="0.2;1;0.2" dur="3s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/></circle>')
    p.append('</g>')

    p.append(f'<g stroke="{LINE}" stroke-width="1"><path d="M0 266 H{W}"/></g>')
    # brilho percorrendo a linha de base
    p.append(f'<ellipse cx="-80" cy="266" rx="80" ry="2" fill="url(#glow)"><animate attributeName="cx" values="-80;{W+80}" dur="6s" repeatCount="indefinite"/></ellipse>')

    p.append(f'<rect x="64" y="56" width="0" height="4" rx="2" fill="url(#g)"><animate attributeName="width" to="120" begin="0.2s" dur="0.6s" fill="freeze"/></rect>')
    p.append(f'<text x="64" y="118" font-size="46" font-weight="700" fill="{TXT}" letter-spacing="-1" opacity="0">Allan Kleitson Teotonio{fade(0.4)}</text>')
    p.append(f'<g clip-path="url(#sub)"><text x="64" y="173" font-size="19" fill="{MUTED}">'
             f'<tspan>Engenheiro de Software Sênior</tspan> <tspan fill="{TEAL}" font-weight="600">· IA aplicada · Cloud · Back-end</tspan></text></g>')

    chips = [("Python", None), ("Agno", None), ("LangChain", None), ("Amazon Bedrock", None),
             ("AWS", None), ("Terraform", None), ("8+ anos", TEAL)]
    x, t = 64.0, 2.1
    p.append(f'<g font-family="{MONO}" font-size="12.5" fill="{MUTED}">')
    for label, accent in chips:
        w = len(label) * 7.6 + (40 if accent else 26)
        stroke = accent or LINE
        op = "0.6" if accent else "1"
        dot = f'<circle cx="{x+15:.1f}" cy="219" r="3.5" fill="{accent}"/>' if accent else ""
        tx = x + w / 2 + (7 if accent else 0)
        p.append(f'<g opacity="0">{fade(round(t,1),0.4)}<rect x="{x:.1f}" y="206" width="{w:.1f}" height="26" rx="13" fill="none" stroke="{stroke}" stroke-opacity="{op}"/>{dot}'
                 f'<text x="{tx:.1f}" y="223" text-anchor="middle">{esc(label)}</text></g>')
        x += w + 10
        t += 0.15
    p.append('</g>')

    # terminal à direita
    cx, cy, cw, ch = 776, 44, 380, 212
    p.append(f'<g opacity="0">{fade(0.6)}<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="{CARD}" stroke="{LINE}"/>'
             f'<circle cx="{cx+20}" cy="{cy+20}" r="5" fill="#ff5f57"/><circle cx="{cx+36}" cy="{cy+20}" r="5" fill="#febc2e"/><circle cx="{cx+52}" cy="{cy+20}" r="5" fill="#28c840"/>'
             f'<text x="{cx+cw-16}" y="{cy+24}" font-family="{MONO}" font-size="11" fill="{MUTED}" text-anchor="end">~/allankltsn</text>'
             f'<path d="M{cx} {cy+38} H{cx+cw}" stroke="{LINE}"/></g>')
    lines = [
        ("$ ", "whoami", TXT),
        ("> ", "dev sênior · back-end Python + AWS", MUTED),
        ("$ ", "cat foco.txt", TXT),
        ("> ", "agentes autônomos · RAG · EDA · IaC", TEAL),
        ("$ ", "git log --reverse | head -1", TXT),
        ("> ", "2018: visão computacional e NLP", BLUE),
    ]
    t = 1.2
    y = cy + 64
    cps = 0.035  # segundos por caractere
    for i, (pre, body, color) in enumerate(lines):
        full = pre + body
        width = len(full) * 7.8 + 4
        dur = max(0.25, len(full) * cps) if pre == "$ " else 0.35
        cid = f"l{i}"
        p.append(f'<clipPath id="{cid}"><rect x="{cx+18}" y="{y-14}" width="0" height="20">'
                 f'<animate attributeName="width" to="{width:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
        pcol = TEAL if pre == "$ " else MUTED
        p.append(f'<text x="{cx+18}" y="{y}" font-family="{MONO}" font-size="13" clip-path="url(#{cid})">'
                 f'<tspan fill="{pcol}">{esc(pre)}</tspan><tspan fill="{color}">{esc(body)}</tspan></text>')
        t += dur + (0.35 if pre == "$ " else 0.25)
        y += 26
    # cursor piscando
    p.append(f'<rect x="{cx+18}" y="{y-13}" width="8" height="16" fill="{TEAL}" opacity="0">'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.5;0.51" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>')
    p.append('</svg>')
    return "\n".join(p)


# ---------------------------------------------------------------- fluxo com agentes
def flow():
    W, H = 1200, 250
    steps = [
        ("História", "critério de aceite"),
        ("Spec", "o quê e por quê"),
        ("Plano", "passos e riscos"),
        ("Especialistas", "modelo por custo"),
        ("Revisão", "gates independentes"),
        ("Entrega", "com evidências"),
    ]
    n = len(steps)
    bw, bh, y0 = 156, 64, 92
    left = 54
    gap = (W - 2 * left - bw) / (n - 1)
    xs = [left + i * gap for i in range(n)]
    cy = y0 + bh / 2
    start, end = xs[0] + bw / 2, xs[-1] + bw / 2
    travel, cycle = 6.0, 7.5

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}" role="img" '
         f'aria-label="Fluxo de trabalho com agentes de IA: história, spec, plano, especialistas, revisão e entrega">']
    p.append(f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient></defs>')
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
    p.append(f'<text x="{left}" y="50" font-size="13" font-family="{MONO}" fill="{TEAL}" letter-spacing="2">SPEC-DRIVEN · MULTIAGENTE</text>')
    p.append(f'<text x="{W-left}" y="50" font-size="13" font-family="{MONO}" fill="{MUTED}" text-anchor="end">Claude Code · Codex · Kiro</text>')
    # trilho
    p.append(f'<path d="M{start} {cy} H{end}" stroke="{LINE}" stroke-width="2"/>')
    p.append(f'<path d="M{start} {cy} H{end}" stroke="url(#g)" stroke-width="2" stroke-dasharray="{end-start}" stroke-dashoffset="{end-start}">'
             f'<animate attributeName="stroke-dashoffset" values="{end-start};0;0;{end-start}" keyTimes="0;{travel/cycle:.3f};0.97;1" dur="{cycle}s" repeatCount="indefinite"/></path>')

    for i, ((title, cap), x) in enumerate(zip(steps, xs)):
        a = (x + bw / 2 - start) / (end - start) * travel / cycle
        k = [0, max(a - 0.001, 0), a + 0.02, min(a + 0.16, 0.985), min(a + 0.2, 0.99), 1]
        if k[1] == 0:
            k[1] = 0.0001
        kt = ";".join(f"{v:.4f}" for v in k)
        dim, hot = LINE, TEAL
        anim = (f'<animate attributeName="stroke" values="{dim};{dim};{hot};{hot};{dim};{dim}" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/>')
        p.append(f'<g opacity="0">{fade(0.2 + i*0.15, 0.4)}')
        p.append(f'<rect x="{x:.1f}" y="{y0}" width="{bw}" height="{bh}" rx="12" fill="{CARD}" stroke="{dim}" stroke-width="1.5">{anim}</rect>')
        p.append(f'<text x="{x+16:.1f}" y="{y0+26}" font-family="{MONO}" font-size="11" fill="{MUTED}">0{i+1}</text>')
        p.append(f'<text x="{x+16:.1f}" y="{y0+47}" font-size="17" font-weight="600" fill="{TXT}">{esc(title)}</text>')
        if title == "Especialistas":
            for j, col in enumerate((TEAL, BLUE, PURPLE)):
                p.append(f'<circle cx="{x+bw-36+j*10:.1f}" cy="{y0+22}" r="3.5" fill="{col}"><animate attributeName="r" values="3.5;5;3.5" dur="1.6s" begin="{j*0.3:.1f}s" repeatCount="indefinite"/></circle>')
        p.append(f'<text x="{x+bw/2:.1f}" y="{y0+bh+30}" font-size="13" fill="{MUTED}" text-anchor="middle">{esc(cap)}</text>')
        p.append('</g>')

    # pulso que percorre o trilho
    p.append(f'<circle cx="{start}" cy="{cy}" r="6" fill="{TEAL}" opacity="0">'
             f'<animate attributeName="cx" values="{start};{end};{end}" keyTimes="0;{travel/cycle:.3f};1" dur="{cycle}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.03;{travel/cycle-0.02:.3f};{travel/cycle+0.03:.3f};1" dur="{cycle}s" repeatCount="indefinite"/></circle>')
    p.append('</svg>')
    return "\n".join(p)


# ---------------------------------------------------------------- linha do tempo
def timeline():
    W, H = 1200, 380
    items = [
        ("2018", "Iniciação científica", "IA para comportamento humano", "e simulação de redes de sensores"),
        ("2018", "Estágio · Stefanini", "ML e deep learning: rosto,", "NLP, sentimento e chatbots"),
        ("2019", "Prêmio destaque IC", "reconhecimento facial em", "vídeo (CNPq · UnB)"),
        ("2020", "Bacharel em CC", "TCC: Machine Learning", "as a Service"),
        ("2021", "Líder técnico", "marketplace de consórcio,", "EDA e Terraform"),
        ("2021–2024", "ISH Tech / SafeLabs", "Digital Risk Protection: crawlers", "na surface, deep e dark web"),
        ("2024–hoje", "NuageIT", "agentes com Agno, LangChain", "e Bedrock · anti-spoofing"),
        ("2026", "Pós em IA aplicada", "engenharia de IA", "(em andamento)"),
    ]
    n = len(items)
    left, right, ay = 140, 1060, 196
    gap = (right - left) / (n - 1)
    grow = 3.2
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}" role="img" '
         f'aria-label="Linha do tempo de 2018 a 2026: pesquisa em IA, estágio, prêmio de iniciação científica, TCC, liderança técnica, ISH Tech, NuageIT e pós em IA aplicada">']
    p.append(f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{PURPLE}"/><stop offset="0.5" stop-color="{BLUE}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient></defs>')
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
    p.append(f'<path d="M{left} {ay} H{right}" stroke="{LINE}" stroke-width="2"/>')
    p.append(f'<path d="M{left} {ay} H{right}" stroke="url(#g)" stroke-width="3" stroke-linecap="round" stroke-dasharray="{right-left}" stroke-dashoffset="{right-left}">'
             f'<animate attributeName="stroke-dashoffset" to="0" begin="0.3s" dur="{grow}s" fill="freeze"/></path>')
    for i, (year, title, l1, l2) in enumerate(items):
        x = left + i * gap
        t = 0.3 + grow * i / (n - 1)
        up = i % 2 == 0
        last = i == n - 1
        col = TEAL if last else (BLUE if i >= 4 else PURPLE)
        stem_y2 = ay - 34 if up else ay + 34
        p.append(f'<g opacity="0">{fade(round(t,2), 0.35)}')
        p.append(f'<path d="M{x:.1f} {ay} V{stem_y2}" stroke="{LINE}" stroke-dasharray="3 3"/>')
        p.append(f'<circle cx="{x:.1f}" cy="{ay}" r="7" fill="{BG}" stroke="{col}" stroke-width="2.5"/>')
        p.append(f'<circle cx="{x:.1f}" cy="{ay}" r="3" fill="{col}"/>')
        if up:
            ys = (ay - 128, ay - 104, ay - 82, ay - 63)
        else:
            ys = (ay + 66, ay + 90, ay + 112, ay + 131)
        p.append(f'<text x="{x:.1f}" y="{ys[0]}" font-family="{MONO}" font-size="13" fill="{col}" text-anchor="middle">{year}</text>')
        p.append(f'<text x="{x:.1f}" y="{ys[1]}" font-size="15" font-weight="600" fill="{TXT}" text-anchor="middle">{esc(title)}</text>')
        p.append(f'<text x="{x:.1f}" y="{ys[2]}" font-size="12.5" fill="{MUTED}" text-anchor="middle">{esc(l1)}</text>')
        p.append(f'<text x="{x:.1f}" y="{ys[3]}" font-size="12.5" fill="{MUTED}" text-anchor="middle">{esc(l2)}</text>')
        p.append('</g>')
        if last:
            p.append(f'<circle cx="{x:.1f}" cy="{ay}" r="7" fill="none" stroke="{TEAL}" stroke-width="2" opacity="0">'
                     f'<animate attributeName="r" values="7;20" dur="1.8s" begin="{t+0.4:.2f}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0.8;0" dur="1.8s" begin="{t+0.4:.2f}s" repeatCount="indefinite"/></circle>')
    p.append('</svg>')
    return "\n".join(p)


for name, fn in (("hero.svg", hero), ("agent-flow.svg", flow), ("timeline.svg", timeline)):
    (OUT / name).write_text(fn(), encoding="utf-8")
    print("ok", name)
