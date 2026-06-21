# fontes/ — scripts de coleta (código, sem LLM)

Onde vivem os coletores do Pesquisador. Comece colando aqui os scripts Python existentes do
Pedro para o **DOU** e o **IOF-MG**. Cada coletor deve devolver o contrato de material bruto
(docs/ARQUITETURA.md §6) e respeitar o dedup contra `estado/<editoria>/ledger.jsonl`.

Sugestão de organização:
- `dou.py` — coleta Diário Oficial da União
- `iof_mg.py` — coleta Imprensa Oficial de MG
- `ia.py` — fontes do editorial IA (‹DECIDIR›)
- `comum.py` — hash, normalização, leitura/escrita de ledger
