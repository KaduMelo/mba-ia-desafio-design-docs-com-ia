# ADR-004: Assinatura HMAC-SHA256 com secret por endpoint e rotação com grace period de 24h

- **Status:** Aceito
- **Data:** decidido na reunião técnica de quinta-feira, 09:00 (a transcrição não traz data de calendário); registrado em 2026-10-15
- **Decisores:** Sofia (Eng. de Segurança), Larissa (Tech Lead), Diego (Eng. Sênior, Plataforma), Bruno (Eng. Pleno, Pedidos)
- **Relacionados:** [ADR-005](ADR-005-entrega-at-least-once-com-x-event-id.md) (demais headers do envio)

## Contexto

Os webhooks levam dados de pedidos para endpoints fora da nossa infraestrutura. O cliente precisa conseguir verificar **que a requisição veio da plataforma** e **que o payload não foi adulterado** no caminho ([09:19] Sofia). Além disso, já houve cliente que vazou uma secret no log da própria aplicação ([09:22] Diego).

## Decisão

1. **HMAC-SHA256 sobre o corpo do request**, enviado no header `X-Signature`. O cliente recalcula e compara do lado dele ([09:20] Sofia, [09:22] Sofia). É o padrão de mercado e há bibliotecas em todas as stacks ([09:20] Sofia).
2. **Uma secret única por endpoint de webhook**, guardada junto com a configuração (url, secret, customer_id, estado ativo) ([09:21] Sofia, [09:21] Bruno).
3. **A secret é gerada pela plataforma** e devolvida ao cliente na criação do webhook ([09:31] Marcos).
4. **Rotação via API:** o cliente pede uma nova secret. A antiga continua válida em paralelo por **24 horas** e depois expira ([09:21] Sofia, [09:22] Sofia).
5. **Revisão de segurança obrigatória** da Sofia, com pelo menos 2 dias úteis, sobre o código de HMAC e de geração de secret antes do deploy ([09:46] Sofia, [09:49] Sofia).

Complementos que **não são decisões arquiteturais** e aparecem aqui só como contexto: URL obrigatoriamente `https`, validada no schema Zod ([09:23] Sofia), e o header `X-Timestamp`, que permite ao cliente detectar replay attack se quiser ([09:44] Diego).

## Alternativas Consideradas

| Alternativa | Por que foi descartada |
|---|---|
| **Secret global da plataforma** (uma para todos os clientes) | "Se vaza uma, vaza tudo" ([09:21] Sofia). |
| **Rotação sem período de convivência** (troca imediata) | Plausível, mas não atende à necessidade de dar tempo ao cliente para migrar os sistemas dele ([09:21] Sofia). Daí o grace period de 24 h. |

## Consequências

**Positivas**
- Integridade e autenticidade verificáveis pelo cliente, com algoritmo padrão.
- Um vazamento fica restrito a um endpoint, e a rotação permite corrigir sem downtime para o cliente.

**Negativas**
- A plataforma passa a guardar segredos de clientes. Como armazená-los e como mantê-los fora dos logs (o `redact` atual em `src/shared/logger/index.ts` não cobre `secret`) ficou para o FDD e para a revisão da Sofia. Ver AMB-07 no inventário.
- Durante as 24 h de rotação, duas secrets valem ao mesmo tempo. O design precisa definir como o cliente distingue qual secret assinou a mensagem.
- Validar a assinatura passa a ser responsabilidade do cliente.

**Trade-off explícito:** aceita-se a complexidade de gerenciar uma secret por endpoint, com rotação e convivência temporária, em troca de **isolar o impacto de vazamentos**, um risco que já aconteceu na prática.

## Referências

- [09:19] Sofia, [09:20] Sofia, [09:20] Bruno, [09:21] Sofia, [09:21] Bruno, [09:22] Diego, [09:22] Sofia: HMAC, secret por endpoint, rotação
- [09:23] Sofia: https obrigatório
- [09:31] Marcos: secret gerada pela plataforma
- [09:44] Diego: `X-Signature`, `X-Timestamp`
- [09:46] Sofia, [09:49] Sofia: revisão de segurança
- `src/shared/logger/index.ts` (lista de `redact`, linhas 4–11)
