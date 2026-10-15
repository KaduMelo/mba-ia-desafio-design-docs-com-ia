# Tracker de Rastreabilidade

Liga cada item registrado em [PRD](PRD.md), [RFC](RFC.md), [FDD](FDD.md) e [ADRs](adrs/README.md) à sua origem: uma fala da reunião ([`TRANSCRICAO.md`](../TRANSCRICAO.md)) ou um arquivo do código.

**Como ler:**

- **Fonte** é `TRANSCRICAO` ou `CODIGO`.
- **Localização** é `[hh:mm] Nome` ou o caminho do arquivo.
- Quando o item cita várias falas, a localização aponta a **principal**. As demais estão no próprio documento.
- Itens marcados nos documentos como *(proposta)* não foram decididos na reunião. A localização deles aponta a fala ou o arquivo que **motivou** a proposta, e o resumo deixa claro que é proposta.

**Totais:** 284 linhas · 242 com fonte `TRANSCRICAO` (85%) · 42 com fonte `CODIGO` (15%).

| ID | Documento | Tipo | Conteúdo (resumo) | Fonte | Localização |
|---|---|---|---|---|---|
| PRD-CTX-01 | `docs/PRD.md` | Contexto | Pedido formal de 3 clientes B2B (Atlas Comercial, MaxDistribuição, Nova Cargo) por notificação de mudança de status | TRANSCRICAO | [09:00] Marcos |
| PRD-CTX-02 | `docs/PRD.md` | Problema | Clientes fazem polling em GET /orders; integração lenta e cara | TRANSCRICAO | [09:00] Marcos |
| PRD-CTX-03 | `docs/PRD.md` | Problema | Risco de churn: Atlas pode migrar para concorrente se não houver entrega até o fim do trimestre | TRANSCRICAO | [09:00] Marcos |
| PRD-CTX-04 | `docs/PRD.md` | Restrição | Prazo alvo: fim de novembro | TRANSCRICAO | [09:45] Marcos |
| PRD-PER-01 | `docs/PRD.md` | Público-alvo | Cliente B2B integrador: Equipe técnica do cliente (ex.: Atlas) que recebe os webhooks no sistema dela | TRANSCRICAO | [09:00] Marcos |
| PRD-PER-02 | `docs/PRD.md` | Público-alvo | Usuário que representa o cliente: Usuário da plataforma, autenticado por JWT, que cadastra e gerencia os webhooks pela API | TRANSCRICAO | [09:32] Marcos |
| PRD-PER-03 | `docs/PRD.md` | Público-alvo | Administrador da plataforma (ADMIN): Reprocessa notificações que falharam definitivamente | TRANSCRICAO | [09:36] Sofia |
| PRD-PER-04 | `docs/PRD.md` | Público-alvo | PM / portal do desenvolvedor: Publica a documentação de integração para os clientes | TRANSCRICAO | [09:26] Marcos |
| PRD-CEN-01 | `docs/PRD.md` | Cenário de uso | A Atlas quer saber só quando os pedidos dela viram SHIPPED ou DELIVERED. Ela cadastra um webhook com esse filtro e não receb… | TRANSCRICAO | [09:33] Marcos |
| PRD-CEN-02 | `docs/PRD.md` | Cenário de uso | Um pedido passa por PAID → PROCESSING → SHIPPED em sequência. O cliente recebe as três notificações, na ordem, em segundos | TRANSCRICAO | [09:12] Larissa |
| PRD-CEN-03 | `docs/PRD.md` | Cenário de uso | O endpoint do cliente fica 2 horas em manutenção planejada. Quando ele volta, as notificações pendentes chegam sozinhas | TRANSCRICAO | [09:16] Diego |
| PRD-CEN-04 | `docs/PRD.md` | Cenário de uso | O cliente vazou a secret num log. Ele pede uma nova pela API e tem 24 h para atualizar os sistemas sem perder notificações | TRANSCRICAO | [09:21] Sofia |
| PRD-CEN-05 | `docs/PRD.md` | Cenário de uso | O cliente quer conferir o que recebeu: consulta as últimas 100 entregas, com status, payload, resposta e tempo | TRANSCRICAO | [09:34] Marcos |
| PRD-CEN-06 | `docs/PRD.md` | Cenário de uso | Uma notificação esgotou as tentativas. Um ADMIN a reprocessa depois que o cliente corrige o problema, e fica registrado quem… | TRANSCRICAO | [09:18] Diego |
| PRD-CEN-07 | `docs/PRD.md` | Cenário de uso | O cliente tem dois cadastros (ex.: ERP e BI) e identifica qual deles originou cada chamada | TRANSCRICAO | [09:44] Sofia |
| PRD-OBJ-01 | `docs/PRD.md` | Objetivo / Métrica | Notificar em "tempo real" — meta: < 10 s. Por desenho, a descoberta leva ≤ 2 s | TRANSCRICAO | [09:02] Marcos |
| PRD-OBJ-02 | `docs/PRD.md` | Objetivo / Métrica | Não perder notificações — meta: 0 (garantia transacional) | TRANSCRICAO | [09:40] Bruno |
| PRD-OBJ-03 | `docs/PRD.md` | Objetivo / Métrica | Tolerar indisponibilidade do cliente — meta: ~15 h (1 envio + 5 retentativas) | TRANSCRICAO | [09:17] Diego |
| PRD-OBJ-04 | `docs/PRD.md` | Objetivo / Métrica | Reter os clientes solicitantes — meta: Até o fim de novembro, em 3 sprints | TRANSCRICAO | [09:45] Marcos |
| PRD-OBJ-05 | `docs/PRD.md` | Objetivo / Métrica — proposta | Reduzir o polling (proposta) — meta: Queda em relação à linha de base medida antes do lançamento. A meta numérica será defin… | TRANSCRICAO | [09:00] Marcos |
| PRD-ESC-01 | `docs/PRD.md` | Escopo (incluso) | Cadastro, edição, remoção e listagem de webhooks por customer via API autenticada | TRANSCRICAO | [09:33] Bruno |
| PRD-ESC-02 | `docs/PRD.md` | Escopo (incluso) | Filtro por webhook dos status de pedido de interesse | TRANSCRICAO | [09:33] Marcos |
| PRD-ESC-03 | `docs/PRD.md` | Escopo (incluso) | Notificação automática a cada mudança de status | TRANSCRICAO | [09:00] Marcos |
| PRD-ESC-04 | `docs/PRD.md` | Escopo (incluso) | Assinatura das notificações e secret exclusiva por webhook, com rotação | TRANSCRICAO | [09:21] Sofia |
| PRD-ESC-05 | `docs/PRD.md` | Escopo (incluso) | Retentativa automática e DLQ com reprocessamento por ADMIN | TRANSCRICAO | [09:18] Diego |
| PRD-ESC-06 | `docs/PRD.md` | Escopo (incluso) | Histórico de entregas consultável pelo cliente | TRANSCRICAO | [09:34] Marcos |
| PRD-OUT-01 | `docs/PRD.md` | Fora de escopo | Email de alerta quando o webhook do cliente falha repetidamente — Adiado para a próxima fase, depois de medir o impacto | TRANSCRICAO | [09:37] Marcos |
| PRD-OUT-02 | `docs/PRD.md` | Fora de escopo | Dashboard visual para o cliente ver os webhooks — Descartado nesta fase: projeto separado do time de frontend. Agora, só end… | TRANSCRICAO | [09:39] Marcos |
| PRD-OUT-03 | `docs/PRD.md` | Fora de escopo | Rate limiting de envio para o cliente — Não entra. Observar em produção e decidir depois | TRANSCRICAO | [09:38] Diego |
| PRD-OUT-04 | `docs/PRD.md` | Fora de escopo | Webhooks de entrada (cliente enviando para a plataforma) — Descartado: só saída | TRANSCRICAO | [09:02] Marcos |
| PRD-OUT-05 | `docs/PRD.md` | Fora de escopo | Arquivamento do histórico após ~30 dias — Fora desta feature | TRANSCRICAO | [09:08] Diego |
| PRD-OUT-06 | `docs/PRD.md` | Fora de escopo | Garantia de ordem global entre pedidos — Não é necessária: os clientes nunca pediram | TRANSCRICAO | [09:14] Marcos |
| PRD-OUT-07 | `docs/PRD.md` | Fora de escopo | Entrega exatamente uma vez (exactly-once) — Descartada pela complexidade. O cliente deduplica | TRANSCRICAO | [09:25] Diego |
| PRD-OUT-08 | `docs/PRD.md` | Fora de escopo | Notificação na criação do pedido — Não nesta fase: só mudanças de status | TRANSCRICAO | [09:40] Bruno |
| PRD-FR-01 | `docs/PRD.md` | Requisito Funcional | A plataforma notifica o customer, por webhook, toda vez que o status de um pedido dele muda | TRANSCRICAO | [09:00] Marcos |
| PRD-FR-02 | `docs/PRD.md` | Requisito Funcional | Um usuário autenticado cadastra um webhook informando o customer, a URL e os status de interesse | TRANSCRICAO | [09:31] Marcos |
| PRD-FR-03 | `docs/PRD.md` | Requisito Funcional | A secret do webhook é gerada pela plataforma e devolvida no cadastro | TRANSCRICAO | [09:31] Marcos |
| PRD-FR-04 | `docs/PRD.md` | Requisito Funcional | O usuário edita um webhook (URL, status de interesse, ativo/inativo) | TRANSCRICAO | [09:33] Bruno |
| PRD-FR-05 | `docs/PRD.md` | Requisito Funcional | O usuário remove um webhook | TRANSCRICAO | [09:33] Bruno |
| PRD-FR-06 | `docs/PRD.md` | Requisito Funcional | O usuário lista os webhooks de um customer | TRANSCRICAO | [09:33] Bruno |
| PRD-FR-07 | `docs/PRD.md` | Requisito Funcional | Cada webhook só recebe os status que escolheu ouvir | TRANSCRICAO | [09:33] Marcos |
| PRD-FR-08 | `docs/PRD.md` | Requisito Funcional | O cliente pode pedir uma nova secret pela API. A anterior continua válida por 24 h | TRANSCRICAO | [09:21] Sofia |
| PRD-FR-09 | `docs/PRD.md` | Requisito Funcional | O cliente consulta as últimas 100 entregas de um webhook, com sucesso ou falha, payload, resposta e tempo de resposta | TRANSCRICAO | [09:34] Marcos |
| PRD-FR-10 | `docs/PRD.md` | Requisito Funcional | Notificações que falham por motivo transitório (ex.: cliente fora do ar) são retentadas automaticamente com intervalos cresc… | TRANSCRICAO | [09:15] Diego |
| PRD-FR-11 | `docs/PRD.md` | Requisito Funcional | Um ADMIN reprocessa uma notificação da DLQ | TRANSCRICAO | [09:18] Diego |
| PRD-FR-12 | `docs/PRD.md` | Requisito Funcional | O reprocessamento registra quem o executou | TRANSCRICAO | [09:36] Sofia |
| PRD-FR-13 | `docs/PRD.md` | Requisito Funcional | Cada notificação traz um identificador único do evento, para o cliente descartar duplicatas | TRANSCRICAO | [09:25] Diego |
| PRD-FR-14 | `docs/PRD.md` | Requisito Funcional | Cada notificação traz a assinatura, o horário de envio e o identificador do webhook que a originou | TRANSCRICAO | [09:44] Diego |
| PRD-FR-15 | `docs/PRD.md` | Requisito Funcional | A notificação traz os dados essenciais do pedido e da mudança (número, status anterior e novo, cliente, valor total), sem os… | TRANSCRICAO | [09:43] Diego |
| PRD-NFR-01 | `docs/PRD.md` | Requisito Não Funcional | Latência abaixo de 10 s entre a mudança de status e a notificação | TRANSCRICAO | [09:02] Marcos |
| PRD-NFR-02 | `docs/PRD.md` | Requisito Não Funcional | A notificação nunca atrasa nem bloqueia a mudança de status de outros pedidos | TRANSCRICAO | [09:04] Bruno |
| PRD-NFR-03 | `docs/PRD.md` | Requisito Não Funcional | Mudança de status e registro da notificação são atômicos: um não existe sem o outro | TRANSCRICAO | [09:06] Diego |
| PRD-NFR-04 | `docs/PRD.md` | Requisito Não Funcional | Entrega pelo menos uma vez: duplicatas são possíveis e documentadas em destaque no portal | TRANSCRICAO | [09:24] Diego |
| PRD-NFR-05 | `docs/PRD.md` | Requisito Não Funcional | Toda notificação é assinada (HMAC-SHA256) com uma secret exclusiva do webhook | TRANSCRICAO | [09:20] Sofia |
| PRD-NFR-06 | `docs/PRD.md` | Requisito Não Funcional | Só são aceitas URLs https | TRANSCRICAO | [09:23] Sofia |
| PRD-NFR-07 | `docs/PRD.md` | Requisito Não Funcional | Notificações acima de 64 KB não são enviadas: geram erro, sem truncar | TRANSCRICAO | [09:23] Sofia |
| PRD-NFR-08 | `docs/PRD.md` | Requisito Não Funcional | O cliente tem até 10 s para responder. Acima disso, conta como falha | TRANSCRICAO | [09:42] Diego |
| PRD-NFR-09 | `docs/PRD.md` | Requisito Não Funcional | A ordem é garantida apenas por pedido, não globalmente | TRANSCRICAO | [09:13] Larissa |
| PRD-NFR-10 | `docs/PRD.md` | Requisito Não Funcional | Sem infraestrutura nova: usa o banco e a stack existentes | TRANSCRICAO | [09:07] Diego |
| PRD-NFR-11 | `docs/PRD.md` | Requisito Não Funcional | O reprocessamento manual é restrito a administradores | TRANSCRICAO | [09:36] Sofia |
| PRD-DEC-01 | `docs/PRD.md` | Decisão / Trade-off | Registrar o evento no banco, na mesma transação da mudança de status — Consistência total, em troca de uma pequena latência… | TRANSCRICAO | [09:06] Diego |
| PRD-DEC-02 | `docs/PRD.md` | Decisão / Trade-off | Processo de envio separado, verificando a cada 2 s — Simplicidade, em troca de até 2 s de espera e de um único processo de e… | TRANSCRICAO | [09:09] Diego |
| PRD-DEC-03 | `docs/PRD.md` | Decisão / Trade-off | 5 retentativas em ~15 h, depois DLQ com reprocesso manual — Teto previsível, em troca de intervenção humana nos casos extrem… | TRANSCRICAO | [09:17] Larissa |
| PRD-DEC-04 | `docs/PRD.md` | Decisão / Trade-off | Assinatura com secret por webhook e rotação com 24 h de carência — Isolamento de vazamentos, em troca de gerenciar uma secre… | TRANSCRICAO | [09:22] Sofia |
| PRD-DEC-05 | `docs/PRD.md` | Decisão / Trade-off | Entrega "pelo menos uma vez" — Simplicidade, em troca de o cliente precisar descartar duplicatas | TRANSCRICAO | [09:26] Larissa |
| PRD-DEC-06 | `docs/PRD.md` | Decisão / Trade-off | Seguir os padrões existentes do código — Velocidade e consistência, herdando as limitações atuais de permissão | TRANSCRICAO | [09:30] Larissa |
| PRD-DEC-07 | `docs/PRD.md` | Decisão / Trade-off | Conteúdo da notificação congelado no momento da mudança — Fidelidade ao momento do evento, em troca de dados possivelmente d… | TRANSCRICAO | [09:52] Larissa |
| PRD-DEP-01 | `docs/PRD.md` | Dependência | Revisão de segurança da Sofia, com 2 dias úteis antes do deploy (HMAC e geração de secret) (Interna, bloqueante para o deplo… | TRANSCRICAO | [09:46] Sofia |
| PRD-DEP-02 | `docs/PRD.md` | Dependência | Documentação no portal do desenvolvedor: como integrar, validar a assinatura e deduplicar (Interna (PM)) | TRANSCRICAO | [09:26] Marcos |
| PRD-DEP-03 | `docs/PRD.md` | Dependência | Confirmação de prazo com os clientes (Externa (PM)) | TRANSCRICAO | [09:47] Marcos |
| PRD-DEP-04 | `docs/PRD.md` | Dependência | Clientes implementam a validação de assinatura e a deduplicação por identificador de evento (Externa) | TRANSCRICAO | [09:25] Sofia |
| PRD-DEP-05 | `docs/PRD.md` | Dependência | Banco MySQL e stack atuais (Prisma, autenticação JWT, papéis ADMIN/OPERATOR) (Técnica, existente) | TRANSCRICAO | [09:11] Diego |
| PRD-DEP-06 | `docs/PRD.md` | Dependência | Deploy de um novo processo de envio, separado da API (Operacional) | TRANSCRICAO | [09:11] Diego |
| PRD-RISK-01 | `docs/PRD.md` | Risco | Atraso na entrega e perda da Atlas para um concorrente — P: Média, I: Alto | TRANSCRICAO | [09:00] Marcos |
| PRD-RISK-02 | `docs/PRD.md` | Risco | Cliente processa notificações duplicadas porque não deduplica — P: Média, I: Médio | TRANSCRICAO | [09:25] Sofia |
| PRD-RISK-03 | `docs/PRD.md` | Risco | Vazamento da secret do lado do cliente (ex.: em log da aplicação dele) — P: Média (já aconteceu), I: Alto | TRANSCRICAO | [09:22] Diego |
| PRD-RISK-04 | `docs/PRD.md` | Risco — proposta | Processo de envio parado → notificações atrasam — P: Média, I: Alto | TRANSCRICAO | [09:11] Diego |
| PRD-RISK-05 | `docs/PRD.md` | Risco | Volume alto de notificações para um mesmo cliente (ex.: 50 por minuto) — P: Média, I: Médio | TRANSCRICAO | [09:38] Diego |
| PRD-RISK-06 | `docs/PRD.md` | Risco | Qualquer usuário autenticado gerencia webhooks de qualquer customer — P: Média, I: Médio | TRANSCRICAO | [09:37] Sofia |
| PRD-AC-01 | `docs/PRD.md` | Critério de aceitação | Entrega: notificação em < 10 s só para status do filtro, com assinatura válida e identificador de evento estável em reenvios | TRANSCRICAO | [09:02] Marcos |
| PRD-AC-02 | `docs/PRD.md` | Critério de aceitação | Cadastro e segurança: URL http:// recusada; secret só no cadastro e na rotação, anterior aceita por 24 h; revisão de seguran… | TRANSCRICAO | [09:21] Sofia |
| PRD-AC-03 | `docs/PRD.md` | Critério de aceitação | Falhas e operação: retentativa automática e DLQ; replay só por ADMIN com autoria registrada; histórico das últimas 100 entre… | TRANSCRICAO | [09:17] Larissa |
| PRD-TEST-01 | `docs/PRD.md` | Estratégia de testes | Testes automatizados (unitários e de integração): Filtro, atomicidade, retentativas, DLQ, permissão de ADMIN e assinatura. D… | TRANSCRICAO | [09:46] Larissa |
| PRD-TEST-02 | `docs/PRD.md` | Estratégia de testes | Revisão de segurança: Código de assinatura e geração de secret, 2 dias úteis antes do deploy | TRANSCRICAO | [09:46] Sofia |
| PRD-TEST-03 | `docs/PRD.md` | Estratégia de testes | Sessão de revisão do design com Bruno e Diego, antes de começar a codar: Aderência deste pacote ao que foi decidido | TRANSCRICAO | [09:50] Larissa |
| PRD-TEST-04 | `docs/PRD.md` | Estratégia de testes — proposta | Validação com os clientes solicitantes (proposta): Atlas, MaxDistribuição e Nova Cargo recebem as notificações no ambiente d… | TRANSCRICAO | [09:47] Marcos |
| PRD-TEST-05 | `docs/PRD.md` | Estratégia de testes | Acompanhamento pós-lançamento: Volume por cliente (insumo para rate limiting) e falhas recorrentes (insumo para o email de a… | TRANSCRICAO | [09:37] Larissa |
| RFC-META-01 | `docs/RFC.md` | Metadado | Autora Larissa (Tech Lead) abre o doc de design; revisores Marcos, Bruno, Diego, Sofia | TRANSCRICAO | [09:50] Larissa |
| RFC-CTX-01 | `docs/RFC.md` | Contexto | Fluxo apenas de saída (outbound): clientes recebem, não enviam | TRANSCRICAO | [09:02] Marcos |
| RFC-CTX-02 | `docs/RFC.md` | Restrição | Mudança de status ocorre em changeStatus, numa transação já pesada (orders, history, estoque) | CODIGO | `src/modules/orders/order.service.ts` |
| RFC-CTX-03 | `docs/RFC.md` | Restrição | Atomicidade: status alterado sem evento é inaceitável | TRANSCRICAO | [09:40] Bruno |
| RFC-CTX-04 | `docs/RFC.md` | Restrição | Isolamento: cliente lento não pode travar mudança de status de outros pedidos | TRANSCRICAO | [09:04] Bruno |
| RFC-PROP-01 | `docs/RFC.md` | Proposta técnica | Registro do evento na outbox via publishWebhookEvent(tx, …) na transação | TRANSCRICAO | [09:41] Bruno |
| RFC-PROP-02 | `docs/RFC.md` | Proposta técnica | Snapshot enxuto filtrado por status na inserção | TRANSCRICAO | [09:52] Larissa |
| RFC-PROP-03 | `docs/RFC.md` | Proposta técnica | Worker separado, PrismaClient próprio, polling 2 s, single-worker | TRANSCRICAO | [09:11] Diego |
| RFC-PROP-04 | `docs/RFC.md` | Proposta técnica | Timeout 10 s, 5 retentativas 1m/5m/30m/2h/12h, DLQ com replay ADMIN | TRANSCRICAO | [09:17] Larissa |
| RFC-PROP-05 | `docs/RFC.md` | Proposta técnica | HMAC-SHA256 do corpo, secret por endpoint, rotação 24 h, só https | TRANSCRICAO | [09:22] Sofia |
| RFC-PROP-06 | `docs/RFC.md` | Proposta técnica | At-least-once com X-Event-Id | TRANSCRICAO | [09:26] Larissa |
| RFC-PROP-07 | `docs/RFC.md` | Proposta técnica | CRUD de webhooks e histórico de entregas via API com JWT | TRANSCRICAO | [09:33] Bruno |
| RFC-PROP-08 | `docs/RFC.md` | Proposta técnica | Módulo src/modules/webhooks reusando AppError, error middleware, requireRole, Zod, Pino; códigos WEBHOOK_ | TRANSCRICAO | [09:30] Larissa |
| RFC-GAR-01 | `docs/RFC.md` | Garantia / Limitação | Consistência status ↔ evento: Forte (mesma transação) | TRANSCRICAO | [09:06] Diego |
| RFC-GAR-02 | `docs/RFC.md` | Garantia / Limitação | Entrega: At-least-once (podem ocorrer duplicatas) | TRANSCRICAO | [09:24] Diego |
| RFC-GAR-03 | `docs/RFC.md` | Garantia / Limitação | Latência de descoberta: ≤ 2 s após o commit, sem contar o tempo de resposta do cliente | TRANSCRICAO | [09:09] Diego |
| RFC-GAR-04 | `docs/RFC.md` | Garantia / Limitação | Ordem: Apenas por pedido, enquanto houver um único worker e na primeira tentativa: um evento em retry pode ser ultrapassado… | TRANSCRICAO | [09:13] Larissa |
| RFC-GAR-05 | `docs/RFC.md` | Garantia / Limitação | Janela de retentativa: ~15 h; depois disso, DLQ | TRANSCRICAO | [09:17] Diego |
| RFC-ALT-01 | `docs/RFC.md` | Alternativa descartada (trade-off) | Disparo HTTP síncrono dentro de changeStatus — A transação é pesada: um cliente lento travaria mudanças de status de outros… | TRANSCRICAO | [09:04] Bruno |
| RFC-ALT-02 | `docs/RFC.md` | Alternativa descartada (trade-off) | Redis Streams / Redis Cluster como fila — Daria mais vazão e reatividade, mas exigiria subir e operar infraestrutura nova: o… | TRANSCRICAO | [09:07] Larissa |
| RFC-ALT-03 | `docs/RFC.md` | Alternativa descartada (trade-off) | Trigger do banco para acordar o worker — O MySQL não tem LISTEN/NOTIFY. O trigger só executa SQL e não notifica processo ext… | TRANSCRICAO | [09:09] Bruno |
| RFC-ALT-04 | `docs/RFC.md` | Alternativa descartada (trade-off) | Worker dentro do processo da API — Mais simples de implantar, mas um restart da API derruba o worker junto | TRANSCRICAO | [09:11] Diego |
| RFC-ALT-05 | `docs/RFC.md` | Alternativa descartada (trade-off) | Retry indefinido ou apenas 3 tentativas — Retry indefinido deixa eventos pendurados para sempre. Com 3 tentativas, um client… | TRANSCRICAO | [09:15] Diego |
| RFC-ALT-06 | `docs/RFC.md` | Alternativa descartada (trade-off) | Exactly-once — Exigiria coordenação entre os dois lados e muito mais complexidade. At-least-once com event_id é o padrão de… | TRANSCRICAO | [09:25] Diego |
| RFC-ALT-07 | `docs/RFC.md` | Alternativa descartada (trade-off) | Secret global da plataforma — Mais simples de gerenciar, mas "se vaza uma, vaza tudo" | TRANSCRICAO | [09:21] Sofia |
| RFC-OPEN-01 | `docs/RFC.md` | Questão em aberto | Rate limiting de saída: o que fazer quando um cliente tem dezenas de pedidos mudando de status no mesmo minuto? | TRANSCRICAO | [09:38] Diego |
| RFC-OPEN-02 | `docs/RFC.md` | Questão em aberto | Escalar além de um worker sem perder a ordem por pedido | TRANSCRICAO | [09:13] Diego |
| RFC-OPEN-03 | `docs/RFC.md` | Questão em aberto | Avisar o cliente por email quando o webhook dele falha repetidamente | TRANSCRICAO | [09:37] Marcos |
| RFC-OPEN-04 | `docs/RFC.md` | Questão em aberto | Endurecer as permissões do CRUD de webhooks (hoje vale qualquer usuário autenticado) | TRANSCRICAO | [09:37] Sofia |
| RFC-OPEN-05 | `docs/RFC.md` | Questão em aberto | Arquivamento das linhas já entregues (~30 dias) | TRANSCRICAO | [09:08] Diego |
| RFC-OPEN-06 | `docs/RFC.md` | Questão em aberto | Listagem da DLQ: o replay é por id, mas não foi definido como o ADMIN descobre os ids | TRANSCRICAO | [09:18] Diego |
| RFC-OPEN-07 | `docs/RFC.md` | Questão em aberto | Incluir o X-Timestamp na assinatura? Com o HMAC só sobre o corpo, o header não impede replay de uma requisição capturada | TRANSCRICAO | [09:22] Sofia |
| RFC-RES-01 | `docs/RFC.md` | Decisão (ambiguidade resolvida) | "5 tentativas" com 5 intervalos listados → Envio inicial + 5 retentativas. É a única leitura compatível com os ~15 h citados… | TRANSCRICAO | [09:17] Diego |
| RFC-RES-02 | `docs/RFC.md` | Decisão (ambiguidade resolvida) | Granularidade da outbox → Uma linha por par evento × webhook, com event_id, retry e DLQ próprios. → ADR-005 | TRANSCRICAO | [09:34] Bruno |
| RFC-RES-03 | `docs/RFC.md` | Decisão (ambiguidade resolvida) | Criação do pedido (null → PENDING) gera evento? → Não nesta fase. Só changeStatus publica. → ADR-007 | TRANSCRICAO | [09:40] Bruno |
| RFC-RISK-01 | `docs/RFC.md` | Risco — proposta | Worker parado → entregas atrasam (single-worker é ponto único de falha) — mitigação: Eventos persistem na outbox e nada se p… | TRANSCRICAO | [09:11] Diego |
| RFC-RISK-02 | `docs/RFC.md` | Risco | Cliente não deduplica → processa eventos em dobro — mitigação: Documentação em destaque no portal. X-Event-Id estável entre… | TRANSCRICAO | [09:25] Sofia |
| RFC-RISK-03 | `docs/RFC.md` | Risco | Vazamento de secret de cliente (já aconteceu) — mitigação: Secret por endpoint, rotação com 24 h de carência, revisão de seg… | TRANSCRICAO | [09:22] Diego |
| RFC-RISK-04 | `docs/RFC.md` | Risco | Inserção na outbox falha → mudança de status falha — mitigação: Comportamento desejado: rollback garante que não exista stat… | TRANSCRICAO | [09:40] Bruno |
| RFC-RISK-05 | `docs/RFC.md` | Risco | Prazo: a Atlas quer a funcionalidade até o fim de novembro — mitigação: Escopo enxuto, com email, dashboard e rate limiting… | TRANSCRICAO | [09:45] Marcos |
| RFC-CRON-01 | `docs/RFC.md` | Restrição (prazo) | Cronograma de 3 sprints com 2 dias úteis de revisão de segurança no fim | TRANSCRICAO | [09:46] Larissa |
| ADR-001 | `docs/adrs/ADR-001-outbox-no-mysql.md` | Decisão | Outbox no MySQL na mesma transação do changeStatus; rollback se a inserção falhar | TRANSCRICAO | [09:08] Larissa |
| ADR-001-ALT-01 | `docs/adrs/ADR-001-outbox-no-mysql.md` | Alternativa descartada | Chamada HTTP síncrona dentro do changeStatus — A transação já é pesada. Um cliente lento travaria a mudança de status de out… | TRANSCRICAO | [09:04] Bruno |
| ADR-001-ALT-02 | `docs/adrs/ADR-001-outbox-no-mysql.md` | Alternativa descartada | Redis Streams / Redis Cluster como fila — Exigiria subir e operar infraestrutura nova. Para um time pequeno, é overengineeri… | TRANSCRICAO | [09:07] Larissa |
| ADR-001-ALT-03 | `docs/adrs/ADR-001-outbox-no-mysql.md` | Alternativa descartada | Injetar um repository de webhooks no OrderService — Acoplamento desnecessário. Uma função que recebe o tx resolve | TRANSCRICAO | [09:41] Diego |
| ADR-002 | `docs/adrs/ADR-002-worker-separado-em-polling.md` | Decisão | Worker em processo separado (src/worker.ts), polling de 2 s, PrismaClient próprio, single-worker | TRANSCRICAO | [09:10] Larissa |
| ADR-002-ALT-01 | `docs/adrs/ADR-002-worker-separado-em-polling.md` | Alternativa descartada | Trigger do banco para tornar o worker reativo — O trigger do MySQL só executa SQL e não notifica processo externo. Avisar o… | TRANSCRICAO | [09:09] Bruno |
| ADR-002-ALT-02 | `docs/adrs/ADR-002-worker-separado-em-polling.md` | Alternativa descartada | Worker dentro do processo da API — Se a API reinicia, o worker morre junto | TRANSCRICAO | [09:11] Diego |
| ADR-002-ALT-03 | `docs/adrs/ADR-002-worker-separado-em-polling.md` | Alternativa descartada | Reusar o PrismaClient da API — Não é possível: o PrismaClient é por processo | TRANSCRICAO | [09:29] Diego |
| ADR-002-ALT-04 | `docs/adrs/ADR-002-worker-separado-em-polling.md` | Alternativa descartada | Múltiplos workers em paralelo — A garantia de ordem se perde. Particionar por order_id ou usar lock pessimista foi deixado p… | TRANSCRICAO | [09:13] Diego |
| ADR-003 | `docs/adrs/ADR-003-retry-backoff-e-dlq.md` | Decisão | Backoff 1m/5m/30m/2h/12h (1 envio + 5 retries) e DLQ em webhook_dead_letter com replay ADMIN | TRANSCRICAO | [09:17] Larissa |
| ADR-003-ALT-01 | `docs/adrs/ADR-003-retry-backoff-e-dlq.md` | Alternativa descartada | Retry indefinido com backoff — O evento fica pendurado para sempre se o cliente sumiu | TRANSCRICAO | [09:15] Diego |
| ADR-003-ALT-02 | `docs/adrs/ADR-003-retry-backoff-e-dlq.md` | Alternativa descartada | 3 tentativas (mais agressivo) — Pouco: três tentativas em ~30 min matariam o evento durante uma manutenção comum de 2 h | TRANSCRICAO | [09:16] Bruno |
| ADR-003-ALT-03 | `docs/adrs/ADR-003-retry-backoff-e-dlq.md` | Alternativa descartada | DLQ como status "failed" na própria outbox — Uma tabela separada mantém a leitura da outbox limpa e serve de evidência para… | TRANSCRICAO | [09:17] Larissa |
| ADR-004 | `docs/adrs/ADR-004-hmac-sha256-com-secret-por-endpoint.md` | Decisão | HMAC-SHA256 sobre o corpo, secret por endpoint gerada pela plataforma, rotação com grace de 24 h | TRANSCRICAO | [09:22] Sofia |
| ADR-004-ALT-01 | `docs/adrs/ADR-004-hmac-sha256-com-secret-por-endpoint.md` | Alternativa descartada | Secret global da plataforma (uma para todos os clientes) — "Se vaza uma, vaza tudo" | TRANSCRICAO | [09:21] Sofia |
| ADR-004-ALT-02 | `docs/adrs/ADR-004-hmac-sha256-com-secret-por-endpoint.md` | Alternativa plausível (não discutida) | Rotação sem período de convivência (troca imediata) — Plausível, mas não atende à necessidade de dar tempo ao cliente para m… | TRANSCRICAO | [09:21] Sofia |
| ADR-005 | `docs/adrs/ADR-005-entrega-at-least-once-com-x-event-id.md` | Decisão | Entrega at-least-once; X-Event-Id (UUID) para deduplicação; 1 linha de outbox por evento × webhook | TRANSCRICAO | [09:26] Larissa |
| ADR-005-ALT-01 | `docs/adrs/ADR-005-entrega-at-least-once-com-x-event-id.md` | Alternativa descartada | Exactly-once — Exigiria coordenação entre os dois lados e "fica muito mais complexo". At-least-once com event_id resolve a g… | TRANSCRICAO | [09:25] Diego |
| ADR-005-ALT-02 | `docs/adrs/ADR-005-entrega-at-least-once-com-x-event-id.md` | Alternativa plausível (não discutida) | At-most-once (sem retry) — Plausível, mas incompatível com a política de retry aceita (ADR-003): perder um evento é pior par… | TRANSCRICAO | [09:24] Diego |
| ADR-006 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Decisão | Reuso máximo dos padrões: módulo, AppError, códigos WEBHOOK_, error middleware, requireRole, Zod, Pino | TRANSCRICAO | [09:30] Larissa |
| ADR-006-ALT-01 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Alternativa plausível (não discutida) | Padrões próprios para o módulo (outro formato de erro, outro logger) — Plausível, mas não traria ganho. "Não vamos botar nad… | TRANSCRICAO | [09:29] Bruno |
| ADR-006-ALT-02 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Alternativa descartada | Restringir o CRUD de configuração a ADMIN — Mexer em configuração de webhook pode ser feito por qualquer role autenticada po… | TRANSCRICAO | [09:36] Marcos |
| ADR-006-COD-01 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Módulo por domínio (controller, service, repository, routes, schemas) → Nova pasta src/modules/webhooks/ (a criar) com a mes… | CODIGO | `src/modules/orders/` |
| ADR-006-COD-02 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Classe base de erro → Todos os erros do módulo derivam dela | CODIGO | `src/shared/errors/app-error.ts` |
| ADR-006-COD-03 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Erros HTTP com código customizável e erros de domínio → Novos erros seguem o mesmo modelo, com prefixo WEBHOOK_, ex.: WEBHOO… | CODIGO | `src/shared/errors/http-errors.ts` |
| ADR-006-COD-04 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Exportação central dos erros → Novos erros exportados pelo mesmo barrel | CODIGO | `src/shared/errors/index.ts` |
| ADR-006-COD-05 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Middleware de erro centralizado → Trata os erros do módulo sem nenhuma alteração | CODIGO | `src/middlewares/error.middleware.ts` |
| ADR-006-COD-06 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Autenticação e autorização → CRUD com authenticate. Replay da DLQ com requireRole('ADMIN'), como já é feito em src/modules/u… | CODIGO | `src/middlewares/auth.middleware.ts` |
| ADR-006-COD-07 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Validação Zod → Schemas do módulo, incluindo a regra https da URL | CODIGO | `src/middlewares/validate.middleware.ts` |
| ADR-006-COD-08 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Logger → API e worker usam o mesmo logger, sem lib nova | CODIGO | `src/shared/logger/index.ts` |
| ADR-006-COD-09 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Registro de rotas → Rotas e controller do módulo registrados da mesma forma | CODIGO | `src/routes/index.ts` |
| ADR-006-COD-10 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | IDs UUID → Novas tabelas com UUID | CODIGO | `prisma/schema.prisma` |
| ADR-006-COD-11 | `docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md` | Padrão de código reutilizado | Bootstrap de processo → Modelo para o novo src/worker.ts (a criar) | CODIGO | `src/server.ts` |
| ADR-007 | `docs/adrs/ADR-007-payload-snapshot-e-filtro-na-insercao.md` | Decisão | Payload snapshot renderizado na inserção; filtro de status na inserção; payload enxuto sem items | TRANSCRICAO | [09:52] Bruno |
| ADR-007-ALT-01 | `docs/adrs/ADR-007-payload-snapshot-e-filtro-na-insercao.md` | Alternativa descartada | Guardar só o order_id e renderizar no envio — Se o pedido mudar depois, o evento deixaria de refletir o estado do momento da… | TRANSCRICAO | [09:52] Larissa |
| ADR-007-ALT-02 | `docs/adrs/ADR-007-payload-snapshot-e-filtro-na-insercao.md` | Alternativa descartada | Filtrar no envio — Inseriria linhas que nunca seriam enviadas. Filtrar na inserção "economiza linha na tabela" | TRANSCRICAO | [09:34] Bruno |
| ADR-007-ALT-03 | `docs/adrs/ADR-007-payload-snapshot-e-filtro-na-insercao.md` | Alternativa descartada | Payload completo, com itens — Infla o payload sem necessidade | TRANSCRICAO | [09:43] Diego |
| FDD-OT-1 | `docs/FDD.md` | Objetivo técnico | Notificar o cliente em menos de 10 s após o commit da mudança de status — Polling ≤ 2 s + envio com timeout de 10 s | TRANSCRICAO | [09:02] Marcos |
| FDD-OT-2 | `docs/FDD.md` | Objetivo técnico | Evento gravado na mesma transação da mudança de status — Rollback desfaz os dois; falha na outbox desfaz a mudança | TRANSCRICAO | [09:06] Diego |
| FDD-OT-3 | `docs/FDD.md` | Objetivo técnico | Nenhum evento perdido por indisponibilidade do cliente — 1 envio + 5 retentativas (~15 h) e depois DLQ | TRANSCRICAO | [09:17] Larissa |
| FDD-OT-4 | `docs/FDD.md` | Objetivo técnico | Autenticidade e integridade verificáveis pelo cliente — HMAC-SHA256 com secret por endpoint | TRANSCRICAO | [09:22] Sofia |
| FDD-OT-5 | `docs/FDD.md` | Objetivo técnico | Zero infraestrutura nova e zero dependência nova — Mesmo MySQL, Prisma, Pino, Zod e uuid já instalados | TRANSCRICAO | [09:07] Diego |
| FDD-OUT-01 | `docs/FDD.md` | Exclusão | Múltiplos workers em paralelo | TRANSCRICAO | [09:13] Diego |
| FDD-OUT-02 | `docs/FDD.md` | Exclusão | Evento na criação do pedido (create, order.service.ts:95-113) | TRANSCRICAO | [09:40] Bruno |
| FDD-OUT-03 | `docs/FDD.md` | Exclusão | Endpoint para listar a DLQ (a reunião só definiu o replay por id; questão em aberto Q6 do RFC) | TRANSCRICAO | [09:18] Diego |
| FDD-DADOS-01 | `docs/FDD.md` | Modelo de dados | Model WebhookEndpoint: url, events (Json), secret, previousSecret + expiração, active, deletedAt | TRANSCRICAO | [09:21] Bruno |
| FDD-DADOS-02 | `docs/FDD.md` | Modelo de dados | Model WebhookOutbox: eventId único, payload snapshot, status, attempts, nextAttemptAt; índices status/createdAt | TRANSCRICAO | [09:08] Diego |
| FDD-DADOS-03 | `docs/FDD.md` | Modelo de dados | Model WebhookDelivery: tentativa, sucesso, status/corpo da resposta, durationMs | TRANSCRICAO | [09:34] Marcos |
| FDD-DADOS-04 | `docs/FDD.md` | Modelo de dados | Model WebhookDeadLetter: payload, reason, attempts, failedAt, replayedAt/By | TRANSCRICAO | [09:18] Diego |
| FDD-DADOS-05 | `docs/FDD.md` | Modelo de dados | IDs UUID Char(36) no padrão do schema existente | CODIGO | `prisma/schema.prisma` |
| FDD-DADOS-06 | `docs/FDD.md` | Modelo de dados — proposta | Status FAILED como estado terminal na outbox; evidência na DLQ (proposta, resolve AMB-02) | TRANSCRICAO | [09:08] Diego |
| FDD-DADOS-07 | `docs/FDD.md` | Modelo de dados — proposta | DELETE lógico com deletedAt para preservar histórico e DLQ (proposta) | TRANSCRICAO | [09:18] Diego |
| FDD-FLUXO-01 | `docs/FDD.md` | Fluxo | Inserção na outbox após orderStatusHistory.create, dentro do $transaction de changeStatus | CODIGO | `src/modules/orders/order.service.ts` |
| FDD-FLUXO-02 | `docs/FDD.md` | Fluxo | Filtro na inserção: só endpoints ativos do customer que ouvem o to_status | TRANSCRICAO | [09:34] Bruno |
| FDD-FLUXO-03 | `docs/FDD.md` | Fluxo — proposta | Worker: ciclo a cada 2 s, lote de 10 (proposta), envio sequencial por createdAt | TRANSCRICAO | [09:09] Diego |
| FDD-FLUXO-04 | `docs/FDD.md` | Fluxo — proposta | Recuperação de crash: PROCESSING volta a PENDING na inicialização (proposta) | TRANSCRICAO | [09:24] Diego |
| FDD-FLUXO-05 | `docs/FDD.md` | Fluxo | Retry: tabela de backoff por attempts; 6º envio falho → DLQ | TRANSCRICAO | [09:17] Diego |
| FDD-FLUXO-06 | `docs/FDD.md` | Fluxo — proposta | Classificação de retry: timeout, rede, 5xx, 408, 429 retentam; demais 3xx/4xx → DLQ (proposta, AMB-09) | TRANSCRICAO | [09:42] Diego |
| FDD-FLUXO-07 | `docs/FDD.md` | Fluxo — proposta | Replay: mesma linha da outbox volta a PENDING com o mesmo eventId | TRANSCRICAO | [09:18] Diego |
| FDD-FLUXO-08 | `docs/FDD.md` | Fluxo — proposta | Rotação: secret anterior válida 24 h; duas assinaturas em X-Signature (proposta) | TRANSCRICAO | [09:21] Sofia |
| FDD-CONTRATO-01 | `docs/FDD.md` | Contrato público | POST /api/v1/webhooks — cadastra webhook; customerId no body; secret devolvida só aqui; 201 | TRANSCRICAO | [09:31] Marcos |
| FDD-CONTRATO-02 | `docs/FDD.md` | Contrato público — proposta | GET /api/v1/customers/:customerId/webhooks — lista webhooks do customer (customerId no path); 200 | TRANSCRICAO | [09:33] Bruno |
| FDD-CONTRATO-03 | `docs/FDD.md` | Contrato público | PATCH /api/v1/webhooks/:id — edita url, events, active; 200 | TRANSCRICAO | [09:33] Bruno |
| FDD-CONTRATO-04 | `docs/FDD.md` | Contrato público — proposta | DELETE /api/v1/webhooks/:id — remoção lógica; 204 | TRANSCRICAO | [09:33] Bruno |
| FDD-CONTRATO-05 | `docs/FDD.md` | Contrato público — proposta | POST /api/v1/webhooks/:id/rotate-secret — nova secret, anterior válida 24 h; 200 | TRANSCRICAO | [09:21] Sofia |
| FDD-CONTRATO-06 | `docs/FDD.md` | Contrato público | GET /api/v1/webhooks/:id/deliveries — últimas 100 tentativas com payload, resposta e tempo; 200 | TRANSCRICAO | [09:34] Marcos |
| FDD-CONTRATO-07 | `docs/FDD.md` | Contrato público | POST /api/v1/admin/webhooks/dead-letter/:id/replay — ADMIN, auditado; 202 | TRANSCRICAO | [09:35] Diego |
| FDD-CONTRATO-08 | `docs/FDD.md` | Contrato público | Contrato de saída: payload event_id, event_type, timestamp, order_id, order_number, from/to_status, customer_id, total_cents | TRANSCRICAO | [09:43] Diego |
| FDD-CONTRATO-09 | `docs/FDD.md` | Contrato público | Headers de saída: Content-Type, X-Event-Id, X-Webhook-Id, X-Timestamp, X-Signature | TRANSCRICAO | [09:44] Diego |
| FDD-CONTRATO-10 | `docs/FDD.md` | Contrato público | customerId nunca vem do JWT | TRANSCRICAO | [09:32] Larissa |
| FDD-CONTRATO-11 | `docs/FDD.md` | Contrato público | Endpoints sob /api/v1 com authenticate | CODIGO | `src/app.ts` |
| FDD-ERR-01 | `docs/FDD.md` | Erro (matriz) | WEBHOOK_NOT_FOUND: Webhook inexistente ou removido | TRANSCRICAO | [09:28] Bruno |
| FDD-ERR-02 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_CUSTOMER_NOT_FOUND: customerId inexistente na criação ou listagem | TRANSCRICAO | [09:32] Larissa |
| FDD-ERR-03 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_DEAD_LETTER_NOT_FOUND: Id de DLQ inexistente no replay | TRANSCRICAO | [09:18] Diego |
| FDD-ERR-04 | `docs/FDD.md` | Erro (matriz) | WEBHOOK_INVALID_URL: URL malformada ou não-https. A regra fica no schema Zod, e validate.middleware.ts:31 converte para VALI… | TRANSCRICAO | [09:23] Sofia |
| FDD-ERR-05 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_INVALID_EVENT_FILTER: events vazio ou com valor fora de OrderStatus (mesmo mecanismo acima) | TRANSCRICAO | [09:33] Marcos |
| FDD-ERR-06 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_INACTIVE: Operação sobre webhook removido ou desativado | TRANSCRICAO | [09:21] Bruno |
| FDD-ERR-07 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_DEAD_LETTER_ALREADY_REPLAYED: Replay repetido da mesma entrada | TRANSCRICAO | [09:18] Diego |
| FDD-ERR-08 | `docs/FDD.md` | Erro (matriz) | WEBHOOK_DELIVERY_TIMEOUT: Sem resposta em 10 s | TRANSCRICAO | [09:42] Diego |
| FDD-ERR-09 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_DELIVERY_FAILED: Resposta 5xx, 408 ou 429 | TRANSCRICAO | [09:15] Diego |
| FDD-ERR-10 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_DELIVERY_REJECTED: Resposta 3xx ou 4xx (exceto 408 e 429): o cliente recusou a requisição | TRANSCRICAO | [09:15] Diego |
| FDD-ERR-11 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_NETWORK_ERROR: DNS, conexão recusada, TLS | TRANSCRICAO | [09:14] Larissa |
| FDD-ERR-12 | `docs/FDD.md` | Erro (matriz) | WEBHOOK_MAX_ATTEMPTS_EXCEEDED: Falha no 6º envio | TRANSCRICAO | [09:17] Larissa |
| FDD-ERR-13 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_PAYLOAD_TOO_LARGE: Corpo serializado acima de 64 KB. A checagem fica no worker, não na transação, para que um payloa… | TRANSCRICAO | [09:23] Sofia |
| FDD-ERR-14 | `docs/FDD.md` | Erro (matriz) — proposta | WEBHOOK_SECRET_REQUIRED: Endpoint sem secret válida no envio, o que indica estado inconsistente: não se envia sem assinar (p… | TRANSCRICAO | [09:28] Bruno |
| FDD-ERR-BASE | `docs/FDD.md` | Restrição de código | NotFoundError fixa o código NOT_FOUND → 404 do módulo estendem AppError | CODIGO | `src/shared/errors/http-errors.ts` |
| FDD-ERR-ZOD | `docs/FDD.md` | Restrição de código | validate.middleware converte ZodError em VALIDATION_ERROR → WEBHOOK_INVALID_URL vai em details | CODIGO | `src/middlewares/validate.middleware.ts` |
| FDD-RES-01 | `docs/FDD.md` | Resiliência | Timeout HTTP: 10 s, com fetch nativo + AbortSignal.timeout(10_000) (Node ≥ 20, package.json:7-9) | TRANSCRICAO | [09:42] Diego |
| FDD-RES-02 | `docs/FDD.md` | Resiliência | Retries: 5, depois do envio inicial | TRANSCRICAO | [09:17] Larissa |
| FDD-RES-03 | `docs/FDD.md` | Resiliência | Backoff: 1m, 5m, 30m, 2h, 12h (fixo, não calculado) | TRANSCRICAO | [09:17] Diego |
| FDD-RES-04 | `docs/FDD.md` | Resiliência | Fallback: DLQ + replay manual por ADMIN. Não há email nesta fase | TRANSCRICAO | [09:18] Diego |
| FDD-RES-05 | `docs/FDD.md` | Resiliência | Limite de payload: 64 KB → DLQ, sem truncar | TRANSCRICAO | [09:23] Sofia |
| FDD-RES-06 | `docs/FDD.md` | Resiliência | Isolamento da API: A API nunca faz HTTP de saída. Só o worker faz | TRANSCRICAO | [09:06] Diego |
| FDD-RES-07 | `docs/FDD.md` | Resiliência — proposta | Crash do worker: Linhas PROCESSING voltam a PENDING na inicialização (proposta) | TRANSCRICAO | [09:24] Diego |
| FDD-RES-08 | `docs/FDD.md` | Resiliência — proposta | Shutdown gracioso: SIGINT/SIGTERM: termina o evento em curso, para o loop e chama prisma.$disconnect (modelo de src/server.t… | TRANSCRICAO | [09:11] Larissa |
| FDD-RES-09 | `docs/FDD.md` | Resiliência | Isolamento entre endpoints: Uma linha por evento × webhook: o retry de um endpoint não atrasa os outros | TRANSCRICAO | [09:44] Sofia |
| FDD-RES-10 | `docs/FDD.md` | Limitação | Ordem por pedido só na 1ª tentativa; evento em retry pode ser ultrapassado | TRANSCRICAO | [09:12] Diego |
| FDD-OBS-01 | `docs/FDD.md` | Observabilidade — proposta | Logs estruturados Pino: enqueued, succeeded, failed, moved_to_dlq, secret_rotated, worker_cycle | CODIGO | `src/shared/logger/index.ts` |
| FDD-OBS-02 | `docs/FDD.md` | Observabilidade | Log de auditoria webhook_dlq_replayed com userId | TRANSCRICAO | [09:36] Sofia |
| FDD-OBS-03 | `docs/FDD.md` | Observabilidade — proposta | Redact dos campos secret e previousSecret no logger | TRANSCRICAO | [09:22] Diego |
| FDD-OBS-04 | `docs/FDD.md` | Observabilidade — proposta | Métricas (proposta): pendentes, idade do pendente mais antigo vs. 10 s, sucesso, p95, DLQ/dia | TRANSCRICAO | [09:02] Marcos |
| FDD-OBS-05 | `docs/FDD.md` | Observabilidade | Métrica de volume por customer como insumo para decidir rate limiting | TRANSCRICAO | [09:39] Larissa |
| FDD-OBS-06 | `docs/FDD.md` | Observabilidade — proposta | Tracing (proposta): correlação requestId → eventId → webhookId, sem OpenTelemetry | CODIGO | `src/middlewares/request-logger.middleware.ts` |
| FDD-SEG-01 | `docs/FDD.md` | Segurança — proposta | HMAC-SHA256 do corpo com node:crypto; comparação com timingSafeEqual (proposta) | TRANSCRICAO | [09:22] Sofia |
| FDD-SEG-02 | `docs/FDD.md` | Segurança — proposta | Secret gerada com randomBytes(32), prefixo whsec_ (proposta) | TRANSCRICAO | [09:31] Marcos |
| FDD-SEG-03 | `docs/FDD.md` | Segurança | Armazenamento da secret: coluna própria, nunca devolvida, mascarada; criptografia em repouso para a revisão | TRANSCRICAO | [09:46] Sofia |
| FDD-SEG-04 | `docs/FDD.md` | Segurança | https obrigatório no schema Zod | TRANSCRICAO | [09:23] Sofia |
| FDD-SEG-05 | `docs/FDD.md` | Segurança | Replay restrito a ADMIN e auditado | TRANSCRICAO | [09:36] Sofia |
| FDD-SEG-06 | `docs/FDD.md` | Segurança | Risco: X-Timestamp fora do HMAC não impede replay → Q7 para a revisão de segurança | TRANSCRICAO | [09:44] Diego |
| FDD-SEG-07 | `docs/FDD.md` | Segurança | CRUD sem vínculo usuário ↔ customer (aceito por ora) | TRANSCRICAO | [09:37] Sofia |
| FDD-INT-01 | `docs/FDD.md` | Integração com código existente | Em changeStatus (linha 126), dentro do callback de $transaction (linha 131), adicionar await publishWebhookEvent(tx, order,… | CODIGO | `src/modules/orders/order.service.ts` |
| FDD-INT-02 | `docs/FDD.md` | Integração com código existente | Sem alteração. O enum de status que alimenta o filtro vem de OrderStatus, e as transições possíveis definem quais from → to… | CODIGO | `src/modules/orders/order.status.ts` |
| FDD-INT-03 | `docs/FDD.md` | Integração com código existente | Novos enum WebhookOutboxStatus e models WebhookEndpoint, WebhookOutbox, WebhookDelivery e WebhookDeadLetter (§4). Relação in… | CODIGO | `prisma/schema.prisma` |
| FDD-INT-04 | `docs/FDD.md` | Integração com código existente | Base dos 404 do módulo, que estendem AppError diretamente porque NotFoundError fixa NOT_FOUND | CODIGO | `src/shared/errors/app-error.ts` |
| FDD-INT-05 | `docs/FDD.md` | Integração com código existente | Novas classes WebhookError, ao lado das classes de domínio existentes (linhas 45 e 55), reusando BadRequestError, ConflictEr… | CODIGO | `src/shared/errors/http-errors.ts` |
| FDD-INT-06 | `docs/FDD.md` | Integração com código existente | Exportar as novas classes no barrel | CODIGO | `src/shared/errors/index.ts` |
| FDD-INT-07 | `docs/FDD.md` | Integração com código existente | Sem alteração. O ramo de AppError (linhas 15–24) já serializa { error: { code, message, details } } | CODIGO | `src/middlewares/error.middleware.ts` |
| FDD-INT-08 | `docs/FDD.md` | Integração com código existente | authenticate (linha 27) em todas as rotas. requireRole('ADMIN') (linha 49) na rota de replay, como em src/modules/users/user… | CODIGO | `src/middlewares/auth.middleware.ts` |
| FDD-INT-09 | `docs/FDD.md` | Integração com código existente | validate({ params, body }) com os schemas de webhook.schemas.ts, no mesmo padrão de src/modules/orders/order.schemas.ts (z.s… | CODIGO | `src/middlewares/validate.middleware.ts` |
| FDD-INT-10 | `docs/FDD.md` | Integração com código existente | Adicionar webhooks em Controllers (linhas 13–19) e montar, em buildApiRouter (linha 21), /webhooks, /customers/:customerId/w… | CODIGO | `src/routes/index.ts` |
| FDD-INT-11 | `docs/FDD.md` | Integração com código existente | Em buildControllers (linhas 26–53), instanciar WebhookRepository → WebhookService → WebhookController. O OrderService (linha… | CODIGO | `src/app.ts` |
| FDD-INT-12 | `docs/FDD.md` | Integração com código existente | Modelo do novo src/worker.ts (a criar): bootstrap, logs worker_started, shutdown em SIGINT/SIGTERM com $disconnect (linhas 6… | CODIGO | `src/server.ts` |
| FDD-INT-13 | `docs/FDD.md` | Integração com código existente | O worker chama createPrismaClient (linha 4) para ter instância própria. Não importa o prisma singleton da API | CODIGO | `src/config/database.ts` |
| FDD-INT-14 | `docs/FDD.md` | Integração com código existente | Mesmo DATABASE_URL e LOG_LEVEL. Nenhuma variável nova é obrigatória: intervalos, lote e timeout são constantes do módulo (pr… | CODIGO | `src/config/env.ts` |
| FDD-INT-15 | `docs/FDD.md` | Integração com código existente | Mesmo logger na API e no worker. Acrescentar.secret e.previousSecret em redactPaths (linhas 4–11) | CODIGO | `src/shared/logger/index.ts` |
| FDD-INT-16 | `docs/FDD.md` | Integração com código existente | paginated (linha 22) na listagem de webhooks | CODIGO | `src/shared/http/response.ts` |
| FDD-INT-17 | `docs/FDD.md` | Integração com código existente | Novos scripts: "worker": "tsx watch --env-file=.env src/worker.ts" (entry-point a criar) e "start:worker": "node --env-file=… | CODIGO | `package.json` |
| FDD-INT-18 | `docs/FDD.md` | Integração com código existente | Incluir webhookDelivery, webhookDeadLetter, webhookOutbox e webhookEndpoint no deleteMany do beforeEach (linhas 8–16), antes… | CODIGO | `tests/setup.ts` |
| FDD-INT-19 | `docs/FDD.md` | Integração com código existente | Novos casos ao lado de "transitions PENDING -> PAID" (linha 59). Ver §14 | CODIGO | `tests/orders.test.ts` |
| FDD-INT-NOVOS | `docs/FDD.md` | Integração (arquivos novos) | Arquivos a criar: src/modules/webhooks/ (controller, service, repository, routes, schemas, publisher, processor, signature)… | TRANSCRICAO | [09:28] Bruno |
| FDD-DEP-01 | `docs/FDD.md` | Dependência / Compatibilidade | Sem dependência nova: Prisma, uuid, Zod, Pino, fetch nativo, node:crypto | CODIGO | `package.json` |
| FDD-DEP-02 | `docs/FDD.md` | Dependência / Compatibilidade | MySQL 8.0 com suporte a Json; migration aditiva | CODIGO | `prisma/schema.prisma` |
| FDD-DEP-03 | `docs/FDD.md` | Dependência / Compatibilidade | API aditiva; PATCH /orders/:id/status mantém contrato | CODIGO | `src/modules/orders/order.routes.ts` |
| FDD-DEP-04 | `docs/FDD.md` | Dependência / Compatibilidade | Deploy de um novo processo start:worker, exatamente uma instância | TRANSCRICAO | [09:11] Diego |
| FDD-DEP-05 | `docs/FDD.md` | Dependência / Compatibilidade | Clientes validam X-Signature e deduplicam por X-Event-Id; portal documenta | TRANSCRICAO | [09:26] Marcos |
| FDD-RISK-01 | `docs/FDD.md` | Risco | Eventos fora de ordem quando há retry (§8) — P: Média, I: Médio | TRANSCRICAO | [09:12] Diego |
| FDD-RISK-02 | `docs/FDD.md` | Risco | Vazamento da secret armazenada na plataforma (o vazamento do lado do cliente está no PRD) — P: Baixa, I: Alto | TRANSCRICAO | [09:46] Sofia |
| FDD-RISK-03 | `docs/FDD.md` | Risco — proposta | Worker parado sem ninguém perceber — P: Média, I: Alto | TRANSCRICAO | [09:11] Diego |
| FDD-RISK-04 | `docs/FDD.md` | Risco | changeStatus fica mais lento — P: Baixa, I: Médio | TRANSCRICAO | [09:04] Bruno |
| FDD-RISK-05 | `docs/FDD.md` | Risco | Crescimento contínuo da outbox e das deliveries — P: Alta, I: Baixo | TRANSCRICAO | [09:08] Diego |
| FDD-RISK-06 | `docs/FDD.md` | Risco | CRUD sem vínculo usuário ↔ customer — P: Média, I: Médio | TRANSCRICAO | [09:37] Sofia |
| FDD-RISK-07 | `docs/FDD.md` | Risco — proposta | Admin sem forma de descobrir ids da DLQ (não há endpoint de listagem) — P: Alta, I: Baixo | TRANSCRICAO | [09:18] Diego |
| FDD-TEST-01 | `docs/FDD.md` | Teste | Unit: Tabela de backoff: o attempts 1..5 dá o nextAttemptAt correto e o 6 vai para a DLQ | TRANSCRICAO | [09:17] Diego |
| FDD-TEST-02 | `docs/FDD.md` | Teste | Unit: sign(secret, body) bate com um vetor conhecido de HMAC-SHA256; alterar o corpo invalida a assinatura; durante a rotaçã… | TRANSCRICAO | [09:22] Sofia |
| FDD-TEST-03 | `docs/FDD.md` | Teste | Unit: Filtro: um endpoint que não ouve to não recebe linha | TRANSCRICAO | [09:34] Bruno |
| FDD-TEST-04 | `docs/FDD.md` | Teste | Integração: PATCH /orders/:id/status com um webhook interessado cria 1 linha PENDING com o snapshot correto | CODIGO | `tests/orders.test.ts` |
| FDD-TEST-05 | `docs/FDD.md` | Teste | Integração: A inserção na outbox falha (mock) e a ordem continua no status anterior, sem history novo | TRANSCRICAO | [09:40] Bruno |
| FDD-TEST-06 | `docs/FDD.md` | Teste | Integração: Sem webhook interessado, nenhuma linha é criada | TRANSCRICAO | [09:34] Bruno |
| FDD-TEST-07 | `docs/FDD.md` | Teste | Integração: Worker com servidor HTTP local: 200 → DELIVERED; 500 e 429 → retry em +1 min; 404 → DLQ imediata com WEBHOOK_DEL… | TRANSCRICAO | [09:42] Diego |
| FDD-TEST-08 | `docs/FDD.md` | Teste | Integração: Seis falhas levam a FAILED + linha na DLQ; replay como OPERATOR → 403; como ADMIN → 202 com o mesmo eventId | TRANSCRICAO | [09:36] Sofia |
| FDD-TEST-09 | `docs/FDD.md` | Teste | Contrato: POST /webhooks com http:// → 400; a secret só aparece em 201 e no rotate | TRANSCRICAO | [09:23] Sofia |
| FDD-TEST-10 | `docs/FDD.md` | Teste | Segurança: Revisão manual da Sofia sobre HMAC e geração de secret, com 2 dias úteis antes do deploy | TRANSCRICAO | [09:46] Sofia |
| FDD-AC-01 | `docs/FDD.md` | Critério de aceite técnico | Transação e filtro: outbox na mesma transação (falha desfaz a mudança); nada para endpoint que não ouve o status ou inativo;… | TRANSCRICAO | [09:40] Bruno |
| FDD-AC-02 | `docs/FDD.md` | Critério de aceite técnico | Contrato e segurança: payload e 5 headers com assinatura válida; rotação com 24 h de carência; http:// → 400; secret fora de… | TRANSCRICAO | [09:44] Diego |
| FDD-AC-03 | `docs/FDD.md` | Critério de aceite técnico | Falhas: retry 1m/5m/30m/2h/12h e DLQ após o 6º envio; payload > 64 KB → DLQ; replay ADMIN com mesmo eventId e userId no log | TRANSCRICAO | [09:17] Larissa |
| FDD-AC-04 | `docs/FDD.md` | Critério de aceite técnico | Padrões e operação: erros WEBHOOK_ via error.middleware sem alteração; worker via npm run worker com PrismaClient próprio; t… | TRANSCRICAO | [09:30] Larissa |
