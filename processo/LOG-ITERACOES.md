# Log de Iterações

Registre aqui cada correção relevante feita sobre o que a IA gerou. Vira a seção
"Iterações e ajustes" do README.

| # | Fase | O que a IA gerou de errado/superficial | Como detectei | Correção (prompt ou edição) |
|---|------|----------------------------------------|---------------|-----------------------------|
| 1 | 0 | O inventário citava `src/worker.ts` e `src/modules/webhooks/` ao lado de arquivos reais, o que poderia levar o Tracker a marcá-los como Fonte = CODIGO, mas eles ainda não existem | Script de validação (regex de timestamps/falantes + `os.path.exists` nos caminhos) apontou 3 caminhos inexistentes; os 237 timestamps estavam válidos | Nota no topo do INVENTARIO: arquivos propostos na reunião têm origem TRANSCRICAO, nunca CODIGO |
| 2 | 1 | ADR-002 e ADR-006 citavam `src/worker.ts` e `src/modules/webhooks/` como caminhos comuns; um avaliador poderia ler como arquivo inexistente no repositório (critério "nenhum arquivo citado é inexistente") | Script de validação dos ADRs (seções obrigatórias, timestamps, `os.path.exists`, links relativos) apontou os 2 caminhos | Marcados como "(a criar)" no texto dos ADRs |
| 3 | 1 | Pontos ambíguos da reunião (nº de tentativas, granularidade da outbox, evento na criação do pedido) poderiam virar decisão "fechada" sem origem | Cruzamento com a tabela de Ambiguidades do INVENTARIO (AMB-01, AMB-03, AMB-04) | Registrados nos ADRs 003, 005 e 007 como blocos "Proposta de design (AMB-xx), pendente de confirmação" |
