import json
import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def carregar_perfil():
    with open(DATA_DIR / "perfil_investidor.json", "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_produtos():
    with open(DATA_DIR / "produtos_financeiros.json", "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_transacoes():
    transacoes = []
    with open(DATA_DIR / "transacoes.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transacoes.append(row)
    return transacoes

def carregar_historico():
    historico = []
    with open(DATA_DIR / "historico_atendimento.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            historico.append(row)
    return historico

def formatar_transacoes(transacoes):
    linhas = []
    totais = {}
    for t in transacoes:
        linhas.append(f"  - {t['data']}: {t['descricao']} ({t['categoria']}) - R$ {float(t['valor']):.2f} [{t['tipo']}]")
        if t['tipo'] == 'saida':
            cat = t['categoria']
            totais[cat] = totais.get(cat, 0) + float(t['valor'])
    
    resumo = "\nTOTAIS POR CATEGORIA (saídas):\n"
    for cat, val in sorted(totais.items(), key=lambda x: -x[1]):
        resumo += f"  - {cat}: R$ {val:.2f}\n"
    
    total_saidas = sum(totais.values())
    total_entradas = sum(float(t['valor']) for t in transacoes if t['tipo'] == 'entrada')
    resumo += f"  TOTAL saídas: R$ {total_saidas:.2f}\n"
    resumo += f"  TOTAL entradas: R$ {total_entradas:.2f}\n"
    resumo += f"  SALDO DO MÊS: R$ {total_entradas - total_saidas:.2f}\n"
    
    return "\n".join(linhas) + resumo

def formatar_historico(historico):
    linhas = []
    for h in historico:
        linhas.append(f"  - {h['data']} via {h['canal']}: tema '{h['tema']}' — {h['resumo']} (resolvido: {h['resolvido']})")
    return "\n".join(linhas)

def formatar_metas(perfil):
    linhas = []
    for meta in perfil.get("metas", []):
        linhas.append(f"  - {meta['meta']}: R$ {meta['valor_necessario']:.2f} até {meta['prazo']}")
    return "\n".join(linhas)

def formatar_produtos(produtos):
    linhas = []
    for p in produtos:
        linhas.append(
            f"  - {p['nome']} ({p['categoria']}): risco {p['risco']}, "
            f"rentabilidade {p['rentabilidade']}, "
            f"mínimo R$ {p['aporte_minimo']:.2f} — indicado para: {p['indicado_para']}"
        )
    return "\n".join(linhas)

def construir_system_prompt():
    perfil = carregar_perfil()
    transacoes = carregar_transacoes()
    historico = carregar_historico()
    produtos = carregar_produtos()

    reserva_atual = perfil.get("reserva_emergencia_atual", 0)
    meta_reserva = next((m for m in perfil.get("metas", []) if "reserva" in m["meta"].lower()), None)
    reserva_meta_val = meta_reserva["valor_necessario"] if meta_reserva else 0
    reserva_falta = max(0, reserva_meta_val - reserva_atual)

    contexto = f"""
<contexto_do_cliente>
PERFIL DO CLIENTE:
  - Nome: {perfil['nome']}
  - Idade: {perfil['idade']} anos
  - Profissão: {perfil['profissao']}
  - Renda Mensal: R$ {perfil['renda_mensal']:.2f}
  - Perfil de Investidor: {perfil['perfil_investidor']}
  - Aceita risco: {"Sim" if perfil.get('aceita_risco') else "Não"}
  - Objetivo Principal: {perfil['objetivo_principal']}
  - Patrimônio Total: R$ {perfil['patrimonio_total']:.2f}
  - Reserva de Emergência Atual: R$ {reserva_atual:.2f} (faltam R$ {reserva_falta:.2f} para a meta)

METAS FINANCEIRAS:
{formatar_metas(perfil)}

TRANSAÇÕES RECENTES:
{formatar_transacoes(transacoes)}

HISTÓRICO DE ATENDIMENTOS:
{formatar_historico(historico)}

PRODUTOS DISPONÍVEIS (apenas para fins educativos — não recomendar qual escolher):
{formatar_produtos(produtos)}
</contexto_do_cliente>
"""

    system_prompt = f"""Você é o FinBot, um assistente financeiro educativo e pessoal para iniciantes.

Seu objetivo é ajudar o cliente a entender suas finanças pessoais, seus hábitos de gasto e conceitos do mundo dos investimentos — sempre de forma clara, acolhedora e sem julgamentos.

{contexto}

REGRAS OBRIGATÓRIAS:
1. Baseie TODAS as suas respostas nos dados fornecidos no contexto acima. Nunca invente valores, datas ou informações financeiras.
2. NUNCA indique onde o cliente deve investir seu dinheiro. Você pode explicar como produtos funcionam, mas a decisão de investimento é sempre do cliente.
3. Se não tiver uma informação, diga claramente que não tem esse dado. Nunca invente.
4. Mantenha sempre o tom informal, acolhedor e educativo. Evite jargão financeiro sem explicação.
5. Quando usar um termo técnico (CDI, Selic, liquidez, rentabilidade), sempre explique brevemente o que significa.
6. Se a pergunta estiver fora do escopo de finanças pessoais, responda gentilmente que você é especializado em finanças.
7. Nunca mencione ou compartilhe dados de outros clientes.
8. Celebre conquistas e progresso financeiro do cliente.
9. Seja proativo: conecte dados com metas sempre que pertinente.
10. Responda sempre em português brasileiro.

Você é o amigo que estudou finanças e quer ajudar — não um gerente de banco tentando vender produto."""

    return system_prompt

