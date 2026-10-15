# ADR-007: Payload como snapshot gravado na inserção, com filtro de status na inserção

- **Status:** Aceito
- **Data:** decidido na reunião técnica de quinta-feira, 09:00 (a transcrição não traz data de calendário); registrado em 2026-10-15
- **Decisores:** Larissa (Tech Lead), Diego (Eng. Sênior, Plataforma), Bruno (Eng. Pleno, Pedidos), Marcos (PM)
- **Relacionados:** [ADR-001](ADR-001-outbox-no-mysql.md) (a inserção na outbox), [ADR-005](ADR-005-entrega-at-least-once-com-x-event-id.md) (unidade de entrega)

## Contexto

Com a outbox definida ([ADR-001](ADR-001-outbox-no-mysql.md)), faltavam duas decisões sobre **o que** é gravado nela e **quando**:

1. A linha guarda o payload pronto, ou só o `order_id`, montando o payload na hora do envio? ([09:51] Bruno)
2. Cada webhook escolhe os status que quer receber ([09:33] Marcos). Esse filtro é aplicado ao inserir na outbox ou ao enviar? ([09:34] Diego)

O payload pode ficar horas na outbox por causa dos retries ([ADR-003](ADR-003-retry-backoff-e-dlq.md)), e o pedido pode mudar nesse intervalo.

## Decisão

1. **Snapshot na inserção.** O payload é renderizado e gravado no momento da mudança de status, dentro da transação. Ele reflete o estado do pedido **naquele momento**, mesmo que o pedido mude depois ([09:52] Larissa, [09:52] Diego, [09:52] Bruno).
2. **Filtro na inserção.** `publishWebhookEvent` só insere eventos para os webhooks ativos do customer que ouvem o `to_status`. Se nenhum quiser aquele status, nada é inserido ([09:34] Bruno, [09:34] Diego).
3. **Payload enxuto:** dados de identificação e de status do pedido, como `order_id`, `order_number`, `from_status`, `to_status`, `customer_id` e `total_cents`, **sem os itens**. Quem precisar de detalhes consulta `GET /orders/:id` ([09:43] Diego, [09:44] Bruno). O contrato exato fica no FDD.

> **Decisão de escopo (AMB-04), definida na revisão desta documentação em 2026-10-15:** a reunião tratou apenas de `changeStatus` ([09:40] Bruno). A criação do pedido (`create()` em `src/modules/orders/order.service.ts`, que grava o histórico `null → PENDING`) **não gera evento** nesta fase. Incluir a criação depende de validação do PM com os clientes.

## Alternativas Consideradas

| Alternativa | Por que foi descartada |
|---|---|
| **Guardar só o `order_id` e renderizar no envio** | Se o pedido mudar depois, o evento deixaria de refletir o estado do momento da mudança. "Senão tem caso esquisito" ([09:52] Larissa). |
| **Filtrar no envio** | Inseriria linhas que nunca seriam enviadas. Filtrar na inserção "economiza linha na tabela" ([09:34] Bruno). |
| **Payload completo, com itens** | Infla o payload sem necessidade ([09:43] Diego). |

## Consequências

**Positivas**
- O que o cliente recebe é coerente com a transição notificada, mesmo em um retry 15 h depois.
- O worker não precisa consultar `orders` para enviar: lê a linha e dispara.
- A outbox só contém trabalho real, porque não há linhas descartadas no envio.

**Negativas**
- A consulta aos webhooks do customer e a renderização do payload passam a rodar **dentro da transação** de `changeStatus` (`src/modules/orders/order.service.ts:131`), aumentando um pouco o seu custo.
- Uma alteração de filtro feita depois do evento não afeta eventos já inseridos.
- Um snapshot "envelhece": em um retry tardio, o cliente pode receber um estado já superado. A mitigação é consultar `GET /orders/:id` e conferir o `X-Event-Id` ([ADR-005](ADR-005-entrega-at-least-once-com-x-event-id.md)).

**Trade-off explícito:** troca-se um pequeno custo extra dentro da transação, e a impossibilidade de reavaliar filtros já aplicados, por **fidelidade do evento ao momento da mudança** e por uma outbox sem linhas inúteis.

## Referências

- [09:33] Bruno, [09:33] Marcos, [09:34] Diego, [09:34] Bruno: filtro na inserção
- [09:43] Marcos, [09:43] Diego, [09:44] Bruno: formato enxuto do payload
- [09:51] Bruno, [09:52] Larissa, [09:52] Diego, [09:52] Bruno: snapshot
- [09:40] Bruno: escopo em `changeStatus`
- `src/modules/orders/order.service.ts` (`changeStatus`, linhas 126–131; `create`, linhas 95–113)
- `src/modules/orders/order.status.ts` (status válidos para o filtro)
- `prisma/schema.prisma` (`enum OrderStatus`, `model Order`)
