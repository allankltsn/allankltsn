"""Painel de stack (seção 01): chips pastel com logos simple-icons (CC0), fade-in
escalonado e linha de detalhe no hover. Só fatos do currículo e dos repositórios.

Para acrescentar uma tecnologia: edite CATS (rótulo, slug do logo em assets/logos ou None, detalhe).
"""
from svgkit import *  # noqa: F401,F403

# (categoria, cor, [(rótulo, logo, detalhe)])
CATS = [
    ("IA aplicada", MINT, [
        ("Agno", None, "NuageIT · agentes autônomos e times de agentes; estudo no repositório agno_study"),
        ("LangChain", "langchain", "NuageIT · agentes autônomos para diferentes segmentos de mercado"),
        ("Amazon Bedrock", None, "NuageIT · agentes em Python com Agno, LangChain e Bedrock"),
        ("RAG", None, "NuageIT · agentes com recuperação de contexto"),
        ("Bancos vetoriais", None, "NuageIT · usados junto com RAG nos agentes"),
        ("Prompt engineering", None, "NuageIT · agentes e workflows com times de agentes"),
        ("scikit-learn", None, "IC, TCC e estudos 2018–2020 · KNN, Naive Bayes e SVM"),
        ("NLTK", None, "Text-Mining-and-NLP · limpeza, stemming e vetorização"),
    ]),
    ("Dev com IA", LAVENDER, [
        ("Claude Code", "claude", "fluxo diário · um dos dois adapters da guilda"),
        ("Codex", "openai", "fluxo diário · o outro adapter da guilda"),
        ("Kiro", None, "kit setup_kiro · hooks, steering e skills (separado da guilda)"),
        ("Spec-driven", None, "história, spec e plano aprovados antes do código"),
        ("Orquestração multiagente", None, "guilda · 28 papéis; o principal orquestra e não implementa"),
    ]),
    ("Linguagens", SKY, [
        ("Python", "python", "{Python} repositórios · NuageIT, ISH Tech e Stefanini"),
        ("TypeScript", "typescript", "{TypeScript} repositórios nas duas contas"),
        ("JavaScript / Node.js", "nodedotjs", "{JavaScript} repositórios · Node.js na Stefanini (REST e GraphQL)"),
        ("Java", "openjdk", "listado no currículo · fora dos repositórios mensuráveis"),
        ("C", "c", "{C} repositórios · ex.: Programacao-Paralela"),
        ("C++", "cplusplus", "{Cpp} repositórios · ex.: Algoritimo_Genetico, competitive_programming"),
        ("C#", None, "listado no currículo"),
        ("SQL / PL/pgSQL", "postgresql", "{PLpgSQL} repositórios com PL/pgSQL"),
        ("Shell", "gnubash", "{Shell} repositórios · automação e hooks"),
        ("LaTeX", None, "listado como skill · fora dos repositórios mensuráveis"),
    ]),
    ("Cloud AWS", PEACH, [
        ("Lambda", "awslambda", "Stefanini, ISH Tech e NuageIT · funções com arquitetura orientada a eventos"),
        ("API Gateway", "amazonapigateway", "repositório aws_apigateway_authenticator (2024)"),
        ("SQS", None, "filas nas arquiteturas de eventos da Stefanini"),
        ("S3", None, "listado no currículo"),
        ("DynamoDB", None, "repositórios python-dynamo e aws_apigateway_authenticator"),
        ("RDS", None, "listado no currículo"),
        ("Batch", None, "AWS Batch · tarefas de computação em lote"),
        ("CloudFront", None, "listado no currículo"),
        ("Lex", None, "listado no currículo"),
        ("EKS", None, "listado no currículo · Kubernetes desde o estágio na Stefanini"),
    ]),
    ("Infra e DevOps", PINK, [
        ("Terraform", "terraform", "IaC · deploys contínuos na Stefanini e provisionamento na NuageIT"),
        ("CloudFormation", None, "IaC na AWS · NuageIT e ISH Tech"),
        ("CDK", None, "IaC na AWS · NuageIT e ISH Tech"),
        ("Docker", "docker", "serviços em containers (CaaS) desde a Stefanini"),
        ("Kubernetes", "kubernetes", "orquestração de containers desde o estágio (2018)"),
        ("OpenTelemetry", "opentelemetry", "repositório fastapi-observability-opentelemetry"),
        ("CI/CD", None, "entrega contínua com DevSecOps"),
    ]),
    ("Dados", BUTTER, [
        ("PostgreSQL", "postgresql", "SQL desde o estágio na Stefanini"),
        ("MySQL", None, "SQL desde o estágio na Stefanini"),
        ("MongoDB", "mongodb", "NoSQL desde o estágio na Stefanini"),
        ("Elasticsearch", "elasticsearch", "NoSQL desde o estágio na Stefanini"),
    ]),
    ("Arquitetura", AQUA, [
        ("Microsserviços", None, "APIs REST em containers, da Stefanini à NuageIT"),
        ("Event-driven", None, "marketplace de consórcio (Stefanini), Lambda e filas"),
        ("REST / GraphQL", "graphql", "Stefanini · APIs em Node.js e Python"),
        ("SOLID", None, "controle de qualidade na Stefanini e na ISH Tech"),
        ("Clean Code", None, "controle de qualidade na Stefanini e na ISH Tech"),
        ("DevSecOps", None, "Stefanini, ISH Tech e NuageIT"),
    ]),
]


def logo_use(slug, x, y, size, used):
    if not logo_path(slug):
        return ""
    used.add(slug)
    return f'<use href="#lg-{slug}" transform="translate({x:.1f} {y:.1f}) scale({size/24:.3f})"/>'


def build():
    D = load_public()
    counts = {k.replace("C++", "Cpp"): v["repos"] for k, v in D["by_language"].items()}
    W = 1200
    lab_x, chip_x0, chip_x1 = 40, 250, 1160
    ch, hg, vg = 34, 10, 10
    rows, items_flat = [], []
    y, idx = 30, 0
    for cat, col, its in CATS:
        placed, x, yy = [], chip_x0, 0
        for lab, lg, det in its:
            w = text_width(lab, 13, True) + 32 + (24 if lg else 0)
            if x + w > chip_x1:
                x, yy = chip_x0, yy + ch + vg
            placed.append((lab, lg, x, yy, w, idx))
            items_flat.append((col, lab, det.format_map(counts)))
            x += w + hg
            idx += 1
        h = yy + ch
        rows.append((cat, col, y, placed, h, len(its)))
        y += h + 26
    by = y + 4
    H = by + 70
    css = (BASE_CSS + ".chart:hover .pt:not(:hover){opacity:.4}"
           ".pt:hover rect{stroke:#fff;stroke-width:2;filter:drop-shadow(0 0 6px rgba(255,255,255,.6))}.chart:hover .hint{opacity:0}"
           ".pt text{fill:%s;font-size:13px;font-weight:600}use{fill:%s}.dt{font-size:15px;font-weight:700}.dd{font-size:13px;fill:%s}" % (INK, INK, TXT)
           + tip_rule("c", "d", range(idx)))
    used = set()
    p = [""]
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/><g class="chart">')
    for r, (cat, col, ry, placed, h, cnt) in enumerate(rows):
        t0 = 0.1 + r * 0.18
        p.append(f'<g opacity="0">{fade(round(t0,2),0.5)}' + R(lab_x, ry, 4, h, 2, col)
                 + T(lab_x + 18, ry + 20, cat, 16, col, weight=700) + T(lab_x + 18, ry + 38, f"{cnt} itens", 12, DIM, mono=True) + '</g>')
        if r:
            p.append(L(lab_x, ry - 13, W - 40, ry - 13, LINE, 1, 'opacity="0.7"'))
        for lab, lg, x, yy, w, i in placed:
            t = t0 + 0.08 + (i % 10) * 0.05
            tx = x + 15 + (24 if lg else 0)
            p.append(f'<g id="c{i}" opacity="0"><animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".4s" fill="freeze"/><g class="pt hv">'
                     + R(f"{x:.0f}", ry + yy, f"{w:.0f}", ch, 17, col)
                     + (logo_use(lg, x + 13, ry + yy + 8, 18, used) if lg else C(f"{x+14:.0f}", ry + yy + 17, 3, INK, 'opacity=".45"'))
                     + f'<text x="{tx if lg else x + 24:.0f}" y="{ry + yy + 22}">{esc(lab)}</text></g></g>')
    # barra de detalhe: fundo fixo e um bloco de texto por chip (irmão posterior do chip)
    p.append(R(40, by, W - 80, 50, 12, CARD, LINE, 1.2))
    for i, (col, lab, det) in enumerate(items_flat):
        p.append(f'<g class="tip" id="d{i}"><text class="dt" fill="{col}" x="64" y="{by+21}">{esc(lab)}</text>'
                 f'<text class="dd" x="64" y="{by+40}">{esc(det)}</text></g>')
    dash = 'stroke-dasharray="4 5"'
    p.append(f'<g class="hint" pointer-events="none">{R(40, by, W - 80, 50, 12, "none", LINE, 1, dash)}'
             + T(W / 2, by + 30, "passe o mouse sobre uma tecnologia para ver onde ela foi usada", 13, DIM, "middle") + '</g>')
    p.append('</g></svg>')
    defs = "".join(f'<path id="lg-{g}" d="{logo_path(g)}"/>' for g in sorted(used))
    p[0] = svg_open(W, H, "Stack por área: IA aplicada, desenvolvimento com IA, linguagens, cloud AWS, infra e DevOps, dados e arquitetura", css, defs)
    return "".join(p)
