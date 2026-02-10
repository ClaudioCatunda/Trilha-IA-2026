import ollama

def auditoria_detalhada(caminho):
    print("🎯 Focando nos indicadores-chave da tabela...")
    
    # Prompt de localização espacial
    prompt_tecnico = """
    AJA COMO UM AUDITOR DE DADOS. 
    Nesta imagem, localize a tabela 'DRE Sintética' e a coluna '4Q23'.
    
    EXTRAIA OS VALORES EXATOS PARA:
    1. Lucro Líquido (Geralmente a primeira ou última linha do bloco de lucro).
    2. Margem Financeira Bruta.
    3. Índice de Inadimplência > 90 dias (Busque pelo símbolo %).

    REGRAS:
    - Se o valor tiver parênteses ex: (100), retorne como número negativo: -100.
    - Se houver ponto como separador de milhar, ignore-o e use apenas para decimais.
    
    FORMATO DE SAÍDA:
    {
        "lucro_liquido": 0.0,
        "margem_bruta": 0.0,
        "inadimplencia_perc": 0.0,
        "data_referencia": "4Q23"
    }
    """

    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{'role': 'user', 'content': prompt_tecnico, 'images': [caminho]}]
    )
    return response['message']['content']

print(auditoria_detalhada("./data/balanco_teste.png"))
