import requests
import json

# Cores para o terminal
class Cores:
    HEADER = '\033[95m'
    INFO = '\033[94m'
    WARN = '\033[93m'
    DANGER = '\033[91m'
    END = '\033[0m'

def processar_alerta(insight_json):
    try:
        dados = json.loads(insight_json)
        
        # Normalizamos para maiúsculo para evitar erro de Case Sensitivity
        nivel = str(dados.get("nivel", "INFO")).upper()
        servico = dados.get("servico", "desconhecido")
        causa = dados.get("causa", "não identificada")

        print(f"\n{Cores.HEADER}--- MONITORAMENTO ATIVO (SSD) ---{Cores.END}")

        # Verificamos tanto em Inglês quanto em Português
        alertas_criticos = ["CRITICAL", "ERROR", "ERRO", "FALHA"]
        
        if nivel in alertas_criticos:
            print(f"{Cores.DANGER}[🚨 ALERTA CRÍTICO]{Cores.END} Falha em: {servico}")
            print(f"Ação sugerida: Reiniciar {servico} imediatamente. Causa: {causa}")
        
        elif nivel == "WARN" or nivel == "AVISO":
            print(f"{Cores.WARN}[⚠️ AVISO]{Cores.END} Comportamento anômalo em: {servico}")
            print(f"Observação: Verificar logs de {causa} em breve.")
        
        else:
            print(f"{Cores.INFO}[✅ STATUS OK]{Cores.END} {servico} operando normalmente.")
            print(f"Relatório: {causa}")

    except Exception as e:
        print(f"Erro ao processar insight: {e}")

def obter_insight_ia(texto):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3.2:1b",
        "messages": [
            {"role": "system", "content": "Você é um monitor de infra. Responda APENAS JSON com: nivel, servico, causa."},
            {"role": "user", "content": texto}
        ],
        "format": "json",
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json()['message']['content']

if __name__ == "__main__":
    # Simule aqui o log que você quer testar
    #log_teste = "CRITICAL FAILURE: SSD Storage at /Volumes/Catunda_SSD is not responding!"
    log_teste = "2026-02-03 19:45:00 ERROR: Database connection failed on Service-API due to invalid credentials"
    
    insight = obter_insight_ia(log_teste)
    processar_alerta(insight)