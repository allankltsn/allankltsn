"""Seção 04: o fluxo da guilda (raias), os gates em detalhe e as camadas de modelo.

Fatos verificados em allankltsn/guilda (tag v2.0.0). Não usa os elementos "só no desenho"
dos diagramas da própria guilda (backlog/done, P0-P3, nota 7/10, orchestrator-agent).
Kiro entra pelo kit setup_kiro, não é adapter da guilda (adapters: Claude Code e Codex).
Texto mínimo de 12 px (SVGs de 1200 de largura). Tudo que se move ou só decora tem
pointer-events="none" e, se for loop infinito, a classe .mo (some em prefers-reduced-motion).
"""
import math
import re

from svgkit import *  # noqa: F401,F403

W = 1200
CYCLE = 18.0
DECO = 'class="mo" pointer-events="none"'


# ---------------------------------------------------------------- geometria
def slim(svg):
    """Enxuga o markup sem mudar o desenho: tira padrões (text-anchor=start), espaços antes de '>' e pares vazios."""
    svg = svg.replace(' text-anchor="start"', "").replace(' fill="none" stroke-width="1"', ' fill="none"')
    svg = re.sub(r"\s+>", ">", svg)
    svg = re.sub(r"(?<!/)></(rect|circle)>", "/>", svg)
    svg = re.sub(r"(?<=[\"( ,])(-?\d+)\.0(?=[\"), ])", lambda m: m.group(1), svg)  # 150.0 -> 150
    svg = svg.replace(' font-size="12"', "").replace("<svg ", '<svg font-size="12" ', 1)  # 12 px vira o padrão herdado
    svg = svg.replace('"#ffffff"', '"#fff"').replace('opacity="0.', 'opacity=".')
    return svg.replace('id="t-', 'id="t').replace("~#t-", "~#t")  # ids de tooltip mais curtos


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def seg(a, b):
    """Curva centro a centro com tangentes horizontais (reta se mesma altura)."""
    (x1, y1), (x2, y2) = a, b
    if abs(y1 - y2) < 0.5:
        return [(x1, y1), (x1 + (x2 - x1) / 3, y1), (x1 + 2 * (x2 - x1) / 3, y2), (x2, y2)]
    m = (x2 - x1) / 2
    return [(x1, y1), (x1 + m, y1), (x2 - m, y2), (x2, y2)]


def line_c(a, b):
    """Reta escrita como cúbica (para somar comprimentos e compor caminhos)."""
    return [a, (a[0] + (b[0] - a[0]) / 3, a[1] + (b[1] - a[1]) / 3), (a[0] + 2 * (b[0] - a[0]) / 3, a[1] + 2 * (b[1] - a[1]) / 3), b]


def seg_len(c, n=40):
    pts = [bez(*c, i / n) for i in range(n + 1)]
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(n))


def path_d(curves):
    d = f"M{curves[0][0][0]:.0f},{curves[0][0][1]:.0f}"
    for c in curves:
        d += f" C{c[1][0]:.0f},{c[1][1]:.0f} {c[2][0]:.0f},{c[2][1]:.0f} {c[3][0]:.0f},{c[3][1]:.0f}"
    return d


def window(s, e):
    """Anima opacity visível só entre as frações s e e do ciclo."""
    return (f'<animate attributeName="visibility" values="hidden;visible;hidden;hidden" keyTimes="0;{s:.3f};{e:.3f};1" calcMode="discrete" '
            f'dur="{CYCLE}s" repeatCount="indefinite"/>')


def token(d, s, e, color, r=6):
    return (f'<circle r="{r}" fill="{color}" visibility="hidden" {DECO}><animateMotion dur="{CYCLE}s" repeatCount="indefinite" path="{d}" '
            f'keyPoints="0;0;1;1" keyTimes="0;{s:.4f};{e:.4f};1" calcMode="linear"/>{window(s, e)}</circle>')


def ring(cx, cy, f, color, r0=15, r1=28):
    f = min(f, 0.93)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="none" stroke="{color}" stroke-width="2.5" opacity="0" {DECO}>'
            f'<animate attributeName="r" values="{r0};{r0};{r1};{r1}" keyTimes="0;{f:.4f};{f+0.05:.4f};1" dur="{CYCLE}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0;0.95;0;0" keyTimes="0;{f:.4f};{f+0.002:.4f};{f+0.05:.4f};1" dur="{CYCLE}s" repeatCount="indefinite"/></circle>')


def glow_box(x, y, w, h, rx, f, color, span=0.07):
    f = min(f, 0.9)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{color}" opacity="0" {DECO}>'
            f'<animate attributeName="opacity" values="0;0;0.35;0;0" keyTimes="0;{f:.4f};{f+0.01:.4f};{f+span:.4f};1" dur="{CYCLE}s" repeatCount="indefinite"/></rect>')


def chevron(c, color):
    (x, y), (x2, y2) = bez(*c, 0.5), bez(*c, 0.52)
    ang = math.degrees(math.atan2(y2 - y, x2 - x))
    return f'<path d="M-4,-4 L3,0 L-4,4 Z" fill="{color}" transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})"/>'


# ---------------------------------------------------------------- fluxo principal
LANES = [  # chave, título, subtítulo, y0, altura, cor
    ("A", "Principal", "orquestra, não implementa", 64, 100, LAVENDER),
    ("B", "Produto e design", "história e critérios", 164, 90, PINK),
    ("C", "Especialistas", "um autor por vez", 254, 120, SKY),
    ("D", "Gates independentes", "o mesmo snapshot", 374, 300, MINT),
    ("E", "Humano", "aceite separado", 674, 90, PEACH),
    ("F", "Suporte contínuo", "vale para todo o fluxo", 764, 150, BUTTER),
]
LY = {k: y0 + 36 for k, _, _, y0, _, _ in LANES}
LC = {k: c for k, _, _, _, _, c in LANES}
X0, DX = 188, 62

# id, lane, rótulo (linhas), título do tooltip, texto do tooltip
NODES = [
    (1, "A", ["Demanda"], "Demanda", "O principal decompõe o pedido: domínio, stack real, risco e fase."),
    (2, "B", ["História", "+ DoR"], "História + DoR", "O product-owner escreve a história [S-NNN] com Given/When/Then e regras BR-NNN, no critério INVEST, com DoR de 9 itens."),
    (3, "A", ["Brainstorm"], "Brainstorm", "Os especialistas questionam as premissas. Consulta não dá permissão de escrita."),
    (4, "A", ["Spec", "aprovada"], "Spec aprovada", "Proporcional ao risco: rollback, segurança e validação definidos antes do código."),
    (5, "A", ["Plano"], "Plano", "Pacotes com escopo de escrita disjunto e dono único dos arquivos compartilhados. O plano não autoriza deploy."),
    (6, "A", ["Staffing"], "Staffing", "Cada tarefa vai para o especialista certo, em um de 8 formatos de equipe. Lacuna nunca é preenchida em silêncio."),
    (7, "A", ["Camada por", "despacho"], "Camada por despacho", "Deep, standard ou light, por 5 sinais: impacto, ambiguidade, contexto, falha anterior e custo do erro. Gate nunca abaixo de standard."),
    (8, "A", ["Brief", "+ card"], "Brief + card", "Brief de cerca de 15 linhas, por referência. O card do quadro vai de pending para in-progress."),
    (9, "C", ["Implementação"], "Implementação", "Um autor por vez, com testes do escopo e handoff de até 40 linhas."),
    (10, "A", ["Snapshot congelado"], "Snapshot congelado", "SHA, arquivos staged, unstaged e novos, com hashes. Todos os gates validam o mesmo snapshot."),
]
NX = {nid: X0 + DX * (nid - 1) for nid, *_ in NODES}
GATES = [  # id, rótulo, obrigatório, título, texto
    ("g1", "Conformidade", True, "Revisão de conformidade", "Revisão independente de conformidade. Obrigatória em toda implementação."),
    ("g2", "Revisão técnica", True, "Revisão técnica", "Revisão técnica independente. Obrigatória em toda implementação."),
    ("g3", "Segurança", True, "Segurança", "Revisão de segurança, com devsecops-infra quando há IaC. Obrigatória em toda implementação."),
    ("g4", "Privacidade", False, "Privacidade", "Tem poder de veto nas decisões de design e usabilidade (LGPD e GDPR). Condicional."),
    ("g5", "Conformidade de design", False, "Conformidade de design", "Revisão de conformidade de design. Condicional."),
    ("g6", "Usabilidade", False, "Usabilidade", "Dois usuários leigos simulados, em 7 passos, com precedência em 5 níveis. Condicional."),
]
GX, GW, GH = 800, 172, 28
for _g in GATES:
    assert text_width(_g[1], 12, True) <= GW - 16, _g[1]
SUPPORT = [
    ("Quadro GitHub Projects", "9 estados · parado 24h/7d/30d · validação dupla", "O quadro tem 9 estados; um card parado é sinalizado após 24h, 7 dias e 30 dias, e a validação é dupla."),
    ("Economia de tokens", "muda como executa, nunca o que verifica", "A economia muda como a tarefa é executada, nunca o que é verificado."),
    ("Continuidade de sessão", "marcos em 100k, 200k, 300k e 400k tokens", "A sessão registra marcos em 100k, 200k, 300k e 400k tokens para poder ser retomada."),
    ("Evidência real", "prova executada, não declaração", "A entrega vem com evidência real, não com declaração."),
    ("Registro de instalações", "tudo que se instala fica registrado", "Tudo que é instalado fica registrado."),
    ("Polyrepo", "contratos primeiro e prova de integração", "Em produtos com vários repositórios, os contratos vêm primeiro e a integração é provada."),
]
LOOP = [  # título, subtítulo, tooltip
    ("Achado com ID", "estável + reprodução", "Achado com ID estável: severidade, arquivo:linha e reprodução. Critical/High bloqueiam a conclusão (completed), salvo decisão de risco explícita."),
    ("Volta ao autor", "correção + evidência", "A correção traz evidência: falhava antes, passa depois. O autor não fecha o achado."),
    ("Confirmação", "independente", "Outro especialista confirma a correção. Quem escreveu não fecha o próprio achado."),
    ("Revalida o delta", "gates afetados", "Refaz os gates afetados pelo delta, sobre o snapshot final."),
    ("2 rodadas iguais", "escalar: causa raiz", "Após 2 rodadas iguais: investigar a causa raiz, chamar um 3º especialista ou subir a camada do modelo."),
]
for _t in LOOP:
    assert text_width(_t[1], 12) <= 148, _t[1]


def flow():
    H = 914
    # ---- tempos
    pts1 = [(NX[nid], LY[l]) for nid, l, *_ in NODES]
    c1 = [seg(pts1[i], pts1[i + 1]) for i in range(len(pts1) - 1)]
    L1 = [seg_len(c) for c in c1]
    tot1 = sum(L1)
    s1, e1 = 0.02, 0.44
    node_f, acc = {}, 0
    for i, (nid, *_r) in enumerate(NODES):
        node_f[nid] = s1 + (acc / tot1) * (e1 - s1)
        if i < len(L1):
            acc += L1[i]
    d1 = path_d(c1)
    gy = [408 + k * 36 for k in range(6)]
    qy = 634
    f_fan, f_gate, f_qa = 0.45, 0.52, 0.64
    snap = (NX[10], LY["A"])
    fan = [[(snap[0] + 14, snap[1]), (snap[0] + 40, snap[1]), (GX - 24, y + GH / 2), (GX, y + GH / 2)] for y in gy]
    # fechamento: QA -> verificação -> tag -> aceite humano
    VX, TX, AX = 1007, 1090, 1175
    qa_out = (GX + GW, qy + GH / 2)
    v, tg, ac = (VX, LY["A"]), (TX, LY["A"]), (AX, LY["E"])
    c2 = [[qa_out, (990, qa_out[1]), (VX, qa_out[1] - 40), (VX, qa_out[1] - 90)],
          line_c((VX, qa_out[1] - 90), v), seg(v, tg),
          [tg, (TX + 50, tg[1]), (AX, tg[1] + 10), (AX, tg[1] + 60)], line_c((AX, tg[1] + 60), ac)]
    L2 = [seg_len(c) for c in c2]
    tot2 = sum(L2)
    s2, e2 = 0.68, 0.90
    d2 = path_d(c2)
    f_v = s2 + (sum(L2[:2]) / tot2) * (e2 - s2)
    f_t = s2 + (sum(L2[:3]) / tot2) * (e2 - s2)
    f_a = e2 - 0.01
    # laço de correção (elipse)
    rcx, rcy, rx, ry = 450, 522, 210, 84
    lp = []
    for a, (t1, t2, tip) in zip([-90, -18, 54, 126, 198], LOOP):
        lp.append((rcx + rx * math.cos(math.radians(a)), rcy + ry * math.sin(math.radians(a)), t1, t2, tip))

    ids = [f"n{i}" for i in range(1, 15)] + [g[0] for g in GATES] + ["qa", "l1", "l2"]  # ids com arestas para realçar
    tip_ids = ids + [f"l{i}" for i in range(3, 6)] + [f"f{i}" for i in range(1, 7)]
    css = (BASE_CSS + ".chart:hover .pt:not(:hover){opacity:.4}.pt:hover .hz{transform:scale(1.3)}"
           ".edge{transition:opacity .15s,stroke-width .15s}.chart:hover .edge{opacity:.22}"
           + "".join(f".chart:has(#{i}:hover) .e-{i}{{opacity:1;stroke-width:3;stroke:#fff}}" for i in ids)
           + "".join(f"#{i}:hover~#t-{i}{{opacity:1}}" for i in tip_ids))
    marker = (f'<marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{CORAL}"/></marker>'
              f'<marker id="am" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{MINT}"/></marker>'
              f'<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="8" fill="{CORAL}" opacity="0.55"/></pattern>')
    p = [svg_open(W, H, "Fluxo da guilda em raias: o principal orquestra, produto escreve a história, especialistas implementam, gates independentes validam o mesmo snapshot, o laço de correção volta ao autor e o aceite humano é separado", css, marker)]
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
    p.append(T(24, 34, "Fluxo da guilda: do pedido à entrega", 17, TXT, weight=700))
    p.append(T(24, 54, "o principal orquestra · especialistas executam · gates independentes validam · ninguém revisa a própria entrega", 12, DIM))
    p.append(T(W - 24, 34, "passe o mouse nos nós", 12, DIM, "end"))
    for k, title, sub, y0, h, col in LANES:
        p.append(R(12, y0 + 2, W - 24, h - 4, 10, CARD, extra='opacity="0.55" pointer-events="none"') + R(12, y0 + 2, 4, h - 4, 2, col))
        p.append(T(28, y0 + 26, title, 12.5, col, weight=700))
        for j, ln in enumerate(wrap(sub, 18)):
            p.append(T(28, y0 + 42 + j * 14, ln, 12, DIM))
    # barreira: silêncio nunca aprova
    p.append(f'<rect x="992" y="388" width="9" height="270" rx="3" fill="url(#hatch)" stroke="{CORAL}" stroke-width="1" pointer-events="none"/>')
    p.append(T(1020, 416, "Silêncio ≠ aprovação", 13, CORAL, weight=700))
    for j, ln in enumerate(["timeout, impasse,", "validador ausente", "ou orçamento", "esgotado nunca", "aprovam"]):
        p.append(T(1020, 436 + j * 16, ln, 12, MUTED))
    p.append(T(180, 396, "LAÇO DE CORREÇÃO", 12, DIM, mono=True, extra='letter-spacing="2"'))
    p.append(R(GX, 384, 12, 9, 3, MINT, extra='pointer-events="none"') + T(GX + 18, 393, "obrigatório", 12, DIM)
             + R(GX + 96, 384, 12, 9, 3, "none", MINT, 1.2, 'stroke-dasharray="3 2" pointer-events="none"') + T(GX + 114, 393, "condicional", 12, DIM))
    p.append(T(GX - 12, qy + 19, "por último", 12, DIM, "end"))
    p.append(T(190, 722, "O aceite humano é separado dos gates:", 12, DIM) + T(190, 738, "identidade, data e escopo ficam registrados.", 12, DIM))
    p.append('<g class="chart">')
    # ---- arestas (atrás dos nós, dentro de .chart para o realce e o esmaecimento funcionarem)
    p.append('<g pointer-events="none">')
    for i, c in enumerate(c1):
        a, b = i + 1, i + 2
        p.append(f'<path class="edge e-n{a} e-n{b}" d="{path_d([c])}" fill="none" stroke="{LAVENDER}" stroke-width="2.2" opacity="0.8"/>')
        p.append(chevron(c, LAVENDER))
    for k, c in enumerate(fan):
        p.append(f'<path class="edge e-n10 e-g{k+1}" d="{path_d([c])}" fill="none" stroke="{MINT}" stroke-width="1.8" opacity="0.8"/>')
    for k, y in enumerate(gy):  # chaves dos gates -> QA
        p.append(L(GX + GW, y + GH / 2, GX + GW + 8, y + GH / 2, MINT, 1.5, f'class="edge e-g{k+1}" opacity="0.7"'))
    p.append(f'<path class="edge e-qa" d="M{GX+GW+8},{gy[0]+GH/2} V{gy[-1]+GH/2} V{qy-8} H{GX+GW/2} V{qy-2}" fill="none" stroke="{MINT}" stroke-width="1.6" opacity="0.7" marker-end="url(#am)"/>')
    for c in c2:
        p.append(f'<path class="edge e-qa e-n11 e-n12 e-n13" d="{path_d([c])}" fill="none" stroke="{LAVENDER}" stroke-width="2.2" opacity="0.8"/>')
    p.append(L(AX - 14, ac[1], TX + 14, ac[1], MINT, 2, 'class="edge e-n13 e-n14" marker-end="url(#am)"'))
    # laço: elipse, setas coral e a bolinha que orbita (abaixo dos cartões, que a cobrem)
    p.append(f'<ellipse cx="{rcx}" cy="{rcy}" rx="{rx}" ry="{ry}" fill="none" stroke="{LINE}" stroke-width="2"/>')
    p.append(f'<ellipse class="edge" cx="{rcx}" cy="{rcy}" rx="{rx}" ry="{ry}" fill="none" stroke="{CORAL}" stroke-width="2" stroke-dasharray="6 10" opacity="0.85">'
             f'<animate attributeName="stroke-dashoffset" from="0" to="-64" dur="2s" repeatCount="indefinite"/></ellipse>')
    p.append(f'<circle r="5.5" fill="{CORAL}" {DECO}><animateMotion dur="7s" repeatCount="indefinite" path="M{rcx-rx},{rcy} a{rx},{ry} 0 1,1 {2*rx},0 a{rx},{ry} 0 1,1 {-2*rx},0"/></circle>')
    back = f"M{rcx+90},{rcy-ry-22} C{rcx+170},{rcy-ry-90} 640,300 {NX[9]-15},299"
    p.append(f'<path class="edge e-l1 e-n9" d="{back}" fill="none" stroke="{CORAL}" stroke-width="2" stroke-dasharray="6 6" marker-end="url(#ar)">'
             f'<animate attributeName="stroke-dashoffset" from="0" to="-48" dur="1.6s" repeatCount="indefinite"/></path>')
    p.append(T(575, 376, "volta ao autor", 12, CORAL, "middle", True))
    to_ring = f"M{GX},{gy[3]+GH/2:.0f} C770,{gy[3]+GH/2:.0f} 760,498 {lp[1][0]+82:.0f},498"
    p.append(f'<path class="edge e-l2 e-g4" d="{to_ring}" fill="none" stroke="{CORAL}" stroke-width="2" stroke-dasharray="6 6" marker-end="url(#ar)">'
             f'<animate attributeName="stroke-dashoffset" from="0" to="-48" dur="1.6s" repeatCount="indefinite"/></path>')
    p.append(T(758, 556, "achados", 12, CORAL, "middle", True))
    p.append('</g>')
    # ---- nós
    delay = 0.1

    def label_lines(cx, cy, lines, above):
        o = []
        for j, ln in enumerate(lines):
            y = cy - 22 - (len(lines) - 1 - j) * 14 if above else cy + 31 + j * 14
            o.append(T(cx, y, ln, 12, TXT, "middle"))
        return "".join(o)

    def nodegroup(nid, cx, cy, lines, col, num, above=False, f=None, hit=None):
        hx, hy, hw, hh = hit or (cx - 34, cy - 20, 68, 72)
        o = [f'<g id="{nid}" opacity="0">{fade(round(delay,2),0.4)}<g class="pt hv">', R(hx, hy, hw, hh, 10, "none", extra='pointer-events="all"')]
        if f is not None:
            o.append(ring(cx, cy, f, col))
        o.append(f'<g class="hz">{C(cx, cy, 14, col)}{T(cx, cy + 4.5, num, 13, INK, "middle", True, 700)}</g>')
        o.append(label_lines(cx, cy, lines, above))
        o.append('</g></g>')
        return "".join(o)

    sat = (NX[3], LY["C"])
    for nid, lane, lines, title, tip in NODES:
        col, x = LC[lane], NX[nid]
        if nid == 3:
            p.append(f'<g id="n3" opacity="0">{fade(round(delay,2),0.4)}<g class="pt hv">'
                     + R(x - 40, 78, 80, 232, 10, "none", extra='pointer-events="all"')
                     + L(x, LY["A"] + 14, x, sat[1] - 12, LAVENDER, 1.4, 'stroke-dasharray="3 4"')
                     + ring(x, LY["A"], node_f[3], col)
                     + f'<g class="hz">{C(x, LY["A"], 14, col)}{T(x, LY["A"] + 4.5, "3", 13, INK, "middle", True, 700)}</g>'
                     + T(x, LY["A"] + 31, "Brainstorm", 12, TXT, "middle")
                     + R(x - 46, sat[1] - 13, 92, 26, 13, NODE, SKY, 1.4) + T(x, sat[1] + 4.5, "especialistas", 12, SKY, "middle", True)
                     + T(x, sat[1] + 32, "só consulta", 12, DIM, "middle") + '</g></g>')
        else:
            hit = (x - 62, 80, 124, 36) if nid == 10 else None
            p.append(nodegroup(f"n{nid}", x, LY[lane], lines, col, str(nid), above=(nid == 10), f=node_f[nid], hit=hit))
        delay += 0.12
    closing = [(11, VX, "A", ["Verificação"], LAVENDER, f_v), (12, TX, "A", ["Tag SemVer"], LAVENDER, f_t)]
    for nid, x, lane, lines, col, f in closing:
        p.append(nodegroup(f"n{nid}", x, LY[lane], lines, col, str(nid), above=True, f=f))
        delay += 0.12
    # nós 13 (aceite humano) e 14 (closed + postmortem), na raia do humano
    ey = LY["E"]
    for nid, x, lines, f in ((13, AX, ["Aceite", "humano"], f_a), (14, TX, ["closed +", "postmortem"], min(f_a + 0.02, 0.93))):
        p.append(nodegroup(f"n{nid}", x, ey, lines, PEACH, str(nid), f=f, hit=(x - 40, ey - 20, 80, 72)))
        delay += 0.12
    p.append(glow_box(GX - 6, gy[0] - 6, GW + 12, gy[-1] - gy[0] + GH + 12, 12, f_gate, "#ffffff", 0.09))
    for k, (gid, lab, ob, title, tip) in enumerate(GATES):
        y = gy[k]
        fill, tcol = (MINT, INK) if ob else ("none", MINT)
        dash = "" if ob else 'stroke-dasharray="4 3"'
        p.append(f'<g id="{gid}"><g class="pt hv">'
                 + R(GX - 6, y - 3, GW + 12, GH + 6, 10, "none", extra='pointer-events="all"')
                 + '<g class="hz">' + R(GX, y, GW, GH, 9, fill, MINT, 1.6, dash) + T(GX + GW / 2, y + 19, lab, 12, tcol, "middle", weight=600) + '</g></g></g>')
        delay += 0.1
    p.append(f'<g id="qa"><g class="pt hv">' + R(GX - 6, qy - 3, GW + 12, GH + 6, 10, "none", extra='pointer-events="all"')
             + glow_box(GX, qy, GW, GH, 9, f_qa, "#ffffff")
             + '<g class="hz">' + R(GX, qy, GW, GH, 9, MINT, MINT, 1.6) + T(GX + GW / 2, qy + 19, "QA adversarial", 12, INK, "middle", weight=700) + '</g></g></g>')
    pw = 160
    for i, (x, y, t1, t2, tip) in enumerate(lp):
        p.append(f'<g id="l{i+1}"><g class="pt hv">' + R(f"{x-pw/2-4:.1f}", f"{y-24:.1f}", pw + 8, 48, 10, "none", extra='pointer-events="all"')
                 + '<g class="hz">' + R(f"{x-pw/2:.1f}", f"{y-20:.1f}", pw, 40, 10, NODE, CORAL, 1.5)
                 + T(f"{x:.1f}", f"{y-3:.1f}", t1, 12, CORAL, "middle", weight=700) + T(f"{x:.1f}", f"{y+13:.1f}", t2, 12, MUTED, "middle") + '</g></g></g>')
        delay += 0.1
    p.append('<g pointer-events="none">' + T(rcx, rcy - 14, "Critical/High bloqueiam", 13, TXT, "middle", weight=700)
             + T(rcx, rcy + 4, "a conclusão (completed), salvo", 12, MUTED, "middle") + T(rcx, rcy + 20, "decisão de risco explícita", 12, MUTED, "middle") + '</g>')
    # suporte contínuo (raia F)
    fy = [(170 + (i % 3) * 344, 780 + (i // 3) * 56) for i in range(6)]
    for i, ((t1, t2, _tip), (x, y)) in enumerate(zip(SUPPORT, fy)):
        p.append(f'<g id="f{i+1}"><g class="pt hv">' + R(x, y, 330, 46, 12, NODE, BUTTER, 1.4)
                 + C(x + 20, y + 23, 5, BUTTER, 'class="mo" pointer-events="none"', f'<animate attributeName="opacity" values="1;0.35;1" dur="3s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/>')
                 + T(x + 36, y + 20, t1, 12.5, BUTTER, weight=700) + T(x + 36, y + 37, t2, 12, MUTED) + '</g></g>')
    # tokens e pulsos (decoração: sem ponteiro, somem em reduced motion)
    p.append('<g pointer-events="none">')
    p.append(token(d1, s1, e1, PINK))
    for c in fan:
        p.append(token(path_d([c]), f_fan, f_fan + 0.07, MINT, 4.5))
    p.append(token(d2, s2, e2, PINK))
    p.append('</g>')

    # ---- tooltips (irmãos posteriores dos alvos)
    def tp(nid, cx, cy, title, tip, col, wd=300):
        return tooltip(cx, cy, wrap(tip, 40), col, W, f"t-{nid}", title=title, width=wd)

    for nid, lane, lines, title, tip in NODES:
        p.append(tp(f"n{nid}", NX[nid], LY[lane] + 52 if lane != "C" else LY[lane] + 44, title, tip, LC[lane]))
    p.append(tp("n11", VX - 70, LY["A"] + 30, "Verificação do principal", "O principal reexecuta pelo menos um comando e audita o quadro antes de seguir.", LAVENDER, 280))
    p.append(tp("n12", TX - 70, LY["A"] + 30, "Tag SemVer publicada", "A tag SemVer é publicada antes de o código entrar na main.", LAVENDER, 280))
    p.append(tp("n13", AX - 150, ey - 120, "Aceite humano", "Identidade, data e escopo do aceite ficam registrados, separados dos gates.", PEACH, 290))
    p.append(tp("n14", TX - 80, ey - 100, "closed + postmortem", "Depois do aceite, o card vai para closed e o postmortem é escrito.", PEACH, 290))
    for k, (gid, lab, ob, title, tip) in enumerate(GATES):
        p.append(tp(gid, GX - 170, gy[k] - 6, title, tip, MINT, 290))
    p.append(tp("qa", GX - 170, qy - 70, "QA adversarial", "Roda por último, depois dos demais gates, sobre o mesmo snapshot. Obrigatório em toda implementação.", MINT, 290))
    for i, (x, y, t1, t2, tip) in enumerate(lp):
        p.append(tp(f"l{i+1}", x if i != 1 else 600, y - 130 if i == 0 else y + 28, f"{t1} {t2}" if i == 4 else t1, tip, CORAL, 300))
    for i, ((t1, _t2, tip), (x, y)) in enumerate(zip(SUPPORT, fy)):
        lines = wrap(tip, 44)
        p.append(tooltip(x + 165, y - (16 * (len(lines) + 1) + 18) - 6, lines, BUTTER, W, f"t-f{i+1}", title=t1, width=330))
    p.append('</g></svg>')
    return slim(chr(10).join(p))


# ---------------------------------------------------------------- gates em detalhe
def gates():
    H = 480
    cards = [
        ("Conformidade", True, "Revisão de conformidade", "Obrigatória em toda implementação. Revisão independente do que foi entregue.", ""),
        ("Técnica", True, "Revisão técnica", "Obrigatória em toda implementação. Revisão técnica independente.", ""),
        ("Segurança", True, "Segurança", "Obrigatória em toda implementação. Entra devsecops-infra quando há IaC.", "+ devsecops-infra"),
        ("Privacidade", False, "Privacidade", "Condicional. Tem poder de veto nas decisões de design e usabilidade (LGPD e GDPR).", "veto em design e usabilidade"),
        ("Design", False, "Conformidade de design", "Condicional. Revisão de conformidade de design.", ""),
        ("Usabilidade", False, "Usabilidade", "Condicional. Dois usuários leigos simulados, 7 passos, precedência em 5 níveis.", "2 usuários leigos"),
        ("QA adversarial", True, "QA adversarial", "Obrigatório em toda implementação. Roda por último, depois dos demais gates.", ""),
    ]
    chain = [
        ("Achado", "ID estável", "severidade, arquivo:linha e reprodução", LAVENDER),
        ("Volta ao autor", "só o autor corrige", "mas não fecha o achado", PINK),
        ("Evidência", "falhava antes", "e passa depois", PEACH),
        ("Confirmação", "independente", "feita por outro especialista", SKY),
        ("Revalida o delta", "gates afetados", "refeitos no snapshot final", MINT),
        ("2 rodadas iguais", "escalar", "causa raiz, 3º especialista ou camada acima", CORAL),
    ]
    n1, n2 = len(cards), len(chain)
    css = (BASE_CSS + ".chart:hover .pt:not(:hover){opacity:.45}.pt:hover .hz{transform:translateY(-3px)}"
           + tip_rule("k", "kt", range(n1)) + tip_rule("s", "st", range(n2)))
    p = [svg_open(W, H, "Gates independentes e laço de correção: três gates obrigatórios, três condicionais, QA por último; achado com ID estável, correção com evidência, confirmação independente e revalidação do delta", css)]
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
    p.append(T(40, 40, "Gates e laço de correção", 17, TXT, weight=700))
    p.append(T(W - 40, 40, "passe o mouse nos cartões", 12, DIM, "end"))
    cw, gap = 152, 10
    p.append(T(40, 78, "EM PARALELO, SOBRE O MESMO SNAPSHOT", 12, DIM, mono=True, extra='letter-spacing="1.5"'))
    p.append(L(40, 86, 40 + 6 * cw + 5 * gap, 86, MINT, 1.5, 'opacity="0.6"'))
    p.append(T(40 + 6 * (cw + gap), 78, "POR ÚLTIMO", 12, DIM, mono=True, extra='letter-spacing="1.5"'))
    p.append(L(40 + 6 * (cw + gap), 86, 40 + 7 * cw + 6 * gap, 86, MINT, 1.5, 'opacity="0.6"'))
    p.append('<g class="chart">')
    for i, (nm, ob, title, tip, sub) in enumerate(cards):
        x = 40 + i * (cw + gap)
        tag = "OBRIGATÓRIO" if ob else "CONDICIONAL"
        dash = "" if ob else 'stroke-dasharray="5 4"'
        subl = wrap(sub, 17)
        p.append(f'<g id="k{i}" opacity="0">{fade(round(0.2+i*0.12,2),0.45)}<g class="pt hv"><g class="hz">'
                 + R(x, 100, cw, 100, 14, CARD, MINT, 1.6, dash) + R(x, 100, cw, 6, 3, MINT if ob else "none")
                 + T(x + 14, 128, tag, 12, MINT, mono=True)
                 + T(x + 14, 154, nm, 15, TXT, weight=700)
                 + C(x + cw - 16, 122, 4, MINT, 'class="mo" pointer-events="none"', f'<animate attributeName="opacity" values="1;0.3;1" dur="2.4s" begin="{i*0.25:.2f}s" repeatCount="indefinite"/>')
                 + "".join(T(x + 14, 174 + j * 15, ln, 12, MUTED) for j, ln in enumerate(subl))
                 + '</g></g></g>')
    p.append(T(40, 240, "ACHADO ATÉ FECHAR", 12, DIM, mono=True, extra='letter-spacing="1.5"'))
    cw2 = 176
    g2 = (W - 80 - n2 * cw2) / (n2 - 1)
    for i, (t1, t2, t3, col) in enumerate(chain):
        x = 40 + i * (cw2 + g2)
        p.append(f'<g id="s{i}" opacity="0">{fade(round(1.0+i*0.15,2),0.45)}<g class="pt hv"><g class="hz">'
                 + R(x, 254, cw2, 108, 14, CARD, col, 1.5) + C(x + 22, 279, 11, col) + T(x + 22, 283.5, str(i + 1), 12, INK, "middle", True, 700)
                 + T(x + 42, 283, t1, 13, col, weight=700) + T(x + 16, 306, t2, 12, TXT)
                 + "".join(T(x + 16, 324 + j * 15, ln, 12, MUTED) for j, ln in enumerate(wrap(t3, 22)))
                 + '</g></g></g>')
        if i < n2 - 1:
            ax = x + cw2 + 4
            p.append(f'<path d="M{ax:.1f},291 h{g2-8:.1f}" stroke="{col}" stroke-width="2" stroke-dasharray="4 4" pointer-events="none"><animate attributeName="stroke-dashoffset" from="0" to="-16" dur="1s" repeatCount="indefinite"/></path>'
                     f'<path d="M{ax+g2-12:.1f},286 l6,5 l-6,5" fill="none" stroke="{col}" stroke-width="2" pointer-events="none"/>')
    p.append(R(40, 386, 560, 70, 14, NODE, CORAL, 1.4) + T(60, 412, "Critical/High bloqueiam a conclusão (completed)", 14, CORAL, weight=700)
             + T(60, 432, "salvo decisão de risco explícita; o laço volta ao autor", 12, MUTED)
             + T(60, 448, "até a confirmação independente", 12, MUTED))
    p.append(R(620, 386, 540, 70, 14, NODE, MINT, 1.4) + T(640, 412, "Silêncio nunca é aprovação", 14, MINT, weight=700)
             + T(640, 432, "timeout, impasse, validador ausente ou orçamento", 12, MUTED)
             + T(640, 448, "esgotado não aprovam", 12, MUTED))
    for i, (nm, ob, title, tip, sub) in enumerate(cards):
        x = 40 + i * (cw + gap) + cw / 2
        p.append(tooltip(x, 208, wrap(tip, 36), MINT, W, f"kt{i}", title=title, width=290))
    steps_tip = ["Cada achado recebe ID estável, com severidade, arquivo:linha e reprodução.",
                 "O achado volta ao autor da implementação.",
                 "A correção traz evidência de que falhava antes e passa depois. O autor não fecha o achado.",
                 "Outro especialista confirma a correção.",
                 "Refaz os gates afetados no snapshot final.",
                 "Depois de 2 rodadas iguais: causa raiz, 3º especialista ou camada de modelo acima."]
    for i, (t1, t2, t3, col) in enumerate(chain):
        x = 40 + i * (cw2 + g2) + cw2 / 2
        p.append(tooltip(x, 370, wrap(steps_tip[i], 36), col, W, f"st{i}", title=t1, width=290))
    p.append('</g></svg>')
    return slim(chr(10).join(p))


# ---------------------------------------------------------------- camadas de modelo e papéis
def camadas():
    H = 540
    tiers = [("deep", 5, LAVENDER), ("standard", 21, SKY), ("light", 2, MINT)]
    modes = [("diagnóstico", 12, PEACH), ("autor", 6, PINK), ("implementador", 5, SKY), ("revisão", 4, LAVENDER), ("QA", 1, MINT)]
    # agrupamento oficial do README da guilda (v2.0.0)
    areas = [("Plataforma e nuvem", 12, SKY), ("Produto e design", 6, PEACH), ("Engenharia", 4, LAVENDER),
             ("Qualidade e conformidade", 4, MINT), ("Apoio", 2, BUTTER)]
    assert sum(v for _, v, _ in tiers) == sum(v for _, v, _ in modes) == sum(v for _, v, _ in areas) == 28
    css = (BASE_CSS + ".chart:hover .pt:not(:hover){opacity:.4}.pt:hover .hz{transform:scaleY(1.12)}"
           + tip_rule("t", "tt", range(3)) + tip_rule("m", "mt", range(5)) + tip_rule("a", "at", range(len(areas))))
    p = [svg_open(W, H, "28 papéis da guilda: 5 deep, 21 standard e 2 light; por modo e por área, com 10 perfis, 11 ações, 8 políticas, 8 workflows, 20 templates e 2 adapters", css)]
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
    p.append(T(40, 40, "28 papéis, três camadas de modelo", 17, TXT, weight=700))
    p.append(T(W - 40, 40, "passe o mouse nos blocos", 12, DIM, "end"))
    p.append('<g class="chart">')

    def stacked(items, y, label, pre, x0=40, tw=520):
        o = [T(x0, y - 14, label, 12, MUTED, mono=True, extra='letter-spacing="1.5"')]
        x = x0
        for i, (nm, v, col) in enumerate(items):
            w = tw * v / 28
            cx = x + w / 2 - 1.5
            narrow = w <= 60
            o.append(f'<g id="{pre}{i}" opacity="0">{fade(round(0.3+i*0.15,2),0.5)}<g class="pt hv"><g class="hz">'
                     + R(f"{x:.1f}", y, f"{w-3:.1f}", 54, 10, col)
                     + T(f"{cx:.1f}", y + (33 if narrow else 25), str(v), 14 if narrow else 20, INK, "middle", weight=700)
                     + (T(f"{cx:.1f}", y + 44, nm, 12, INK, "middle") if not narrow else "")
                     + (T(f"{min(max(cx, x0 + 14), x0 + tw - 14):.1f}", y + 72, nm, 12, col, "middle") if narrow else "") + '</g></g></g>')
            x += w
        return "".join(o)

    p.append(stacked(tiers, 100, "CAMADA DE MODELO", "t"))
    p.append(stacked(modes, 206, "MODO DO PAPEL", "m"))
    p.append(T(40, 304, "12 diagnósticos · 6 autores · 5 implementadores · 4 revisores · 1 QA", 12, DIM))
    p.append(T(40, 336, "A CAMADA É ESCOLHIDA POR DESPACHO, POR 5 SINAIS", 12, MUTED, mono=True, extra='letter-spacing="1.5"'))
    sx = 40
    for i, (s_, col) in enumerate([("impacto", PINK), ("ambiguidade", LAVENDER), ("contexto", SKY), ("falha anterior", PEACH), ("custo do erro", CORAL)]):
        w = text_width(s_, 12) + 40
        p.append(f'<g opacity="0">{fade(round(1.0+i*0.12,2),0.4)}' + R(sx, 348, w, 30, 15, "none", col, 1.4) + C(sx + 15, 363, 4, col) + T(sx + 26, 367, s_, 12, col) + '</g>')
        sx += w + 8
    p.append(T(40, 404, "Gate nunca roda abaixo de standard.", 12.5, TXT, weight=600))
    ax0, mx = 640, 12
    p.append(T(ax0, 86, "PAPÉIS POR ÁREA (AGRUPAMENTO DO README DA GUILDA)", 12, MUTED, mono=True, extra='letter-spacing="1"'))
    for i, (nm, v, col) in enumerate(areas):
        y = 108 + i * 52
        w = 330 * v / mx
        p.append(f'<g id="a{i}" opacity="0">{fade(round(0.4+i*0.1,2),0.4)}<g class="pt hv">' + R(ax0 - 8, y - 6, 530, 44, 8, "none", extra='pointer-events="all"')
                 + T(ax0 + 188, y + 20, nm, 13, MUTED, "end") + R(ax0 + 202, y + 6, 320, 18, 9, CARD)
                 + R(ax0 + 202, y + 6, 0, 18, 9, col, extra='class="hz"', inner=f'<animate attributeName="width" to="{320*v/mx:.0f}" begin="{0.6+i*0.1:.1f}s" dur="0.8s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0 0.2 1"/>')
                 + T(ax0 + 210 + 320 * v / mx, y + 20, str(v), 12.5, TXT, mono=True) + '</g></g>')
    kp = [("10", "perfis"), ("11", "ações"), ("8", "políticas"), ("8", "workflows"), ("20", "templates"), ("2", "adapters"), ("158", "testes, 3 ignorados")]
    cols = [MINT, SKY, LAVENDER, PEACH, PINK, BUTTER, AQUA]
    ws = [100, 100, 118, 118, 128, 118, 330]
    gp = (W - 80 - sum(ws)) / 6
    x = 40
    for i, (v, l) in enumerate(kp):
        w = ws[i]
        p.append(f'<g opacity="0">{fade(round(1.3+i*0.1,2),0.4)}' + R(f"{x:.1f}", 428, w, 54, 12, CARD, LINE) + R(f"{x:.1f}", 428, w, 4, 2, cols[i])
                 + T(f"{x+14:.1f}", 464, v, 24, cols[i], weight=700) + T(f"{x+14+text_width(v, 24, True)+8:.1f}", 464, l, 12, MUTED) + '</g>')
        x += w + gp
    p.append(T(40, 506, "ações:  /qa  /security  /aws  /hosting  /kubernetes  /sre  /cicd  /devsecops-infra  /story  /usability  /privacy", 12, DIM, mono=True))
    p.append(T(40, 524, "adapters: Claude Code e Codex  ·  versões: v1.0.0, v1.1.0, v1.2.0, v1.3.0, v2.0.0", 12, DIM, mono=True))
    for i, (nm, v, col) in enumerate(tiers):
        x0 = 40 + 520 * sum(t[1] for t in tiers[:i]) / 28 + 520 * v / 56
        p.append(tooltip(x0, 172, [f"{v} de 28 papéis ({round(100*v/28)}%)", "escolhida por despacho, por 5 sinais"], col, W, f"tt{i}", title=f"camada {nm}", width=270))
    for i, (nm, v, col) in enumerate(modes):
        x0 = 40 + 520 * sum(t[1] for t in modes[:i]) / 28 + 520 * v / 56
        p.append(tooltip(x0, 282, [f"{v} de 28 papéis ({round(100*v/28)}%)"], col, W, f"mt{i}", title=f"modo {nm}", width=250))
    for i, (nm, v, col) in enumerate(areas):
        y = 108 + i * 52
        p.append(tooltip(ax0 + 202 + 320 * v / mx + 40, y + 34, [f"{v} de 28 papéis ({round(100*v/28)}%)"], col, W, f"at{i}", title=nm, width=260))
    p.append('</g></svg>')
    return slim(chr(10).join(p))
