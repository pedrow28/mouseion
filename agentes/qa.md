# QA — especificação (lint estrutural, sem LLM)

> Checagem determinística. Não avalia estética — só estrutura.

## Função
Antes do commit, verificar que a edição do dia está estruturalmente sã.

## Checa
- Toda editoria habilitada para hoje tem conteúdo? (nenhuma seção vazia)
- Há link quebrado nas fontes?
- Matérias de Saúde têm fonte/link presentes?
- Cursores de currículo avançaram (não geraram a mesma aula de novo)?
- O ledger foi atualizado com o que saiu hoje?

## Saída
Relatório curto pass/fail. Se falhar, a edição não é publicada — registra o motivo.
