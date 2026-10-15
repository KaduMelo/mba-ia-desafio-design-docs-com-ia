# Plano de Execução — Design Docs do Sistema de Webhooks

Plano para produzir o pacote (ADRs → RFC → FDD → PRD → Tracker → README) com o Claude Code,
uma fase por vez, cada fase disparada com `/goal`. Você é o maestro: **depois de cada fase, revise
criticamente antes de seguir** e registre o que corrigiu em `processo/LOG-ITERACOES.md` (vira a
seção "Iterações e ajustes" do README).

## Regras que valem para TODAS as fases (cole junto em cada goal se abrir sessão nova)

1. Não alterar nada em `src/`, `prisma/`, `tests/`, configs nem `TRANSCRICAO.md`.
2. Toda afirmação precisa de origem: `[hh:mm] Nome` da transcrição ou caminho real de arquivo.
   Se não tem origem, não entra (ou entra explicitamente como "proposta de implementação derivada de X").
3. Fonte única de verdade: `processo/INVENTARIO.md` (Fase 0). Documentos consultam o inventário, não reinterpretam a transcrição.
4. Cada documento fica na sua altura: RFC = arquitetura e decisão (2–4 páginas); ADR = uma decisão;
   FDD = implementação; PRD = produto. Detalhe repetido entre documentos = está no lugar errado → trocar por link.
5. Nomes de ADR: `docs/adrs/ADR-NNN-titulo-em-kebab-case.md` (o `docs/adrs/README.md` atual sugere
   `0001-...`; o enunciado manda `ADR-NNN-...` — seguir o enunciado e atualizar esse README como índice).

---

## Armadilhas da transcrição (checar em toda revisão)

| Armadilha | Correto | Origem |
|---|---|---|
| `customer_id` vem do JWT | **Não.** Vem no body ou path; JWT é do usuário operador | [09:31] Marcos → [09:32] Bruno, [09:32] Larissa |
| Ordering garantido | Só por `order_id` e só com single-worker; limitação conhecida | [09:12] Diego, [09:13] Larissa |
| Arquivamento de entregues (30 dias) | Fora do escopo da feature | [09:08] Diego |
| Email quando webhook falha | Fora — próxima fase | [09:37] Larissa |
| Dashboard visual | Fora — projeto do time de frontend | [09:40] Larissa |
| Rate limiting de saída | **Questão em aberto** ("observar e decidir depois") | [09:39] Diego/Larissa |
| Webhooks inbound | Fora — só outbound | [09:02] Marcos, [09:03] Sofia |
| Payload > 64KB | Erro (não truncar); é RNF, não ADR | [09:23] Sofia, [09:24] Larissa |
| HTTPS | Validação no schema Zod, não decisão arquitetural | [09:23] Sofia |
| Payload renderizado no envio | **Não.** Snapshot na inserção | [09:52] Larissa/Diego/Bruno |
| Filtro de status no envio | **Não.** Filtra na inserção da outbox | [09:34] Bruno/Diego |
| ID auto incremental | **Não.** UUID (padrão do projeto) | [09:51] Larissa |
| Itens do pedido no payload | **Não.** Payload enxuto, cliente chama `GET /orders/:id` | [09:43] Diego |
| CRUD só para ADMIN | Não: CRUD = qualquer role autenticada; só replay de DLQ exige ADMIN (+ log de quem fez) | [09:36] Sofia, [09:37] Sofia |
| "5 tentativas" | Ambíguo: 5 intervalos (1m/5m/30m/2h/12h) → 5 retries após a 1ª falha ou 5 no total? Registrar a interpretação e marcar como questão em aberto/nota | [09:17] Diego/Larissa |
| Métricas/tracing | Não foram discutidos. Propor sem nova infra (Pino já existe, correlação por `event_id`) e marcar como proposta | [09:29] Bruno |

## Alternativas descartadas (matéria-prima do RFC e dos ADRs)

| Alternativa | Por que caiu | Origem |
|---|---|---|
| Disparo síncrono no `changeStatus` | Transação pesada; cliente lento trava outros pedidos; rollback impossível | [09:04] Bruno, [09:06] Diego |
| Redis Streams / Redis Cluster | Mais infra, time pequeno, overengineering | [09:07] Larissa/Diego |
| Trigger do banco / LISTEN-NOTIFY | MySQL não notifica processo externo | [09:09] Bruno/Diego |
| Worker dentro do processo da API | Restart da API mata o worker | [09:11] Diego |
| Retry indefinido | Evento pendurado para sempre | [09:15] Diego |
| 3 tentativas | Janela de 30 min curta demais (cliente com 2h de manutenção) | [09:16] Bruno/Diego |
| DLQ como status `failed` na outbox | Tabela separada é mais limpa e serve de evidência | [09:17]–[09:18] Larissa/Diego |
| Secret global | Se vaza uma, vaza tudo | [09:21] Sofia |
| Exactly-once | Coordenação dos dois lados, complexo demais | [09:25] Diego |
| Injetar repository no OrderService | Função `publishWebhookEvent(tx, ...)` é mais simples | [09:41] Bruno/Diego |
| Mesmo PrismaClient no worker | PrismaClient é por processo | [09:30] Bruno |

## Questões em aberto (RFC)

- Rate limiting de saída — observar e decidir depois ([09:38]–[09:39] Diego/Larissa)
- Escalar para múltiplos workers (particionar por `order_id` ou lock pessimista) ([09:13] Diego)
- Notificação por email em falhas — próxima fase ([09:37] Larissa)
- Endurecer permissões do CRUD ([09:37] Sofia "mais pra frente")
- Arquivamento das linhas entregues após ~30 dias ([09:08] Diego)

## Ganchos no código (verificados)

| Arquivo | Uso no design |
|---|---|
| `src/modules/orders/order.service.ts` | `changeStatus` (l.126) usa `prisma.$transaction` (l.131) → chamar `publishWebhookEvent(tx, order, from, to)` dentro da transação |
| `src/modules/orders/order.status.ts` | Máquina de estados / status válidos para o filtro de eventos |
| `src/shared/errors/app-error.ts`, `http-errors.ts`, `index.ts` | Base `AppError`; novos erros `WEBHOOK_*` estendendo `NotFoundError`/`BadRequestError`/`ConflictError`/`UnprocessableEntityError` |
| `src/middlewares/error.middleware.ts` | Já trata AppError/Zod/Prisma — sem mudança |
| `src/middlewares/auth.middleware.ts` | `authenticate` e `requireRole` (l.49) para o replay ADMIN |
| `src/middlewares/validate.middleware.ts` + `*.schemas.ts` | Padrão Zod (validação https, filtro de status) |
| `src/shared/logger/index.ts` | Pino |
| `src/config/database.ts`, `src/config/env.ts` | PrismaClient / `DATABASE_URL` — worker cria instância própria |
| `src/server.ts` | Modelo para o novo entry-point `src/worker.ts` + script `npm run worker` |
| `src/routes/index.ts` | Registro das rotas do módulo |
| `prisma/schema.prisma` | Padrão `@id @default(uuid()) @db.Char(36)`; enums `UserRole`, `OrderStatus`; model `OrderStatusHistory` |
| `src/modules/orders/*` | Padrão controller/service/repository/routes/schemas a replicar em `src/modules/webhooks/` |

---

## Fases

### Ciclo de cada fase (branch → commit → revisão → merge)

1. **Rode o `/goal` da fase.** Ele cria a branch `docs/fase-N-...` a partir da `main`, gera o conteúdo,
   faz o commit e **para antes do merge**.
2. **Revise você mesmo** com o checklist "Revisão sua" da fase (`git diff main` ajuda).
3. **Peça as correções** em prompts pontuais (quantas rodadas forem precisas). Cada rodada vira um commit na mesma branch.
4. **Feche a fase** com este prompt (troque N e a branch):

```
Fase N revisada. Registre em processo/LOG-ITERACOES.md as correções feitas nesta fase (o que a IA errou, como detectei, como corrigi), faça o commit "docs: log de iterações da fase N" na branch atual, faça git push -u origin <branch>, abra o PR no fork com gh pr create --repo KaduMelo/mba-ia-desafio-design-docs-com-ia --base main --head <branch> (título "Fase N: <descrição>", corpo com resumo e pontos de revisão), faça o merge com gh pr merge --merge e depois git switch main && git pull.
```

5. Siga para a próxima fase. O fechamento de **cada** fase faz push da branch, abre um PR no fork (`KaduMelo/...`, **nunca** no repositório original `devfullcycle`) e faz o merge por ele.

> Por que parar antes do merge: o enunciado espera de 3 a 5 ciclos de revisão. Se o merge acontecer junto
> com a geração, a `main` recebe conteúdo que você ainda não revisou, e o histórico deixa de mostrar as iterações.

### Fase 0 — Exploração e inventário (fonte da verdade)

```
/goal Ler TRANSCRICAO.md inteiro e o código em src/ e prisma/, e criar processo/INVENTARIO.md com tabelas separadas para: (a) decisões fechadas, (b) requisitos funcionais, (c) requisitos não funcionais/restrições, (d) alternativas descartadas com o motivo, (e) itens fora de escopo/adiados, (f) questões em aberto, (g) detalhes técnicos secundários (payload, headers, timeout, UUID, snapshot), (h) ganchos no código com caminho real e número de linha. Toda linha deve ter coluna Origem com [hh:mm] Nome ou caminho de arquivo existente. Usar processo/PLANO.md (seção Armadilhas) como checklist. Concluído quando cada tabela estiver preenchida, nenhuma linha sem origem, e todos os caminhos citados existirem (verificar com ls). Não alterar src/, prisma/, tests/ nem TRANSCRICAO.md. Fluxo git: antes de começar, garantir main atualizada e working tree limpa, e criar a branch docs/fase-0-inventario a partir da main (git switch -c docs/fase-0-inventario); ao terminar, fazer commit em português no padrão 'docs: ...' nessa branch e PARAR sem fazer merge, mostrando um resumo do que foi gerado para minha revisão.
```

Revisão sua: confira à mão 10 timestamps aleatórios contra a transcrição. Algum item "fora de escopo" virou requisito?

### Fase 1 — ADRs (7 arquivos)

```
/goal Criar 7 ADRs em docs/adrs/ no formato MADR, nomeados ADR-NNN-titulo-em-kebab-case.md, usando apenas processo/INVENTARIO.md como fonte: 001 outbox no MySQL na mesma transação do changeStatus; 002 worker em processo separado com polling de 2s (src/worker.ts, PrismaClient próprio, single-worker, ordering só por order_id); 003 retry com backoff 1m/5m/30m/2h/12h e DLQ em tabela webhook_dead_letter com replay ADMIN; 004 HMAC-SHA256 com secret por endpoint e rotação com grace period de 24h; 005 entrega at-least-once com X-Event-Id; 006 reuso dos padrões do projeto (citar src/shared/errors/app-error.ts, src/shared/errors/http-errors.ts, src/middlewares/error.middleware.ts, src/middlewares/auth.middleware.ts requireRole, src/shared/logger/index.ts, padrão src/modules/*); 007 payload como snapshot na inserção com filtro de status na inserção. Cada ADR com seções Status, Data, Decisores (participantes da reunião), Contexto, Decisão, Alternativas Consideradas (as descartadas na reunião com o motivo), Consequências (positivas, negativas e trade-off explícito) e Referências com [hh:mm] Nome. Atualizar docs/adrs/README.md como índice com links. Concluído quando os 7 arquivos existirem, todos tiverem as seções obrigatórias, nenhum ADR repetir o conteúdo de outro e todo caminho de código citado existir. Fluxo git: antes de começar, garantir main atualizada e working tree limpa, e criar a branch docs/fase-1-adrs a partir da main (git switch -c docs/fase-1-adrs); ao terminar, fazer commit em português no padrão 'docs: ...' nessa branch e PARAR sem fazer merge, mostrando um resumo do que foi gerado para minha revisão.
```

Revisão sua: cada ADR cabe em ~1 página? Algum ADR descreve endpoints/payloads em detalhe (isso é FDD)? Contradiz alguma armadilha?

### Fase 2 — RFC

```
/goal Escrever docs/RFC.md (2 a 4 páginas, nível arquitetura) a partir de processo/INVENTARIO.md e dos ADRs em docs/adrs/. Seções: Metadados (autor Larissa como Tech Lead, status "Em revisão", data, revisores Marcos, Bruno, Diego, Sofia), TL;DR, Contexto e problema, Proposta técnica (visão geral com um diagrama mermaid de componentes: API/changeStatus -> webhook_outbox -> worker -> endpoint do cliente, com DLQ), Alternativas consideradas (no mínimo síncrono, Redis Streams, trigger/LISTEN, retry indefinido, exactly-once — cada uma com o trade-off que levou ao descarte e o [hh:mm] Nome), Questões em aberto (rate limiting, escala multi-worker/ordering, email, endurecer permissões do CRUD, arquivamento, interpretação das 5 tentativas), Impacto e riscos, Cronograma (3 sprints + 2 dias de revisão de segurança da Sofia), Decisões relacionadas com link relativo para cada ADR. Proibido no RFC: payloads JSON completos, lista de códigos de erro, schema de tabela coluna a coluna (isso é FDD). Concluído quando todas as seções existirem, houver links válidos para pelo menos 5 ADRs e o texto tiver menos de ~1800 palavras. Fluxo git: antes de começar, garantir main atualizada e working tree limpa, e criar a branch docs/fase-2-rfc a partir da main (git switch -c docs/fase-2-rfc); ao terminar, fazer commit em português no padrão 'docs: ...' nessa branch e PARAR sem fazer merge, mostrando um resumo do que foi gerado para minha revisão.
```

Revisão sua: rode `wc -w docs/RFC.md`. O RFC "fala em decisão" ou já está explicando implementação?

### Fase 3 — FDD (o mais pesado — pode exigir 2 goals)

```
/goal Escrever docs/FDD.md acionável para um dev começar a codar, baseado em processo/INVENTARIO.md, ADRs e RFC (linkar em vez de repetir justificativas). Seções obrigatórias: Contexto e motivação técnica; Objetivos técnicos; Escopo e exclusões; Modelo de dados (webhook_endpoints, webhook_outbox, webhook_deliveries, webhook_dead_letter em sintaxe Prisma seguindo prisma/schema.prisma: uuid Char(36), índices em status e created_at); Fluxos detalhados com diagramas de sequência mermaid (inserção na outbox dentro do $transaction de changeStatus via publishWebhookEvent(tx, order, fromStatus, toStatus) com filtro de status; ciclo do worker a cada 2s; retry 1m/5m/30m/2h/12h; ida para DLQ; replay manual; rotação de secret com grace 24h); Contratos públicos (POST /webhooks, GET /webhooks, PATCH /webhooks/:id, DELETE /webhooks/:id, rotação de secret, GET /webhooks/:id/deliveries, POST /admin/webhooks/dead-letter/:id/replay — cada um com auth/role, request, response de exemplo, status codes; mais o contrato do webhook enviado: payload JSON e headers X-Event-Id, X-Signature, X-Timestamp, X-Webhook-Id, Content-Type); Matriz de erros WEBHOOK_* (código, HTTP status, classe base reutilizada de src/shared/errors/http-errors.ts, quando ocorre); Estratégias de resiliência (timeout 10s, retries, backoff, limite 64KB, fallback=DLQ); Observabilidade (logs Pino estruturados com event_id/webhook_id, métricas e tracing marcados como proposta sem nova infra); Segurança; Integração com o sistema existente (no mínimo 6 caminhos reais: order.service.ts changeStatus, http-errors.ts, error.middleware.ts, auth.middleware.ts requireRole, server.ts -> worker.ts, routes/index.ts, schema.prisma, logger); Dependências e compatibilidade; Plano de testes; Critérios de aceite técnicos; Riscos e mitigação. Regras: customer_id NÃO vem do JWT; endpoints/nomes não citados na reunião devem ser marcados como "proposta de design" no texto. Concluído quando todas as seções existirem, houver pelo menos 4 endpoints com request+response+status codes, todos os códigos de erro começarem com WEBHOOK_ e todo caminho citado existir no repositório. Fluxo git: antes de começar, garantir main atualizada e working tree limpa, e criar a branch docs/fase-3-fdd a partir da main (git switch -c docs/fase-3-fdd); ao terminar, fazer commit em português no padrão 'docs: ...' nessa branch e PARAR sem fazer merge, mostrando um resumo do que foi gerado para minha revisão.
```

Revisão sua: o JSON do payload tem exatamente os campos de [09:43]? O mermaid renderiza no GitHub? Algum endpoint ignora a regra do `customer_id`?

### Fase 4 — PRD

```
/goal Escrever docs/PRD.md (nível produto, sem detalhe técnico do FDD — linkar) consolidando INVENTARIO, ADRs, RFC e FDD. Seções: Resumo e contexto; Problema e motivação (Atlas Comercial, MaxDistribuição, Nova Cargo, polling no GET /orders, risco de churn da Atlas); Público-alvo e cenários de uso; Objetivos e métricas de sucesso (pelo menos uma meta quantitativa rastreável, ex: notificação em menos de 10s após a mudança de status; entrega até fim de novembro/3 sprints); Escopo incluso e Fora de escopo (no mínimo email de alerta, dashboard visual, webhooks inbound, arquivamento de 30 dias, rate limiting como em aberto); Requisitos funcionais numerados PRD-FR-NN (no mínimo 8, cada um com [hh:mm] Nome); Requisitos não funcionais PRD-NFR-NN; Decisões e trade-offs (resumo de 1 linha + link para o ADR); Dependências; Riscos com tabela Probabilidade/Impacto/Mitigação (no mínimo 3); Critérios de aceitação; Estratégia de testes e validação (incluir revisão de segurança de 2 dias da Sofia). Concluído quando houver pelo menos 8 FRs com origem, pelo menos 1 métrica com meta numérica, pelo menos 2 itens fora de escopo explicitamente descartados/adiados na reunião, e nenhuma métrica inventada sem origem. Fluxo git: antes de começar, garantir main atualizada e working tree limpa, e criar a branch docs/fase-4-prd a partir da main (git switch -c docs/fase-4-prd); ao terminar, fazer commit em português no padrão 'docs: ...' nessa branch e PARAR sem fazer merge, mostrando um resumo do que foi gerado para minha revisão.
```

Revisão sua: há métrica que ninguém na reunião pediu (ex: "99,9% de entrega")? Se sim, remova ou marque como proposta.

### Fase 5 — Tracker

```
/goal Criar docs/TRACKER.md com uma tabela | ID | Documento | Tipo | Conteúdo (resumo) | Fonte | Localização | cobrindo todos os itens identificáveis de docs/PRD.md, docs/RFC.md, docs/FDD.md e docs/adrs/*.md (FRs, NFRs, decisões, alternativas, questões em aberto, fora de escopo, contratos, erros, integrações, riscos). IDs no padrão PRD-FR-01, PRD-NFR-01, RFC-ALT-01, RFC-OPEN-01, FDD-CONTRATO-01, FDD-ERR-01, FDD-INT-01, ADR-001. Fonte é TRANSCRICAO ou CODIGO; Localização é [hh:mm] Nome (formato exato) ou caminho real de arquivo. Se um item não tiver origem, NÃO inventar: listar numa seção "Itens sem origem" ao final para eu decidir. Depois escrever um script em scratchpad que valide: % de linhas TRANSCRICAO com regex ^\[\d{2}:\d{2}\] [A-Z][a-z]+ e timestamp/nome existentes na transcrição, caminhos CODIGO existentes, e conte linhas CODIGO. Concluído quando o script reportar >=70% TRANSCRICAO válidas, >=5 linhas CODIGO com caminho existente, 0 timestamps inexistentes e cobertura estimada >=80% dos itens dos documentos. Fluxo git: antes de começar, garantir main atualizada e working tree limpa, e criar a branch docs/fase-5-tracker a partir da main (git switch -c docs/fase-5-tracker); ao terminar, fazer commit em português no padrão 'docs: ...' nessa branch e PARAR sem fazer merge, mostrando um resumo do que foi gerado para minha revisão.
```

Revisão sua: decida os "Itens sem origem" — remover do documento ou justificar.

### Fase 6 — Revisão cruzada (consistência e duplicação)

```
/goal Revisar o pacote docs/ inteiro contra processo/PLANO.md (tabela Armadilhas) e o checklist de critérios de aceite do enunciado. Gerar processo/REVISAO.md listando: contradições com a transcrição, conteúdo duplicado entre documentos (sugerir troca por link), itens descartados aparecendo como requisito, caminhos de código inexistentes, critérios de aceite não atendidos. NÃO corrigir ainda — só listar com arquivo e linha. Concluído quando o relatório cobrir todos os critérios de aceite do enunciado, um por um, com status OK/FALHA. Fluxo git: antes de começar, garantir main atualizada e working tree limpa, e criar a branch docs/fase-6-revisao a partir da main (git switch -c docs/fase-6-revisao); ao terminar, fazer commit em português no padrão 'docs: ...' nessa branch e PARAR sem fazer merge, mostrando um resumo do que foi gerado para minha revisão.
```

Depois: leia o relatório, escolha o que corrigir, peça as correções em prompts específicos. **Isso é iteração real — registre no LOG.**

### Fase 7 — README do processo

```
/goal Substituir README.md pela documentação do processo, com as seções: Sobre o desafio (1–2 parágrafos), Ferramentas de IA utilizadas (Claude Code com o modelo usado, /goal, subagentes se usados, e o papel de cada), Workflow adotado (ordem das fases 0 a 7 e como a interação foi organizada com INVENTARIO como fonte única), Prompts customizados (no mínimo 3 em blocos de código, copiados de processo/PLANO.md), Iterações e ajustes (baseado em processo/LOG-ITERACOES.md, com número de iterações principais e exemplos concretos do que a IA errou e como foi corrigido), Como navegar a entrega (árvore de arquivos e ordem de leitura: PRD -> RFC -> ADRs -> FDD -> TRACKER). Manter link para o enunciado original no repositório base. Concluído quando todas as seções existirem e cada iteração citada corresponder a uma entrada real do LOG. Fluxo git: antes de começar, garantir main atualizada e working tree limpa, e criar a branch docs/fase-7-readme a partir da main (git switch -c docs/fase-7-readme); ao terminar, fazer commit em português no padrão 'docs: ...' nessa branch e PARAR sem fazer merge, mostrando um resumo do que foi gerado para minha revisão.
```

### Fase 8 — Checklist final e entrega

```
/goal Criar a branch docs/fase-8-checklist a partir da main. Rodar de novo o script de validação do tracker; confirmar que git diff --stat e7f6311 -- src prisma tests TRANSCRICAO.md está vazio; verificar que todo link relativo em README.md, docs/*.md e docs/adrs/*.md aponta para arquivo existente; conferir item a item o checklist de critérios de aceite do enunciado original (o README foi substituído na Fase 7; ler com git show e7f6311:README.md) (PRD, RFC, FDD, ADRs, Tracker, README, Consistência) e gravar o resultado em processo/CHECKLIST-FINAL.md com OK/FALHA e evidência (arquivo:linha ou contagem). Corrigir apenas falhas mecânicas (link quebrado, contagem, formato de nome); falhas de conteúdo devem ser listadas para minha decisão. Commit na branch e PARAR sem merge. Concluído quando todos os itens estiverem OK ou listados como pendência para mim.
```

Depois de aprovar: feche a fase com o prompt padrão (merge) e então:

```
Faça git push origin main e confirme que o repositório GitHub KaduMelo/mba-ia-desafio-design-docs-com-ia está público (gh repo view --json visibility). Liste os links do GitHub para README.md, docs/RFC.md e docs/adrs/ para eu conferir a renderização (tabelas, mermaid, links dos ADRs).
```

---

## Branches e commits

| Fase | Branch | Commit principal |
|---|---|---|
| Plano | `docs/fase-plano` | `docs: plano de execução e log de iterações` |
| 0 | `docs/fase-0-inventario` | `docs: inventário da transcrição e do código` |
| 1 | `docs/fase-1-adrs` | `docs: ADRs 001-007` |
| 2 | `docs/fase-2-rfc` | `docs: RFC do sistema de webhooks` |
| 3 | `docs/fase-3-fdd` | `docs: FDD do sistema de webhooks` |
| 4 | `docs/fase-4-prd` | `docs: PRD do sistema de webhooks` |
| 5 | `docs/fase-5-tracker` | `docs: tracker de rastreabilidade` |
| 6 | `docs/fase-6-revisao` | `docs: relatório de revisão cruzada` + commits de correção |
| 7 | `docs/fase-7-readme` | `docs: README do processo` |
| 8 | `docs/fase-8-checklist` | `docs: checklist final` |

Os merges com `--no-ff` deixam cada fase visível em `git log --graph`. O histórico também é evidência das iterações.
