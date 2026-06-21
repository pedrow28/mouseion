# Pesquisador — especificação (código, sem LLM)

> Este papel NÃO é um LLM. É código determinístico. Esta é a especificação que o código cumpre.

## Função
Trazer matéria-prima para as editorias com fonte externa (Saúde, IA, e a coleta que alimenta
Ideias de Negócio). Nunca interpreta nem redige — só recupera e normaliza.

## Entrada
A pauta do dia (de qual editoria/seção coletar), vinda do Editor-chefe (planejamento).

## Saída (contrato — ver docs/ARQUITETURA.md §6)
Lista de objetos de material bruto:
```json
{"editoria":"saude","tipo":"noticia","url":"...","titulo":"...","texto_recuperado":"...","fonte":"DOU","data":"AAAA-MM-DD"}
```

## Regras
- **Dedup primeiro:** calcula o hash de cada item e descarta o que já existe em
  `estado/<editoria>/ledger.jsonl`.
- **Saúde:** `texto_recuperado` é obrigatório e deve vir da fonte oficial (DOU/IOF). Sem texto
  recuperado, o item não passa adiante.
- Fontes Saúde: scripts Python existentes do Pedro (ligar em `fontes/`).
- Fontes IA / Ideias de Negócio: ‹DECIDIR› (arXiv, blogs de labs, releases, RSS, MCP).
- Sem LLM. Sem juízo de valor. Só coleta + normalização + dedup.
