# Diagramador — especificação (template fixo, sem LLM)

> Este papel NÃO é um LLM. Layout não se revisa com LLM todo dia (CLAUDE.md, regra 4).

## Função
Pegar as matérias prontas (saída do Redator) e encaixá-las no template visual fixo de
`template/`, gerando a edição HTML do dia em `edicoes/`.

## Entrada
Lista de matérias prontas (contrato docs/ARQUITETURA.md §6), já ordenadas pelo Editor-chefe.

## Saída
`edicoes/AAAA-MM-DD.html` (ou índice + páginas), pronto para o GitHub Pages.

## Regras
- O visual mora no template. O Diagramador só preenche slots — não inventa layout.
- Nenhuma chamada de LLM aqui.
- A beleza é resolvida uma vez, no template; ajustes são feitos no template, não por edição.
