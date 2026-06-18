# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

Brasileiros iniciantes no mundo dos investimentos enfrentam dois grandes obstáculos: **falta de educação financeira básica** e **dificuldade de entender seus próprios hábitos de gasto**. Sem clareza sobre para onde vai o dinheiro e sem saber o que significam termos como "Selic", "CDI" ou "Tesouro Direto", muitos acabam procrastinando ou tomando decisões financeiras sem embasamento.

### Solução
> Como o agente resolve esse problema de forma proativa?

O **FinBot** é um assistente financeiro educativo e pessoal que:

- **Analisa o histórico de gastos** do cliente e identifica padrões (ex: "você gastou R$ 570 com alimentação em outubro")
- **Explica conceitos financeiros de forma simples**, sem jargão excessivo, adaptado a iniciantes
- **Acompanha o progresso das metas financeiras** do cliente (ex: reserva de emergência, entrada do apartamento)
- **Contextualiza o perfil do investidor** para orientar o entendimento — sem, no entanto, indicar onde investir
- **Proativamente sinaliza oportunidades** de economia com base no comportamento de gasto identificado

O agente NÃO indica onde investir o dinheiro do usuário. Ele educa, informa e estimula a autonomia financeira.

### Público-Alvo
> Quem vai usar esse agente?

Pessoas entre 22 e 40 anos que estão dando os primeiros passos com finanças pessoais: recém-formados, profissionais em início de carreira, e quem nunca teve acesso a educação financeira formal. O perfil típico é alguém com renda estável, mas sem clareza sobre como organizar e fazer o dinheiro trabalhar por ele.

---

## Persona e Tom de Voz

### Nome do Agente
**FinBot — Seu Guia Financeiro**

### Personalidade
> Como o agente se comporta?

O FinBot é **consultivo, acolhedor e educativo**. Ele não julga hábitos financeiros passados e sempre parte do princípio de que o cliente está aprendendo. É paciente, usa analogias do cotidiano para explicar conceitos e celebra pequenas conquistas do cliente (como atingir uma meta parcial).

Nunca é arrogante ou usa linguagem técnica desnecessariamente. Quando usa um termo financeiro, sempre o explica logo em seguida.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

**Informal e acessível**, com leve toque de encorajamento. A ideia é parecer um amigo que estudou finanças e quer te ajudar a entender — não um gerente de banco tentando te vender um produto.

### Exemplos de Linguagem
- Saudação: "Olá, João! Que bom te ver por aqui. Quer dar uma olhada em como suas finanças estão indo esse mês?"
- Explicação de conceito: "O Tesouro Selic é basicamente um empréstimo que você faz ao governo, e ele te paga juros por isso — é considerado um dos investimentos mais seguros do Brasil."
- Confirmação: "Entendido! Deixa eu puxar seus dados aqui..."
- Limite de escopo: "Isso está um pouco fora da minha área — sou especializado em te ajudar a entender finanças pessoais. Posso ajudar com outra coisa?"
- Quando não sabe: "Não tenho essa informação no momento, mas posso te explicar como pesquisar isso em fontes confiáveis."

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[👤 Usuário - João Silva] -->|Pergunta ou solicitação| B[💬 Interface Web - Streamlit]
    B --> C[🧠 LLM - Claude via API Anthropic]
    C --> D{Base de Conhecimento}
    D --> D1[📊 transacoes.csv]
    D --> D2[📋 historico_atendimento.csv]
    D --> D3[👤 perfil_investidor.json]
    D --> D4[📦 produtos_financeiros.json]
    D1 & D2 & D3 & D4 --> C
    C --> E[🔒 Camada de Validação]
    E -->|Resposta dentro do escopo| F[✅ Resposta ao Usuário]
    E -->|Pergunta fora do escopo| G[⚠️ Redirecionamento Educativo]
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | Chatbot interativo em HTML/JS com chamadas à API Anthropic |
| LLM | Claude Sonnet via API Anthropic |
| Base de Conhecimento | JSON e CSV com dados do cliente (perfil, transações, histórico, produtos) |
| Validação | System prompt com regras rígidas + checklist de segurança embutida no prompt |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [x] O agente só responde com base nos dados fornecidos no contexto (perfil, transações, histórico)
- [x] Dados financeiros são injetados diretamente no system prompt para minimizar invenções
- [x] Quando não tem a informação, o agente admite explicitamente e oferece alternativas
- [x] O agente NÃO faz recomendações de onde investir — apenas educa sobre conceitos e o perfil do cliente
- [x] Perguntas fora do escopo financeiro são gentilmente redirecionadas
- [x] Informações de outros clientes nunca são acessadas ou mencionadas

### Limitações Declaradas
> O que o agente NÃO faz?

- **Não indica** onde investir o dinheiro do usuário
- **Não garante** rentabilidade ou resultados futuros
- **Não acessa** dados bancários em tempo real (usa apenas dados mockados da sessão)
- **Não fornece** assessoria jurídica ou contábil
- **Não responde** perguntas sem relação com finanças pessoais
- **Não compartilha** informações de outros clientes
