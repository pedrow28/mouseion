# estado/ — a memória editorial (fonte da verdade)

Tudo o que evita repetição e mantém o currículo no lugar mora aqui. **Sempre versionado.**
Leia antes de gerar, grave depois. Ver `docs/ARQUITETURA.md` §5.

- `<editoria>/ledger.jsonl` — itens de notícia já publicados (dedup por hash).
- `<editoria>/syllabus.md` + `cursor.json` — currículo e onde paramos.
- `imersao/tema_atual.json` + `imersao/arquivo/` — slot rotativo.
