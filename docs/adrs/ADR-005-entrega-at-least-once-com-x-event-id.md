# ADR-005: Garantia de entrega at-least-once com deduplicação via `X-Event-Id`

- **Status:** Aceito
- **Data:** decidido na reunião técnica de quinta-feira, 09:00 (a transcrição não traz data de calendário); registrado em 2026-10-15
- **Decisores:** Diego (Eng. Sênior, Plataforma), Larissa (Tech Lead), Sofia (Eng. de Segurança), Bruno (Eng. Pleno, Pedidos), Marcos (PM)
- **Relacionados:** [ADR-003](ADR-003-retry-backoff-e-dlq.md) (retries geram duplicatas), [ADR-004](ADR-004-hmac-sha256-com-secret-por-endpoint.md) (assinatura do envio)

## Contexto

Com retries ([ADR-003](ADR-003-retry-backoff-e-dlq.md)), existem cenários em que o cliente recebe e processa o evento, mas a plataforma não registra o sucesso: um timeout depois do processamento, uma queda do worker entre o envio e a marcação. Nesses casos, o evento é reenviado. Era preciso decidir qual garantia oferecer e como o cliente lida com duplicatas.

## Decisão

1. **A plataforma garante entrega at-least-once.** O cliente pode receber o mesmo evento mais de uma vez e precisa estar preparado ([09:24] Diego).
2. **Todo evento tem um `event_id`**, um UUID gerado quando o evento entra na outbox. Ele é enviado no header **`X-Event-Id`** e permanece o mesmo em todas as tentativas ([09:25] Diego).
3. **A deduplicação é feita pelo cliente**, usando o `event_id` ([09:25] Diego, [09:26] Larissa).
4. O comportamento **será documentado em destaque** no portal do desenvolvedor ([09:26] Marcos).
5. O header **`X-Webhook-Id`** acompanha o envio para identificar qual cadastro originou a chamada, útil para clientes com vários endpoints ([09:44] Sofia, [09:45] Diego).

> **Decisão de design (AMB-03), definida na revisão desta documentação em 2026-10-15:** como o filtro de status é por webhook e cada envio leva um `X-Webhook-Id`, adota-se **uma linha de outbox por par (evento × webhook)**. Cada linha tem seu próprio `event_id`, retry e destino de DLQ. Assim, uma falha em um endpoint não atrasa os outros endpoints do mesmo cliente. O modelo exato fica no FDD.

## Alternativas Consideradas

| Alternativa | Por que foi descartada |
|---|---|
| **Exactly-once** | Exigiria coordenação entre os dois lados e "fica muito mais complexo" ([09:25] Diego). At-least-once com event_id resolve a grande maioria dos casos e é o modelo usado por Stripe e GitHub ([09:25] Diego). |
| **At-most-once** (sem retry) | Plausível, mas incompatível com a política de retry aceita ([ADR-003](ADR-003-retry-backoff-e-dlq.md)): perder um evento é pior para o cliente do que recebê-lo em dobro. |

## Consequências

**Positivas**
- Implementação simples do nosso lado, sem coordenação distribuída.
- Modelo conhecido pelos clientes, porque é o mesmo dos grandes provedores.

**Negativas**
- Joga responsabilidade para o cliente, como a Sofia apontou ([09:25] Sofia). Um cliente que não deduplica vai processar eventos repetidos.
- Depende de a documentação no portal ser clara e visível.

**Trade-off explícito:** troca-se uma garantia mais forte (exactly-once) por **simplicidade de implementação**, transferindo ao cliente a tarefa de deduplicar por `X-Event-Id`.

## Referências

- [09:24] Diego, [09:25] Bruno, [09:25] Diego, [09:25] Sofia, [09:26] Marcos, [09:26] Larissa: at-least-once e `X-Event-Id`
- [09:44] Diego, [09:44] Sofia, [09:45] Diego: headers do envio
- [09:48] Larissa: resumo final
- `package.json` (dependência `uuid` já disponível, linha 32)
