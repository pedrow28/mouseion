# template/ — o visual fixo da revista

A beleza é resolvida **uma vez** aqui (CLAUDE.md, regra 4). O Diagramador só preenche slots;
nenhum ajuste estético é feito por edição. Toda edição herda este visual automaticamente —
basta editar `estilo.css` e todas as edições (passadas e futuras) mudam juntas.

Arquivos:
- `base.html` — esqueleto da edição (masthead, sumário, blocos por editoria). **Não mexa nas
  classes nem nos marcadores `<!-- SLOT:x -->`**: o diagramador depende deles.
- `estilo.css` — identidade visual completa.

## Direção de arte — "a casa das Musas"

Revista literária erudita: papel marfim com grão, tinta quente, **ouro de manuscrito
iluminado** como acento da marca, serifa de alto contraste. Sem dependência de imagem externa
— os ornamentos são **SVG vetorial embutido no CSS** (nítidos na tela e na impressão).

- **Tipografia:** `Fraunces` (display — masthead, títulos, "ideia central"), `Spectral`
  (corpo de leitura), `Archivo` (vinhetas/rótulos em caixa-alta espaçada). Algarismos
  old-style ligados.
- **Cor:** marfim `--papel`, tinta quente `--tinta`, acento-marca `--ouro`. Cada editoria
  tem seu acento herança (`--c-saude` … `--c-vendas`), exposto como `--accent` via a classe
  `.e-xxx`.
- **Emblemas clássicos:** a lira das Musas no masthead; e um emblema por editoria
  (bastão de Asclépio, constelação de nós, coluna dórica, compasso, profundezas, coruja de
  Atena, tocha, lâmpada votiva, elos) como marca-d'água no cabeçalho — definidos em
  `--emblema` e tingidos com `--accent` por máscara CSS.
- **Estrutura editorial:** masthead com fólio rulado · sumário numerado como índice de
  revista · fleurão `❧` entre editorias · cartão "Para guardar" escuro com filete dourado ·
  capitular na matéria de abertura quando a edição abre em notícia.

Para mexer no visual, edite só as variáveis em `:root` (cores, fontes, medida) ou os blocos
de componente. A revelação na carga respeita `prefers-reduced-motion`; há estilos de
impressão dedicados.
