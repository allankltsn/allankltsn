"""Seção 02, "Código em números": barras de linguagem e linha de repositórios por ano.

Dados: tools/github_public.json (gerado por make_public_data.py). Privados só como agregados.
Hover em CSS puro (ver svgkit.py). Chamado por gen_cards.py.
"""
from svgkit import *  # noqa: F401,F403

# Contexto de cada ano, conferido com as datas do currículo (acrescente/ajuste aqui).
YEAR_CONTEXT = {
    "2018": "IC e estágio na Stefanini (05/2018)",
    "2019": "IC, prêmio destaque, analista na Stefanini",
    "2020": "TCC e bacharelado (06/2020), Stefanini",
    "2021": "líder técnico (05/2021), ISH Tech (11/2021)",
    "2022": "sem repositórios novos; ISH Tech / SafeLabs",
    "2023": "ISH Tech / SafeLabs",
    "2024": "ISH Tech / SafeLabs até 06/2024; NuageIT depois",
    "2025": "NuageIT: testes E2E e templates",
    "2026": "NuageIT: agentes, guilda, Aura",
}
LANG_LABEL = {"PLpgSQL": "PL/pgSQL", "Jupyter Notebook": "Jupyter"}


def build(D):
    n = D["total_repos"]
    nl = {k: v["repos"] for k, v in D["by_language"].items()}
    npriv = D["private"]
    pub = D["public_repos"]
    assert len(pub) + npriv == n, "públicos + privados diverge do total"
    assert sum(D["by_year"].values()) == n
    ex = {}
    for lg, v in D["by_language"].items():
        has = [r for r in pub if lg in r["languages"]]
        has.sort(key=lambda r: (r["languages"].index(lg), r["repo"].lower()))
        assert len(has) + v["private_repos"] == v["repos"], f"contagem de {lg} diverge"
        ex[lg] = ([r["repo"].split("/")[1] for r in has[:3]], v["private_repos"])
    years = {y: D["by_year"].get(y, 0) for y in map(str, range(2018, 2027))}
    priv_by_year = D["private_by_year"]
    since = min(D["by_year"])
    minor = D["below_threshold_languages"]

    W2, H2 = 1200, 700
    css = (BASE_CSS + ".chart:hover .pt:not(:hover){opacity:.35}"
           ".bar:hover .fill{filter:brightness(1.12)}.bar:hover .hz{transform:scaleY(1.35)}"
           ".dot:hover .hz{transform:scale(2)}.dot:hover .hl{stroke-width:3.5}")
    bars = sorted(nl.items(), key=lambda t: (-t[1], t[0]))
    mx = bars[0][1]
    x0, wmax, row, by0 = 40, 330, 29, 192
    css += tip_rule("b", "bt", range(len(bars)))
    pt_x0, pt_w, base, ph = 690, 450, 520, 260
    ylist = list(years)
    pk = max(years.values())
    gap = pt_w / (len(ylist) - 1)
    pts = [(pt_x0 + i * gap, base - ph * years[y] / pk) for i, y in enumerate(ylist)]
    css += tip_rule("y", "yt", range(len(ylist)))

    p = [svg_open(W2, H2, f"Código em números: {n} repositórios em 2 contas, {len(nl)} linguagens, desde {since}, {npriv} privados", css,
                  f'<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LAVENDER}" stop-opacity="0.55"/><stop offset="1" stop-color="{LAVENDER}" stop-opacity="0"/></linearGradient>'
                  f'<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{SKY}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'),
         f'<rect width="{W2}" height="{H2}" rx="14" fill="{BG}"/>']
    tiles = [(str(n), "repositórios", MINT), ("2", "contas (@allankltsn, @AllanKT)", SKY), (str(len(nl)), "linguagens", LAVENDER),
             (since, "primeiro repositório", PEACH), (str(npriv), "repositórios privados", PINK)]
    tw = 208
    for i, (v, l, c) in enumerate(tiles):
        x = 40 + i * (tw + 20)
        p.append(f'<g opacity="0">{fade(0.1 + i * 0.12)}' + R(x, 28, tw, 92, 14, CARD, LINE) + R(x, 28, tw, 5, 2, c)
                 + T(x + 22, 82, v, 42, c, weight=700) + T(x + 22, 106, l, 13, MUTED) + '</g>')
    p.append(f'<g opacity="0">{fade(0.6)}' + T(40, 164, "Linguagens por número de repositórios", 15, TXT, weight=600)
             + T(40, 183, "linguagem presente em ≥ 1% dos bytes do repositório", 12, DIM) + '</g>')
    p.append('<g class="chart" id="barchart">')
    for i, (lg, v) in enumerate(bars):
        y = by0 + i * row
        c = LANG_COLOR.get(lg, MUTED)
        wv = wmax * v / mx
        p.append(f'<g id="b{i}" opacity="0">{fade(0.7 + i * 0.05, 0.4)}<g class="pt bar hv">'
                 + R(x0 - 6, y - 3, 560, row - 3, 8, "none", extra='pointer-events="all"')
                 + T(x0 + 124, y + 15, LANG_LABEL.get(lg, lg), 13, MUTED, "end")
                 + R(x0 + 140, y + 2, wmax, 14, 7, CARD)
                 + R(x0 + 140, y + 2, 0, 14, 7, c, extra='class="fill hz"', inner=f'<animate attributeName="width" to="{wv:.0f}" begin="{0.9 + i * 0.07:.2f}s" dur="0.9s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0 0.2 1"/>')
                 + T(x0 + 148 + wv, y + 14, str(v), 12, TXT, mono=True) + '</g></g>')
    for i, (lg, v) in enumerate(bars):
        y = by0 + i * row
        exs, hidden = ex[lg]
        lines = ["ex.: " + ", ".join(exs)] if exs else ["exemplos em repositórios privados"]
        if exs and hidden:
            lines.append(f"+ {hidden} privado(s) não listado(s)")
        p.append(tooltip(x0 + 190, y + row - 2, lines, LANG_COLOR.get(lg, MUTED), 640, f"bt{i}",
                         title=f"{LANG_LABEL.get(lg, lg)}: {v} repositórios", width=360))
    p.append('</g>')
    p.append(f'<g opacity="0">{fade(0.6)}' + T(pt_x0 - 30, 164, "Repositórios criados por ano", 15, TXT, weight=600)
             + T(pt_x0 - 30, 183, "passe o mouse nos pontos", 12, DIM) + '</g>')
    p.append(L(pt_x0 - 20, base, pt_x0 + pt_w + 20, base, LINE))
    for g in (0, 0.5, 1):
        yy = base - ph * g
        p.append(L(pt_x0 - 20, f"{yy:.0f}", pt_x0 + pt_w + 20, f"{yy:.0f}", LINE, 1, 'stroke-dasharray="2 5" opacity="0.6"'))
        p.append(T(pt_x0 - 28, f"{yy+4:.0f}", f"{round(pk*g)}", 12, DIM, "end", True))
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = line + f" L{pts[-1][0]:.1f},{base} L{pts[0][0]:.1f},{base} Z"
    p.append(f'<path d="{area}" fill="url(#ar)" opacity="0" pointer-events="none"><animate attributeName="opacity" to="1" begin="1.6s" dur="0.8s" fill="freeze"/></path>')
    p.append(f'<path d="{line}" pathLength="1" fill="none" stroke="url(#ln)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1" pointer-events="none">'
             f'<animate attributeName="stroke-dashoffset" to="0" begin="0.9s" dur="1.4s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.3 0 0.2 1"/></path>')
    p.append('<g class="chart" id="linechart">')
    cols = [PINK if y == ylist[-1] else (SKY if int(y) >= 2024 else LAVENDER) for y in ylist]
    for i, (y, (px, py)) in enumerate(zip(ylist, pts)):
        col = cols[i]
        p.append(f'<g id="y{i}" opacity="0">{fade(1.2 + i * 0.12, 0.4)}<g class="pt dot hv">'
                 + C(f"{px:.1f}", f"{py:.1f}", 18, "none", 'pointer-events="all"')
                 + C(f"{px:.1f}", f"{py:.1f}", 6, BG, f'class="hl" stroke="{col}" stroke-width="2.5"')
                 + C(f"{px:.1f}", f"{py:.1f}", 3, col, 'class="hz"')
                 + T(f"{px:.1f}", f"{py-14:.1f}", str(years[y]), 12, TXT, "middle", True)
                 + T(f"{px:.1f}", base + 20, y, 12, MUTED, "middle", True) + '</g></g>')
    for i, (y, (px, py)) in enumerate(zip(ylist, pts)):
        col = cols[i]
        pv = priv_by_year.get(y, 0)
        lines = [YEAR_CONTEXT.get(y, "")]
        if years[y]:
            lines.append(f"{pv} privado(s), {years[y]-pv} público(s)")
        guide = L(f"{px:.1f}", f"{py:.1f}", f"{px:.1f}", base, col, 1.5, 'stroke-dasharray="4 4"')
        inner = tooltip(px, base + 34, lines, col, W2, f"yin{i}", title=f"{y}: {years[y]} repositório(s)", width=330, hidden=False)
        p.append(f'<g class="tip" id="yt{i}">{guide}{inner}</g>')
    p.append('</g>')
    cap = (f"O gráfico mede só repositórios das duas contas (@allankltsn e @AllanKT) visíveis pela API do GitHub: {n} únicos, {npriv} deles privados, "
           "sem forks duplicados, sem bibliotecas versionadas e sem repositórios de terceiros. "
           "Java e LaTeX fazem parte da stack, mas não estão em repositórios mensuráveis. "
           f"Abaixo de 1% dos bytes e fora da contagem: {', '.join(minor)}.")
    for i, ln in enumerate(wrap(cap, 175)):
        p.append(f'<g opacity="0">{fade(2.4)}' + T(40, H2 - 54 + i * 18, ln, 12, DIM) + '</g>')
    p.append('</svg>')
    return "\n".join(p), dict(n=n, nl=nl, years=years, npriv=npriv, minor=minor)
