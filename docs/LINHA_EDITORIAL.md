# Linha Editorial

## DNA

A revista não é oito newsletters automatizadas. É um instrumento de formação. O que a
diferencia de um agregador é uma regra: **construída para retenção, não para consumo.** As
editorias de currículo seguem os heurísticos de aprendizado — recordação ativa, Feynman,
conexão entre domínios, sumarização progressiva. Conteúdo que não é retido não tem valor aqui.

## Aprofundamento em todo campo

Toda editoria — de currículo ou de notícia — fecha com **"Para aprofundar"**: 2–3
artigos/materiais de desenvolvimento (com link), coletados via Apify (`rag-web-browser`). O
peso editorial é **maior no aprofundamento do que na notícia efêmera**: a notícia diz o que
mudou; o artigo técnico desenvolve o campo — é o que serve ao deep generalist. As queries por
editoria ficam em `editorias/aprofundamento.yaml`; o coletor é `coletar_aprofundamento`.

## Os dois motores

| | **NOTÍCIA** | **CURRÍCULO** |
|---|---|---|
| Conteúdo | Efêmero, sensível ao tempo | Atemporal, sequencial |
| Origem | Coleta fresca | LLM gera a partir de um syllabus |
| "Diário" = | Há coisa nova hoje | Hoje é a próxima aula |
| Estado | Ledger de dedup | Cursor no syllabus |
| Risco se mal feito | Alucinação de fonte | Aula rasa e repetitiva |

## Carga & cadência

Oito editorias é muito para ler todo dia. A cadência por editoria mantém a edição digerível —
provavelmente Saúde e IA diárias, e as de formação leves ou alternadas. Cortar cadência antes
de cortar profundidade. As cadências marcadas `‹DECIDIR›` ainda serão fechadas.

---

## Fichas

### 1. Saúde — *híbrido*
- **Estrutura:** (1) *Pulso oficial* — resumo DOU + IOF-MG; (2) *Aprofundamento* — gestão
  hospitalar ou IA na saúde (rotação); (3) *Coletânea* — artigos da web.
- **Fontes:** scripts Python existentes (DOU/IOF) · ‹DECIDIR› fontes de curadoria.
- **Cadência:** diária.
- **Regra especial:** só resume texto recuperado, com link. **Zero invenção.** (Alimenta o
  trabalho na Fhemig — acurácia é absoluta.)

### 2. Inteligência Artificial — *híbrido* (motor da Thauma)
- **Estrutura:** (1) *Pulso IA* — o que mudou (modelos, papers, ferramentas); (2) *Aplicado* —
  técnica/caso/padrão amarrado ao que a Thauma constrói.
- **Fontes:** ‹DECIDIR› — arXiv, blogs de labs, releases, agregadores.
- **Cadência:** diária.
- **Regra especial:** o *Aplicado* sempre puxa pra "como isso vira entrega/produto".

### 3. Gestão — *currículo* (MBA guiado)
- **Fontes:** LLM a partir do syllabus.
- **Cadência:** diária (1 aula/dia).
- **Syllabus:** a desenhar — é o **protótipo do molde** (ver `MOLDE_AULA.md`). Espinha de 10
  módulos (~65 aulas com revisões): Fundamentos · Estratégia · Economia · Contabilidade &
  Finanças · Marketing · Operações · Pessoas & Liderança · Dados & Decisão · Execução &
  Mudança · Integração (casos).

### 4. Imersão — *currículo, slot rotativo*
- **O que é:** mergulho profundo num tema por vez. **Ocupante atual: Teoria dos Jogos**
  (pílulas). Ao concluir, troca para o próximo tema (config-driven).
- **Fontes:** LLM a partir do syllabus.
- **Cadência:** diária (1 pílula/dia).

### 5. Mente (Psicologia · Filosofia · Teologia) — *currículo com rotação*
- **Rotação:** ‹DECIDIR› — ex. Seg/Qui Psicologia (Jung, Freud) · Ter/Sex Filosofia ·
  Qua/Sáb Teologia. Cada fio tem seu cursor.
- **Fontes:** LLM a partir dos syllabi (um por fio).
- **Cadência:** diária (o fio do dia).

### 6. Fitness — *curadoria leve*
- **O que é:** conteúdo pra manter engajamento no processo de recomposição. Não vira curso.
- **Fontes:** ‹DECIDIR›.
- **Cadência:** ‹DECIDIR›.

### 7. Ideias de Negócio — *síntese / oportunidade*
- **O que é:** conecta o que está acontecendo (IA, mercados, o que as outras editorias
  coletaram) a oportunidades de ganhar dinheiro, com a lente "onde a Thauma pode jogar".
- **Fontes:** material já coletado em IA/Saúde + web.
- **Cadência:** ‹DECIDIR› — sugestão 2–3×/semana.
- **Saída:** 1–3 ângulos acionáveis por edição, não notícia genérica.

### 8. Família — *formação aplicada*
- **O que é:** a editoria mais ligada à identidade — quem o Pedro é em casa. Paternidade e
  parceria: presença, escuta, rituais, disciplina afetuosa, conserto de conflito, divisão de
  carga.
- **Formato:** lição curta + **uma micro-prática pra aplicar hoje** (em família, conhecimento
  só conta quando vira gesto). Pode rotacionar facetas: pai / marido / casa.
- **Fontes:** LLM a partir do syllabus + curadoria leve.
- **Cadência:** ‹DECIDIR›.
- **Regra especial:** **aplicação > teoria.** Fecha sempre com uma ação concreta pra hoje.

---

## Feature futura: síntese cross-editorial
Um fecho que conecta o que apareceu hoje em domínios diferentes (estilo *latticework*). É o
que transforma consumo em pensamento. Opcional, Fase 4 — mas é candidata a alma do projeto.
