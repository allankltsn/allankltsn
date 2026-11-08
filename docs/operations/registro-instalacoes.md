# Registro de instalações

Local: `docs/operations/registro-instalacoes.md`. Regra (`.engineering/policies/installations.md`): nada é instalado, habilitado ou concedido sem proposta, aprovação explícita e uma linha aqui, no mesmo turno.

## Instalado ou habilitado
| Data (UTC) | O quê | Origem | Versão/commit | Escopo (projeto/usuário/global) | Aprovado por | Arquivos/configurações alterados | Como remover | Verificação |
|---|---|---|---|---|---|---|---|---|
| 2026-11-07 | 23 ícones SVG de marcas em `assets/logos/` (lista e sha256 abaixo): dados de path SVG, sem código executável | `https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/<slug>.svg` (pacote npm `simple-icons`, baixados só os arquivos individuais; o pacote não foi instalado) | simple-icons 13.21.0 (fixada); o `package.json` da mesma versão declara licença CC0-1.0 e repositório `github.com/simple-icons/simple-icons` | projeto (só este repositório); embutidos no SVG gerado, nada é carregado em tempo de execução | Allan (o usuário), em chat, em 2026-11-08, ao dizer "continue" depois de o download dos logos ter sido nomeado | `assets/logos/*.svg` (novos), `tools/fetch_logos.py` (novo), `tools/stack_panel.py`, `tools/svgkit.py` e `assets/stack.svg` (usam os paths) | apagar `assets/logos/` e `tools/fetch_logos.py`, trocar os logos por pontos em `tools/stack_panel.py` e regenerar com `python tools/gen_svgs.py assets` | `python tools/fetch_logos.py` baixa de novo, confere sha256 e recusa arquivo que não comece com `<svg` ou tenha `<script`, `on...=` ou href externo (saída: 23 ok, exit 0, em 2026-11-08); todos os SVGs de `assets/` são lidos como XML sem `<script`, `@import` nem `href` externo |

### Necessidade e adoção
- **Necessidade:** o painel de stack da seção 01 usa logos de marca nos chips; o repositório não tinha nenhum, e desenhá-los à mão seria pior. Lacuna registrada no briefing da tarefa. Os três logos que o painel atual não embute (amazonwebservices, amazonsqs, amazondynamodb) ficaram em `assets/logos/` para uso futuro e podem ser apagados.
- **Procedência:** projeto público e identificável (simple-icons); repositório e licença conferidos no `package.json` da versão baixada.
- **Adoção:** não medida nesta sessão (estrelas e downloads não foram coletados; não havia autorização de rede além de `cdn.jsdelivr.net`). Estado: não verificado.
- **Revisão de segurança:** rodada 1 do gate SEC aberta sobre este registro (achados SEC-04 e SEC-06); confirmação independente pendente, não aprovada pelo autor. Verificações do autor: arquivos pequenos de um `<path>` cada, sem script, sem atributo `on...=` e sem href externo (checagem automática em `tools/fetch_logos.py`).
- **Reversibilidade:** apagar os arquivos; não há desinstalação de pacote porque nada foi instalado.
- **Marcas:** os arquivos são CC0, mas as marcas continuam sendo propriedade de seus donos.

### sha256 dos 23 logos (simple-icons 13.21.0)
| arquivo | sha256 |
|---|---|
| amazonapigateway.svg | `0e6fbe7a5a18480443c888bb7996625475352103a90a30a49f2bc356a301a557` |
| amazondynamodb.svg | `b1ccfa7134591728f9532d56669eeb1e87433edaeb518d3c49619ff113f4ea45` |
| amazonsqs.svg | `d4fdea1e6f3ce16b31d7f870229f2cfe14a5b0311849f92e54adc7695471817f` |
| amazonwebservices.svg | `f67734a0f5a7f925c84b6a9ea6e5489fe7af96e4ae167da6b71506a5d6afcab4` |
| awslambda.svg | `3d2a1a33cacaec01728917af5dd1f94e9d77c85f3d2708474df0f6efa9d50670` |
| c.svg | `fde4284070eedf24f3acc2f78368b8c25a204f9a1b8831caaae4652c3e716c88` |
| claude.svg | `2d6fda79eb18ddccca35b799eeb3cece0dfabc22520ce3b10abd25668df9fa93` |
| cplusplus.svg | `adf33f5026f3f70d54f1068cb5d1a790c37b2105cbe728edd170251759d13f18` |
| docker.svg | `65571291c261ef869c31540a38f3ca0f0ee3bb73f179c172211c8860f19a6359` |
| elasticsearch.svg | `f866863bb80c3f1e22cb49541442c9db2112bba74b8c1210328bd3536984e6a3` |
| gnubash.svg | `edee96774ff71b672c429c28eb092ab13373677157c86abe7edb0dd699e07986` |
| graphql.svg | `fc8ca4d195a8a79470540edf33677e24f6113b8b8d9b442acc5f62b57a2951cb` |
| kubernetes.svg | `ceee2f4e87fa1533600672190c156194039f744fa9b5da10e83f002178e84b47` |
| langchain.svg | `6d8347547ea7e96b9d183d28a0a4068d329250724aecd260674d09339a6b5fcf` |
| mongodb.svg | `6698757ee85997e8167b2eacaff8395d6987954185488f2e90b88ef387fec6c7` |
| nodedotjs.svg | `021851b758cde7d3e04819c3ac02047d0ff281c712e8387afa0c76a6dac6db6c` |
| openai.svg | `2b4a04ddc2395b20d168694d3850ce2050a702c4a0cdeb4d8b31b9a970481a8c` |
| openjdk.svg | `31c94bd8f864b018d9733c251df186f36e9a0036e43f78d0656895108d438bb3` |
| opentelemetry.svg | `1e93836eeedaf02fb985130ed05c4d692c66ff56269f50af8478a219645ee741` |
| postgresql.svg | `c8ccadbd88c9312c2ad3734c4861b31d3485ce179ee91d64793143f83cfa745c` |
| python.svg | `ad9468e1c4903f73ae7eebfbe980f0f727a10db695be3d914e7d8bd25356a862` |
| terraform.svg | `9c3737d360a174afec8fa0208332a3991f087ea0b7bacb1eea16598883e1a730` |
| typescript.svg | `7f023e8d1e767370306ec9437d2de5d5af97491d6208dd7799a3808a7c10a36a` |

## Tentado, mas não instalado
| Data | O quê | Motivo (cancelado/bloqueado/rejeitado na revisão de segurança) | Alternativa usada |
|---|---|---|---|
| 2026-11-07 | ícones csharp, amazoncloudfront, cloudfront, awscloudformation, aws, kiro, nltk, aws-lex, amazonlex (mesma versão do simple-icons) | não existem na versão 13.21.0 (HTTP 404), nada foi gravado | chip com ponto colorido, sem logo |
| 2026-11-07 | ícones javascript, react, amazoncloudwatch, awsfargate, awsorganizations, anthropic, spring, scikitlearn, latex, mysql, amazons3, githubactions, amazonrds, amazoneks | baixados e removidos depois: não usados ou pesados demais para manter `stack.svg` abaixo de 50 KB | chip com ponto; os badges do shields.io mostram o logo quando o serviço o oferece |
| 2026-11-08 | chamadas de teste ao shields.io (34 URLs com `&logo=`) | só leitura de imagens remotas, nada instalado | `&logo=` mantido apenas onde a resposta tem `<image` |

## Arquivos temporários fora do repositório
| Caminho | Criado para | Pode apagar depois de |
|---|---|---|
| `C:/Users/Allan/AppData/Local/Temp/claude/acb806183c039203/fe315104-ec0c-4519-a148-305aa0f9698d/scratchpad/` (shot.sh, PNGs de conferência, `head.md`, `urls.txt`, `badge_result.txt`, `hashes.txt`, cópias de dados do GitHub) | capturas de tela de conferência no Edge headless e rascunhos | o fim da sessão (nada ali é necessário para regenerar) |
| perfil temporário do Edge headless (criado e removido pelo próprio navegador) | capturas de tela | imediatamente |

Nenhum pacote foi instalado (`pip`, `npm`): os geradores usam só a biblioteca padrão do Python. Os badges do shields.io no README são imagens remotas carregadas pelo navegador de quem lê, sem instalação local.

## Arquivos alterados nesta entrega
`README.md`, `.gitignore`, `docs/operations/registro-instalacoes.md`, `tools/` (`palette.py`, `svgkit.py`, `charts_numbers.py`, `stack_panel.py`, `guilda_flow.py`, `gen_svgs.py`, `gen_cards.py`, `gen_readme_badges.py`, `fetch_logos.py`, `make_public_data.py`, `github_public.json`; `stats.json` removido) e `assets/**` regenerados.
