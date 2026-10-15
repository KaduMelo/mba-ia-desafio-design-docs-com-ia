"""Gera docs/TRACKER.md a partir das tabelas dos documentos + itens curados manualmente.
Uso: python3 -I gen_tracker.py <raiz-do-repo>
"""
import os
import re
import sys

ROOT = sys.argv[1]
TS = re.compile(r'\[(\d{2}:\d{2})\] ([A-Z][a-z]+)')
PATH = re.compile(r'`((?:src|prisma|tests)/[\w./-]+?|package\.json)(?::[\d,–-]+)?`')


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


def section(text, heading):
    """Texto a partir do heading (prefixo) até o próximo heading de nível <= ao dele."""
    m = re.search(r'^(#+) ' + re.escape(heading) + r'.*$', text, re.M)
    assert m, heading
    level = len(m.group(1))
    rest = text[m.end():]
    n = re.search(r'^#{1,%d} ' % level, rest, re.M)
    return rest[: n.start()] if n else rest


def tables(chunk):
    out, cur = [], []
    for line in chunk.splitlines():
        if line.startswith('|'):
            cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
            cur.append(cells)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    # remove header e separador
    return [t[2:] for t in out]


def clean(s, n=125):
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    s = s.replace('**', '').replace('`', '').replace('*', '').replace('|', '/')
    s = re.sub(r'\s+', ' ', s).strip()
    s = TS.sub('', s)
    s = re.sub(r'\(\s*[,;]?\s*\)', '', s).strip(' ,;.—-')
    s = re.sub(r'\s+([.,;:])', r'\1', s)
    return s if len(s) <= n else s[: n - 1].rstrip() + '…'


def locate(text):
    m = TS.search(text)
    if m:
        return 'TRANSCRICAO', f'[{m.group(1)}] {m.group(2)}'
    for p in PATH.findall(text):
        if os.path.exists(os.path.join(ROOT, p)):
            return 'CODIGO', p
    return None, None


ROWS = []


def add(id_, doc, tipo, resumo, fonte=None, loc=None, src_text='', raw=''):
    if 'proposta' in (resumo + ' ' + src_text + ' ' + raw).lower():
        tipo = f'{tipo} — proposta'
    if fonte is None:
        fonte, loc = locate(src_text)
    ROWS.append([id_, doc, tipo, clean(resumo), fonte, loc])


def from_table(doc, heading, prefix, tipo, summ, idx_table=0, id_col=None, start=1, skip_first=False):
    t = tables(section(read(doc), heading))[idx_table]
    for i, row in enumerate(t, start=start):
        id_ = row[id_col] if id_col is not None else f'{prefix}-{i:02d}'
        id_ = clean(id_)
        add(id_, doc, tipo, summ(row), src_text=' '.join(row))


PRD, RFC, FDD = 'docs/PRD.md', 'docs/RFC.md', 'docs/FDD.md'

# ---------------- PRD ----------------
add('PRD-CTX-01', PRD, 'Contexto', 'Pedido formal de 3 clientes B2B (Atlas Comercial, MaxDistribuição, Nova Cargo) por notificação de mudança de status', src_text='[09:00] Marcos')
add('PRD-CTX-02', PRD, 'Problema', 'Clientes fazem polling em GET /orders; integração lenta e cara', src_text='[09:00] Marcos')
add('PRD-CTX-03', PRD, 'Problema', 'Risco de churn: Atlas pode migrar para concorrente se não houver entrega até o fim do trimestre', src_text='[09:00] Marcos')
add('PRD-CTX-04', PRD, 'Restrição', 'Prazo alvo: fim de novembro', src_text='[09:45] Marcos')
from_table(PRD, '3. Público-alvo', 'PRD-PER', 'Público-alvo', lambda r: f'{r[0]}: {r[1]}', 0)
from_table(PRD, '3. Público-alvo', 'PRD-CEN', 'Cenário de uso', lambda r: r[1], 1, id_col=None)
for r in ROWS:
    if r[0].startswith('PRD-CEN-'):
        pass
from_table(PRD, '4. Objetivos', 'PRD-OBJ', 'Objetivo / Métrica', lambda r: f'{r[1]} — meta: {r[3]}')
for i, txt in enumerate([
    'Cadastro, edição, remoção e listagem de webhooks por customer via API autenticada',
    'Filtro por webhook dos status de pedido de interesse',
    'Notificação automática a cada mudança de status',
    'Assinatura das notificações e secret exclusiva por webhook, com rotação',
    'Retentativa automática e DLQ com reprocessamento por ADMIN',
    'Histórico de entregas consultável pelo cliente'], 1):
    loc = ['[09:33] Bruno', '[09:33] Marcos', '[09:00] Marcos', '[09:21] Sofia', '[09:18] Diego', '[09:34] Marcos'][i - 1]
    add(f'PRD-ESC-{i:02d}', PRD, 'Escopo (incluso)', txt, src_text=loc)
from_table(PRD, '5.2 Fora de escopo', 'PRD-OUT', 'Fora de escopo', lambda r: f'{r[0]} — {r[1]}')
from_table(PRD, '6. Requisitos funcionais', None, 'Requisito Funcional', lambda r: r[1], id_col=0)
from_table(PRD, '7. Requisitos não funcionais', None, 'Requisito Não Funcional', lambda r: r[1], id_col=0)
DEC_LOC = ['[09:06] Diego', '[09:09] Diego', '[09:17] Larissa', '[09:22] Sofia', '[09:26] Larissa', '[09:30] Larissa', '[09:52] Larissa']
t = tables(section(read(PRD), '8. Decisões'))[0]
for i, row in enumerate(t, 1):
    add(f'PRD-DEC-{i:02d}', PRD, 'Decisão / Trade-off', f'{row[0]} — {row[1]}', src_text=DEC_LOC[i - 1])
from_table(PRD, '9. Dependências', 'PRD-DEP', 'Dependência', lambda r: f'{r[0]} ({r[1]})')
from_table(PRD, '10. Riscos', 'PRD-RISK', 'Risco', lambda r: f'{r[0]} — P: {r[1]}, I: {r[2]}')
AC = [('Entrega: notificação em < 10 s só para status do filtro, com assinatura válida e identificador de evento estável em reenvios', '[09:02] Marcos'),
      ('Cadastro e segurança: URL http:// recusada; secret só no cadastro e na rotação, anterior aceita por 24 h; revisão de segurança antes do deploy', '[09:21] Sofia'),
      ('Falhas e operação: retentativa automática e DLQ; replay só por ADMIN com autoria registrada; histórico das últimas 100 entregas; falha no registro impede a mudança de status', '[09:17] Larissa')]
for i, (txt, loc) in enumerate(AC, 1):
    add(f'PRD-AC-{i:02d}', PRD, 'Critério de aceitação', txt, src_text=loc)
from_table(PRD, '12. Estratégia de testes', 'PRD-TEST', 'Estratégia de testes', lambda r: f'{r[0]}: {r[1]}')

# ---------------- RFC ----------------
add('RFC-META-01', RFC, 'Metadado', 'Autora Larissa (Tech Lead) abre o doc de design; revisores Marcos, Bruno, Diego, Sofia', src_text='[09:50] Larissa')
add('RFC-CTX-01', RFC, 'Contexto', 'Fluxo apenas de saída (outbound): clientes recebem, não enviam', src_text='[09:02] Marcos')
add('RFC-CTX-02', RFC, 'Restrição', 'Mudança de status ocorre em changeStatus, numa transação já pesada (orders, history, estoque)', 'CODIGO', 'src/modules/orders/order.service.ts')
add('RFC-CTX-03', RFC, 'Restrição', 'Atomicidade: status alterado sem evento é inaceitável', src_text='[09:40] Bruno')
add('RFC-CTX-04', RFC, 'Restrição', 'Isolamento: cliente lento não pode travar mudança de status de outros pedidos', src_text='[09:04] Bruno')
COMP = [('Registro do evento na outbox via publishWebhookEvent(tx, …) na transação', '[09:41] Bruno'),
        ('Snapshot enxuto filtrado por status na inserção', '[09:52] Larissa'),
        ('Worker separado, PrismaClient próprio, polling 2 s, single-worker', '[09:11] Diego'),
        ('Timeout 10 s, 5 retentativas 1m/5m/30m/2h/12h, DLQ com replay ADMIN', '[09:17] Larissa'),
        ('HMAC-SHA256 do corpo, secret por endpoint, rotação 24 h, só https', '[09:22] Sofia'),
        ('At-least-once com X-Event-Id', '[09:26] Larissa'),
        ('CRUD de webhooks e histórico de entregas via API com JWT', '[09:33] Bruno'),
        ('Módulo src/modules/webhooks reusando AppError, error middleware, requireRole, Zod, Pino; códigos WEBHOOK_', '[09:30] Larissa')]
for i, (txt, loc) in enumerate(COMP, 1):
    add(f'RFC-PROP-{i:02d}', RFC, 'Proposta técnica', txt, src_text=loc)
GAR_LOC = ['[09:06] Diego', '[09:24] Diego', '[09:09] Diego', '[09:13] Larissa', '[09:17] Diego']
t = tables(section(read(RFC), '3.3 Garantias'))[0]
for i, row in enumerate(t, 1):
    add(f'RFC-GAR-{i:02d}', RFC, 'Garantia / Limitação', f'{row[0]}: {row[1]}', src_text=GAR_LOC[i - 1])
from_table(RFC, '4. Alternativas', 'RFC-ALT', 'Alternativa descartada (trade-off)', lambda r: f'{r[1]} — {r[2]}')
from_table(RFC, '5. Questões em aberto', 'RFC-OPEN', 'Questão em aberto', lambda r: r[1])
from_table(RFC, '5.1 Ambiguidades', 'RFC-RES', 'Decisão (ambiguidade resolvida)', lambda r: f'{r[1]} → {r[2]}')
from_table(RFC, '6. Impacto e riscos', 'RFC-RISK', 'Risco', lambda r: f'{r[0]} — mitigação: {r[1]}')
add('RFC-CRON-01', RFC, 'Restrição (prazo)', 'Cronograma de 3 sprints com 2 dias úteis de revisão de segurança no fim', src_text='[09:46] Larissa')

# ---------------- ADRs ----------------
ADRS = sorted(f for f in os.listdir(os.path.join(ROOT, 'docs/adrs')) if f.startswith('ADR-'))
ADR_DEC = {
    'ADR-001': ('Outbox no MySQL na mesma transação do changeStatus; rollback se a inserção falhar', '[09:08] Larissa'),
    'ADR-002': ('Worker em processo separado (src/worker.ts), polling de 2 s, PrismaClient próprio, single-worker', '[09:10] Larissa'),
    'ADR-003': ('Backoff 1m/5m/30m/2h/12h (1 envio + 5 retries) e DLQ em webhook_dead_letter com replay ADMIN', '[09:17] Larissa'),
    'ADR-004': ('HMAC-SHA256 sobre o corpo, secret por endpoint gerada pela plataforma, rotação com grace de 24 h', '[09:22] Sofia'),
    'ADR-005': ('Entrega at-least-once; X-Event-Id (UUID) para deduplicação; 1 linha de outbox por evento × webhook', '[09:26] Larissa'),
    'ADR-006': ('Reuso máximo dos padrões: módulo, AppError, códigos WEBHOOK_, error middleware, requireRole, Zod, Pino', '[09:30] Larissa'),
    'ADR-007': ('Payload snapshot renderizado na inserção; filtro de status na inserção; payload enxuto sem items', '[09:52] Bruno'),
}
for f in ADRS:
    adr_id = f[:7]
    doc = f'docs/adrs/{f}'
    txt, loc = ADR_DEC[adr_id]
    add(adr_id, doc, 'Decisão', txt, src_text=loc)
    t = tables(section(read(doc), 'Alternativas Consideradas'))[0]
    for i, row in enumerate(t, 1):
        add(f'{adr_id}-ALT-{i:02d}', doc, 'Alternativa descartada', f'{row[0]} — {row[1]}', src_text=' '.join(row))
    if adr_id == 'ADR-006':
        t = tables(section(read(doc), 'Decisão'))[0]
        for i, row in enumerate(t, 1):
            fonte, loc2 = locate(row[1])
            add(f'ADR-006-COD-{i:02d}', doc, 'Padrão de código reutilizado', f'{row[0]} → {row[2]}', fonte, loc2, src_text=row[1])

# ---------------- FDD ----------------
from_table(FDD, '2. Objetivos técnicos', None, 'Objetivo técnico', lambda r: f'{r[1]} — {r[2]}', id_col=0)
# renomeia OT-x -> FDD-OT-x
for r in ROWS:
    if re.fullmatch(r'OT-\d', r[0]):
        r[0] = 'FDD-' + r[0]
from_table(FDD, '3. Escopo', 'FDD-OUT', 'Exclusão', lambda r: r[0])
MODELS = [('Model WebhookEndpoint: url, events (Json), secret, previousSecret + expiração, active, deletedAt', '[09:21] Bruno'),
          ('Model WebhookOutbox: eventId único, payload snapshot, status, attempts, nextAttemptAt; índices status/createdAt', '[09:08] Diego'),
          ('Model WebhookDelivery: tentativa, sucesso, status/corpo da resposta, durationMs', '[09:34] Marcos'),
          ('Model WebhookDeadLetter: payload, reason, attempts, failedAt, replayedAt/By', '[09:18] Diego'),
          ('IDs UUID Char(36) no padrão do schema existente', 'prisma/schema.prisma'),
          ('Status FAILED como estado terminal na outbox; evidência na DLQ (proposta, resolve AMB-02)', '[09:08] Diego'),
          ('DELETE lógico com deletedAt para preservar histórico e DLQ (proposta)', '[09:18] Diego')]
for i, (txt, loc) in enumerate(MODELS, 1):
    if loc.startswith('['):
        add(f'FDD-DADOS-{i:02d}', FDD, 'Modelo de dados', txt, src_text=loc)
    else:
        add(f'FDD-DADOS-{i:02d}', FDD, 'Modelo de dados', txt, 'CODIGO', loc)
FLOWS = [('Inserção na outbox após orderStatusHistory.create, dentro do $transaction de changeStatus', 'CODIGO', 'src/modules/orders/order.service.ts'),
         ('Filtro na inserção: só endpoints ativos do customer que ouvem o to_status', None, '[09:34] Bruno'),
         ('Worker: ciclo a cada 2 s, lote de 10 (proposta), envio sequencial por createdAt', None, '[09:09] Diego'),
         ('Recuperação de crash: PROCESSING volta a PENDING na inicialização (proposta)', None, '[09:24] Diego'),
         ('Retry: tabela de backoff por attempts; 6º envio falho → DLQ', None, '[09:17] Diego'),
         ('Classificação de retry: timeout, rede, 5xx, 408, 429 retentam; demais 3xx/4xx → DLQ (proposta, AMB-09)', None, '[09:42] Diego'),
         ('Replay: mesma linha da outbox volta a PENDING com o mesmo eventId', None, '[09:18] Diego'),
         ('Rotação: secret anterior válida 24 h; duas assinaturas em X-Signature (proposta)', None, '[09:21] Sofia')]
for i, (txt, f_, loc) in enumerate(FLOWS, 1):
    if f_:
        add(f'FDD-FLUXO-{i:02d}', FDD, 'Fluxo', txt, f_, loc)
    else:
        add(f'FDD-FLUXO-{i:02d}', FDD, 'Fluxo', txt, src_text=loc)
CONTR = [('POST /api/v1/webhooks — cadastra webhook; customerId no body; secret devolvida só aqui; 201', '[09:31] Marcos'),
         ('GET /api/v1/customers/:customerId/webhooks — lista webhooks do customer (customerId no path); 200', '[09:33] Bruno'),
         ('PATCH /api/v1/webhooks/:id — edita url, events, active; 200', '[09:33] Bruno'),
         ('DELETE /api/v1/webhooks/:id — remoção lógica; 204', '[09:33] Bruno'),
         ('POST /api/v1/webhooks/:id/rotate-secret — nova secret, anterior válida 24 h; 200', '[09:21] Sofia'),
         ('GET /api/v1/webhooks/:id/deliveries — últimas 100 tentativas com payload, resposta e tempo; 200', '[09:34] Marcos'),
         ('POST /api/v1/admin/webhooks/dead-letter/:id/replay — ADMIN, auditado; 202', '[09:35] Diego'),
         ('Contrato de saída: payload event_id, event_type, timestamp, order_id, order_number, from/to_status, customer_id, total_cents', '[09:43] Diego'),
         ('Headers de saída: Content-Type, X-Event-Id, X-Webhook-Id, X-Timestamp, X-Signature', '[09:44] Diego'),
         ('customerId nunca vem do JWT', '[09:32] Larissa'),
         ('Endpoints sob /api/v1 com authenticate', 'src/app.ts')]
for i, (txt, loc) in enumerate(CONTR, 1):
    if loc.startswith('['):
        add(f'FDD-CONTRATO-{i:02d}', FDD, 'Contrato público', txt, src_text=loc)
    else:
        add(f'FDD-CONTRATO-{i:02d}', FDD, 'Contrato público', txt, 'CODIGO', loc)
ERR_LOC = {  # erros sem fala direta: fala ou arquivo que motivou
    'WEBHOOK_CUSTOMER_NOT_FOUND': ('TRANSCRICAO', '[09:32] Larissa'),
    'WEBHOOK_DEAD_LETTER_NOT_FOUND': ('TRANSCRICAO', '[09:18] Diego'),
    'WEBHOOK_INVALID_EVENT_FILTER': ('TRANSCRICAO', '[09:33] Marcos'),
    'WEBHOOK_INACTIVE': ('TRANSCRICAO', '[09:21] Bruno'),
    'WEBHOOK_DEAD_LETTER_ALREADY_REPLAYED': ('TRANSCRICAO', '[09:18] Diego'),
    'WEBHOOK_DELIVERY_FAILED': ('TRANSCRICAO', '[09:15] Diego'),
    'WEBHOOK_DELIVERY_REJECTED': ('TRANSCRICAO', '[09:15] Diego'),
    'WEBHOOK_NETWORK_ERROR': ('TRANSCRICAO', '[09:14] Larissa'),
}
seen = set()
n = 0
for t in tables(section(read(FDD), '7. Matriz de erros')):
    for row in t:
        code = clean(row[0])
        if code in seen:
            continue
        seen.add(code)
        n += 1
        quando = row[3] if len(row) == 5 else row[2]
        if code in ERR_LOC:
            f_, loc = ERR_LOC[code]
            add(f'FDD-ERR-{n:02d}', FDD, 'Erro (matriz)', f'{code}: {quando}', f_, loc, raw=' '.join(row))
        else:
            add(f'FDD-ERR-{n:02d}', FDD, 'Erro (matriz)', f'{code}: {quando}', src_text=' '.join(row))
add('FDD-ERR-BASE', FDD, 'Restrição de código', 'NotFoundError fixa o código NOT_FOUND → 404 do módulo estendem AppError', 'CODIGO', 'src/shared/errors/http-errors.ts')
add('FDD-ERR-ZOD', FDD, 'Restrição de código', 'validate.middleware converte ZodError em VALIDATION_ERROR → WEBHOOK_INVALID_URL vai em details', 'CODIGO', 'src/middlewares/validate.middleware.ts')
RES_LOC = {'Crash do worker': '[09:24] Diego', 'Isolamento entre endpoints': '[09:44] Sofia'}
t = tables(section(read(FDD), '8. Estratégias de resiliência'))[0]
for i, row in enumerate(t, 1):
    k = clean(row[0])
    add(f'FDD-RES-{i:02d}', FDD, 'Resiliência', f'{row[0]}: {row[1]}', src_text=RES_LOC.get(k, ' '.join(row)), raw=' '.join(row))
add(f'FDD-RES-{len(t) + 1:02d}', FDD, 'Limitação', 'Ordem por pedido só na 1ª tentativa; evento em retry pode ser ultrapassado', src_text='[09:12] Diego')
OBS = [('Logs estruturados Pino: enqueued, succeeded, failed, moved_to_dlq, secret_rotated, worker_cycle', 'CODIGO', 'src/shared/logger/index.ts'),
       ('Log de auditoria webhook_dlq_replayed com userId', None, '[09:36] Sofia'),
       ('Redact dos campos secret e previousSecret no logger', None, '[09:22] Diego'),
       ('Métricas (proposta): pendentes, idade do pendente mais antigo vs. 10 s, sucesso, p95, DLQ/dia', None, '[09:02] Marcos'),
       ('Métrica de volume por customer como insumo para decidir rate limiting', None, '[09:39] Larissa'),
       ('Tracing (proposta): correlação requestId → eventId → webhookId, sem OpenTelemetry', 'CODIGO', 'src/middlewares/request-logger.middleware.ts')]
for i, (txt, f_, loc) in enumerate(OBS, 1):
    if f_:
        add(f'FDD-OBS-{i:02d}', FDD, 'Observabilidade', txt, f_, loc)
    else:
        add(f'FDD-OBS-{i:02d}', FDD, 'Observabilidade', txt, src_text=loc)
SEG = [('HMAC-SHA256 do corpo com node:crypto; comparação com timingSafeEqual (proposta)', '[09:22] Sofia'),
       ('Secret gerada com randomBytes(32), prefixo whsec_ (proposta)', '[09:31] Marcos'),
       ('Armazenamento da secret: coluna própria, nunca devolvida, mascarada; criptografia em repouso para a revisão', '[09:46] Sofia'),
       ('https obrigatório no schema Zod', '[09:23] Sofia'),
       ('Replay restrito a ADMIN e auditado', '[09:36] Sofia'),
       ('Risco: X-Timestamp fora do HMAC não impede replay → Q7 para a revisão de segurança', '[09:44] Diego'),
       ('CRUD sem vínculo usuário ↔ customer (aceito por ora)', '[09:37] Sofia')]
for i, (txt, loc) in enumerate(SEG, 1):
    add(f'FDD-SEG-{i:02d}', FDD, 'Segurança', txt, src_text=loc)
t = tables(section(read(FDD), '11. Integração'))[0]
for row in t:
    p = re.search(r'`([^`]+)`', row[1]).group(1)
    add(f'FDD-INT-{int(row[0]):02d}', FDD, 'Integração com código existente', clean(row[2], 125), 'CODIGO', p)
add('FDD-INT-NOVOS', FDD, 'Integração (arquivos novos)', 'Arquivos a criar: src/modules/webhooks/* (controller, service, repository, routes, schemas, publisher, processor, signature) e src/worker.ts', src_text='[09:28] Bruno')
DEP = [('Sem dependência nova: Prisma, uuid, Zod, Pino, fetch nativo, node:crypto', 'CODIGO', 'package.json'),
       ('MySQL 8.0 com suporte a Json; migration aditiva', 'CODIGO', 'prisma/schema.prisma'),
       ('API aditiva; PATCH /orders/:id/status mantém contrato', 'CODIGO', 'src/modules/orders/order.routes.ts'),
       ('Deploy de um novo processo start:worker, exatamente uma instância', None, '[09:11] Diego'),
       ('Clientes validam X-Signature e deduplicam por X-Event-Id; portal documenta', None, '[09:26] Marcos')]
for i, (txt, f_, loc) in enumerate(DEP, 1):
    if f_:
        add(f'FDD-DEP-{i:02d}', FDD, 'Dependência / Compatibilidade', txt, f_, loc)
    else:
        add(f'FDD-DEP-{i:02d}', FDD, 'Dependência / Compatibilidade', txt, src_text=loc)
RISK_LOC = {1: '[09:12] Diego', 3: '[09:11] Diego', 4: '[09:04] Bruno', 7: '[09:18] Diego'}
t = tables(section(read(FDD), '13. Riscos'))[0]
for i, row in enumerate(t, 1):
    src = RISK_LOC.get(i, ' '.join(row))
    add(f'FDD-RISK-{i:02d}', FDD, 'Risco', f'{row[0]} — P: {row[1]}, I: {row[2]}', src_text=src, raw=' '.join(row))
TEST_LOC = {1: '[09:17] Diego', 2: '[09:22] Sofia', 7: '[09:42] Diego', 8: '[09:36] Sofia', 9: '[09:23] Sofia'}
t = tables(section(read(FDD), '14. Plano de testes'))[0]
for i, row in enumerate(t, 1):
    src = TEST_LOC.get(i, ' '.join(row))
    add(f'FDD-TEST-{i:02d}', FDD, 'Teste', f'{row[0]}: {row[1]}', src_text=src, raw=' '.join(row))
AC = [('Transação e filtro: outbox na mesma transação (falha desfaz a mudança); nada para endpoint que não ouve o status ou inativo; envio em ≤ 2 s', '[09:40] Bruno'),
      ('Contrato e segurança: payload e 5 headers com assinatura válida; rotação com 24 h de carência; http:// → 400; secret fora de logs e respostas', '[09:44] Diego'),
      ('Falhas: retry 1m/5m/30m/2h/12h e DLQ após o 6º envio; payload > 64 KB → DLQ; replay ADMIN com mesmo eventId e userId no log', '[09:17] Larissa'),
      ('Padrões e operação: erros WEBHOOK_ via error.middleware sem alteração; worker via npm run worker com PrismaClient próprio; testes e revisão da Sofia concluídos', '[09:30] Larissa')]
for i, (txt, loc) in enumerate(AC, 1):
    add(f'FDD-AC-{i:02d}', FDD, 'Critério de aceite técnico', txt, src_text=loc)

OVERRIDE = {
    'PRD-OUT-08': ('TRANSCRICAO', '[09:40] Bruno'),
    'FDD-OUT-07': ('TRANSCRICAO', '[09:40] Bruno'),
    'ADR-005-ALT-02': ('TRANSCRICAO', '[09:24] Diego'),
    'ADR-006-COD-01': ('CODIGO', 'src/modules/orders/'),
}
for r in ROWS:
    if r[0] in OVERRIDE:
        r[4], r[5] = OVERRIDE[r[0]]
# itens que o FDD marca como proposta mas cujo resumo não contém a palavra
PROP_IDS = {'FDD-CONTRATO-02', 'FDD-CONTRATO-04', 'FDD-CONTRATO-05', 'FDD-FLUXO-07', 'FDD-OBS-01', 'FDD-OBS-03'}
# alternativas registradas nos ADRs como "plausíveis" (não discutidas na reunião)
PLAUSIVEIS = {'ADR-004-ALT-02', 'ADR-005-ALT-02', 'ADR-006-ALT-01'}
for r in ROWS:
    if r[0] in PROP_IDS and not r[2].endswith('proposta'):
        r[2] = f'{r[2]} — proposta'
    if r[0] in PLAUSIVEIS:
        r[2] = 'Alternativa plausível (não discutida)'

# ---------------- saída ----------------
sem = [r for r in ROWS if not r[4]]
ok = [r for r in ROWS if r[4]]
total = len(ROWS)
n_tr = sum(1 for r in ok if r[4] == 'TRANSCRICAO')
n_cd = sum(1 for r in ok if r[4] == 'CODIGO')
ids = [r[0] for r in ROWS]
dups = sorted({i for i in ids if ids.count(i) > 1})

lines = []
lines.append('# Tracker de Rastreabilidade')
lines.append('')
lines.append('Liga cada item registrado em [PRD](PRD.md), [RFC](RFC.md), [FDD](FDD.md) e [ADRs](adrs/README.md) à sua origem: '
             'uma fala da reunião ([`TRANSCRICAO.md`](../TRANSCRICAO.md)) ou um arquivo do código.')
lines.append('')
lines.append('**Como ler:**')
lines.append('')
lines.append('- **Fonte** é `TRANSCRICAO` ou `CODIGO`.')
lines.append('- **Localização** é `[hh:mm] Nome` ou o caminho do arquivo.')
lines.append('- Quando o item cita várias falas, a localização aponta a **principal**. As demais estão no próprio documento.')
lines.append('- Itens marcados nos documentos como *(proposta)* não foram decididos na reunião. A localização deles aponta a fala ou o arquivo que **motivou** a proposta, e o resumo deixa claro que é proposta.')
lines.append('')
lines.append(f'**Totais:** {total} linhas · {n_tr} com fonte `TRANSCRICAO` ({100 * n_tr / total:.0f}%) · {n_cd} com fonte `CODIGO` ({100 * n_cd / total:.0f}%).')
lines.append('')
lines.append('| ID | Documento | Tipo | Conteúdo (resumo) | Fonte | Localização |')
lines.append('|---|---|---|---|---|---|')
for r in ok:
    lines.append(f'| {r[0]} | `{r[1]}` | {r[2]} | {r[3]} | {r[4]} | {"`" + r[5] + "`" if r[4] == "CODIGO" else r[5]} |')
if sem:
    lines.append('')
    lines.append('## Itens sem origem')
    lines.append('')
    for r in sem:
        lines.append(f'- {r[0]} ({r[1]}): {r[3]}')
with open(os.path.join(ROOT, 'docs/TRACKER.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print('total', total, 'transcricao', n_tr, 'codigo', n_cd, 'sem origem', len(sem), 'dups', dups)
for r in sem:
    print('SEM', r[0], r[3][:80])
