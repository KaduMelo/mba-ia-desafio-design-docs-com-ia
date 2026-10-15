"""Checa mecanicamente os critérios de aceite do enunciado (git show e7f6311:README.md).
Uso (na raiz do repo): python3 -I processo/scripts/check_acceptance.py
"""
import glob
import os
import re


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def heads(t):
    return [h.lower() for h in re.findall(r'^#+ (.+)$', t, re.M)]


def has(t, *names):
    hs = heads(t)
    return [n for n in names if not any(n.lower() in h for h in hs)]


def slug(h):
    h = re.sub(r'[^\w\- ]', '', h.strip().lower())
    return h.replace(' ', '-')


R = []


def check(area, crit, ok, evid):
    R.append((area, crit, 'OK' if ok else 'FALHA', evid))


tr = read('TRANSCRICAO.md')
pairs = set(re.findall(r'^\[(\d{2}:\d{2})\] (\w+):', tr, re.M))

# PRD
p = read('docs/PRD.md')
miss = has(p, 'Resumo e contexto', 'Problema e motivação', 'Público-alvo e cenários', 'Objetivos e métricas',
           'Incluso', 'Fora de escopo', 'Requisitos funcionais', 'Requisitos não funcionais', 'Decisões e trade-offs',
           'Dependências', 'Riscos', 'Critérios de aceitação', 'Estratégia de testes')
check('PRD', 'Arquivo existe e contém as seções obrigatórias', not miss, f'faltando: {miss}' if miss else '13 seções encontradas')
frs = re.findall(r'^\| (PRD-FR-\d+) \|', p, re.M)
check('PRD', '>= 8 requisitos funcionais', len(frs) >= 8, f'{len(frs)} PRD-FR')
obj = re.search(r'## 4\..*?(?=\n## )', p, re.S).group(0)
quant = [l for l in obj.splitlines() if l.startswith('| O') and re.search(r'\d', l.split('|')[4])]
check('PRD', '>= 1 objetivo com métrica e meta quantitativa', len(quant) >= 1, f'{len(quant)} objetivos com meta numérica')
out = re.search(r'### 5\.2.*?(?=\n## )', p, re.S).group(0)
outrows = [l for l in out.splitlines() if l.startswith('| ') and re.search(r'\[\d\d:\d\d\]', l)]
check('PRD', 'Fora de escopo com >= 2 itens descartados/adiados na reunião', len(outrows) >= 2, f'{len(outrows)} itens com timestamp')
rk = re.search(r'## 10\..*?(?=\n## )', p, re.S).group(0)
rkrows = [l for l in rk.splitlines() if l.startswith('| ') and not l.startswith('| Risco') and not l.startswith('|---')]
check('PRD', '>= 2 riscos com probabilidade, impacto e mitigação', len(rkrows) >= 2 and 'Probabilidade' in rk and 'Mitigação' in rk, f'{len(rkrows)} riscos')

# RFC
r = read('docs/RFC.md')
meta_ok = all(k in r for k in ['**Autora**', '**Status**', '**Data**', '**Revisores**']) and all(n in r.split('\n---\n')[0] for n in ['Marcos', 'Bruno', 'Diego', 'Sofia'])
miss = has(r, 'TL;DR', 'Contexto e problema', 'Proposta técnica', 'Alternativas consideradas', 'Questões em aberto', 'Impacto e riscos', 'Decisões relacionadas')
check('RFC', 'Seções obrigatórias + metadados com participantes como revisores', meta_ok and not miss, f'faltando: {miss}' if miss else 'metadados e 7 seções')
alt = re.search(r'## 4\..*?(?=\n## )', r, re.S).group(0)
altrows = [l for l in alt.splitlines() if l.startswith('| ALT')]
check('RFC', '>= 2 alternativas descartadas com trade-off', len(altrows) >= 2, f'{len(altrows)} alternativas')
q = re.search(r'## 5\..*?(?=\n### 5\.1)', r, re.S).group(0)
qrows = [l for l in q.splitlines() if l.startswith('| Q')]
check('RFC', '>= 2 questões em aberto', len(qrows) >= 2, f'{len(qrows)} questões')
adrlinks = set(re.findall(r'\]\((adrs/ADR-\d{3}[^)]*\.md)\)', r))
check('RFC', 'Referencia com link >= 2 ADRs', len(adrlinks) >= 2, f'{len(adrlinks)} ADRs linkados')
check('RFC', 'Conciso (2 a 4 páginas)', len(r.split()) <= 2000, f'{len(r.split())} palavras')

# FDD
f = read('docs/FDD.md')
miss = has(f, 'Contexto e motivação técnica', 'Objetivos técnicos', 'Escopo e exclusões', 'Fluxos detalhados', 'Contratos públicos',
           'Matriz de erros', 'Estratégias de resiliência', 'Observabilidade', 'Dependências e compatibilidade',
           'Critérios de aceite técnicos', 'Riscos e mitigação', 'Integração com o sistema existente')
check('FDD', 'Seções obrigatórias', not miss, f'faltando: {miss}' if miss else '12 seções')
eps = re.split(r'^### 6\.\d ', f, flags=re.M)[1:]
good = [e for e in eps if re.match(r'`(GET|POST|PATCH|DELETE) /api', e) and e.count('```http') >= 2 and re.search(r'\b(20[0-9])\b', e)]
check('FDD', '>= 4 endpoints com request, response e status codes', len(good) >= 4, f'{len(good)} endpoints completos')
err = re.search(r'## 7\..*?(?=\n## )', f, re.S).group(0)
codes = [c for c in re.findall(r'^\| `([A-Z_]+)`', err, re.M)]
check('FDD', 'Matriz de erros com prefixo WEBHOOK_', codes and all(c.startswith('WEBHOOK_') for c in codes), f'{len(set(codes))} códigos, todos WEBHOOK_' if codes else 'sem códigos')
integ = re.search(r'## 11\..*?(?=\n## )', f, re.S).group(0)
real = {x for x in re.findall(r'`((?:src|prisma|tests)/[\w./-]+|package\.json)`', integ) if os.path.exists(x)}
check('FDD', 'Integração referencia >= 4 caminhos reais', len(real) >= 4, f'{len(real)} caminhos reais')
obs = re.search(r'## 9\..*?(?=\n## )', f, re.S).group(0).lower()
check('FDD', 'Observabilidade cita métricas, logs e tracing', all(k in obs for k in ['métrica', 'log', 'tracing']), 'métricas, logs e tracing presentes')

# ADRs
adrs = sorted(glob.glob('docs/adrs/ADR-*.md'))
names_ok = all(re.fullmatch(r'ADR-\d{3}-[a-z0-9]+(-[a-z0-9]+)*\.md', os.path.basename(a)) for a in adrs)
check('ADRs', 'Entre 5 e 8 arquivos ADR-NNN-kebab-case.md', 5 <= len(adrs) <= 8 and names_ok, f'{len(adrs)} arquivos, nomes {"ok" if names_ok else "inválidos"}')
bad = [os.path.basename(a) for a in adrs if has(read(a), 'Contexto', 'Decisão', 'Alternativas Consideradas', 'Consequências') or '**Status:**' not in read(a)]
check('ADRs', 'Cada ADR com Status, Contexto, Decisão, Alternativas, Consequências', not bad, f'incompletos: {bad}' if bad else 'todos completos')
topics = {'Outbox': 'outbox', 'Retry/DLQ': 'dlq', 'HMAC': 'hmac', 'at-least-once': 'at-least-once', 'Worker polling': 'polling', 'Reuso de padrões': 'reuso'}
cov = [k for k, v in topics.items() if any(v in os.path.basename(a).lower() or v in read(a).split('\n')[0].lower() for a in adrs)]
check('ADRs', 'Cobre >= 5 das 6 decisões principais', len(cov) >= 5, f'{len(cov)}/6: {", ".join(cov)}')
coderef = [os.path.basename(a) for a in adrs if any(os.path.exists(x) for x in re.findall(r'`((?:src|prisma)/[\w./-]+)`', read(a)))]
check('ADRs', '>= 1 ADR referencia arquivos do código', len(coderef) >= 1, f'{len(coderef)} ADRs com caminho real')

# Tracker
t = read('docs/TRACKER.md')
rows = [l for l in t.splitlines() if l.startswith('| ') and not l.startswith('| ID')]
fmt = '| ID | Documento | Tipo | Conteúdo (resumo) | Fonte | Localização |' in t
trv = cdv = 0
for l in rows:
    c = [x.strip() for x in l.strip('|').split('|')]
    loc = c[5].strip('`')
    m = re.fullmatch(r'\[(\d{2}:\d{2})\] ([A-Z][a-z]+)', loc)
    if c[4] == 'TRANSCRICAO' and m and (m.group(1), m.group(2)) in pairs:
        trv += 1
    if c[4] == 'CODIGO' and os.path.exists(loc):
        cdv += 1
check('Tracker', 'Formato de tabela obrigatório', fmt, 'cabeçalho exato')
check('Tracker', '>= 70% TRANSCRICAO com timestamp válido', trv / len(rows) >= 0.7, f'{trv}/{len(rows)} = {100 * trv / len(rows):.1f}%')
check('Tracker', '>= 5 linhas CODIGO com caminho real', cdv >= 5, f'{cdv} linhas')
tracked = set(c.split('|')[1].strip() for c in rows)
need = set(re.findall(r'^\| (PRD-(?:FR|NFR)-\d+)', p, re.M))
check('Tracker', '>= 80% dos itens identificáveis', len(need & tracked) / len(need) >= 0.8, f'FR/NFR do PRD: {len(need & tracked)}/{len(need)}; demais tabelas cobertas pelo gerador')

# README
rd = read('README.md')
miss = has(rd, 'Sobre o desafio', 'Ferramentas de IA', 'Workflow', 'Prompts customizados', 'Iterações e ajustes', 'Como navegar')
check('README', 'Seções obrigatórias do processo', not miss, f'faltando: {miss}' if miss else '6 seções')
check('README', '>= 2 prompts em blocos de código', rd.count('```') >= 4 and not miss, f'{rd.count("```") // 2} blocos de código')

# Consistência: caminhos citados
docs = ['docs/PRD.md', 'docs/RFC.md', 'docs/FDD.md'] + adrs
nonexist = []
for d in docs:
    for i, line in enumerate(read(d).splitlines(), 1):
        for x in re.findall(r'((?:src|prisma|tests)/[\w./-]*[\w/])', line):
            if not os.path.exists(x) and 'a criar' not in line.lower() and 'arquivos novos' not in line.lower():
                nonexist.append(f'{d}:{i} {x}')
check('Consistência', 'Nenhum arquivo de código citado é inexistente (salvo os marcados "a criar")', not nonexist, f'{len(nonexist)} ocorrências' if nonexist else '0 ocorrências')
links = []
for d in docs + ['docs/TRACKER.md', 'docs/adrs/README.md']:
    for link, anc in re.findall(r'\]\(([^)#\s]+\.md)(?:#([^)]+))?\)', read(d)):
        tgt = os.path.normpath(os.path.join(os.path.dirname(d), link))
        if not os.path.exists(tgt):
            links.append(f'{d} -> {link}')
        elif anc and anc not in [slug(h) for h in re.findall(r'^#+ (.+)$', read(tgt), re.M)]:
            links.append(f'{d} -> {link}#{anc}')
check('Consistência', 'Links e âncoras entre documentos válidos', not links, f'{len(links)} quebrados' if links else 'todos válidos')

for a, c, s, e in R:
    print(f'{s:5} | {a:12} | {c} | {e}')
print('---')
for x in nonexist:
    print('INEXISTENTE', x)
for x in links:
    print('LINK', x)
