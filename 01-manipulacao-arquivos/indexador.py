import requests
import os
import json

def indexar_em_json(diretorio):
    arquivos = [f for f in os.listdir(diretorio) if f.endswith(('.md', '.txt'))]
    conhecimento = ""

    for nome in arquivos:
        with open(os.path.join(diretorio, nome), 'r', encoding='utf-8') as f:
            conhecimento += f"\nArquivo: {nome}\nConteúdo: {f.read()}\n"

    url = "http://localhost:11434/api/chat"
    
    # O Pulo do Gato: Instrução de Formato e parâmetro 'format': 'json'
    payload = {
        "model": "llama3.2:1b",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um parser de dados. Analise os documentos e retorne APENAS um JSON "
                    "no seguinte formato: {\"arquivos\": [{\"nome\": \"\", \"resumo\": \"\", \"tags\": []}]}"
                )
            },
            {"role": "user", "content": conhecimento}
        ],
        "format": "json", # Força o Ollama a estruturar a saída
        "stream": False
    }

    print("🤖 IA Gerando JSON estruturado...")
    response = requests.post(url, json=payload)
    return response.json()['message']['content']

if __name__ == "__main__":
    pasta = "/Volumes/Catunda_SSD/Developer/Documents"
    json_string = indexar_em_json(pasta)
    
    # Converter string em objeto Python e salvar bonito (indentado)
    dados_finais = json.loads(json_string)
    
    caminho_saida = os.path.join(pasta, "mapa_conhecimento.json")
    with open(caminho_saida, "w", encoding='utf-8') as f:
        json.dump(dados_finais, f, indent=4, ensure_ascii=False)
    
    print(f"🚀 JSON gerado com sucesso em: {caminho_saida}")