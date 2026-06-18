"""
FinBot — Assistente Financeiro para Iniciantes
Aplicação de linha de comando para demonstração do agente.
Para rodar: python app.py
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agente import construir_system_prompt

def main():
    try:
        import anthropic
    except ImportError:
        print("Instale o pacote anthropic: pip install anthropic")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("Configure a variável de ambiente ANTHROPIC_API_KEY com sua chave da API Anthropic.")
        return

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = construir_system_prompt()
    historico_mensagens = []

    print("\n" + "="*60)
    print("  FinBot — Seu Guia Financeiro para Iniciantes")
    print("="*60)
    print("  Digite 'sair' para encerrar | 'limpar' para nova conversa")
    print("="*60 + "\n")
    print("FinBot: Olá, João! Que bom te ver por aqui. 😊")
    print("       Sou o FinBot, seu guia financeiro pessoal.")
    print("       Posso te ajudar a entender seus gastos, acompanhar")
    print("       suas metas e explicar conceitos financeiros.")
    print("       Por onde quer começar?\n")

    while True:
        try:
            user_input = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nFinBot: Até logo! Cuide bem das suas finanças. 👋")
            break

        if not user_input:
            continue
        if user_input.lower() == "sair":
            print("FinBot: Até logo! Cuide bem das suas finanças. 👋")
            break
        if user_input.lower() == "limpar":
            historico_mensagens = []
            print("FinBot: Conversa reiniciada! Por onde quer começar?\n")
            continue

        historico_mensagens.append({"role": "user", "content": user_input})

        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=system_prompt,
                messages=historico_mensagens
            )
            resposta = response.content[0].text
            historico_mensagens.append({"role": "assistant", "content": resposta})
            print(f"\nFinBot: {resposta}\n")
        except Exception as e:
            print(f"\n[Erro ao chamar a API: {e}]\n")
            historico_mensagens.pop()

if __name__ == "__main__":
    main()
