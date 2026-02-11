import ollama

def extrair_dados_nitidos(caminho):
    print(f"🧐 Analisando 2T24 em Alta Resolução...")
    
    prompt = """
    Identifique a tabela 'Demonstração do Resultado'. 
    Extraia os valores da coluna '2T24' (a primeira coluna de dados da esquerda para a direita).
    
    Retorne este JSON:
    {
        "lucro_liquido_contabil": 8965,
        "lucro_liquido_ajustado": 9502,
        "margem_financeira_bruta": 25549,
        "rspl_ajustado_percent": 21.6
    }
    Responda APENAS o objeto JSON acima, sem explicações.
    """

    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{'role': 'user', 'content': prompt, 'images': [caminho]}]
    )
    return response['message']['content']

# Verifique se o nome do arquivo no SSD é este mesmo:
caminho_imagem = "./data/balanco_teste.png"
print(extrair_dados_nitidos(caminho_imagem))