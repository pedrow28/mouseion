# Molde de Aula

A anatomia de "uma aula de um dia". **Reusada em toda editoria de currículo** (Gestão, Imersão,
Mente, Família). É desenhada para *retenção*, não exposição — por isso os beats de recordação
e conexão não são opcionais.

## Os 7 beats

1. **Onde estamos** — Módulo X · Aula N/Total. (Visão geral antes do detalhe.)
2. **A ideia central** — *um* conceito, em uma frase.
3. **Desenvolvimento** — o conteúdo, curto, uma leitura só.
4. **Exemplo / aplicação** — um caso concreto (de preferência do mundo do Pedro).
5. **Conexão** — onde isso aparece no que ele já sabe / em outra editoria (o *latticework*).
6. **Recordação** — 1–2 perguntas de recall ativo, ou um desafio Feynman.
7. **Para guardar** — um cartão curto pro segundo cérebro / Anki.

### Variação por editoria
- **Família:** o beat 6 (Recordação) vira **micro-prática pra aplicar hoje**. O resto serve igual.
- **Imersão (pílulas):** desenvolvimento mais curto; mantém todos os beats.

### Ritmo de revisão
A cada ~5 aulas, um **dia de revisão**: recall do módulo inteiro, sem conteúdo novo. Isso
embute repetição espaçada no próprio currículo.

## Exemplo completo (Gestão, Aula 1)

> **Onde estamos:** Módulo 1 · Aula 1/5
>
> **A ideia central:** Gestão é tornar um grupo de pessoas capaz de produzir junto o que
> nenhuma produziria sozinha.
>
> **Desenvolvimento:** Drucker definiu gestão menos como controle e mais como tornar o trabalho
> produtivo e o trabalhador realizado. O gestor não é quem faz — é quem desenha as condições
> para os outros fazerem bem. Isso desloca o foco de "minha entrega" para "a entrega do sistema
> que coordeno".
>
> **Exemplo:** Na GCI da Fhemig, o resultado não é um contrato que *você* redige, mas o fluxo
> que faz oito contratos municipais correrem sem você no meio de cada um.
>
> **Conexão:** Liga ao "papéis vs. implementação" da própria revista — desenhar o sistema vale
> mais que executar cada peça.
>
> **Recordação:** Em 3 frases, explique a diferença entre "fazer o trabalho" e "gerir o
> trabalho".
>
> **Para guardar:** Gestão = tornar produtivo o esforço coletivo (Drucker), não fazer
> pessoalmente.

## Formato de saída
Cada aula é gerada como Markdown e entregue ao Diagramador conforme o contrato em
`docs/ARQUITETURA.md` (§6). O Redator nunca decide qual aula é "a de hoje" — isso vem do cursor
em `estado/<editoria>/cursor.json`.
