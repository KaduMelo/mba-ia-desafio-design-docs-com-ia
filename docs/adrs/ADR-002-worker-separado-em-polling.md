# ADR-002: Worker em processo separado, lendo a outbox por polling de 2 segundos

- **Status:** Aceito
- **Data:** decidido na reunião técnica de quinta-feira, 09:00 (a transcrição não traz data de calendário); registrado em 2026-10-15
- **Decisores:** Larissa (Tech Lead), Diego (Eng. Sênior, Plataforma), Bruno (Eng. Pleno, Pedidos), Marcos (PM)
- **Relacionados:** [ADR-001](ADR-001-outbox-no-mysql.md) (a tabela consumida), [ADR-003](ADR-003-retry-backoff-e-dlq.md) (o que acontece quando a entrega falha)

## Contexto

Com a outbox ([ADR-001](ADR-001-outbox-no-mysql.md)), alguém precisa ler os eventos pendentes e fazer a chamada HTTP. Faltava decidir três coisas: **como** o consumidor descobre que há eventos novos, **onde** ele roda e **quantas** instâncias existem.

Para os clientes, "tempo real" é qualquer coisa abaixo de 10 segundos ([09:02] Marcos). O MySQL não tem um mecanismo de notificação para processos externos equivalente ao `LISTEN/NOTIFY` do Postgres ([09:09] Diego).

## Decisão

1. **Polling em loop a cada 2 segundos.** A cada ciclo, o worker busca os eventos pendentes mais antigos em lote pequeno, processa e marca o resultado ([09:09] Diego, [09:08] Diego). A latência de até 2 s no pior caso foi aceita ([09:10] Marcos, [09:10] Larissa).
2. **Processo separado da API.** O worker tem entry-point próprio, `src/worker.ts` (arquivo novo, a criar), e script `npm run worker` (a criar), seguindo o modelo de `src/server.ts` ([09:11] Diego, [09:11] Larissa).
3. **Mesmo banco, mesma stack, PrismaClient próprio.** O worker usa a mesma `DATABASE_URL` (`src/config/env.ts`), mas cria a própria instância via `createPrismaClient()` (`src/config/database.ts`), porque o PrismaClient é por processo ([09:11] Bruno, [09:30] Bruno).
4. **Uma única instância (single-worker).** Os eventos são processados em ordem de `created_at`. Isso garante a ordem **apenas por `order_id`** e **apenas enquanto houver um único worker**. Fica documentado como limitação conhecida ([09:12] Diego, [09:13] Larissa).

## Alternativas Consideradas

| Alternativa | Por que foi descartada |
|---|---|
| **Trigger do banco** para tornar o worker reativo | O trigger do MySQL só executa SQL e não notifica processo externo. Avisar o worker exigiria improvisos, como escrever em arquivo ou chamar um endpoint ([09:09] Bruno, [09:09] Diego). |
| **Worker dentro do processo da API** | Se a API reinicia, o worker morre junto ([09:11] Diego). |
| **Reusar o PrismaClient da API** | Não é possível: o PrismaClient é por processo ([09:29] Diego, [09:30] Bruno). |
| **Múltiplos workers em paralelo** | A garantia de ordem se perde. Particionar por `order_id` ou usar lock pessimista foi deixado para o futuro ([09:13] Diego). |

## Consequências

**Positivas**
- Simples de implementar e operar, sem dependência nova.
- Deploys e restarts da API não interrompem as entregas, e vice-versa.
- A latência máxima de descoberta (2 s) fica bem abaixo do teto de 10 s.

**Negativas**
- Consultas ao banco a cada 2 s, mesmo sem eventos novos (custo baixo graças aos índices em `status` e `created_at`).
- O single-worker limita a vazão e é um ponto único de falha: se o worker cair, as entregas atrasam até ele voltar (os eventos não se perdem, ficam na outbox).
- Ordem garantida só por pedido. Os clientes não pediram ordem global ([09:14] Marcos). Com retries ([ADR-003](ADR-003-retry-backoff-e-dlq.md)), a garantia vale só para a primeira tentativa: um evento em backoff pode ser ultrapassado por eventos posteriores do mesmo pedido ([FDD §8](../FDD.md#8-estratégias-de-resiliência)).
- Um novo processo para implantar e monitorar.

**Trade-off explícito:** aceita-se uma latência de até 2 s e uma vazão limitada a um worker, em troca de **simplicidade operacional e ordem por pedido sem coordenação distribuída**. Escalar horizontalmente continua como questão em aberto.

## Referências

- [09:08] Larissa, [09:09] Diego, [09:09] Bruno, [09:10] Marcos, [09:10] Larissa: polling de 2 s
- [09:11] Diego, [09:11] Larissa, [09:11] Bruno, [09:28] Bruno: processo separado e `src/worker.ts` (a criar)
- [09:12] Larissa, [09:12] Diego, [09:13] Bruno, [09:13] Diego, [09:13] Larissa, [09:14] Marcos: ordem e single-worker
- [09:29] Diego, [09:30] Bruno: PrismaClient próprio
- `src/server.ts`, `src/config/database.ts`, `src/config/env.ts`
