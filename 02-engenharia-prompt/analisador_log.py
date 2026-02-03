import requests
import json

def analisar_log(log_bruto):
    url = "http://localhost:11434/api/chat"
    
    # O "Few-Shot": Ensinamos a IA com exemplos antes da pergunta real
    prompt_sistema = (
    "Você é um parser de logs rigoroso. Analise o log e responda APENAS com JSON.\n"
    "Não adicione campos extras além dos exemplificados.\n"
    "Campos obrigatórios: 'nivel', 'servico', 'causa'.\n"
    "Exemplo: {\"nivel\": \"INFO\", \"servico\": \"Kernel\", \"causa\": \"Boot complete\"}"
)

    payload = {
        "model": "llama3.2:1b",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Analise este log: {log_bruto}"}
        ],
        "format": "json",
        "stream": False
    }

    print("🔍 Analisando log no Catunda_SSD...")
    response = requests.post(url, json=payload)
    return response.json()['message']['content']

if __name__ == "__main__":
    caminho_log = "/Volumes/Catunda_SSD/Developer/Documents/setup_infra_ia_2026.md"
    
    try:
        with open(caminho_log, "r", encoding='utf-8') as f:
            conteudo_real = f.read()
        
        # Vamos pegar apenas os últimos 500 caracteres para não estourar o prompt
        resultado = analisar_log(conteudo_real[-500:]) 
        
        print("\n--- Relatório Técnico do Setup (SSD) ---")
        print(resultado)
        
    except FileNotFoundError:
        print("❌ Arquivo não encontrado no Catunda_SSD. Verifique o caminho!")