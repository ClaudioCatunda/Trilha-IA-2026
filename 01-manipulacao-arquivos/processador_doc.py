import requests
import os

def processar_documento(caminho_arquivo):
    # 1. Verificar se o arquivo existe antes de tentar ler
    if not os.path.exists(caminho_arquivo):
        print(f"❌ Erro: O arquivo não foi encontrado em: {caminho_arquivo}")
        return

    # 2. Ler o conteúdo do log de setup no SSD
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    print(f"📄 Arquivo lido com sucesso ({len(conteudo)} caracteres).")

    # 3. Configuração da requisição para o Ollama
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3.2:1b",
        "messages": [
            {
                "role": "system",
                "content": "Você é um especialista em infraestrutura de TI. Resuma o setup realizado em 3 tópicos técnicos e diretos."
            },
            {
                "role": "user", 
                "content": f"Aqui está o log do meu setup, resuma-o para mim: \n\n{conteudo}"
            }
        ],
        "stream": False
    }

    try:
        print("🤖 IA processando no Catunda_SSD (Llama 3.2:1b)...")
        response = requests.post(url, json=payload)
        response.raise_for_status() # Garante que erros de conexão sejam avisados
        
        resumo = response.json()['message']['content']

        # 4. Gravar o resultado de volta no final do arquivo (Modo 'a' de append)
        with open(caminho_arquivo, 'a', encoding='utf-8') as f:
            f.write("\n\n---\n")
            f.write("### 📝 Resumo Executivo (Gerado via Python + Ollama)\n")
            f.write(resumo)
            f.write("\n")
        
        print("✅ Sucesso! O resumo foi adicionado ao final do seu documento no SSD.")

    except Exception as e:
        print(f"❌ Erro na comunicação com a IA: {e}")

if __name__ == "__main__":
    # Caminho exato para o seu arquivo de documentação no SSD
    caminho_do_log = "/Volumes/Catunda_SSD/Developer/Documents/setup_infra_ia_2026.md"
    processar_documento(caminho_do_log)