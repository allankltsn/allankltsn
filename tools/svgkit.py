"""Helpers compartilhados pelos geradores de SVG (sem dependências).

Hover: o GitHub exibe SVGs de README via <img>, onde só SMIL/CSS animam e não há
eventos de ponteiro. O hover aqui é CSS puro (:hover) dentro do próprio SVG e passa
a funcionar quando o arquivo é aberto sozinho (clique na imagem do README).
Tooltips ficam como irmãos POSTERIORES dos alvos, para pintarem por cima de tudo:
    #p3:hover ~ #t3 { opacity: 1 }
"""
import re
from pathlib import Path

from palette import *  # noqa: F401,F403

HERE = Path(__file__).resolve().parent
LOGOS = HERE.parent / "assets" / "logos"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def fade(begin, dur=0.5):
    return f'<animate attributeName="opacity" to="1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'


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


_NARROW, _WIDE = set("iljt.,;:!|'()[]/ fIr-"), set("mwMW")


def text_width(s, size=12, bold=False):
    """Largura estimada (px) de um texto em sans-serif; conservadora (+4%) para evitar estouro."""
    w = 0.0
    for ch in s:
        w += 0.30 if ch in _NARROW else 0.86 if ch in _WIDE else 0.66 if ch.isupper() else 0.56 if ch.isdigit() else 0.54
    return w * size * (1.07 if bold else 1.0) * 1.04


def fit(s, max_px, size=12, bold=False):
    """Trunca com reticências para caber em max_px (medido por text_width)."""
    if text_width(s, size, bold) <= max_px:
        return s
    while s and text_width(s + "…", size, bold) > max_px:
        s = s[:-1]
    return s.rstrip() + "…"


def load_public(path=None):
    import json
    return json.loads((Path(path) if path else HERE / "github_public.json").read_text(encoding="utf-8"))


def wrap(text, width):
    """Quebra simples por número de caracteres."""
    out, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > width:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


def svg_open(W, H, label, extra_style="", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="{SANS}" role="img" aria-label="{esc(label)}">'
            f'<style>{extra_style}</style><defs>{defs}</defs>')


BASE_CSS = (
    ".hv{cursor:pointer}"
    ".tip{opacity:0;pointer-events:none;transition:opacity .15s}"
    ".hz{transform-box:fill-box;transform-origin:center;transition:transform .18s ease,opacity .18s ease,stroke-width .18s}"
    # prefers-reduced-motion: o CSS desliga transições e esconde a decoração em loop (.mo: tokens, pulsos, brilhos).
    # Limitação: animações SMIL (<animate>) não obedecem a CSS; as que carregam sentido (fade-in, barras que crescem,
    # traços tracejados) continuam e terminam sozinhas, só as decorativas infinitas recebem a classe .mo.
    "@media (prefers-reduced-motion:reduce){.hz,.tip{transition:none}.mo{display:none}}"
)


def tip_rule(prefix_p, prefix_t, ids):
    """Regras CSS para tooltips irmãos posteriores: #p3:hover~#t3{opacity:1}."""
    return "".join(f"#{prefix_p}{i}:hover~#{prefix_t}{i}{{opacity:1}}" for i in ids)


def tooltip(x, y, lines, color, W, id_, title=None, width=None, hidden=True):
    """Cartão de tooltip (retângulo escuro + texto). Posiciona dentro do SVG (limita à largura W)."""
    n = len(lines) + (1 if title else 0)
    wd = width or max(150, int(max([text_width(s, 12) for s in lines + ([title] if title else [])]) + 32))
    h = 16 * n + 18
    tx = min(max(x - wd / 2, 8), W - wd - 8)
    ty = y
    o = [f'<g class="tip" id="{id_}">' if hidden else "<g>",
         R(f"{tx:.0f}", f"{ty:.0f}", wd, h, 10, CARD, color, 1.4),
         ]
    yy = ty + 22
    if title:
        o.append(T(f"{tx+14:.0f}", f"{yy:.0f}", title, 13, color, weight=700))
        yy += 16
    for s in lines:
        o.append(T(f"{tx+14:.0f}", f"{yy:.0f}", s, 12, TXT))
        yy += 16
    o.append("</g>")
    return "".join(o)


PREC = 1  # casas decimais dos ícones (18 px): 1 basta e reduz o tamanho do arquivo
NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def compact_path(d, prec=PREC):
    """Reserializa um path SVG com poucas casas decimais, entendendo os flags colados dos arcos."""
    out, i, cmd, idx = [], 0, "", 0
    first = True
    while i < len(d):
        ch = d[i]
        if ch.isalpha() and ch not in "eE":
            out.append(ch)
            cmd, idx, first, i = ch, 0, True, i + 1
        elif ch.isspace() or ch == ",":
            i += 1
        else:
            if cmd in "Aa" and idx % 7 in (3, 4):
                tok, i = ch, i + 1  # flag de arco: um único caractere 0/1
            else:
                m = NUM.match(d, i)
                tok, i = m.group(0), m.end()
                v = round(float(tok), prec)
                tok = f"{v:.{prec}f}".rstrip("0").rstrip(".") or "0"
                if tok.startswith("0."):
                    tok = tok[1:]
                elif tok.startswith("-0."):
                    tok = "-" + tok[2:]
                if tok == "-0":
                    tok = "0"
            sep = "" if (first or tok.startswith("-")) else " "
            out.append(sep + tok)
            first = False
            idx += 1
    return "".join(out)


def logo_path(slug):
    """Retorna o atributo d do <path> do ícone simple-icons salvo em assets/logos (ou None)."""
    f = LOGOS / f"{slug}.svg"
    if not f.exists():
        return None
    m = re.search(r'<path d="([^"]+)"', f.read_text(encoding="utf-8"))
    return compact_path(m.group(1)) if m else None


def logo(slug, x, y, size, fill):
    d = logo_path(slug)
    if not d:
        return ""
    s = size / 24
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.3f})" d="{d}" fill="{fill}"/>'
