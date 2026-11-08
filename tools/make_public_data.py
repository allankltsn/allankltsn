"""Gera tools/github_public.json a partir de tools/github_data.json (entrada local, ignorada pelo git).

Regras:
- repositórios públicos mantêm nome, linguagem principal, ano e a lista de linguagens (>= 1% dos bytes);
- repositórios privados entram só em agregados (por linguagem, por ano e total), sem nome, descrição nem data;
- repositórios de terceiros (donos de outras contas, sem commits do autor) ficam de fora de tudo.
Os geradores usam github_public.json; o arquivo de entrada não é necessário para regenerar os SVGs.
Uso: python tools/make_public_data.py
"""
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
OWN = ("allankltsn/", "AllanKT/")  # contas do autor
THRESHOLD = 0.01

src = json.loads((HERE / "github_data.json").read_text(encoding="utf-8"))
repos = [r for r in src["repos"] if r["repo"].startswith(OWN)]
excluded = sorted(r["repo"] for r in src["repos"] if not r["repo"].startswith(OWN))


def langs_over(r):
    tot = sum(r["languages"].values()) or 1
    return [l for l, b in sorted(r["languages"].items(), key=lambda t: -t[1]) if b / tot >= THRESHOLD]


by_lang, priv_by_lang, below = Counter(), Counter(), set()
for r in repos:
    ok = langs_over(r)
    below |= set(r["languages"]) - set(ok)
    for l in ok:
        by_lang[l] += 1
        if r["private"]:
            priv_by_lang[l] += 1
by_year = Counter(r["created"][:4] for r in repos)
priv_by_year = Counter(r["created"][:4] for r in repos if r["private"])
pub = [dict(repo=r["repo"], lang=r["lang"] if r["lang"] != "-" else None, year=r["created"][:4], fork=r["fork"], languages=langs_over(r))
       for r in repos if not r["private"]]
pub.sort(key=lambda r: r["repo"].lower())
out = {
    "note": "Agregado das contas allankltsn e AllanKT via API do GitHub. Linguagem contada com >= 1% dos bytes do repositório. Privados só em agregados. Terceiros excluídos.",
    "total_repos": len(repos),
    "private": sum(1 for r in repos if r["private"]),
    "excluded_third_party": len(excluded),
    "by_language": {l: {"repos": n, "private_repos": priv_by_lang[l]} for l, n in by_lang.most_common()},
    "by_year": dict(sorted(by_year.items())),
    "private_by_year": dict(sorted(priv_by_year.items())),
    "below_threshold_languages": sorted(below - set(by_lang)),
    "public_repos": pub,
}
(HERE / "github_public.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok", out["total_repos"], "repos;", out["private"], "privados; excluídos:", excluded)
print(dict(by_lang), out["by_year"], out["below_threshold_languages"])
