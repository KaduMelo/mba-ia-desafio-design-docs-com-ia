# Da Reunião ao Documento: Design Docs do Sistema de Webhooks

Pacote de design docs (PRD, RFC, FDD, ADRs e Tracker) da feature **Sistema de Webhooks de Notificação de Pedidos**
do OMS. O pacote foi produzido com IA a partir da transcrição de uma reunião técnica e do código existente.
Este README documenta **como** o pacote foi produzido.

> O enunciado original está no repositório base:
> [devfullcycle/mba-ia-desafio-design-docs-com-ia](https://github.com/devfullcycle/mba-ia-desafio-design-docs-com-ia).
> Neste fork, ele pode ser lido com `git show e7f6311:README.md`.

---

## Sobre o desafio

Uma empresa que opera um Order Management System em Node.js, TypeScript e Prisma/MySQL decidiu, numa call de
cerca de 55 minutos, construir webhooks que avisem os clientes B2B quando o status dos pedidos muda. A reunião
teve tech lead, PM, dois engenheiros e uma engenheira de segurança. Nada foi registrado além da transcrição
([`TRANSCRICAO.md`](TRANSCRICAO.md)). A tarefa era transformar essa conversa num pacote de documentação
acionável, sem alterar o código: PRD, RFC, FDD, de 5 a 8 ADRs e um Tracker que ligue cada item à sua origem.

A parte difícil não era escrever, era **filtrar**. A reunião mistura decisões fechadas, ideias descartadas
(Redis, disparo síncrono, exactly-once), pontos adiados (email, dashboard, rate limiting) e ambiguidades que
ninguém resolveu, como "5 tentativas" com 5 intervalos ou a origem do `customer_id`. Usei a IA como ferramenta
principal de produção. O meu papel foi de maestro: definir as fases, escrever os prompts, revisar cada entrega
e decidir os pontos que a reunião deixou em aberto.

## Ferramentas de IA utilizadas

| Ferramenta | Papel |
|---|---|
| **Claude Code** (extensão do VS Code), modelo **Claude Opus 5.5** | Agente principal. Leu a transcrição e o código, escreveu todos os documentos, rodou as validações e operou o git e o `gh`. |
| **Prompts no formato `/goal`** | Cada fase tem um goal com o **critério de conclusão verificável** (contagens, seções obrigatórias, caminhos existentes). Assim a IA sabe quando terminou e quando ainda precisa corrigir. |
| **Perguntas com opções** (`AskUserQuestion` do Claude Code) | Nas revisões, a IA apresentava 2 a 4 opções com o trade-off de cada uma e uma recomendação. A decisão final foi sempre minha. Algumas vezes escolhi diferente da recomendação, por exemplo o retry de 4xx. |
| **Scripts Python gerados pela IA** ([`processo/scripts/`](processo/scripts/)) | Validadores contra alucinação: conferem cada `[hh:mm] Nome` contra a transcrição, cada caminho contra o repositório e cada critério de aceite do enunciado. Também geram o Tracker. |
| **Memória persistente do Claude Code** | Guardou regras de trabalho entre sessões, como "toda fase fecha com PR no fork KaduMelo e nunca no repositório original". |

Não usei subagentes. Todo o trabalho rodou numa única sessão, para manter o contexto das decisões entre as fases.

## Workflow adotado

O trabalho foi dividido em fases. Cada fase teve uma branch própria, foi revisada por mim e entrou na `main`
por um Pull Request no fork. O histórico do git mostra cada etapa.

| Fase | Entrega | Branch / PR |
|---|---|---|
| Plano | [`processo/PLANO.md`](processo/PLANO.md): fases, goals, tabela de **armadilhas** da transcrição, alternativas descartadas e ganchos no código | `docs/fase-plano` |
| 0 | [`processo/INVENTARIO.md`](processo/INVENTARIO.md): **fonte única de verdade**, com 158 itens (decisões, requisitos, alternativas, fora de escopo, ambiguidades e ganchos no código), todos com origem | `docs/fase-0-inventario` |
| 1 | 7 ADRs | [PR #1](https://github.com/KaduMelo/mba-ia-desafio-design-docs-com-ia/pull/1) |
| 2 | RFC | [PR #2](https://github.com/KaduMelo/mba-ia-desafio-design-docs-com-ia/pull/2) |
| 3 | FDD | [PR #3](https://github.com/KaduMelo/mba-ia-desafio-design-docs-com-ia/pull/3) |
| 4 | PRD | [PR #4](https://github.com/KaduMelo/mba-ia-desafio-design-docs-com-ia/pull/4) |
| 5 | Tracker (gerado por script e validado) | [PR #5](https://github.com/KaduMelo/mba-ia-desafio-design-docs-com-ia/pull/5) |
| 6 | Revisão cruzada ([`processo/REVISAO.md`](processo/REVISAO.md)) e correções | [PR #6](https://github.com/KaduMelo/mba-ia-desafio-design-docs-com-ia/pull/6) |
| 7 | Este README | `docs/fase-7-readme` |

**Como organizei a interação com a IA:**

1. **Inventário antes de qualquer documento.** A Fase 0 extraiu tudo o que a reunião decidiu, descartou,
   adiou ou deixou ambíguo, com `[hh:mm] Nome` em cada linha. Os documentos seguintes leram o inventário, não
   a transcrição. Assim, cada documento não reinterpreta a reunião do seu jeito.
2. **Ordem do enunciado:** ADRs → RFC → FDD → PRD → Tracker → README. As decisões vieram primeiro e
   formaram o esqueleto.
3. **Ciclo de cada fase.** O goal gera o documento e faz o commit. Depois a IA valida com script e para.
   Eu reviso: "vamos revisar juntos" vira perguntas com opções, decido, a IA corrige e registra o ajuste em
   [`processo/LOG-ITERACOES.md`](processo/LOG-ITERACOES.md). Por fim vêm o push, o PR e o merge.
4. **Tudo o que a reunião não fixou fica marcado como *(proposta)*** nos documentos e como "— proposta" no
   Tracker. Assim fica visível o que veio da reunião e o que foi derivado.

## Prompts customizados

Os goals estão em [`processo/PLANO.md`](processo/PLANO.md). Abaixo, quatro dos que foram usados, com quebras
de linha para facilitar a leitura. Os goals das Fases 0 e 1 foram colados literalmente na sessão. Das fases
seguintes em diante, eu pedia "fase N" e a IA executava o goal correspondente do plano.

**1. Fase 0: inventário como fonte única.** Este foi o prompt mais importante, porque cria a base contra
alucinação.

```text
/goal Ler TRANSCRICAO.md inteiro e o código em src/ e prisma/, e criar processo/INVENTARIO.md com tabelas
separadas para: (a) decisões fechadas, (b) requisitos funcionais, (c) requisitos não funcionais/restrições,
(d) alternativas descartadas com o motivo, (e) itens fora de escopo/adiados, (f) questões em aberto,
(g) detalhes técnicos secundários (payload, headers, timeout, UUID, snapshot), (h) ganchos no código com
caminho real e número de linha. Toda linha deve ter coluna Origem com [hh:mm] Nome ou caminho de arquivo
existente. Usar processo/PLANO.md (seção Armadilhas) como checklist. Concluído quando cada tabela estiver
preenchida, nenhuma linha sem origem, e todos os caminhos citados existirem (verificar com ls). Não alterar
src/, prisma/, tests/ nem TRANSCRICAO.md. Fluxo git: antes de começar, garantir main atualizada e working
tree limpa, e criar a branch docs/fase-0-inventario a partir da main (git switch -c docs/fase-0-inventario);
ao terminar, fazer commit em português no padrão 'docs: ...' nessa branch e PARAR sem fazer merge, mostrando
um resumo do que foi gerado para minha revisão.
```

**2. Fase 1: ADRs com escopo fechado.** O prompt diz exatamente quais decisões entram e quais arquivos do
código o ADR de padrões precisa citar. Isso evita ADRs genéricos.

```text
/goal Criar 7 ADRs em docs/adrs/ no formato MADR, nomeados ADR-NNN-titulo-em-kebab-case.md, usando apenas
processo/INVENTARIO.md como fonte: 001 outbox no MySQL na mesma transação do changeStatus; 002 worker em
processo separado com polling de 2s (src/worker.ts, PrismaClient próprio, single-worker, ordering só por
order_id); 003 retry com backoff 1m/5m/30m/2h/12h e DLQ em tabela webhook_dead_letter com replay ADMIN;
004 HMAC-SHA256 com secret por endpoint e rotação com grace period de 24h; 005 entrega at-least-once com
X-Event-Id; 006 reuso dos padrões do projeto (citar src/shared/errors/app-error.ts,
src/shared/errors/http-errors.ts, src/middlewares/error.middleware.ts, src/middlewares/auth.middleware.ts
requireRole, src/shared/logger/index.ts, padrão src/modules/*); 007 payload como snapshot na inserção com
filtro de status na inserção. Cada ADR com seções Status, Data, Decisores (participantes da reunião),
Contexto, Decisão, Alternativas Consideradas (as descartadas na reunião com o motivo), Consequências
(positivas, negativas e trade-off explícito) e Referências com [hh:mm] Nome. Atualizar docs/adrs/README.md
como índice com links. Concluído quando os 7 arquivos existirem, todos tiverem as seções obrigatórias, nenhum
ADR repetir o conteúdo de outro e todo caminho de código citado existir. [+ fluxo git da fase]
```

**3. Fase 6: revisão cruzada que só aponta, sem corrigir.** Separar o diagnóstico da correção me obrigou a
ler os achados e decidir.

```text
/goal Revisar o pacote docs/ inteiro contra processo/PLANO.md (tabela Armadilhas) e o checklist de critérios
de aceite do enunciado. Gerar processo/REVISAO.md listando: contradições com a transcrição, conteúdo
duplicado entre documentos (sugerir troca por link), itens descartados aparecendo como requisito, caminhos de
código inexistentes, critérios de aceite não atendidos. NÃO corrigir ainda — só listar com arquivo e linha.
Concluído quando o relatório cobrir todos os critérios de aceite do enunciado, um por um, com status
OK/FALHA. [+ fluxo git da fase]
```

**4. Fechamento de fase.** O mesmo prompt foi usado ao fim de todas as fases. Ele força o registro da
iteração no LOG antes do merge.

```text
Fase N revisada. Registre em processo/LOG-ITERACOES.md as correções feitas nesta fase (o que a IA errou, como
detectei, como corrigi), faça o commit "docs: log de iterações da fase N" na branch atual, faça git push -u
origin <branch>, abra o PR no fork com gh pr create --repo KaduMelo/mba-ia-desafio-design-docs-com-ia --base
main --head <branch> (título "Fase N: <descrição>", corpo com resumo e pontos de revisão), faça o merge com
gh pr merge --merge e depois git switch main && git pull.
```

## Iterações e ajustes

Foram **7 ciclos principais de revisão**, um por fase (do inventário à revisão cruzada), com **24 ajustes
registrados** em [`processo/LOG-ITERACOES.md`](processo/LOG-ITERACOES.md). Os números entre colchetes abaixo
são as entradas do LOG.

**O que a IA errou ou deixou superficial, e como foi corrigido:**

- **Links para documentos vazios [4].** O primeiro RFC linkava PRD, FDD e Tracker, que ainda eram
  placeholders. Na revisão, disse que links não podem estar vazios. A regra entrou no plano, e cada fase
  passou a criar os links para o documento que acabava de produzir.
- **Ambiguidades tratadas como decisões fechadas [3, 6].** "5 tentativas" com 5 intervalos, uma linha da
  outbox por evento ou por evento × webhook, e se a criação do pedido gera evento: a IA registrou esses pontos
  como pendentes, e eu os decidi com opções. As definições ficaram no RFC (R1–R3), sem atribuí-las a ninguém
  da reunião.
- **Erro que o código desmentia [7, 8].** O primeiro FDD fazia os erros 404 estenderem `NotFoundError`. Mas
  essa classe fixa o código `NOT_FOUND` (`src/shared/errors/http-errors.ts:27`), então `WEBHOOK_NOT_FOUND`
  nunca chegaria ao cliente. No mesmo espírito, a regra "https no Zod" conflitava com o código
  `WEBHOOK_INVALID_URL`, porque `validate.middleware.ts` converte tudo em `VALIDATION_ERROR`. As duas
  soluções foram documentadas sem mexer no código.
- **Garantia falsa [9].** A IA prometia "ordem por pedido com um único worker". Revendo o fluxo de retry,
  ficou claro que um evento em backoff é ultrapassado pelos seguintes. A limitação foi corrigida no FDD, no
  RFC e no ADR-002.
- **A correção que precisou ser desfeita [11].** A IA apontou que o `X-Timestamp` fora do HMAC não impede
  replay. Escolhi incluí-lo na assinatura, e a mudança foi aplicada. Na rodada seguinte, pedi a recomendação
  da IA, e ela mostrou que isso alterava uma decisão fechada duas vezes na reunião ("HMAC sobre o corpo",
  [09:22] Sofia e [09:48] Larissa). Também passava por cima da revisão de segurança combinada. A mudança foi
  revertida: o risco virou a questão em aberto Q7, com a Sofia como dona. Esta foi a lição mais clara do
  desafio: documentar não é redecidir.
- **Retry que desperdiçava 15 horas [13].** O FDD retentava inclusive respostas 4xx permanentes. Agora só se
  retentam falhas transitórias (timeout, rede, 5xx, 408, 429). As demais vão direto para a DLQ, com o código
  `WEBHOOK_DELIVERY_REJECTED`.
- **Inconsistências entre documentos [15, 21].** A probabilidade de "worker parado" era Baixa no PRD e Média
  no FDD. E a mudança de retry da iteração 13 tinha ficado só no FDD, enquanto ADR-003, RFC e PRD ainda diziam
  "toda falha é retentada". As duas inconsistências foram encontradas em revisão cruzada e corrigidas.
- **Duplicação [22].** O FDD repetia 6 itens do fora de escopo do PRD. Ficou só com as exclusões técnicas e um
  link para o PRD.
- **Tracker sem distinguir o que é proposta [17, 19].** A primeira geração deixou 4 itens sem origem e
  classificava alternativas nunca discutidas como "descartadas na reunião". Hoje, 34 linhas marcam
  "— proposta" e 3 marcam "plausível (não discutida)".
- **O validador também errou [24].** O checador de critérios acusou falha no RFC por ler o separador da tabela
  de metadados como fim de seção. Investiguei a falha antes de aceitá-la no relatório.

## Como navegar a entrega

```text
.
├── README.md                 ← este arquivo (processo)
├── TRANSCRICAO.md            ← fonte: reunião técnica (não alterada)
├── docs/
│   ├── PRD.md                ← 1. por que e o quê (produto)
│   ├── RFC.md                ← 2. proposta técnica, alternativas e questões em aberto
│   ├── adrs/
│   │   ├── README.md         ← índice dos ADRs
│   │   ├── ADR-001-outbox-no-mysql.md
│   │   ├── ADR-002-worker-separado-em-polling.md
│   │   ├── ADR-003-retry-backoff-e-dlq.md
│   │   ├── ADR-004-hmac-sha256-com-secret-por-endpoint.md
│   │   ├── ADR-005-entrega-at-least-once-com-x-event-id.md
│   │   ├── ADR-006-reuso-dos-padroes-do-projeto.md
│   │   └── ADR-007-payload-snapshot-e-filtro-na-insercao.md   ← 3. uma decisão por arquivo
│   ├── FDD.md                ← 4. como construir: contratos, erros, fluxos, integração com o código
│   └── TRACKER.md            ← 5. de onde veio cada item (284 linhas)
├── processo/                 ← bastidores da produção
│   ├── PLANO.md              ← fases, goals, armadilhas da transcrição
│   ├── INVENTARIO.md         ← fonte única de verdade extraída da reunião e do código
│   ├── LOG-ITERACOES.md      ← cada ajuste feito sobre o que a IA gerou
│   ├── REVISAO.md            ← revisão cruzada contra o checklist do enunciado
│   └── scripts/              ← gerador e validadores (Tracker e critérios de aceite)
└── src/ prisma/ tests/       ← código original (não alterado)
```

**Ordem de leitura sugerida:** [PRD](docs/PRD.md) → [RFC](docs/RFC.md) → [ADRs](docs/adrs/README.md) →
[FDD](docs/FDD.md) → [Tracker](docs/TRACKER.md). Para auditar uma afirmação, procure o ID dela no Tracker e
siga a localização até a transcrição ou o código.

**Para validar o pacote**, na raiz do repositório:

```bash
python3 -I processo/scripts/validate_tracker.py   # timestamps, caminhos e percentuais do Tracker
python3 -I processo/scripts/check_acceptance.py   # checklist de critérios de aceite do enunciado
```
