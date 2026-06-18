# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Personalizar a conversa com base em interações anteriores (ex: "você já perguntou sobre Tesouro Selic antes") |
| `perfil_investidor.json` | JSON | Contextualizar o perfil, metas e situação financeira atual do cliente |
| `produtos_financeiros.json` | JSON | Fornecer explicações educativas sobre os produtos disponíveis, sem recomendar qual escolher |
| `transacoes.csv` | CSV | Analisar padrões de gasto e calcular totais por categoria |

> [!TIP]
> Os dados são injetados diretamente no system prompt a cada sessão, garantindo que o agente sempre tenha o contexto completo do cliente — sem depender de memória externa ou banco de dados.

---

## Adaptações nos Dados

Os dados mockados foram mantidos essencialmente como fornecidos, com as seguintes interpretações para uso no agente:

- **perfil_investidor.json:** O campo `aceita_risco: false` é usado para calibrar o tom educativo — o agente usa linguagem mais cautelosa ao explicar produtos de maior risco.
- **transacoes.csv:** As categorias (`alimentacao`, `moradia`, `lazer`, `saude`, `transporte`) são usadas para gerar resumos de gasto por categoria de forma automática.
- **historico_atendimento.csv:** O campo `tema` é usado para que o agente reconheça assuntos que o cliente já explorou anteriormente, tornando a conversa mais fluida.
- **produtos_financeiros.json:** Usado apenas para **educação** — o agente explica características dos produtos, mas não recomenda qual o cliente deve escolher.

---

## Estratégia de Integração

### Como os dados são carregados?

No início de cada sessão, os arquivos JSON e CSV são lidos pelo backend Python e formatados como texto estruturado. Esse texto é inserido diretamente no **system prompt**, dentro de uma seção `<contexto_do_cliente>`. Assim, o LLM tem acesso a todos os dados do cliente desde a primeira mensagem.

### Como os dados são usados no prompt?

Os dados vão no **system prompt** como contexto estático da sessão. A cada mensagem do usuário, o LLM consulta esse contexto para formular respostas precisas e personalizadas. Não há consulta dinâmica a banco de dados — toda a informação relevante está no prompt.

---

## Exemplo de Contexto Montado

```
<contexto_do_cliente>
PERFIL DO CLIENTE:
- Nome: João Silva
- Idade: 32 anos
- Profissão: Analista de Sistemas
- Renda Mensal: R$ 5.000,00
- Perfil de Investidor: Moderado
- Aceita risco: Não
- Objetivo Principal: Construir reserva de emergência
- Patrimônio Total: R$ 15.000,00
- Reserva de Emergência Atual: R$ 10.000,00

METAS:
1. Completar reserva de emergência: precisa de R$ 15.000 até junho/2026 (faltam R$ 5.000)
2. Entrada do apartamento: precisa de R$ 50.000 até dezembro/2027

TRANSAÇÕES DE OUTUBRO/2025:
- Receita: R$ 5.000,00 (Salário)
- Moradia: R$ 1.380,00 (Aluguel R$1.200 + Luz R$180)
- Alimentação: R$ 570,00 (Supermercado R$450 + Restaurante R$120)
- Saúde: R$ 188,00 (Farmácia R$89 + Academia R$99)
- Transporte: R$ 295,00 (Uber R$45 + Combustível R$250)
- Lazer: R$ 55,90 (Netflix)
- Total de saídas: R$ 2.488,90
- Saldo do mês: R$ 2.511,10

HISTÓRICO DE ATENDIMENTOS RECENTES:
- 01/10: Perguntou sobre Tesouro Selic (resolvido via chat)
- 12/10: Acompanhou progresso da reserva de emergência (resolvido via chat)

PRODUTOS DISPONÍVEIS (apenas para fins educativos):
- Tesouro Selic: renda fixa, risco baixo, mínimo R$30, 100% da Selic
- CDB Liquidez Diária: renda fixa, risco baixo, mínimo R$100, 102% do CDI
- LCI/LCA: renda fixa, risco baixo, mínimo R$1.000, 95% do CDI (isento de IR, prazo 90 dias)
- Fundo Multimercado: fundo, risco médio, mínimo R$500, CDI+2%
- Fundo de Ações: fundo, risco alto, mínimo R$100, rentabilidade variável
</contexto_do_cliente>
```
