"""Valida docs/TRACKER.md: timestamps/falantes existentes na transcrição, caminhos de código existentes,
percentuais exigidos pelo desafio. Uso (na raiz do repo): python3 -I processo/scripts/validate_tracker.py
"""
import os
import re

tr = open('TRANSCRICAO.md', encoding='utf-8').read()
pairs = set(re.findall(r'^\[(\d{2}:\d{2})\] (\w+):', tr, re.M))
rows = [l for l in open('docs/TRACKER.md', encoding='utf-8').read().splitlines()
        if l.startswith('| ') and not l.startswith('| ID')]
tr_ok = cd_ok = 0
errors = []
for l in rows:
    c = [x.strip() for x in l.strip('|').split('|')]
    fonte, loc = c[4], c[5].strip('`')
    if fonte == 'TRANSCRICAO':
        m = re.fullmatch(r'\[(\d{2}:\d{2})\] ([A-Z][a-z]+)', loc)
        if m and (m.group(1), m.group(2)) in pairs:
            tr_ok += 1
        else:
            errors.append(f'timestamp inválido: {c[0]} {loc}')
    elif fonte == 'CODIGO':
        if os.path.exists(loc):
            cd_ok += 1
        else:
            errors.append(f'caminho inexistente: {c[0]} {loc}')
    else:
        errors.append(f'fonte inválida: {c[0]} {fonte}')
    if not os.path.exists(c[1].strip('`')):
        errors.append(f'documento inexistente: {c[0]} {c[1]}')
n = len(rows)
print(f'linhas: {n}')
print(f'TRANSCRICAO com timestamp válido: {tr_ok} ({100 * tr_ok / n:.1f}%)  [mínimo 70%]')
print(f'CODIGO com caminho real: {cd_ok}  [mínimo 5]')
print('erros:', len(errors))
for e in errors:
    print(' -', e)
raise SystemExit(1 if errors or tr_ok / n < 0.7 or cd_ok < 5 else 0)
