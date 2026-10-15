# PRD — Sistema de Webhooks de Notificação de Pedidos

| Campo | Valor |
|---|---|
| **Responsável de produto** | Marcos (PM) |
| **Tech Lead** | Larissa |
| **Status** | Escopo aprovado na reunião ([09:48] Larissa; confirmações em [09:49]) |
| **Data** | 2026-10-15 (base: reunião técnica de quinta-feira, 09:00) |
| **Prazo alvo** | Fim de novembro, em 3 sprints ([09:45] Marcos, [09:47] Larissa) |
| **Documentos relacionados** | [RFC](RFC.md) · [FDD](FDD.md) · [ADRs](adrs/README.md) |

> Este documento responde **por que** e **o quê**. A arquitetura está no [RFC](RFC.md), as decisões estão nos
> [ADRs](adrs/README.md) e o "como construir" está no [FDD](FDD.md). Itens marcados com ***(proposta)*** não foram
> definidos na reunião e foram acrescentados para tornar o documento verificável.

---

## 1. Resumo e contexto

O OMS vai passar a **avisar os clientes B2B automaticamente, por webhook, sempre que o status de um pedido deles mudar**. Os clientes cadastram uma URL `https` e escolhem os status que querem receber. A plataforma envia uma notificação assinada em menos de 10 segundos, tenta de novo se o cliente estiver fora do ar e guarda o histórico de entregas.

A funcionalidade vem de um pedido formal de três clientes B2B: **Atlas Comercial, MaxDistribuição e Nova Cargo** ([09:00] Marcos). Hoje o OMS não tem nenhum mecanismo de notificação externa.

## 2. Problema e motivação

- **Integração lenta e cara para o cliente.** Para saber se algo mudou, os clientes consultam `GET /orders` periodicamente ([09:00] Marcos). Cada consulta sem novidade é custo para eles e para nós, e a mudança só é percebida na próxima consulta.
- **Risco comercial concreto.** A Atlas sinalizou que pode **migrar para um concorrente** se a funcionalidade não for entregue até o fim do trimestre ([09:00] Marcos).
- **Expectativa clara de latência.** Para os clientes, "tempo real" é qualquer coisa **abaixo de 10 segundos**. O importante é não precisar atualizar manualmente ([09:02] Marcos).

## 3. Público-alvo e cenários de uso

| Persona | Quem é | Origem |
|---|---|---|
| **Cliente B2B integrador** | Equipe técnica do cliente (ex.: Atlas) que recebe os webhooks no sistema dela | [09:00] Marcos |
| **Usuário que representa o cliente** | Usuário da plataforma, autenticado por JWT, que cadastra e gerencia os webhooks pela API | [09:32] Marcos |
| **Administrador da plataforma (ADMIN)** | Reprocessa notificações que falharam definitivamente | [09:36] Sofia |
| **PM / portal do desenvolvedor** | Publica a documentação de integração para os clientes | [09:26] Marcos, [09:40] Marcos |

**Cenários**

| # | Cenário | Origem |
|---|---|---|
| C1 | A Atlas quer saber **só** quando os pedidos dela viram `SHIPPED` ou `DELIVERED`. Ela cadastra um webhook com esse filtro e não recebe os demais status. | [09:33] Marcos |
| C2 | Um pedido passa por `PAID → PROCESSING → SHIPPED` em sequência. O cliente recebe as três notificações, na ordem, em segundos. | [09:12] Larissa |
| C3 | O endpoint do cliente fica 2 horas em manutenção planejada. Quando ele volta, as notificações pendentes chegam sozinhas. | [09:16] Diego |
| C4 | O cliente vazou a secret num log. Ele pede uma nova pela API e tem 24 h para atualizar os sistemas sem perder notificações. | [09:21] Sofia, [09:22] Diego |
| C5 | O cliente quer conferir o que recebeu: consulta as últimas 100 entregas, com status, payload, resposta e tempo. | [09:34] Marcos |
| C6 | Uma notificação esgotou as tentativas. Um ADMIN a reprocessa depois que o cliente corrige o problema, e fica registrado quem fez isso. | [09:18] Diego, [09:36] Sofia |
| C7 | O cliente tem dois cadastros (ex.: ERP e BI) e identifica qual deles originou cada chamada. | [09:44] Sofia |

## 4. Objetivos e métricas de sucesso

| # | Objetivo | Métrica | Meta | Origem |
|---|---|---|---|---|
| O1 | Notificar em "tempo real" | Tempo entre a mudança de status e a chegada da notificação ao cliente (sem contar a resposta dele) | **< 10 s**. Por desenho, a descoberta leva **≤ 2 s** | [09:02] Marcos, [09:10] Larissa |
| O2 | Não perder notificações | Mudanças de status efetivadas sem evento registrado | **0** (garantia transacional) | [09:40] Bruno, [09:41] Diego |
| O3 | Tolerar indisponibilidade do cliente | Janela coberta por retentativas automáticas antes da DLQ | **~15 h** (1 envio + 5 retentativas) | [09:17] Diego, [09:17] Marcos |
| O4 | Reter os clientes solicitantes | Entrega da funcionalidade em produção | **Até o fim de novembro**, em **3 sprints** | [09:45] Marcos, [09:47] Larissa |
| O5 | Reduzir o polling *(proposta)* | Chamadas a `GET /orders` dos 3 clientes solicitantes depois da adoção | Queda em relação à linha de base medida antes do lançamento. A meta numérica será definida com os clientes | [09:00] Marcos |

O O5 não teve meta definida na reunião, mas mede o problema descrito em [09:00]. A decisão sobre os próximos passos, como email de alerta e rate limiting, depende de "medir o impacto" ([09:37] Larissa, [09:39] Diego).

## 5. Escopo

### 5.1 Incluso

- Cadastro, edição, remoção e listagem de webhooks por customer, via API autenticada.
- Filtro, por webhook, dos status de pedido que ele quer receber.
- Notificação automática a cada mudança de status de pedido.
- Assinatura de cada notificação e secret exclusiva por webhook, com rotação.
- Retentativa automática e fila de falhas definitivas (DLQ), com reprocessamento por ADMIN.
- Histórico de entregas consultável pelo cliente.

### 5.2 Fora de escopo

| Item | Situação | Origem |
|---|---|---|
| **Email de alerta** quando o webhook do cliente falha repetidamente | **Adiado** para a próxima fase, depois de medir o impacto | [09:37] Marcos, [09:37] Larissa |
| **Dashboard visual** para o cliente ver os webhooks | **Descartado** nesta fase: projeto separado do time de frontend. Agora, só endpoints | [09:39] Marcos, [09:40] Larissa |
| **Rate limiting** de envio para o cliente | **Não entra.** Observar em produção e decidir depois | [09:38] Diego, [09:39] Larissa |
| **Webhooks de entrada** (cliente enviando para a plataforma) | **Descartado:** só saída | [09:02] Marcos, [09:03] Sofia |
| **Arquivamento** do histórico após ~30 dias | Fora desta feature | [09:08] Diego |
| **Garantia de ordem global** entre pedidos | Não é necessária: os clientes nunca pediram | [09:14] Marcos |
| **Entrega exatamente uma vez** (exactly-once) | Descartada pela complexidade. O cliente deduplica | [09:25] Diego |
| **Notificação na criação do pedido** | Não nesta fase: só mudanças de status | decisão R3 do [RFC](RFC.md#51-ambiguidades-da-reunião-resolvidas-nesta-revisão) |

## 6. Requisitos funcionais

| ID | Requisito | Origem |
|---|---|---|
| PRD-FR-01 | A plataforma notifica o customer, por webhook, toda vez que o status de um pedido dele muda | [09:00] Marcos |
| PRD-FR-02 | Um usuário autenticado cadastra um webhook informando o customer, a URL e os status de interesse | [09:31] Marcos, [09:32] Larissa |
| PRD-FR-03 | A secret do webhook é gerada pela plataforma e devolvida no cadastro | [09:31] Marcos |
| PRD-FR-04 | O usuário edita um webhook (URL, status de interesse, ativo/inativo) | [09:33] Bruno |
| PRD-FR-05 | O usuário remove um webhook | [09:33] Bruno |
| PRD-FR-06 | O usuário lista os webhooks de um customer | [09:33] Bruno |
| PRD-FR-07 | Cada webhook só recebe os status que escolheu ouvir | [09:33] Marcos, [09:34] Bruno |
| PRD-FR-08 | O cliente pode pedir uma nova secret pela API. A anterior continua válida por 24 h | [09:21] Sofia |
| PRD-FR-09 | O cliente consulta as últimas 100 entregas de um webhook, com sucesso ou falha, payload, resposta e tempo de resposta | [09:34] Marcos |
| PRD-FR-10 | Notificações que falham são retentadas automaticamente com intervalos crescentes. Depois do limite, vão para uma fila de falhas (DLQ) | [09:15] Diego, [09:17] Larissa |
| PRD-FR-11 | Um ADMIN reprocessa uma notificação da DLQ | [09:18] Diego, [09:35] Diego |
| PRD-FR-12 | O reprocessamento registra quem o executou | [09:36] Sofia |
| PRD-FR-13 | Cada notificação traz um identificador único do evento, para o cliente descartar duplicatas | [09:25] Diego |
| PRD-FR-14 | Cada notificação traz a assinatura, o horário de envio e o identificador do webhook que a originou | [09:44] Diego, [09:44] Sofia |
| PRD-FR-15 | A notificação traz os dados essenciais do pedido e da mudança (número, status anterior e novo, cliente, valor total), sem os itens | [09:43] Diego |

## 7. Requisitos não funcionais

| ID | Requisito | Origem |
|---|---|---|
| PRD-NFR-01 | Latência abaixo de 10 s entre a mudança de status e a notificação | [09:02] Marcos |
| PRD-NFR-02 | A notificação nunca atrasa nem bloqueia a mudança de status de outros pedidos | [09:04] Bruno |
| PRD-NFR-03 | Mudança de status e registro da notificação são atômicos: um não existe sem o outro | [09:06] Diego, [09:40] Bruno |
| PRD-NFR-04 | Entrega **pelo menos uma vez**: duplicatas são possíveis e documentadas em destaque no portal | [09:24] Diego, [09:26] Marcos |
| PRD-NFR-05 | Toda notificação é assinada (HMAC-SHA256) com uma secret exclusiva do webhook | [09:20] Sofia, [09:21] Sofia |
| PRD-NFR-06 | Só são aceitas URLs `https` | [09:23] Sofia |
| PRD-NFR-07 | Notificações acima de 64 KB não são enviadas: geram erro, sem truncar | [09:23] Sofia, [09:24] Larissa |
| PRD-NFR-08 | O cliente tem até 10 s para responder. Acima disso, conta como falha | [09:42] Diego |
| PRD-NFR-09 | A ordem é garantida apenas por pedido, não globalmente | [09:13] Larissa |
| PRD-NFR-10 | Sem infraestrutura nova: usa o banco e a stack existentes | [09:07] Diego, [09:30] Larissa |
| PRD-NFR-11 | O reprocessamento manual é restrito a administradores | [09:36] Sofia |

## 8. Decisões e trade-offs principais

| Decisão | Trade-off aceito | ADR |
|---|---|---|
| Registrar o evento no banco, na mesma transação da mudança de status | Consistência total, em troca de uma pequena latência e sem fila dedicada | [ADR-001](adrs/ADR-001-outbox-no-mysql.md) |
| Processo de envio separado, verificando a cada 2 s | Simplicidade, em troca de até 2 s de espera e de um único processo de envio | [ADR-002](adrs/ADR-002-worker-separado-em-polling.md) |
| 5 retentativas em ~15 h, depois DLQ com reprocesso manual | Teto previsível, em troca de intervenção humana nos casos extremos | [ADR-003](adrs/ADR-003-retry-backoff-e-dlq.md) |
| Assinatura com secret por webhook e rotação com 24 h de carência | Isolamento de vazamentos, em troca de gerenciar uma secret por cadastro | [ADR-004](adrs/ADR-004-hmac-sha256-com-secret-por-endpoint.md) |
| Entrega "pelo menos uma vez" | Simplicidade, em troca de o cliente precisar descartar duplicatas | [ADR-005](adrs/ADR-005-entrega-at-least-once-com-x-event-id.md) |
| Seguir os padrões existentes do código | Velocidade e consistência, herdando as limitações atuais de permissão | [ADR-006](adrs/ADR-006-reuso-dos-padroes-do-projeto.md) |
| Conteúdo da notificação congelado no momento da mudança | Fidelidade ao momento do evento, em troca de dados possivelmente defasados em retentativas tardias | [ADR-007](adrs/ADR-007-payload-snapshot-e-filtro-na-insercao.md) |

## 9. Dependências

| Dependência | Tipo | Origem |
|---|---|---|
| Revisão de segurança da Sofia, com **2 dias úteis** antes do deploy (HMAC e geração de secret) | Interna, bloqueante para o deploy | [09:46] Sofia, [09:49] Sofia |
| Documentação no **portal do desenvolvedor**: como integrar, validar a assinatura e deduplicar | Interna (PM) | [09:26] Marcos, [09:40] Marcos |
| Confirmação de prazo com os clientes | Externa (PM) | [09:47] Marcos |
| Clientes implementam a validação de assinatura e a deduplicação por identificador de evento | Externa | [09:25] Sofia, [09:26] Marcos |
| Banco MySQL e stack atuais (Prisma, autenticação JWT, papéis ADMIN/OPERATOR) | Técnica, existente | [09:11] Diego, [09:36] Larissa |
| Deploy de um novo processo de envio, separado da API | Operacional | [09:11] Diego |

## 10. Riscos e mitigação

| Risco | Probabilidade | Impacto | Mitigação | Origem |
|---|---|---|---|---|
| Atraso na entrega e perda da Atlas para um concorrente | Média | Alto | Escopo enxuto (email, dashboard e rate limiting fora), estimativa de 3 sprints e prazo confirmado com os clientes | [09:00] Marcos, [09:46] Larissa, [09:47] Marcos |
| Cliente processa notificações duplicadas porque não deduplica | Média | Médio | Identificador de evento estável e documentação em destaque no portal | [09:25] Sofia, [09:26] Marcos |
| Vazamento da secret de um cliente | Média (já aconteceu) | Alto | Secret por webhook, rotação com 24 h de carência e revisão de segurança antes do deploy | [09:22] Diego, [09:21] Sofia, [09:46] Sofia |
| Processo de envio parado → notificações atrasam | Baixa | Alto | As notificações ficam guardadas e saem quando o processo volta. Monitorar a fila *(proposta)* | [09:11] Diego, [09:13] Larissa |
| Volume alto de notificações para um mesmo cliente (ex.: 50 por minuto) | Média | Médio | Observar em produção. Rate limiting é questão em aberto | [09:38] Diego, [09:39] Larissa |
| Qualquer usuário autenticado gerencia webhooks de qualquer customer | Média | Médio | Aceito por enquanto. Endurecimento previsto para depois (Q4 do [RFC](RFC.md#5-questões-em-aberto)) | [09:37] Sofia |

## 11. Critérios de aceitação

- [ ] Um cliente com webhook cadastrado para `SHIPPED` recebe a notificação **em menos de 10 s** depois que um pedido dele muda para `SHIPPED`.
- [ ] O mesmo cliente **não** recebe notificação quando um pedido muda para um status fora do filtro.
- [ ] Uma URL `http://` é recusada no cadastro.
- [ ] A secret aparece só no cadastro e na rotação. Depois da rotação, a secret anterior continua aceita por 24 h.
- [ ] Toda notificação traz assinatura válida e um identificador de evento que se repete em reenvios.
- [ ] Com o endpoint do cliente fora do ar, a notificação é retentada automaticamente e, depois do limite, aparece na DLQ.
- [ ] Um ADMIN reprocessa a notificação da DLQ, e o registro mostra quem fez isso. Um usuário não-ADMIN recebe acesso negado.
- [ ] O histórico mostra as últimas 100 entregas, com sucesso ou falha, payload, resposta e tempo.
- [ ] Se o registro da notificação falhar, a mudança de status do pedido também não acontece.
- [ ] A revisão de segurança da Sofia está concluída antes do deploy.

Os critérios técnicos detalhados estão no [FDD §15](FDD.md#15-critérios-de-aceite-técnicos).

## 12. Estratégia de testes e validação

| Etapa | O que valida | Origem |
|---|---|---|
| Testes automatizados (unitários e de integração) | Filtro, atomicidade, retentativas, DLQ, permissão de ADMIN e assinatura. Detalhes no [FDD §14](FDD.md#14-plano-de-testes) | [09:46] Larissa ("testes ponta a ponta") |
| Revisão de segurança | Código de assinatura e geração de secret, **2 dias úteis** antes do deploy | [09:46] Sofia |
| Sessão de revisão do design com Bruno e Diego, antes de começar a codar | Aderência deste pacote ao que foi decidido | [09:50] Larissa |
| Validação com os clientes solicitantes *(proposta)* | Atlas, MaxDistribuição e Nova Cargo recebem as notificações no ambiente deles, seguindo a documentação do portal | [09:47] Marcos, [09:49] Marcos |
| Acompanhamento pós-lançamento | Volume por cliente (insumo para rate limiting) e falhas recorrentes (insumo para o email de alerta) | [09:37] Larissa, [09:39] Larissa |
