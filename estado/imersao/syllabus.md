# Syllabus — Imersão: Probabilidade e Incerteza (pílulas)

> **Slot rotativo.** Ocupante atual da editoria Imersão (desde 2026-10-21). Ao concluir as 34
> pílulas, a trilha é arquivada (`estado/imersao/arquivo/`) e o tema troca (config em
> `tema_atual.json`). Formato: **pílula diária** — o molde dos 7 beats (`docs/MOLDE_AULA.md`),
> com desenvolvimento mais curto que uma aula plena. Revisão a cada ~5 pílulas. Lente recorrente:
> **Thauma** e decisões do dia a dia — pensar com números quando não se sabe.

Total: **34 pílulas** (28 de conteúdo + 6 de revisão), em 6 blocos.

---

## Bloco A — Fundamentos
- [ ] **Pílula 1 — O que é probabilidade.** Ideia central: probabilidade é a linguagem da incerteza — medir, de 0 a 1, o quão provável é algo, por frequência ou por grau de crença. (ref: Laplace)
- [ ] **Pílula 2 — Incerteza, risco e acaso.** Ideia central: nem todo "não sei" é igual — há risco mensurável, incerteza profunda e puro acaso, e tratá-los igual leva a erro.
- [ ] **Pílula 3 — Espaço amostral e eventos.** Ideia central: antes de calcular, enumere o que pode acontecer; metade dos erros nasce de esquecer um resultado possível.
- [ ] **Pílula 4 — Combinar probabilidades: E, OU, independência.** Ideia central: "e" multiplica, "ou" soma (com cuidado); e supor independência onde não há é a armadilha clássica.
- [ ] **Pílula 5 — Revisão do Bloco A.** Recall dos fundamentos.

## Bloco B — Taxas-base e Bayes
- [ ] **Pílula 6 — Probabilidade condicional.** Ideia central: P(A dado B) — a chance de algo muda quando você já sabe de outra coisa.
- [ ] **Pílula 7 — A taxa-base (o prior).** Ideia central: o que era provável antes de qualquer evidência; ignorá-la é o pecado capital do raciocínio sob incerteza.
- [ ] **Pílula 8 — O teorema de Bayes.** Ideia central: a evidência não substitui a crença anterior — ela a atualiza, na proporção do quanto é diagnóstica. (ref: Bayes)
- [ ] **Pílula 9 — O problema do teste médico.** Ideia central: num mal raro, um teste positivo ainda pode significar "provavelmente saudável" — a taxa-base manda.
- [ ] **Pílula 10 — Negligência da taxa-base.** Ideia central: a mente agarra a história vívida e esquece a frequência de fundo — o erro que Bayes corrige. (ref: Kahneman & Tversky)
- [ ] **Pílula 11 — Revisão do Bloco B.** Recall de condicional e Bayes.

## Bloco C — Distribuições
- [ ] **Pílula 12 — Média, mediana e a cauda que engana.** Ideia central: a média sozinha mente quando a distribuição é torta; a mediana costuma contar a verdade do "típico".
- [ ] **Pílula 13 — Variância e desvio-padrão.** Ideia central: não basta o centro — o quanto as coisas variam decide o risco.
- [ ] **Pílula 14 — A curva normal (e onde ela vale).** Ideia central: a sineta descreve bem o que é soma de muitos acasos pequenos — e falha feio onde não é.
- [ ] **Pílula 15 — A lei dos grandes números.** Ideia central: a média se estabiliza no longo prazo — mas isso nada diz sobre o próximo lance.
- [ ] **Pílula 16 — Caudas gordas e leis de potência.** Ideia central: em muitos sistemas, o raro extremo domina o resultado — e a intuição "normal" quebra. (ref: Pareto; Taleb)
- [ ] **Pílula 17 — Revisão do Bloco C.** Recall de distribuições.

## Bloco D — Falácias probabilísticas
- [ ] **Pílula 18 — A falácia do apostador.** Ideia central: a moeda não tem memória; "já deu cara cinco vezes, vem coroa" é superstição com cara de lógica.
- [ ] **Pílula 19 — Regressão à média.** Ideia central: o extremo tende a voltar ao normal sozinho — e nos faz creditar (ou culpar) a causa errada.
- [ ] **Pílula 20 — Correlação não é causa.** Ideia central: andar junto não é causar; pode haver um terceiro fator, ou puro acaso.
- [ ] **Pílula 21 — A falácia da conjunção (Linda).** Ideia central: "A e B" nunca é mais provável que "A" — mas a história plausível nos engana. (ref: Kahneman & Tversky)
- [ ] **Pílula 22 — Esquecer o denominador.** Ideia central: número absoluto sem a base engana; é a taxa, não a contagem, que informa.
- [ ] **Pílula 23 — Revisão do Bloco D.** Recall das falácias.

## Bloco E — Valor esperado e decisão
- [ ] **Pílula 24 — Valor esperado.** Ideia central: o motor da decisão sob incerteza — pondere cada resultado pela sua probabilidade antes de escolher.
- [ ] **Pílula 25 — Utilidade e aversão a risco.** Ideia central: R$ 1 milhão não vale o dobro de R$ 500 mil para quem o recebe — por isso não maximizamos só o valor esperado. (ref: Bernoulli)
- [ ] **Pílula 26 — Assimetria e opcionalidade.** Ideia central: busque apostas em que a perda é pequena e limitada e o ganho é grande e aberto. (lente: Thauma)
- [ ] **Pílula 27 — A intuição de Kelly.** Ideia central: a pergunta não é só "apostar?", mas "quanto?" — dimensionar a aposta ao edge evita a ruína. (ref: Kelly)
- [ ] **Pílula 28 — Valor da informação.** Ideia central: reduzir a incerteza tem preço e tem valor; só vale pagar pelo dado que muda a decisão.
- [ ] **Pílula 29 — Revisão do Bloco E.** Recall de valor esperado e decisão.

## Bloco F — Incerteza no mundo real
- [ ] **Pílula 30 — Sinal e ruído.** Ideia central: a maior parte da variação do dia a dia é ruído; confundir ruído com sinal gera reação a fantasmas. (ref: Silver)
- [ ] **Pílula 31 — Calibração e previsão.** Ideia central: previsão honesta se mede pela calibração — dizer "80%" e acertar 80% das vezes.
- [ ] **Pílula 32 — Cisnes negros e a incerteza de Knight.** Ideia central: há o que a probabilidade cobre e o que ela não cobre — e confundir os dois é perigoso. (ref: Knight; Taleb)
- [ ] **Pílula 33 — Pensar em apostas.** Ideia central: decisão boa não é a que deu certo, é a que tinha o melhor valor esperado com o que se sabia. (ref: Annie Duke, *Thinking in Bets*)
- [ ] **Pílula 34 — Revisão final.** Recall integrador dos seis blocos — o latticework da incerteza.
