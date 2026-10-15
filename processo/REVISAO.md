# Revisão Cruzada — Fase 6

Este relatório revisa o pacote `docs/` contra o checklist de critérios de aceite do enunciado original
(`git show e7f6311:README.md`) e contra a tabela de Armadilhas do [`PLANO.md`](PLANO.md). Os achados foram
apenas **listados**. As correções dependem da decisão do revisor humano e são feitas em commits seguintes
nesta mesma branch.

**Método:**
1. Checagem mecânica com [`scripts/check_acceptance.py`](scripts/check_acceptance.py): seções, contagens,
   timestamps, caminhos e links.
2. Leitura dirigida para encontrar contradições com a transcrição, divergências entre documentos e
   duplicação de conteúdo.

## 1. Checklist do enunciado

| Área | Critério | Status | Evidência |
|---|---|---|---|
| PRD | Arquivo existe e contém as seções obrigatórias | **OK** | 13 seções encontradas |
| PRD | >= 8 requisitos funcionais | **OK** | 15 PRD-FR |
| PRD | >= 1 objetivo com métrica e meta quantitativa | **OK** | 4 objetivos com meta numérica |
| PRD | Fora de escopo com >= 2 itens descartados/adiados na reunião | **OK** | 7 itens com timestamp |
| PRD | >= 2 riscos com probabilidade, impacto e mitigação | **OK** | 6 riscos |
| RFC | Seções obrigatórias + metadados com participantes como revisores | **OK** | metadados e 7 seções |
| RFC | >= 2 alternativas descartadas com trade-off | **OK** | 7 alternativas |
| RFC | >= 2 questões em aberto | **OK** | 7 questões |
| RFC | Referencia com link >= 2 ADRs | **OK** | 7 ADRs linkados |
| RFC | Conciso (2 a 4 páginas) | **OK** | 1885 palavras |
| FDD | Seções obrigatórias | **OK** | 12 seções |
| FDD | >= 4 endpoints com request, response e status codes | **OK** | 7 endpoints completos |
| FDD | Matriz de erros com prefixo WEBHOOK_ | **OK** | 14 códigos, todos WEBHOOK_ |
| FDD | Integração referencia >= 4 caminhos reais | **OK** | 21 caminhos reais |
| FDD | Observabilidade cita métricas, logs e tracing | **OK** | métricas, logs e tracing presentes |
| ADRs | Entre 5 e 8 arquivos ADR-NNN-kebab-case.md | **OK** | 7 arquivos, nomes ok |
| ADRs | Cada ADR com Status, Contexto, Decisão, Alternativas, Consequências | **OK** | todos completos |
| ADRs | Cobre >= 5 das 6 decisões principais | **OK** | 6/6: Outbox, Retry/DLQ, HMAC, at-least-once, Worker polling, Reuso de padrões |
| ADRs | >= 1 ADR referencia arquivos do código | **OK** | 6 ADRs com caminho real |
| Tracker | Formato de tabela obrigatório | **OK** | cabeçalho exato |
| Tracker | >= 70% TRANSCRICAO com timestamp válido | **OK** | 247/289 = 85.5% |
| Tracker | >= 5 linhas CODIGO com caminho real | **OK** | 42 linhas |
| Tracker | >= 80% dos itens identificáveis | **OK** | FR/NFR do PRD: 26/26; demais tabelas cobertas pelo gerador |
| README | Seções obrigatórias do processo | **FALHA** | faltando: ['Sobre o desafio', 'Ferramentas de IA', 'Workflow', 'Prompts customizados', 'Iterações e ajustes', 'Como navegar'] |
| README | >= 2 prompts em blocos de código | **FALHA** | 1 blocos de código |
| Consistência | Nenhum arquivo de código citado é inexistente (salvo os marcados "a criar") | **FALHA** | 8 ocorrências |
| Consistência | Links e âncoras entre documentos válidos | **OK** | todos válidos |
| Consistência | Nenhum requisito, decisão ou restrição contradiz a transcrição ou o código | **OK com ressalvas** | Nenhuma contradição com a transcrição. Há uma divergência **entre documentos** sobre o retry (achado A1) |

O script tinha um falso positivo no RFC: o separador `|---|` da tabela de metadados era lido como fim de seção.
Ele foi corrigido antes desta execução.

## 2. Achados

| # | Severidade | Tipo | Onde | Achado | Sugestão |
|---|---|---|---|---|---|
| A1 | **Alta** | Divergência entre documentos | `docs/adrs/ADR-003-retry-backoff-e-dlq.md:14-16`, `docs/RFC.md:17` (TL;DR), `docs/RFC.md:61`, `docs/PRD.md:100` (PRD-FR-10) | O FDD §5.3 (iteração 13) passou a mandar falhas **não transitórias** direto para a DLQ: 3xx/4xx exceto 408 e 429, payload acima de 64 KB, endpoint inativo, sem secret. ADR-003, RFC e PRD ainda dizem que toda falha é retentada até a DLQ. | Acrescentar no ADR-003 um item "falhas definitivas vão direto para a DLQ (ver FDD §5.3)" e ajustar a frase do TL;DR, o item 4 da proposta do RFC e o PRD-FR-10 ("falhas transitórias são retentadas"). |
| A2 | Média | Duplicação | `docs/FDD.md:44-55` × `docs/PRD.md:74` (§5.2) | O FDD §3 repete 6 dos 8 itens "fora de escopo" do PRD (inbound, email, dashboard, rate limiting, arquivamento, criação do pedido). O enunciado aponta duplicação como sinal de conteúdo no lugar errado. | Deixar no FDD só as exclusões **técnicas** (múltiplos workers, listagem da DLQ, evento na criação) e trocar o restante por um link para o PRD §5.2. |
| A3 | Baixa | Redação ambígua | `docs/adrs/ADR-003-retry-backoff-e-dlq.md:14` | O item 1 diz "Backoff exponencial com **5 tentativas**". O bloco AMB-01, logo abaixo, define 1 envio + 5 retentativas. Quem ler só o item 1 pode entender 5 envios. | Trocar por "**5 retentativas** após o envio inicial". |
| A4 | Baixa | Caminho inexistente sem marca na linha | `docs/FDD.md:196` (diagrama), `docs/FDD.md:611` (script `package.json`), `docs/FDD.md:616-620` (lista abaixo de "Arquivos novos *(a criar)*"), `docs/adrs/ADR-002-worker-separado-em-polling.md:48` (Referências) | São 8 ocorrências de `src/worker.ts` e `src/modules/webhooks/*`. Todas estão em contexto que diz "a criar", mas não na própria linha. Um avaliador que procure linha a linha pode ler como arquivo inexistente (critério "Nenhum arquivo de código mencionado é inexistente"). | Acrescentar "(a criar)" nas linhas 196 e 611 do FDD e na linha 48 do ADR-002. A lista 616–620 já fica sob o título "a criar". Opcional: repetir a marca em cada item. |
| A5 | **Alta (pendente de fase)** | Critério não atendido | `README.md` | O README ainda é o enunciado original: as 6 seções do processo e os prompts não existem. | Fase 7 (já planejada). |
| A6 | Baixa | Processo | `docs/TRACKER.md` | Corrigir A1–A4 altera textos que o Tracker resume. | Rodar `processo/scripts/gen_tracker.py` e `validate_tracker.py` de novo depois das correções. |

## 3. Verificações sem achado

- **Armadilhas do PLANO:** nenhuma aparece como requisito.
  - `customer_id` vem do body ou do path, nunca do JWT (FDD §6).
  - O payload não tem `items`.
  - Email, dashboard, rate limiting e inbound estão só como fora de escopo ou questão em aberto.
  - Filtro e snapshot acontecem na inserção.
  - Os IDs são UUID.
  - O replay é restrito a ADMIN, e o CRUD a usuário autenticado.
- **Decisões da revisão humana:**
  - R1–R3 (RFC §5.1) estão refletidas nos ADRs 003, 005 e 007.
  - O HMAC assina só o corpo, e o timestamp ficou como Q7.
  - A listagem da DLQ ficou como Q6.
  - Nenhum resquício de "pendente de confirmação" ou de "Q6–Q8" antigos.
- **Duplicações aceitáveis:**
  - RFC §4 × alternativas dos ADRs: o RFC resume, com o trade-off que o enunciado exige, e linka o ADR.
  - PRD §8 × ADRs: uma linha por decisão, com link.
  - RFC §3.3 × FDD §8: a garantia de ordem é a mesma nos dois, e o FDD detalha a limitação.
- **Links e âncoras:** todos válidos entre PRD, RFC, FDD, Tracker e ADRs.
- **Código intocado:** `git diff --stat e7f6311 -- src prisma tests TRANSCRICAO.md` está vazio.

## 4. Decisão do revisor e resultado

**Decisão:** corrigir A1–A4 e regenerar o Tracker (A6). A5 fica para a Fase 7.

| # | Correção aplicada |
|---|---|
| A1 | ADR-003 ganhou o item "falhas definitivas vão direto para a DLQ", com link para o FDD §5.3. O TL;DR e o item 4 da proposta do RFC agora distinguem falha transitória de definitiva. O PRD-FR-10 foi reescrito no mesmo sentido. |
| A2 | O FDD §3 ficou só com as exclusões técnicas (múltiplos workers, evento na criação, listagem da DLQ) e um link para o PRD §5.2. |
| A3 | ADR-003 item 1: "5 retentativas após o envio inicial". |
| A4 | Marca "(a criar)" no diagrama e no script do FDD, em cada item da lista de arquivos novos e na referência do ADR-002. |
| A6 | Tracker regenerado: 284 linhas, 85,2% TRANSCRICAO, 42 CODIGO, 0 erros. A remoção de linhas duplicadas mudou o ID do item "evento na criação". Em vez de uma exceção no gerador, o timestamp ([09:40] Bruno) foi colocado no próprio FDD. |

**Checagem depois das correções:** 25 de 27 critérios OK. As 2 falhas restantes são do README (Fase 7). Nenhum caminho inexistente sem marca e nenhum link quebrado.
