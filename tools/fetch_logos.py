"""Baixa os ícones simple-icons (CC0) usados no painel de stack para assets/logos, com verificação.

Uso: python tools/fetch_logos.py   (só biblioteca padrão; rede só para cdn.jsdelivr.net)
Versão fixada para reprodutibilidade. Cada arquivo é recusado (e não é gravado) se:
o sha256 não bate com o esperado, não começa com "<svg", ou contém <script, atributos on...= ou href externo.
Registro: docs/operations/registro-instalacoes.md
"""
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

VERSION = "13.21.0"
EXPECTED = {
    "amazonapigateway": "0e6fbe7a5a18480443c888bb7996625475352103a90a30a49f2bc356a301a557",
    "amazondynamodb": "b1ccfa7134591728f9532d56669eeb1e87433edaeb518d3c49619ff113f4ea45",
    "amazonsqs": "d4fdea1e6f3ce16b31d7f870229f2cfe14a5b0311849f92e54adc7695471817f",
    "amazonwebservices": "f67734a0f5a7f925c84b6a9ea6e5489fe7af96e4ae167da6b71506a5d6afcab4",
    "awslambda": "3d2a1a33cacaec01728917af5dd1f94e9d77c85f3d2708474df0f6efa9d50670",
    "c": "fde4284070eedf24f3acc2f78368b8c25a204f9a1b8831caaae4652c3e716c88",
    "claude": "2d6fda79eb18ddccca35b799eeb3cece0dfabc22520ce3b10abd25668df9fa93",
    "cplusplus": "adf33f5026f3f70d54f1068cb5d1a790c37b2105cbe728edd170251759d13f18",
    "docker": "65571291c261ef869c31540a38f3ca0f0ee3bb73f179c172211c8860f19a6359",
    "elasticsearch": "f866863bb80c3f1e22cb49541442c9db2112bba74b8c1210328bd3536984e6a3",
    "gnubash": "edee96774ff71b672c429c28eb092ab13373677157c86abe7edb0dd699e07986",
    "graphql": "fc8ca4d195a8a79470540edf33677e24f6113b8b8d9b442acc5f62b57a2951cb",
    "kubernetes": "ceee2f4e87fa1533600672190c156194039f744fa9b5da10e83f002178e84b47",
    "langchain": "6d8347547ea7e96b9d183d28a0a4068d329250724aecd260674d09339a6b5fcf",
    "mongodb": "6698757ee85997e8167b2eacaff8395d6987954185488f2e90b88ef387fec6c7",
    "nodedotjs": "021851b758cde7d3e04819c3ac02047d0ff281c712e8387afa0c76a6dac6db6c",
    "openai": "2b4a04ddc2395b20d168694d3850ce2050a702c4a0cdeb4d8b31b9a970481a8c",
    "openjdk": "31c94bd8f864b018d9733c251df186f36e9a0036e43f78d0656895108d438bb3",
    "opentelemetry": "1e93836eeedaf02fb985130ed05c4d692c66ff56269f50af8478a219645ee741",
    "postgresql": "c8ccadbd88c9312c2ad3734c4861b31d3485ce179ee91d64793143f83cfa745c",
    "python": "ad9468e1c4903f73ae7eebfbe980f0f727a10db695be3d914e7d8bd25356a862",
    "terraform": "9c3737d360a174afec8fa0208332a3991f087ea0b7bacb1eea16598883e1a730",
    "typescript": "7f023e8d1e767370306ec9437d2de5d5af97491d6208dd7799a3808a7c10a36a",
}
BAD = re.compile(r"<script|\son\w+\s*=|href\s*=\s*[\"']?(?:https?:)?//|xlink:href\s*=\s*[\"']?(?:https?:)?//", re.I)
out = Path(__file__).resolve().parent.parent / "assets" / "logos"
out.mkdir(parents=True, exist_ok=True)
failed = []
for slug, sha in EXPECTED.items():
    url = f"https://cdn.jsdelivr.net/npm/simple-icons@{VERSION}/icons/{slug}.svg"
    data = urllib.request.urlopen(url, timeout=30).read()
    text = data.decode("utf-8", "replace")
    problems = []
    if hashlib.sha256(data).hexdigest() != sha:
        problems.append("sha256 diferente do esperado")
    if not text.lstrip().startswith("<svg"):
        problems.append("não começa com <svg")
    if BAD.search(text):
        problems.append("contém <script, on...= ou href externo")
    if problems:
        failed.append(slug)
        print("RECUSADO", slug, "; ".join(problems))
        continue
    (out / f"{slug}.svg").write_bytes(data)
    print("ok", slug)
sys.exit(1 if failed else 0)
