"""Atualiza em README.md os badges shields.io pastel da seção 01 (dentro de <details>),
a partir de stack_panel.CATS. Uso: python tools/gen_readme_badges.py README.md
Entre os marcadores <!-- stack-badges:start --> e <!-- stack-badges:end -->.
"""
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stack_panel  # noqa: E402
from palette import INK, badge_hex  # noqa: E402

# slug do simple-icons no shields.io (quando difere do arquivo de logo local)
SHIELD_LOGO = {"Agno": None, "LangChain": "langchain", "Amazon Bedrock": "amazonwebservices", "scikit-learn": "scikitlearn",
               "Claude Code": "claude", "Codex": "openai", "Python": "python", "TypeScript": "typescript",
               "JavaScript / Node.js": "nodedotjs", "Java": "openjdk", "C": "c", "C++": "cplusplus", "SQL / PL/pgSQL": "postgresql",
               "Shell": "gnubash", "LaTeX": "latex", "Lambda": "awslambda", "API Gateway": "amazonapigateway", "SQS": "amazonsqs",
               "S3": "amazons3", "DynamoDB": "amazondynamodb", "RDS": "amazonrds", "EKS": "amazoneks", "Terraform": "terraform",
               "Docker": "docker", "Kubernetes": "kubernetes", "OpenTelemetry": "opentelemetry", "CI/CD": "githubactions",
               "PostgreSQL": "postgresql", "MySQL": "mysql", "MongoDB": "mongodb", "Elasticsearch": "elasticsearch",
               "REST / GraphQL": "graphql"}


# Logos que o shields.io realmente serve (conferido com curl em 2026-11-08: 34 URLs com &logo=, 24 com <image, 10 sem).
# Sem logo no shields (removidos do badge): linkedin, openai, awslambda, amazonapigateway, amazonsqs, amazons3,
# amazondynamodb, amazonrds, amazoneks, amazonwebservices. Reconferir antes de acrescentar slugs novos.
VERIFIED = {"claude", "langchain", "python", "typescript", "nodedotjs", "openjdk", "c", "cplusplus", "postgresql", "gnubash", "latex",
            "terraform", "docker", "kubernetes", "opentelemetry", "githubactions", "scikitlearn", "mysql", "mongodb", "elasticsearch", "graphql"}


def esc_label(t):
    return quote(t.replace("-", "--").replace("_", "__").replace(" ", "_"), safe="_-")


lines = []
for cat, col, items in stack_panel.CATS:
    lines.append(f"**{cat}**<br>")
    for lab, _logo, _det in items:
        url = f"https://img.shields.io/badge/{esc_label(lab)}-{badge_hex(col)}?style=flat-square&logoColor={badge_hex(INK)}"
        lg = SHIELD_LOGO.get(lab)
        if lg in VERIFIED:
            url += f"&logo={lg}"
        lines.append(f'<img src="{url}" alt="{lab}">')
    lines.append("<br><br>")
block = "\n".join(lines)
path = Path(sys.argv[1])
txt = path.read_text(encoding="utf-8")
a, b = "<!-- stack-badges:start -->", "<!-- stack-badges:end -->"
i, j = txt.index(a) + len(a), txt.index(b)
path.write_text(txt[:i] + "\n" + block + "\n" + txt[j:], encoding="utf-8")
print("ok", sum(len(i[2]) for i in stack_panel.CATS), "badges")
