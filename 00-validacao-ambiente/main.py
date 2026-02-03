import requests

def verificar_ia_local():
    print("🤖 Verificando integridade do setup no Catunda_SSD...")
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:1b",
        "prompt": "Responda apenas: Sistema Operacional de IA 2026 Online.",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            msg = response.json().get('response')
            print(f"✅ SUCESSO! Resposta da IA: {msg}")
        else:
            print("⚠️ O Ollama respondeu, mas com erro. Verifique se o modelo foi baixado.")
    except Exception as e:
        print("❌ ERRO: O servidor Ollama não foi encontrado.")
        print("👉 Lembre-se de rodar 'ollama-ssd' em outra aba do terminal!")

if __name__ == "__main__":
    verificar_ia_local()