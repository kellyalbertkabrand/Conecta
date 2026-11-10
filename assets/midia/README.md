# Mídia do Conecta · Happy Conecta

Biblioteca com **todos os logotipos, fotos e vídeos** usados nos materiais do
Conecta (Núcleo de Negócios ACIGRA) e nos vídeos do Happy Conecta.

Origem: repositório SistemaKA, branch `claude/conecta-repository-7h00xx`, pasta
`conecta/midia/` (commit `93f3891`, 09/11/2026) e pasta `logotipos/` (commit
`987c96e`, 31/10/2026, mesmos arquivos de `logos/`). Trazida para cá em
09/11/2026 para que tudo do Conecta fique no repositório do Conecta.

> O logo oficial para **peças novas** continua sendo o de `assets/logo/`
> (regra do `CLAUDE.md`: nunca redesenhar nem recriar). Os logos do Conecta
> em `logos/conecta_e_parceiros/` são as versões usadas nos vídeos e banners.

## `logos/`

| Pasta | Conteúdo |
| --- | --- |
| `conecta_e_parceiros/` (8) | Conecta (nome e símbolo, azul e branco) · parceiros **ACIGRA** e **EMPREENDER** (azul e branco) |
| `nucleados_originais/` (33) | Logos coloridos originais dos 33 nucleados, PNG transparente (exceto os que têm fundo próprio da marca: Mundo Fit, Central de Imóveis, Zila, Fusoparq e Autock) |
| `happy_conecta/` | Logo do **Happy Conecta** ("Entre brindes e ideias") em PNG transparente, recortado em 10/11/2026 da arte original (`pdfs/Logo_Happy_Conecta.pdf`). Ver a tabela abaixo |
| `nucleados_branco_telao/` (33) | Os mesmos logos em versão branca/monocromática, tratados para fundo escuro (telão do Happy Hour). Numerados na ordem em que aparecem no vídeo |

### Logo Happy Conecta (`logos/happy_conecta/`)

| Arquivo | Uso |
| --- | --- |
| `happy-conecta-logo.png` | Cores originais (turquesa com brilho + frase em branco), fundo transparente. **Só sobre fundo escuro** (navy, preto, foto escura) |
| `happy-conecta-logo-branco.png` | Tudo branco, sem brilho. Fundo escuro ou foto |
| `happy-conecta-logo-marinho.png` | Tudo navy `#1B2A4A`, sem brilho. Fundo claro (warm `#FAF9F7`) |
| `happy-conecta-logo-com-fundo-original.jpg` | Recorte da arte original, com a foto das taças |
| `previa-versoes.png` | Prévia das três versões aplicadas |
| `recorte_happy.py` | Script que gerou os recortes (para refazer, se preciso) |

Tamanho: 1423 × 750 px. A fonte é um JPEG de 2480 px, então não há versão
vetorial. Para uso grande (banner, lona), peça o arquivo aberto a quem criou
a arte. O símbolo do Conecta dentro desse logo é parte da arte do evento: em
peças do Conecta continue usando `assets/logo/`.

## `fotos/` · 65 arquivos

| Pasta | Conteúdo |
| --- | --- |
| `visitas_1a1/` (35) | Visitas Conecta 1:1 |
| `livros_pitch/` (16) | Capas dos livros do Pitch do Livro |
| `eventos_externos/` (7) | Eventos externos (`ev_01` a `ev_05`) e Marcas & Líderes (`ml_01`, `ml_02`) |
| `capacitacoes/` (4) | Capacitações internas (`cap_02` a `cap_05`; não existe `cap_01`) |
| `sensibilizacao/` (1) | Sensibilização de entrada de novos nucleados |
| `visitas_tecnicas/` (1) | Visita técnica à Fusoparq |

## `videos/` · brutos usados nas montagens

| Pasta | Conteúdo |
| --- | --- |
| `pitch_livro/` (6) | Pitches do livro (`pv_01` a `pv_06`) |
| `marcas_e_lideres/` (2) | Participação no Marcas & Líderes (`mlvid_01`, `mlvid_02`) |
| `capacitacoes/` (1) | Capacitação interna (`capvid_01`) |

## `videos_finais/` · vídeos prontos

| Arquivo | Formato | Conteúdo |
| --- | --- | --- |
| `RAP_Conecta_Acoes.mp4` | 1920×1080 · 2 min 07 s · sem áudio | Retrospectiva "Atividades do Conecta 2026" (12 itens): Visitas 1:1, Visitas Técnicas, Pitch Livro (25 títulos), Pitch filmado, Marcas & Líderes, Mercopar, CEO de Si Mesmo, Capacitações e outros |
| `RAP_Conecta_HappyHour.mp4` | 1920×1080 · 1 min 42 s · sem áudio | Telão do Happy Hour (loop): realização Conecta + ACIGRA + Empreender, "Nossos nucleados" com os 33 logos e fechamento com cenas do ano |

Os scripts e textos de montagem desses dois vídeos **não foram guardados**:
só os MP4 finais. Para alterar um item, a montagem precisa ser refeita.

## `pdfs/`

- `Logo_Happy_Conecta.pdf`: logo do Happy Conecta sobre o fundo do vídeo.
- `Painelistas_Conecta.pdf`: imagem dos painelistas.

## Para manter

- Mídia nova do Conecta entra **aqui**, na pasta do tema, seguindo a numeração.
- Sempre que possível, registre data e nomes de quem aparece na foto: isso
  permite que a IA monte retrospectivas, relatórios e cards automaticamente.
- Limite do GitHub: 100 MB por arquivo. Vídeos maiores devem ser comprimidos
  antes de subir.
