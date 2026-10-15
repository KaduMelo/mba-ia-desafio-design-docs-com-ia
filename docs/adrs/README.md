# Architectural Decision Records

Este diretório guarda os ADRs do Sistema de Webhooks de Notificação de Pedidos. Cada arquivo registra
**uma** decisão, no formato MADR, com nome `ADR-NNN-titulo-em-kebab-case.md`.
Todas as decisões vêm da reunião técnica registrada em [`TRANSCRICAO.md`](../../TRANSCRICAO.md).

| ADR | Decisão | Status |
|-----|---------|--------|
| [ADR-001](ADR-001-outbox-no-mysql.md) | Padrão Outbox no MySQL, na mesma transação do `changeStatus` | Aceito |
| [ADR-002](ADR-002-worker-separado-em-polling.md) | Worker em processo separado, polling de 2 s, single-worker | Aceito |
| [ADR-003](ADR-003-retry-backoff-e-dlq.md) | Retry com backoff 1m/5m/30m/2h/12h e DLQ em tabela separada com replay ADMIN | Aceito |
| [ADR-004](ADR-004-hmac-sha256-com-secret-por-endpoint.md) | HMAC-SHA256, secret por endpoint e rotação com grace period de 24 h | Aceito |
| [ADR-005](ADR-005-entrega-at-least-once-com-x-event-id.md) | Entrega at-least-once com deduplicação por `X-Event-Id` | Aceito |
| [ADR-006](ADR-006-reuso-dos-padroes-do-projeto.md) | Reuso dos padrões existentes do projeto | Aceito |
| [ADR-007](ADR-007-payload-snapshot-e-filtro-na-insercao.md) | Payload como snapshot e filtro de status na inserção | Aceito |

As decisões marcadas dentro dos ADRs como **"Proposta de design (AMB-xx)"** são interpretações de pontos
ambíguos da reunião e aguardam confirmação. Ver a tabela de ambiguidades em
[`processo/INVENTARIO.md`](../../processo/INVENTARIO.md).
