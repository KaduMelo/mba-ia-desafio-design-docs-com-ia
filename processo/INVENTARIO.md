# Inventário — Sistema de Webhooks de Notificação de Pedidos

Fonte única de verdade para PRD, RFC, FDD, ADRs e Tracker. Cada linha tem origem na
`TRANSCRICAO.md` (`[hh:mm] Nome`) ou num arquivo real do repositório (`caminho:linha`).
Os documentos consultam este inventário. Se algo não estiver aqui, não tem origem.

> **Arquivos a criar (ainda não existem):** `src/worker.ts`, `src/modules/webhooks/*` e o script `npm run worker`
> foram propostos na reunião ([09:11] Larissa, [09:27] Bruno, [09:28] Bruno). No Tracker, a origem deles é
> `TRANSCRICAO`, nunca `CODIGO`.

Convenção de IDs: `DEC` decisão · `RF` requisito funcional · `RNF` requisito não funcional/restrição ·
`ALT` alternativa descartada · `OUT` fora de escopo/adiado · `OPEN` questão em aberto ·
`TEC` detalhe técnico secundário · `COD` gancho no código · `AMB` ambiguidade a resolver no design.

---

## (a) Decisões fechadas

| ID | Decisão | Origem |
|----|---------|--------|
| DEC-01 | Webhook é **outbound** apenas: sai da plataforma para o cliente | [09:02] Marcos, [09:03] Sofia |
| DEC-02 | Disparo **assíncrono** via **padrão Outbox**: o evento é inserido na tabela `webhook_outbox` na mesma transação SQL que atualiza `orders` e `order_status_history` | [09:06] Diego, [09:08] Larissa |
| DEC-03 | Outbox no **MySQL existente**, sem infraestrutura nova | [09:07] Diego, [09:08] Larissa |
| DEC-04 | Falha ao inserir na outbox provoca **rollback** da mudança de status. Status não pode mudar sem o evento sair | [09:40] Bruno, [09:41] Diego |
| DEC-05 | Worker lê a outbox por **polling a cada 2 segundos**. Latência mínima de 2s no pior caso é aceita | [09:09] Diego, [09:10] Marcos, [09:10] Larissa |
| DEC-06 | Worker roda em **processo separado** da API (mesmo banco, mesma stack) | [09:11] Diego, [09:11] Larissa |
| DEC-07 | Novo entry-point `src/worker.ts` + script `npm run worker` | [09:11] Larissa, [09:28] Bruno |
| DEC-08 | Worker usa **instância própria de PrismaClient** (mesma `DATABASE_URL`) | [09:30] Bruno |
| DEC-09 | **Single-worker**: ordem garantida apenas por `order_id`, processando em ordem de `created_at`. Documentado como limitação conhecida | [09:12] Diego, [09:13] Larissa |
| DEC-10 | Retry com **backoff exponencial**: 5 tentativas, intervalos 1m / 5m / 30m / 2h / 12h (~15h no total) | [09:15] Diego, [09:17] Diego, [09:17] Larissa |
| DEC-11 | Esgotadas as tentativas, o evento vai para a **DLQ em tabela separada** `webhook_dead_letter` | [09:18] Diego, [09:48] Larissa |
| DEC-12 | **Replay manual** da DLQ via endpoint admin. O evento volta para a outbox como pendente | [09:18] Diego, [09:19] Larissa |
| DEC-13 | Replay exige **role ADMIN**, reaproveitando o `requireRole` existente | [09:36] Sofia, [09:36] Larissa |
| DEC-14 | Autenticação da entrega por **HMAC-SHA256** sobre o corpo do request, enviada em `X-Signature` | [09:20] Sofia, [09:22] Sofia |
| DEC-15 | **Secret única por endpoint** de webhook, nunca global | [09:21] Sofia |
| DEC-16 | Secret **rotacionável** via API, com **grace period de 24h**: a antiga continua válida em paralelo e depois expira | [09:21] Sofia, [09:22] Sofia |
| DEC-17 | Garantia de entrega **at-least-once**. O cliente deduplica pelo `X-Event-Id` | [09:24] Diego, [09:25] Diego, [09:26] Larissa |
| DEC-18 | `event_id` é um **UUID gerado quando o evento entra na outbox**, único por evento | [09:25] Diego |
| DEC-19 | **Reuso máximo dos padrões existentes**: AppError, Pino, error middleware, módulo em `src/modules`, schemas Zod e códigos de erro | [09:29] Bruno, [09:30] Larissa |
| DEC-20 | Módulo `src/modules/webhooks` com controller, service, repository, routes e schemas | [09:27] Bruno, [09:30] Larissa |
| DEC-21 | Códigos de erro do módulo com prefixo **`WEBHOOK_`** | [09:28] Bruno, [09:29] Larissa |
| DEC-22 | Nenhuma lib de log nova: usa o Pino já existente | [09:29] Bruno |
| DEC-23 | Integração via função `publishWebhookEvent(tx, order, fromStatus, toStatus)`, que recebe o tx client da transação. Não injeta repository no `OrderService` | [09:41] Bruno, [09:41] Diego |
| DEC-24 | **Filtro de eventos aplicado na inserção** da outbox: se nenhum webhook do customer quer aquele status, não insere | [09:33] Marcos, [09:34] Bruno, [09:34] Diego |
| DEC-25 | Payload é **snapshot renderizado na inserção** (reflete o estado no momento da mudança) | [09:52] Larissa, [09:52] Diego, [09:52] Bruno |
| DEC-26 | IDs das novas tabelas são **UUID**, como no resto do projeto | [09:51] Larissa |
| DEC-27 | Endpoints de CRUD de configuração: **qualquer role autenticada** (por enquanto) | [09:36] Marcos, [09:37] Sofia |
| DEC-28 | `customer_id` vai no **body ou no path**, **não vem do JWT** (JWT é do usuário operador) | [09:32] Bruno, [09:32] Larissa |
| DEC-29 | Webhooks são cadastrados **pela API da plataforma**, com JWT do sistema (usuários que representam o cliente) | [09:32] Marcos |

## (b) Requisitos funcionais

| ID | Requisito | Origem |
|----|-----------|--------|
| RF-01 | Notificar o cliente B2B quando o status de um pedido dele muda | [09:00] Marcos |
| RF-02 | Cadastrar webhook (`POST`): campos `url` e lista de status de interesse. `customer_id` no body ou no path | [09:31] Marcos, [09:32] Larissa |
| RF-03 | A **secret é gerada pela plataforma** e devolvida na criação | [09:31] Marcos |
| RF-04 | Configuração do webhook armazena url, secret, customer_id e estado ativo | [09:21] Bruno, [09:21] Sofia |
| RF-05 | Editar webhook (`PATCH`) | [09:33] Bruno |
| RF-06 | Remover webhook (`DELETE`) | [09:33] Bruno |
| RF-07 | Listar os webhooks de um customer (`GET`) | [09:33] Bruno |
| RF-08 | Filtro de eventos por endpoint: lista de status que o webhook quer ouvir (ex.: só `SHIPPED` e `DELIVERED`) | [09:33] Bruno, [09:33] Marcos |
| RF-09 | Rotacionar a secret: endpoint para o cliente pedir uma nova secret pela API | [09:21] Sofia |
| RF-10 | Histórico de entregas `GET /webhooks/:id/deliveries`: últimas 100 entregas com sucesso/falha, payload, response e tempo de resposta | [09:34] Marcos |
| RF-11 | Replay de DLQ `POST /admin/webhooks/dead-letter/:id/replay` | [09:18] Diego, [09:35] Diego |
| RF-12 | O replay registra em log **quem** o executou (auditoria) | [09:36] Sofia |
| RF-13 | Worker processa eventos pendentes, envia o HTTP e marca como entregue | [09:08] Diego, [09:09] Diego |
| RF-14 | Falha de entrega agenda retry conforme o backoff. Após a última tentativa, move para a DLQ | [09:15] Diego, [09:17] Larissa |
| RF-15 | DLQ guarda payload, motivo da falha e timestamp | [09:18] Diego |
| RF-16 | Cada request de webhook leva os headers `X-Event-Id`, `X-Signature`, `X-Timestamp`, `X-Webhook-Id` e `Content-Type: application/json` | [09:44] Diego, [09:44] Sofia, [09:45] Diego |

## (c) Requisitos não funcionais / restrições

| ID | Requisito / restrição | Origem |
|----|-----------------------|--------|
| RNF-01 | Latência percebida como "tempo real": **< 10 segundos** da mudança de status até a notificação | [09:02] Marcos |
| RNF-02 | Polling de 2s atende o requisito de < 10s | [09:09] Diego, [09:10] Marcos |
| RNF-03 | Lentidão ou indisponibilidade do cliente **não pode travar** a mudança de status de outros pedidos | [09:04] Bruno |
| RNF-04 | Atomicidade: evento registrado se e somente se a transação de status commitar | [09:06] Diego, [09:40] Bruno |
| RNF-05 | URL do webhook **obrigatoriamente `https`**. `http` é recusado com erro de validação no schema Zod | [09:23] Sofia |
| RNF-06 | Payload limitado a **64KB**. Acima disso gera **erro** (não trunca) | [09:23] Sofia, [09:24] Diego, [09:24] Larissa |
| RNF-07 | **Timeout de 10s** na chamada HTTP do worker. Estourou o timeout, conta como falha e vai para retry | [09:42] Diego |
| RNF-08 | Índices da outbox em `status` e `created_at`. O worker lê pendentes em **batch pequeno** | [09:08] Diego |
| RNF-09 | Sem nova infraestrutura (time pequeno) | [09:07] Diego |
| RNF-10 | **Revisão de segurança da Sofia: pelo menos 2 dias úteis** antes do deploy (HMAC e geração de secret) | [09:46] Sofia, [09:49] Sofia |
| RNF-11 | Prazo: **3 sprints**, incluindo a revisão de segurança. A Atlas quer até **fim de novembro** | [09:45] Marcos, [09:46] Larissa, [09:47] Larissa |
| RNF-12 | Ordenação: não há garantia global. Só por `order_id` enquanto houver um único worker | [09:13] Larissa, [09:14] Marcos |
| RNF-13 | Payload **enxuto**, sem `items`. Detalhes via `GET /orders/:id` | [09:43] Diego, [09:44] Bruno |
| RNF-14 | At-least-once precisa estar **documentado em destaque** no portal do desenvolvedor | [09:26] Marcos |

## (d) Alternativas descartadas

| ID | Alternativa | Motivo do descarte | Origem |
|----|-------------|--------------------|--------|
| ALT-01 | Disparo HTTP **síncrono** dentro do `changeStatus` | Transação já é pesada; um cliente lento trava mudanças de outros pedidos; não dá para fazer rollback do status se o cliente estiver fora | [09:04] Bruno, [09:06] Diego |
| ALT-02 | **Redis Streams / Redis Cluster** como fila | Exige subir mais infra; overengineering para um time pequeno | [09:07] Larissa, [09:07] Diego |
| ALT-03 | **Trigger do banco** para o worker ser mais reativo | MySQL não tem LISTEN/NOTIFY; trigger só executa SQL e não notifica processo externo. Avisar o worker exigiria improviso | [09:09] Bruno, [09:09] Diego |
| ALT-04 | Worker **dentro do processo da API** | Se a API reinicia, perde o worker | [09:11] Diego |
| ALT-05 | **Retry indefinido** com backoff | Evento fica pendurado para sempre se o cliente sumiu | [09:15] Diego |
| ALT-06 | **3 tentativas** | Pouco: três retries em ~30 min mataria o evento; já houve cliente com 2h de manutenção planejada | [09:16] Bruno, [09:16] Diego |
| ALT-07 | DLQ como **status "failed" na própria outbox** | Tabela separada deixa a leitura da outbox mais limpa e serve de evidência para debug/reprocessamento | [09:17] Larissa, [09:18] Diego |
| ALT-08 | **Secret global** da plataforma | Se vaza uma, vaza tudo | [09:21] Sofia |
| ALT-09 | **Truncar** payload acima do limite | Se chegou nesse tamanho, há algo errado: melhor errar | [09:23] Sofia |
| ALT-10 | Garantia **exactly-once** | Exige coordenação dos dois lados, muito mais complexo. At-least-once + event_id é o padrão de mercado (Stripe, GitHub) | [09:25] Diego |
| ALT-11 | **Injetar o repository** de webhook no `OrderService` | Função pura recebendo o `tx` é suficiente | [09:41] Bruno, [09:41] Diego |
| ALT-12 | **Compartilhar o PrismaClient** da API com o worker | PrismaClient é por processo | [09:29] Diego, [09:30] Bruno |
| ALT-13 | Filtrar eventos **na hora do envio** | Filtrar na inserção economiza linhas na tabela | [09:34] Diego, [09:34] Bruno |
| ALT-14 | Guardar só `order_id` e **renderizar o payload no envio** | O pedido pode mudar depois; o evento deve refletir o estado do momento da mudança | [09:51] Bruno, [09:52] Larissa |
| ALT-15 | ID **auto incremental** na outbox | Projeto usa UUID em tudo | [09:51] Diego, [09:51] Larissa |
| ALT-16 | `customer_id` **extraído do JWT** | JWT é do usuário operador, não do cliente | [09:31] Marcos, [09:32] Bruno, [09:32] Larissa |
| ALT-17 | Incluir **items** do pedido no payload | Infla o payload; o cliente busca em `GET /orders/:id` | [09:43] Diego |

## (e) Fora de escopo / adiado

| ID | Item | Situação | Origem |
|----|------|----------|--------|
| OUT-01 | **Email** para o cliente quando o webhook falha repetidamente | Adiado para a próxima fase, depois de medir impacto | [09:37] Marcos, [09:37] Larissa, [09:38] Marcos |
| OUT-02 | **Dashboard visual** para o cliente ver os webhooks | Fora: projeto separado do time de frontend; agora só endpoints | [09:39] Marcos, [09:40] Larissa |
| OUT-03 | **Webhooks inbound** (cliente enviando para nós) | Fora: só outbound | [09:02] Marcos, [09:03] Sofia |
| OUT-04 | **Arquivamento** de linhas entregues após ~30 dias | Fora do escopo desta feature | [09:08] Diego |
| OUT-05 | **Múltiplos workers em paralelo** (particionar por `order_id` ou lock pessimista) | Problema do futuro | [09:13] Diego |
| OUT-06 | **Rate limiting** de envio ao cliente | Não entra agora: observar e decidir depois (ver OPEN-01) | [09:39] Diego, [09:39] Larissa |
| OUT-07 | **Ordenação global** de eventos | Clientes nunca pediram | [09:14] Marcos |

## (f) Questões em aberto

| ID | Questão | Estado | Origem |
|----|---------|--------|--------|
| OPEN-01 | Rate limiting de saída quando muitos pedidos de um cliente mudam ao mesmo tempo (ex.: 50/min) | Observar e decidir depois | [09:38] Diego, [09:39] Diego, [09:39] Larissa |
| OPEN-02 | Escalar além de um worker sem perder a ordem por `order_id` | Adiado: particionamento ou lock pessimista | [09:13] Bruno, [09:13] Diego |
| OPEN-03 | Notificação por email em falhas consecutivas (ex.: 3 seguidas) | Próxima fase, depois de medir impacto | [09:37] Marcos, [09:37] Larissa |
| OPEN-04 | Endurecer as permissões do CRUD de configuração (hoje qualquer role autenticada) | "Mais pra frente" | [09:37] Sofia |
| OPEN-05 | Política de arquivamento das linhas entregues (~30 dias) | Fora desta feature, sem dono definido | [09:08] Diego |

## (g) Detalhes técnicos secundários

| ID | Detalhe | Origem |
|----|---------|--------|
| TEC-01 | Payload JSON: `event_id`, `event_type` (`"order.status_changed"`), `timestamp` ISO 8601, `order_id`, `order_number`, `from_status`, `to_status`, `customer_id` e campos básicos do pedido, como `total_cents` | [09:43] Diego |
| TEC-02 | Header `X-Event-Id`: UUID do evento | [09:25] Diego, [09:44] Diego |
| TEC-03 | Header `X-Signature`: HMAC-SHA256 do corpo | [09:20] Sofia, [09:44] Diego |
| TEC-04 | Header `X-Timestamp`: momento do envio, para o cliente detectar replay attack se quiser | [09:44] Diego |
| TEC-05 | Header `X-Webhook-Id`: id do endpoint cadastrado, para clientes com vários cadastros | [09:44] Sofia, [09:45] Diego |
| TEC-06 | Header `Content-Type: application/json` | [09:44] Diego |
| TEC-07 | Timeout HTTP de 10s | [09:42] Diego |
| TEC-08 | Status da outbox: pendente, processando, falhou, entregue | [09:08] Diego |
| TEC-09 | Polling busca os pendentes **mais antigos** primeiro (ordem de `created_at`) | [09:09] Diego, [09:12] Diego |
| TEC-10 | Snapshot do payload gravado na inserção | [09:52] Larissa |
| TEC-11 | IDs UUID | [09:51] Larissa |
| TEC-12 | DLQ: payload, motivo da falha, timestamp | [09:18] Diego |
| TEC-13 | Lógica de processamento em arquivo do módulo, `webhook.worker.ts` ou `webhook.processor.ts` (nome não fechado) | [09:28] Bruno |
| TEC-14 | Exemplos de códigos de erro: `WEBHOOK_NOT_FOUND`, `WEBHOOK_INVALID_URL`, `WEBHOOK_SECRET_REQUIRED` ("etc.") | [09:28] Bruno |
| TEC-15 | Limite de payload: 64KB | [09:24] Diego |
| TEC-16 | Backoff 1m, 5m, 30m, 2h, 12h | [09:17] Diego |
| TEC-17 | Estimativa por bloco: outbox+DLQ 1 sprint; worker+retry 1 sprint; CRUD+deliveries ½; integração no order.service + testes E2E ½; HMAC/schemas/validações "mais um pouco" | [09:46] Larissa |

## (h) Ganchos no código

| ID | Caminho:linha | O que existe | Relevância para a feature | Origem na reunião |
|----|---------------|--------------|---------------------------|-------------------|
| COD-01 | `src/modules/orders/order.service.ts:126` | `changeStatus(id, input, userId)` | Ponto de inserção do evento | [09:40] Bruno |
| COD-02 | `src/modules/orders/order.service.ts:131` | `this.prisma.$transaction(async (tx) => ...)` | `publishWebhookEvent(tx, ...)` é chamado dentro deste callback | [09:41] Bruno |
| COD-03 | `src/modules/orders/order.service.ts:138-139` | `from = order.status`, `to = input.toStatus` | Fornecem `fromStatus`/`toStatus` | [09:41] Bruno |
| COD-04 | `src/modules/orders/order.service.ts:151-167` | Débito/reposição de estoque, `order.update`, `orderStatusHistory.create` | Confirma a "transação pesada"; a inserção na outbox entra depois do history | [09:04] Bruno |
| COD-05 | `src/modules/orders/order.service.ts:24` | `type TxClient = Prisma.TransactionClient` | Tipo do parâmetro `tx` de `publishWebhookEvent` | [09:41] Diego |
| COD-06 | `src/modules/orders/order.service.ts:95-113` | `create()` grava o history inicial `null -> PENDING` sem passar por `changeStatus` | Ver AMB-04 | — (só código) |
| COD-07 | `src/modules/orders/order.status.ts:3-10` | Máquina de estados (PENDING→PAID→PROCESSING→SHIPPED→DELIVERED; CANCELLED) | Valores válidos para o filtro de eventos | [09:12] Larissa |
| COD-08 | `prisma/schema.prisma:16-23` | `enum OrderStatus` | Tipo da lista de status do filtro (`z.nativeEnum`) | [09:33] Marcos |
| COD-09 | `prisma/schema.prisma:26` (e demais models) | `id String @id @default(uuid()) @db.Char(36)` | Padrão de ID das novas tabelas | [09:51] Larissa |
| COD-10 | `prisma/schema.prisma:74-97` | `model Order` com `orderNumber`, `customerId`, `totalCents`, índices `@@index` | Campos do snapshot e padrão de índice | [09:43] Diego |
| COD-11 | `prisma/schema.prisma:116-131` | `model OrderStatusHistory` (`order_status_history`) | Tabela citada na transação | [09:06] Diego |
| COD-12 | `prisma/schema.prisma:25-38` | `model User` sem relação com `Customer` | Ver AMB-05 | [09:32] Marcos |
| COD-13 | `src/shared/errors/app-error.ts:3-16` | `AppError(message, statusCode, errorCode, details)` | Base dos erros `WEBHOOK_*` | [09:28] Bruno |
| COD-14 | `src/shared/errors/http-errors.ts:3,27,33,39` | `BadRequestError`, `NotFoundError`, `ConflictError`, `UnprocessableEntityError` com `code` customizável | Classes-base para os erros `WEBHOOK_*` | [09:28] Bruno |
| COD-15 | `src/shared/errors/http-errors.ts:45,55` | `InvalidStatusTransitionError`, `InsufficientStockError` | Modelo de erro específico de domínio | [09:28] Bruno |
| COD-16 | `src/shared/errors/index.ts:1-13` | Barrel de exportação dos erros | Onde exportar os novos erros | [09:30] Larissa |
| COD-17 | `src/middlewares/error.middleware.ts:15-24` | Trata `AppError` → `{ error: { code, message, details } }` | Erros `WEBHOOK_*` tratados sem mudança | [09:29] Bruno |
| COD-18 | `src/middlewares/error.middleware.ts:26,37` | Trata `ZodError` e `PrismaClientKnownRequestError` (P2002, P2025) | Validação https/payload e not found já cobertos | [09:29] Bruno |
| COD-19 | `src/middlewares/auth.middleware.ts:27` | `authenticate` (JWT Bearer, `req.user = { id, email, role }`) | Protege o CRUD; `req.user.id` alimenta o log de auditoria do replay | [09:32] Larissa, [09:36] Sofia |
| COD-20 | `src/middlewares/auth.middleware.ts:49` | `requireRole(...roles)` | Replay exige `requireRole('ADMIN')` | [09:36] Larissa |
| COD-21 | `src/middlewares/auth.middleware.ts:9` | `role: 'ADMIN' \| 'OPERATOR'` | Roles disponíveis | [09:35] Larissa |
| COD-22 | `src/modules/users/user.routes.ts:14-15` | Único uso atual de `authenticate, requireRole('ADMIN')` | Exemplo a seguir no endpoint admin | [09:36] Larissa |
| COD-23 | `src/middlewares/validate.middleware.ts:11` | `validate({ body, query, params })` com Zod | Validação dos endpoints de webhook | [09:23] Sofia, [09:30] Larissa |
| COD-24 | `src/modules/orders/order.schemas.ts:4,18-21` | `z.string().uuid()` para params; `z.nativeEnum(OrderStatus)` | Padrão para `webhookIdParamSchema` e lista de status | [09:30] Larissa |
| COD-25 | `src/modules/orders/order.routes.ts:12-27` | Router com `router.use(authenticate)` + `validate(...)` | Modelo do `webhook.routes.ts` | [09:27] Bruno |
| COD-26 | `src/modules/orders/` (controller, service, repository, routes, schemas) | Estrutura padrão de módulo | Replicar em `src/modules/webhooks/` | [09:27] Bruno |
| COD-27 | `src/routes/index.ts:13-31` | `Controllers` + `buildApiRouter` | Registrar `/webhooks` e a rota admin | [09:27] Bruno |
| COD-28 | `src/app.ts:26-53` | `buildControllers(prisma)` instancia repository → service → controller | Instanciar o módulo de webhooks | [09:27] Bruno |
| COD-29 | `src/app.ts:67` | `app.use('/api/v1', buildApiRouter(...))` | Endpoints reais ficam sob `/api/v1` (ex.: `/api/v1/webhooks`) | — (só código) |
| COD-30 | `src/server.ts:6-27` | `bootstrap()`, shutdown em SIGINT/SIGTERM com `prisma.$disconnect()` | Modelo para `src/worker.ts` | [09:11] Larissa |
| COD-31 | `src/config/database.ts:4-8` | `createPrismaClient()` | Worker chama a factory para ter instância própria | [09:30] Bruno |
| COD-32 | `src/config/env.ts:3-10` | Schema Zod de env (`DATABASE_URL`, `LOG_LEVEL`, ...) | Mesma `DATABASE_URL` no worker | [09:30] Bruno |
| COD-33 | `src/shared/logger/index.ts:13-32` | Pino com `redact` (authorization, password, token) e timestamp ISO | Logger do módulo/worker; a lista de redact não cobre `secret` (ver AMB-07) | [09:29] Bruno, [09:22] Diego |
| COD-34 | `src/middlewares/request-logger.middleware.ts:5-28` | `X-Request-Id` (uuid v4) + log `http_request` com `durationMs` | Padrão de log estruturado e correlação | [09:29] Bruno |
| COD-35 | `package.json:32` | Dependência `uuid` 11.0.3 já instalada | Geração do `event_id` sem lib nova | [09:25] Diego |
| COD-36 | `package.json:10-21` | Scripts `dev`, `start`, `test`... (sem `worker`) | Adicionar `worker` | [09:11] Larissa |
| COD-37 | `package.json:7-9` | `engines.node >= 20` | `fetch` nativo + `AbortSignal.timeout` permitem os 10s sem lib nova | [09:42] Diego |
| COD-38 | `src/shared/http/response.ts:22-24` | `paginated(data, page, pageSize, total)` | Formato de listagem (GET webhooks/deliveries) | [09:30] Larissa |
| COD-39 | `tests/setup.ts:8-16` | `beforeEach` limpa as tabelas com `deleteMany` | As novas tabelas precisam entrar na limpeza | [09:40] Bruno |
| COD-40 | `tests/orders.test.ts:59` | Teste "transitions PENDING -> PAID and decrements stock" | Base para o teste de integração outbox + changeStatus | [09:40] Bruno |
| COD-41 | `src/modules/orders/order.controller.ts:38-41` | `changeStatus` recebe `req.user.id` | Fluxo HTTP até o service, sem mudança de contrato | [09:40] Bruno |

---

## Ambiguidades (não decididas na reunião; as resolvidas na revisão estão marcadas como **Resolvido**)

| ID | Ambiguidade | Evidência | Origem |
|----|-------------|-----------|--------|
| AMB-01 | **"5 tentativas" com 5 intervalos**: 1 envio + 5 retries (6 chamadas) ou 5 chamadas no total? A soma de ~15h só fecha com 5 intervalos após a 1ª falha **Resolvido (2026-10-15):** 1 envio + 5 retries. | "teto de tentativas" e "5" vs. lista de 5 intervalos e "~15 horas entre primeira falha e última tentativa" | [09:15] Diego, [09:17] Diego, [09:48] Larissa |
| AMB-02 | Status "falhou" na outbox coexistindo com a DLQ separada: significa "falhou, aguardando retry"? **Proposta no FDD §4:** `FAILED` = estado terminal na outbox; evidência na DLQ. | Lista de status vs. DLQ em tabela própria | [09:08] Diego, [09:18] Diego |
| AMB-03 | **Uma linha na outbox por evento ou por (evento × webhook)?** O cliente pode ter vários cadastros (`X-Webhook-Id`) e o filtro é por webhook **Resolvido (2026-10-15):** 1 linha por evento × webhook. | Filtro "se nenhum webhook do customer quer" + header por webhook + event_id "único por evento" | [09:25] Diego, [09:34] Bruno, [09:44] Sofia |
| AMB-04 | A **criação do pedido** (`null → PENDING`) gera evento? A reunião só fala de `changeStatus` **Resolvido (2026-10-15):** não gera evento nesta fase. | `create()` grava history sem passar por `changeStatus` | `src/modules/orders/order.service.ts:95-113`, [09:40] Bruno |
| AMB-05 | **Vínculo usuário ↔ customer** não existe no código: qualquer usuário autenticado pode gerenciar webhooks de qualquer customer | Coerente com DEC-27 e OPEN-04, mas precisa estar explícito como risco | `prisma/schema.prisma:25-38`, [09:32] Marcos, [09:37] Sofia |
| AMB-06 | `customer_id` no **body ou no path**: não foi escolhido **Proposta no FDD §6:** body na criação, path na listagem. | "passado no body ou no path" | [09:32] Larissa |
| AMB-07 | Como a secret é **armazenada e protegida** (inclusive dos logs) não foi discutido; houve caso de vazamento em log de cliente **Proposta no FDD §10:** coluna própria, nunca devolvida após criação, mascarada no logger; criptografia em repouso para a revisão da Sofia. | Redact atual do Pino não inclui `secret` | [09:22] Diego, `src/shared/logger/index.ts:4-11` |
| AMB-08 | `WEBHOOK_SECRET_REQUIRED` foi citado como exemplo, mas a secret é gerada pela plataforma: em que caso ocorre? **Proposta no FDD §7:** erro do worker quando o endpoint está sem secret válida → DLQ. | Exemplo "etc." | [09:28] Bruno, [09:31] Marcos |
| AMB-09 | **Respostas 2xx = sucesso?** Quais status do cliente contam como falha (4xx também retenta?) **Proposta no FDD §5.3:** qualquer resposta fora de 2xx retenta. | Só o timeout foi definido como falha | [09:42] Diego |
| AMB-10 | Métricas e tracing **não foram discutidos**; só existe Pino **Proposta no FDD §9:** métricas via logs/SQL e correlação por IDs, sem infra nova. | Qualquer métrica no FDD é proposta | [09:29] Bruno, `src/shared/logger/index.ts` |
| AMB-11 | Deliveries "últimos 100": limite fixo ou paginação? **Proposta no FDD §6.6:** últimas 100, sem paginação. | Só "últimos 100" | [09:34] Marcos |
| AMB-12 | Onde os 64KB são verificados (na inserção na outbox, que roda dentro do `changeStatus`, ou no envio)? Se for na inserção, o erro derruba a mudança de status **Proposta no FDD §7:** checagem no worker; excedeu → DLQ sem retry. | "a gente não envia" / "erro caso ultrapasse" | [09:23] Sofia, [09:24] Larissa |

---

## Checklist das Armadilhas (`processo/PLANO.md`)

| Armadilha | Onde ficou registrada | OK |
|-----------|-----------------------|----|
| `customer_id` não vem do JWT | DEC-28, ALT-16 | ✅ |
| Ordering só por `order_id` e single-worker | DEC-09, RNF-12, OUT-07 | ✅ |
| Arquivamento de 30 dias fora | OUT-04, OPEN-05 | ✅ |
| Email fora (próxima fase) | OUT-01, OPEN-03 | ✅ |
| Dashboard fora | OUT-02 | ✅ |
| Rate limiting em aberto | OUT-06, OPEN-01 | ✅ |
| Inbound fora | DEC-01, OUT-03 | ✅ |
| 64KB = erro, RNF e não ADR | RNF-06, ALT-09 | ✅ |
| HTTPS = validação Zod | RNF-05 | ✅ |
| Snapshot na inserção | DEC-25, ALT-14 | ✅ |
| Filtro na inserção | DEC-24, ALT-13 | ✅ |
| UUID | DEC-26, ALT-15 | ✅ |
| Payload sem items | RNF-13, ALT-17 | ✅ |
| CRUD autenticado / replay ADMIN + log | DEC-13, DEC-27, RF-12 | ✅ |
| Ambiguidade das 5 tentativas | AMB-01 | ✅ |
| Métricas/tracing são proposta | AMB-10 | ✅ |
