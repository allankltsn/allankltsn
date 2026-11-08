"""Gera os SVGs animados do README de perfil (allankltsn): hero, trajetória, stack
e o fluxo da guilda (seção 04).

Uso: python tools/gen_svgs.py assets
Só biblioteca padrão. Paleta em tools/palette.py; helpers em tools/svgkit.py.
Hover é CSS puro dentro de cada SVG (vale ao abrir o arquivo sozinho; ver svgkit.py).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from svgkit import *  # noqa: E402,F401,F403

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1200, 296
    p = [svg_open(W, H, "Allan Kleitson Teotonio, engenheiro de software sênior: IA aplicada, cloud, back-end e agentes de IA multiagente",
                  defs=(f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{MINT}"/><stop offset="0.5" stop-color="{SKY}"/><stop offset="1" stop-color="{LAVENDER}"/></linearGradient>'
                        f'<radialGradient id="glow"><stop offset="0" stop-color="{PINK}" stop-opacity="0.9"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>'
                        f'<radialGradient id="b1"><stop offset="0" stop-color="{LAVENDER}" stop-opacity="0.28"/><stop offset="1" stop-color="{LAVENDER}" stop-opacity="0"/></radialGradient>'
                        f'<radialGradient id="b2"><stop offset="0" stop-color="{MINT}" stop-opacity="0.2"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></radialGradient>'
                        '<clipPath id="sub"><rect x="64" y="150" width="0" height="34"><animate attributeName="width" values="0;700" keyTimes="0;1" begin="1.0s" dur="1.2s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.2 1"/></rect></clipPath>'))]
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
    # manchas pastel que respiram
    p.append(f'<circle cx="180" cy="40" r="220" fill="url(#b1)"><animate attributeName="cx" values="180;260;180" dur="14s" repeatCount="indefinite"/></circle>')
    p.append(f'<circle cx="980" cy="250" r="240" fill="url(#b2)"><animate attributeName="cx" values="980;900;980" dur="16s" repeatCount="indefinite"/></circle>')
    # rede neural esmaecida atrás do nome
    nodes = [(560, 40), (620, 70), (600, 120), (680, 40), (700, 100), (650, 150), (740, 60)]
    edges = [(0, 1), (1, 2), (1, 3), (3, 4), (2, 5), (4, 5), (4, 6), (3, 6)]
    cols = [MINT, SKY, LAVENDER, PEACH, PINK, BUTTER, AQUA]
    p.append('<g opacity="0.45">')
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        p.append(L(x1, y1, x2, y2, LINE, 1))
    for i, (x, y) in enumerate(nodes):
        p.append(C(x, y, 3.5, cols[i], inner=f'<animate attributeName="opacity" values="0.25;1;0.25" dur="3s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/>'))
    p.append('</g>')
    p.append(f'<path d="M0 266 H{W}" stroke="{LINE}" stroke-width="1"/>')
    p.append(f'<ellipse cx="-80" cy="266" rx="90" ry="2.5" fill="url(#glow)"><animate attributeName="cx" values="-80;{W+80}" dur="6s" repeatCount="indefinite"/></ellipse>')
    p.append(f'<rect x="64" y="56" width="0" height="4" rx="2" fill="url(#g)"><animate attributeName="width" to="120" begin="0.2s" dur="0.6s" fill="freeze"/></rect>')
    p.append(f'<text x="64" y="118" font-size="46" font-weight="700" fill="{TXT}" letter-spacing="-1" opacity="0">Allan Kleitson Teotonio{fade(0.4)}</text>')
    p.append(f'<g clip-path="url(#sub)"><text x="64" y="173" font-size="19" fill="{MUTED}">'
             f'<tspan>Engenheiro de Software Sênior</tspan> <tspan fill="{MINT}" font-weight="600">· IA aplicada · Cloud · Back-end</tspan></text></g>')
    chips = [[("Python", SKY), ("Agno", MINT), ("LangChain", LAVENDER), ("Amazon Bedrock", PEACH), ("AWS", BUTTER), ("Terraform", PINK)],
             [("multiagente", AQUA), ("RAG", MINT), ("8+ anos", CORAL)]]
    t = 2.1
    for row, ry in zip(chips, (196, 230)):
        x = 64.0
        for label, col in row:
            w = len(label) * 7.7 + 40
            p.append(f'<g opacity="0">{fade(round(t,1),0.4)}{R(f"{x:.1f}", ry, f"{w:.1f}", 26, 13, "none", col, 1.2)}{C(f"{x+15:.1f}", ry+13, 3.5, col)}'
                     f'{T(f"{x+w/2+6:.1f}", ry+17.5, label, 12.5, col, "middle", True)}</g>')
            x += w + 10
            t += 0.15
    # terminal
    cx, cy, cw, ch = 776, 44, 380, 212
    p.append(f'<g opacity="0">{fade(0.6)}{R(cx, cy, cw, ch, 12, CARD, LINE)}'
             f'{C(cx+20, cy+20, 5, CORAL)}{C(cx+36, cy+20, 5, BUTTER)}{C(cx+52, cy+20, 5, MINT)}'
             f'{T(cx+cw-16, cy+24, "~/allankltsn", 12, DIM, "end", True)}<path d="M{cx} {cy+38} H{cx+cw}" stroke="{LINE}"/></g>')
    lines = [("$ ", "whoami", TXT),
             ("> ", "dev sênior · back-end Python + AWS", MUTED),
             ("$ ", "cat foco.txt", TXT),
             ("> ", "agentes · multiagente · RAG · EDA · IaC", MINT),
             ("$ ", "git log --reverse | head -1", TXT),
             ("> ", "2018: reconhecimento facial e IA", SKY)]
    t, y, cps = 1.2, cy + 64, 0.035
    for i, (pre, body, color) in enumerate(lines):
        full = pre + body
        width = len(full) * 7.8 + 4
        dur = max(0.25, len(full) * cps) if pre == "$ " else 0.35
        p.append(f'<clipPath id="l{i}"><rect x="{cx+18}" y="{y-14}" width="0" height="20"><animate attributeName="width" to="{width:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
        pcol = PINK if pre == "$ " else MUTED
        p.append(f'<text x="{cx+18}" y="{y}" font-family="{MONO}" font-size="13" clip-path="url(#l{i})"><tspan fill="{pcol}">{esc(pre)}</tspan><tspan fill="{color}">{esc(body)}</tspan></text>')
        t += dur + (0.35 if pre == "$ " else 0.25)
        y += 26
    p.append(f'<rect x="{cx+18}" y="{y-13}" width="8" height="16" fill="{PINK}" opacity="0">'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.5;0.51" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>')
    p.append('</svg>')
    return "\n".join(p)


# ---------------------------------------------------------------- trajetória
# Como acrescentar uma conquista: adicione um dict em ITEMS. Campos:
#   when   texto da data exibida ("05/2018", "2018–2019", "em andamento")
#   sort   (ano, mês) para ordenar. Use o mês SÓ quando o currículo traz o mês; senão (ano, 0).
#          Desempate: a ordenação é estável, então itens com a mesma chave ficam na ordem desta lista,
#          e os de (ano, 0) vêm antes dos datados do mesmo ano (isso não afirma ordem real).
#          None = sem data: vai para o fim da linha do tempo, sem inventar data.
#   cat    formacao | pesquisa | carreira | projeto   (define lado e cor)
#   title  título curto (1 linha);  org  instituição/empresa (1 linha); ambos são medidos e truncados
#   detail texto que aparece no hover (frases curtas)
#   now    True para marcar "em andamento" (opcional)
# A altura do SVG cresce sozinha com o número de itens. Só use fatos do currículo.
CATS = {  # categoria: (rótulo, cor, lado)  lado L = formação e pesquisa, R = carreira e projetos
    "formacao": ("Formação", SKY, "L"),
    "pesquisa": ("Pesquisa", LAVENDER, "L"),
    "carreira": ("Carreira", MINT, "R"),
    "projeto": ("Projeto", PEACH, "R"),
}
ITEMS = [
    dict(when="06/2015", sort=(2015, 6), cat="formacao", title="Técnico em Redes de Computadores", org="IESB",
         detail="Formação técnica em redes de computadores, concluída em 06/2015."),
    dict(when="2018", sort=(2018, 0), cat="pesquisa", title="IC: reconfiguração de RSSF", org="IESB",
         detail="Iniciação científica: simulação de algoritmos de reconfiguração de Redes de Sensores Sem Fio."),
    dict(when="2018", sort=(2018, 0), cat="pesquisa", title="IC: comportamentos humanos com IA", org="CNPq",
         detail="Iniciação científica (CNPq): pesquisador em projeto de IA para identificação de comportamentos humanos."),
    dict(when="2018", sort=(2018, 0), cat="pesquisa", title="Artigo: Bengala Multissensorial", org="SENID, Passo Fundo",
         detail="Trabalho em coautoria publicado no Seminário Nacional de Inclusão Digital (SENID)."),
    dict(when="2018–2019", sort=(2018, 0), cat="pesquisa", title="IC: reconhecimento facial em vídeo", org="CNPq",
         detail="Algoritmo de Machine Learning para reconhecer e identificar pessoas em vídeo, em tempo real."),
    dict(when="05/2018", sort=(2018, 5), cat="carreira", title="Estagiário em Desenvolvimento", org="Stefanini",
         detail="ML e deep learning para reconhecimento facial, NLP, sentimento e chatbots. Containers com Kubernetes. Bancos SQL e NoSQL."),
    dict(when="2019", sort=(2019, 0), cat="pesquisa", title="Prêmio Destaque de IC", org="Universidade de Brasília",
         detail="Prêmio Destaque de Iniciação Científica pelo trabalho de reconhecimento facial em vídeo."),
    dict(when="05/2019", sort=(2019, 5), cat="carreira", title="Analista de Sistemas", org="Stefanini",
         detail="APIs REST e GraphQL em Node.js e Python, entregues como CaaS. Lambda com arquitetura orientada a eventos."),
    dict(when="06/2020", sort=(2020, 6), cat="formacao", title="Bacharel em Ciência da Computação", org="IESB",
         detail="TCC: Machine Learning as a Service, um serviço em container que treina e avalia modelos."),
    dict(when="05/2021", sort=(2021, 5), cat="carreira", title="Líder Técnico", org="Stefanini",
         detail="Marketplace de cotas de consórcio 100% digital, com arquitetura de eventos, Terraform e DevSecOps."),
    dict(when="11/2021–06/2024", sort=(2021, 11), cat="carreira", title="Desenvolvedor Sênior", org="ISH Tech / SafeLabs",
         detail="Refatoração completa de uma solução de Digital Risk Protection (surface, deep e dark web) com webcrawlers."),
    dict(when="06/2024–hoje", sort=(2024, 6), cat="carreira", title="Desenvolvedor Sênior", org="NuageIT", now=True,
         detail="Liderou autenticação de chamadas contra spoofing em telecom. Agentes com Agno, LangChain e Bedrock com RAG. Fluxo padronizado de codificação com agentes."),
    dict(when="11/2026", sort=(2026, 11), cat="projeto", title="guilda v2.0.0 publicada", org="allankltsn/guilda",
         detail="Time de engenharia de IA para Claude Code e Codex: 28 papéis, 10 perfis, 11 ações."),
    dict(when="em andamento", sort=None, cat="formacao", title="Pós em Engenharia de IA Aplicada", org="UNIPDS", now=True,
         detail="Pós-graduação em andamento, sem data de conclusão."),
]


def timeline():
    for d in ITEMS:
        assert d["cat"] in CATS, f"categoria desconhecida: {d['cat']}"
    items = sorted(ITEMS, key=lambda d: (d["sort"] is None, d["sort"] or (0, 0)))  # estável; sem data vai ao fim
    W = 1200
    top, step, spine = 120, 46, 600
    H = top + len(items) * step + 100
    n = len(items)
    css = (BASE_CSS + ".chart:hover .pt:not(:hover){opacity:.4}.pt:hover .hz{transform:scale(1.7)}"
           ".pt:hover .card{stroke-width:2.2}" + tip_rule("n", "tt", range(n)))
    p = [svg_open(W, H, "Linha do tempo de 2015 a 2026 em duas raias: formação e pesquisa à esquerda, carreira e projetos à direita; pós-graduação em andamento ao fim", css,
                  f'<linearGradient id="sp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY}"/><stop offset="0.5" stop-color="{LAVENDER}"/><stop offset="1" stop-color="{MINT}"/></linearGradient>')]
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
    # cabeçalho das raias e legenda
    p.append(T(spine - 64 - 440, 44, "FORMAÇÃO E PESQUISA", 12, MUTED, "start", True, extra='letter-spacing="2"'))
    p.append(T(spine + 64, 44, "CARREIRA E PROJETOS", 12, MUTED, "start", True, extra='letter-spacing="2"'))
    lx = 40
    for k, (lab, col, _) in CATS.items():
        p.append(C(lx + 6, 78, 6, col) + T(lx + 20, 82, lab, 12, MUTED))
        lx += 20 + len(lab) * 7 + 22
    p.append(T(W - 40, 82, "passe o mouse nos pontos para ver o detalhe", 12, DIM, "end"))
    y0 = top
    yend = top + (n - 1) * step
    ln = yend - y0 + 60
    p.append(L(spine, y0 - 20, spine, y0 - 20 + ln, LINE, 3, 'stroke-linecap="round"'))
    p.append(f'<path d="M{spine} {y0-20} V{y0-20+ln}" stroke="url(#sp)" stroke-width="3" stroke-linecap="round" stroke-dasharray="{ln}" stroke-dashoffset="{ln}">'
             f'<animate attributeName="stroke-dashoffset" to="0" begin="0.2s" dur="3.4s" fill="freeze"/></path>')
    # espaço para acrescentar: continuação pontilhada e nó fantasma
    p.append(f'<path d="M{spine} {y0-20+ln} V{y0-20+ln+36}" stroke="{LINE}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>')
    p.append(C(spine, y0 - 20 + ln + 46, 6, "none", f'stroke="{LINE}" stroke-width="2" stroke-dasharray="3 3"'))
    p.append('<g class="chart">')
    cw, ch = 440, 38
    maxw = cw - 40
    tips = []
    for i, d in enumerate(items):
        lab, col, side = CATS[d["cat"]]
        y = y0 + i * step
        t = 0.3 + 3.2 * i / max(n - 1, 1)
        left = side == "L"
        cx0 = spine - 64 - cw if left else spine + 64
        edge = cx0 + cw if left else cx0
        a = "end" if left else "start"
        tx = edge - 16 if left else edge + 16
        p.append(f'<g id="n{i}" opacity="0">{fade(round(t,2),0.4)}<g class="pt hv">'
                 + R(cx0 - 6 if left else cx0 - 6, y - ch / 2 - 4, cw + 12, ch + 8, 12, "none", extra='pointer-events="all"')
                 + R(cx0, y - ch / 2, cw, ch, 10, CARD, LINE, 1.2, 'class="card"')
                 + R(edge - 5 if left else edge, y - ch / 2 + 6, 5, ch - 12, 2.5, col)
                 + L(edge + (0 if left else 0), y, spine - (9 if left else -9), y, col, 1.5, 'stroke-dasharray="3 3" opacity="0.7"')
                 + T(tx, y - 3, fit(d["title"], maxw, 13.5, True), 13.5, TXT, a, weight=600)
                 + T(tx, y + 13, fit(f'{d["when"]}  ·  {d["org"]}', maxw, 12), 12, col, a)
                 + C(spine, y, 8, BG, f'stroke="{col}" stroke-width="2.5"')
                 + C(spine, y, 3.5, col, 'class="hz"') + '</g></g>')
        if d.get("now"):
            p.append(C(spine, y, 8, "none", f'class="mo" pointer-events="none" stroke="{col}" stroke-width="2" opacity="0"',
                       f'<animate attributeName="r" values="8;22" dur="2s" begin="{t+0.6:.2f}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="opacity" values="0.8;0" dur="2s" begin="{t+0.6:.2f}s" repeatCount="indefinite"/>'))
        wl = wrap(d["detail"], 50)
        tcx = (spine + 60 + 200) if left else (spine - 60 - 200)
        tips.append(tooltip(tcx, min(y + 22, H - 40 - 16 * (len(wl) + 1)), wl, col, W, f"tt{i}", title=f'{d["when"]} · {d["title"]}', width=410))
    p.extend(tips)
    p.append('</g>')
    p.append('</svg>')
    return "\n".join(p)


if __name__ == "__main__":
    import stack_panel
    import guilda_flow
    out = {"hero.svg": hero(), "timeline.svg": timeline(), "stack.svg": stack_panel.build(),
           "agent-flow.svg": guilda_flow.flow(), "guilda-gates.svg": guilda_flow.gates(),
           "guilda-camadas.svg": guilda_flow.camadas()}
    for name, svg in out.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print("ok", name, len(svg.encode("utf-8")), "bytes")
