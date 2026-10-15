# ADR-001: Padrão Outbox no MySQL, na mesma transação do `changeStatus`

- **Status:** Aceito
- **Data:** decidido na reunião técnica de quinta-feira, 09:00 (a transcrição não traz data de calendário); registrado em 2026-10-15
- **Decisores:** Larissa (Tech Lead), Diego (Eng. Sênior, Plataforma), Bruno (Eng. Pleno, Pedidos)
- **Relacionados:** [ADR-002](ADR-002-worker-separado-em-polling.md) (quem consome a outbox), [ADR-007](ADR-007-payload-snapshot-e-filtro-na-insercao.md) (o que é gravado nela)

## Contexto

Três clientes B2B (Atlas Comercial, MaxDistribuição, Nova Cargo) querem ser notificados quando o status dos pedidos deles muda. Hoje eles fazem polling em `GET /orders` ([09:00] Marcos).

A mudança de status acontece em `OrderService.changeStatus` (`src/modules/orders/order.service.ts:126`). Ela roda dentro de um `prisma.$transaction` (linha 131) que já atualiza `orders`, grava `order_status_history` e debita ou repõe estoque (linhas 151–167). Bruno chamou essa transação de "pesada" ([09:04] Bruno).

A notificação precisa sair **se e somente se** a mudança de status for efetivada. Ao mesmo tempo, um cliente lento ou fora do ar não pode afetar a mudança de status de outros pedidos ([09:04] Bruno).

## Decisão

Adotar o **padrão Outbox na base MySQL existente**:

1. Dentro da mesma transação de `changeStatus`, depois de gravar o `order_status_history`, é inserida uma linha na nova tabela `webhook_outbox` com o evento ([09:06] Diego).
2. A inserção é feita pela função `publishWebhookEvent(tx, order, fromStatus, toStatus)`, que recebe o `tx` da transação corrente ([09:41] Bruno, [09:41] Diego).
3. Se a inserção na outbox falhar, a transação inteira faz rollback. Não pode haver status alterado sem evento registrado ([09:40] Bruno, [09:41] Diego).
4. A entrega HTTP **nunca** acontece dentro da transação. Ela fica com um processo consumidor ([ADR-002](ADR-002-worker-separado-em-polling.md)).
5. A tabela tem índices em `status` e `created_at`, para leitura eficiente dos pendentes ([09:08] Diego).

## Alternativas Consideradas

| Alternativa | Por que foi descartada |
|---|---|
| **Chamada HTTP síncrona dentro do `changeStatus`** | A transação já é pesada. Um cliente lento travaria a mudança de status de outros pedidos, e não há como "desfazer" um status porque o cliente está fora do ar ([09:04] Bruno). "Síncrono está fora de questão" ([09:06] Diego). |
| **Redis Streams / Redis Cluster** como fila | Exigiria subir e operar infraestrutura nova. Para um time pequeno, é overengineering ([09:07] Larissa, [09:07] Diego). |
| **Injetar um repository de webhooks no `OrderService`** | Acoplamento desnecessário. Uma função que recebe o `tx` resolve ([09:41] Diego). |

## Consequências

**Positivas**
- Consistência garantida pelo próprio banco: commit grava status e evento juntos, rollback descarta os dois ([09:06] Diego).
- A latência e a disponibilidade dos clientes deixam de afetar a mudança de status.
- Nenhuma infraestrutura nova: mesmo MySQL, mesmo Prisma.

**Negativas**
- A transação de `changeStatus` ganha mais um `INSERT`. Uma falha nele derruba a mudança de status (efeito desejado, mas é um novo ponto de falha).
- A tabela cresce continuamente. O arquivamento das linhas entregues (~30 dias) ficou **fora do escopo** desta feature ([09:08] Diego).
- A entrega deixa de ser imediata e passa a depender do intervalo de leitura do consumidor ([ADR-002](ADR-002-worker-separado-em-polling.md)).

**Trade-off explícito:** troca-se a latência mínima de uma chamada síncrona e a escalabilidade de um broker dedicado por **atomicidade sem infraestrutura nova**. Para um time pequeno, com requisito de "< 10 s" ([09:02] Marcos), essa troca é favorável.

## Referências

- [09:03] Larissa, [09:04] Bruno, [09:06] Diego, [09:07] Larissa, [09:07] Diego, [09:08] Diego, [09:08] Larissa: discussão e decisão
- [09:40] Bruno, [09:41] Bruno, [09:41] Diego: integração com `changeStatus` via `publishWebhookEvent(tx, ...)`
- `src/modules/orders/order.service.ts` (linhas 24, 126, 131, 151–167)
- `prisma/schema.prisma` (`model OrderStatusHistory`, linhas 116–131)
