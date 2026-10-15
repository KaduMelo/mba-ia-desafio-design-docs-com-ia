# ADR-003: Retry com backoff exponencial (1m/5m/30m/2h/12h) e DLQ em tabela separada

- **Status:** Aceito
- **Data:** decidido na reunião técnica de quinta-feira, 09:00 (a transcrição não traz data de calendário); registrado em 2026-10-15
- **Decisores:** Larissa (Tech Lead), Diego (Eng. Sênior, Plataforma), Bruno (Eng. Pleno, Pedidos), Marcos (PM), Sofia (Eng. de Segurança)
- **Relacionados:** [ADR-002](ADR-002-worker-separado-em-polling.md) (quem executa os retries), [ADR-005](ADR-005-entrega-at-least-once-com-x-event-id.md) (efeito dos retries para o cliente)

## Contexto

O endpoint do cliente pode estar fora do ar, lento ou em manutenção. Já houve cliente com duas horas de indisponibilidade em manutenção planejada ([09:16] Diego). Era preciso decidir quantas vezes tentar de novo, com que intervalos, e o que fazer com um evento que nunca consegue ser entregue.

## Decisão

1. **Backoff exponencial com 5 tentativas**, nos intervalos **1 min → 5 min → 30 min → 2 h → 12 h**. São cerca de 15 horas entre a primeira falha e a última tentativa ([09:15] Diego, [09:17] Diego, [09:17] Larissa).
2. **Um timeout de 10 s** na chamada HTTP conta como falha e entra no retry ([09:42] Diego).
3. **Esgotadas as tentativas, o evento vai para a DLQ**, a tabela separada `webhook_dead_letter`. Ela guarda o payload, o motivo da falha e o timestamp ([09:18] Diego).
4. **Replay manual** via `POST /admin/webhooks/dead-letter/:id/replay`. O replay recoloca o evento na outbox como pendente ([09:18] Diego, [09:35] Diego).
5. O replay **exige role `ADMIN`** (reaproveita o `requireRole`, ver [ADR-006](ADR-006-reuso-dos-padroes-do-projeto.md)) e **registra em log quem o executou**, para auditoria ([09:36] Sofia, [09:36] Larissa).

> **Proposta de design (AMB-01, pendente de confirmação):** a reunião fala em "5 tentativas" e lista 5 intervalos. Interpretamos como **envio inicial + 5 retentativas**, uma após cada intervalo. É a única leitura em que os "~15 h entre a primeira falha e a última tentativa" ([09:17] Diego) fecham com os intervalos citados.

## Alternativas Consideradas

| Alternativa | Por que foi descartada |
|---|---|
| **Retry indefinido** com backoff | O evento fica pendurado para sempre se o cliente sumiu ([09:15] Diego). |
| **3 tentativas** (mais agressivo) | Pouco: três tentativas em ~30 min matariam o evento durante uma manutenção comum de 2 h ([09:16] Bruno, [09:16] Diego). |
| **DLQ como status "failed" na própria outbox** | Uma tabela separada mantém a leitura da outbox limpa e serve de evidência para debug e reprocessamento ([09:17] Larissa, [09:18] Diego). |

## Consequências

**Positivas**
- Cobre indisponibilidades de até ~15 h sem intervenção humana. Para o PM, um cliente fora por mais tempo "já tá com problema sério dele" ([09:17] Marcos).
- Nenhum evento se perde em silêncio: o que falha definitivamente fica auditável na DLQ.
- O replay controlado por ADMIN, com log de autoria, atende ao pedido de segurança.

**Negativas**
- Um evento pode chegar com até ~15 h de atraso, e os retries podem entregar o mesmo evento mais de uma vez (tratado no [ADR-005](ADR-005-entrega-at-least-once-com-x-event-id.md)).
- O reprocessamento da DLQ é manual. O cliente não é avisado proativamente: o alerta por email ficou para a próxima fase ([09:37] Larissa).
- Uma tabela a mais para modelar e manter.

**Trade-off explícito:** troca-se a garantia de "tentar até conseguir" por um **teto previsível de ~15 h**, com falhas definitivas visíveis e reprocessáveis por um humano.

## Referências

- [09:14] Larissa, [09:15] Diego, [09:15] Bruno, [09:16] Bruno, [09:16] Diego, [09:16] Larissa, [09:17] Diego, [09:17] Marcos, [09:17] Larissa: política de retry
- [09:17] Larissa, [09:18] Diego, [09:18] Bruno, [09:19] Larissa: DLQ e replay
- [09:35] Larissa, [09:35] Diego, [09:36] Sofia, [09:36] Larissa: replay ADMIN com auditoria
- [09:42] Sofia, [09:42] Diego: timeout de 10 s
- [09:48] Larissa: resumo final
- `src/middlewares/auth.middleware.ts` (`requireRole`, linha 49)
