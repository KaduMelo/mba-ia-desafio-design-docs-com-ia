# ADR-006: Reuso dos padrões existentes do projeto no módulo de webhooks

- **Status:** Aceito
- **Data:** decidido na reunião técnica de quinta-feira, 09:00 (a transcrição não traz data de calendário); registrado em 2026-10-15
- **Decisores:** Larissa (Tech Lead), Bruno (Eng. Pleno, Pedidos), Diego (Eng. Sênior, Plataforma), Sofia (Eng. de Segurança)
- **Relacionados:** [ADR-002](ADR-002-worker-separado-em-polling.md) (entry-point do worker), [ADR-003](ADR-003-retry-backoff-e-dlq.md) (replay ADMIN)

## Contexto

O OMS já tem convenções consolidadas: módulos de domínio, hierarquia de erros com códigos, middleware de erro centralizado, autenticação JWT com checagem de role, validação com Zod e log com Pino. A feature de webhooks poderia trazer padrões próprios ou seguir os existentes ([09:27] Bruno).

## Decisão

**Reuso máximo do que já existe. O webhook entra como um módulo igual aos outros** ([09:30] Larissa):

| Padrão existente | Onde está | Como o módulo de webhooks usa |
|---|---|---|
| Módulo por domínio (controller, service, repository, routes, schemas) | `src/modules/orders/*`, `src/modules/customers/*` | Nova pasta `src/modules/webhooks/` (a criar) com a mesma estrutura ([09:27] Bruno) |
| Classe base de erro | `src/shared/errors/app-error.ts` (`AppError(message, statusCode, errorCode, details)`) | Todos os erros do módulo derivam dela |
| Erros HTTP com código customizável e erros de domínio | `src/shared/errors/http-errors.ts` (`NotFoundError`, `ConflictError`, `UnprocessableEntityError`, `InvalidStatusTransitionError`, `InsufficientStockError`) | Novos erros seguem o mesmo modelo, com **prefixo `WEBHOOK_`**, ex.: `WEBHOOK_NOT_FOUND`, `WEBHOOK_INVALID_URL` ([09:28] Bruno, [09:29] Larissa) |
| Exportação central dos erros | `src/shared/errors/index.ts` | Novos erros exportados pelo mesmo barrel |
| Middleware de erro centralizado | `src/middlewares/error.middleware.ts` (trata `AppError`, `ZodError` e erros do Prisma) | Trata os erros do módulo **sem nenhuma alteração** ([09:29] Bruno) |
| Autenticação e autorização | `src/middlewares/auth.middleware.ts` (`authenticate`, `requireRole`) | CRUD com `authenticate`. Replay da DLQ com `requireRole('ADMIN')`, como já é feito em `src/modules/users/user.routes.ts` ([09:36] Larissa) |
| Validação Zod | `src/middlewares/validate.middleware.ts` + `*.schemas.ts` | Schemas do módulo, incluindo a regra `https` da URL ([09:23] Sofia) |
| Logger | `src/shared/logger/index.ts` (Pino) | API e worker usam o mesmo logger, sem lib nova ([09:29] Bruno) |
| Registro de rotas | `src/routes/index.ts`, `src/app.ts` (`buildControllers`) | Rotas e controller do módulo registrados da mesma forma |
| IDs UUID | `prisma/schema.prisma` (`@id @default(uuid()) @db.Char(36)`) | Novas tabelas com UUID ([09:51] Larissa) |
| Bootstrap de processo | `src/server.ts` | Modelo para o novo `src/worker.ts` (a criar) ([09:11] Larissa) |

## Alternativas Consideradas

| Alternativa | Por que foi descartada |
|---|---|
| **Padrões próprios para o módulo** (outro formato de erro, outro logger) | Plausível, mas não traria ganho. "Não vamos botar nada novo" ([09:29] Bruno), e o middleware atual já trata os erros sem mudança. |
| **Restringir o CRUD de configuração a ADMIN** | Mexer em configuração de webhook pode ser feito por qualquer role autenticada **por enquanto**. Só o replay de DLQ exige ADMIN ([09:36] Marcos, [09:37] Sofia). Endurecer as permissões fica como questão em aberto. |

## Consequências

**Positivas**
- Curva de aprendizado mínima: quem conhece `orders` entende `webhooks`.
- Respostas de erro no mesmo formato `{ error: { code, message, details } }` para o cliente da API.
- Nenhuma mudança em `src/middlewares/error.middleware.ts` e nenhuma dependência nova de log.

**Negativas**
- O módulo herda as limitações atuais. Por exemplo, `src/middlewares/auth.middleware.ts` só conhece as roles `ADMIN` e `OPERATOR`, e `prisma/schema.prisma` não liga `User` a `Customer`. Com isso, qualquer usuário autenticado pode gerenciar webhooks de qualquer customer (AMB-05 no inventário).
- A lista de `redact` do logger precisa ser estendida para não vazar secrets ([ADR-004](ADR-004-hmac-sha256-com-secret-por-endpoint.md)).

**Trade-off explícito:** aceita-se herdar as limitações do modelo atual, como a autorização apenas por role, em troca de **consistência e velocidade de entrega** dentro do prazo de 3 sprints ([09:46] Larissa).

## Referências

- [09:27] Bruno, [09:28] Diego, [09:28] Bruno: estrutura de módulo e localização do worker
- [09:28] Bruno, [09:29] Larissa: códigos `WEBHOOK_*`
- [09:29] Bruno, [09:30] Larissa: Pino, error middleware, decisão de reuso máximo
- [09:36] Sofia, [09:36] Larissa, [09:37] Sofia: roles
- `src/shared/errors/app-error.ts`, `src/shared/errors/http-errors.ts`, `src/shared/errors/index.ts`
- `src/middlewares/error.middleware.ts`, `src/middlewares/auth.middleware.ts`, `src/middlewares/validate.middleware.ts`
- `src/shared/logger/index.ts`, `src/routes/index.ts`, `src/app.ts`, `src/server.ts`, `src/modules/users/user.routes.ts`, `prisma/schema.prisma`
