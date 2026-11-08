"""Paleta pastel única do perfil. Importada por todos os geradores.

Texto sobre preenchimento pastel usa sempre INK (o fundo escuro).
Contrastes (WCAG): TXT/MUTED/DIM sobre BG e CARD >= 4.5:1; INK sobre qualquer pastel >= 9:1.
"""

# superfícies
BG = "#1f1d2b"      # fundo dos SVGs (cada SVG carrega o próprio fundo)
CARD = "#2a2838"    # cartões e painéis
NODE = "#181624"    # área interna mais funda (ilustrações, nós)
LINE = "#3b3950"    # linhas e bordas
INK = "#1f1d2b"     # texto sobre pastel

# texto
TXT = "#f4f1fb"
MUTED = "#b7b2cc"
DIM = "#9a96b4"

# pastéis
MINT = "#b8f2d8"
SKY = "#a9cdfb"
LAVENDER = "#cdb8f6"
PEACH = "#ffcfa8"
PINK = "#ffb3cf"
BUTTER = "#fbeaa0"
CORAL = "#ffb0a8"
AQUA = "#a8ecf0"

PASTELS = [MINT, SKY, LAVENDER, PEACH, PINK, BUTTER, CORAL, AQUA]

# nomes usados nos geradores (mapeiam a família antiga para a pastel)
TEAL, BLUE, PURPLE, AMBER, GREEN, RED = AQUA, SKY, LAVENDER, PEACH, MINT, CORAL

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# cores de linguagem (pastel), usadas nos cards e nos gráficos
LANG_COLOR = {
    "Python": SKY, "JavaScript": BUTTER, "TypeScript": AQUA, "Shell": MINT, "HTML": CORAL,
    "CSS": LAVENDER, "Jupyter Notebook": PEACH, "Dockerfile": "#9fd4f5", "C++": PINK, "C": "#c9d6ea",
    "Java": "#ffd9a0", "PLpgSQL": "#b9c7f7", "HCL": "#d8b6f5", "PowerShell": "#a3dcc7",
}


def badge_hex(c):
    """Cor sem '#', para URLs do shields.io."""
    return c.lstrip("#")
