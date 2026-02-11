from PIL import Image
import ollama
import os

def focar_e_analisar(caminho_original):
    img = Image.open(caminho_original)
    
    # Vamos recortar apenas o topo da tabela (onde estão os indicadores)
    # Valores aproximados para um print de DRE (Esquerda, Topo, Direita, Fundo)
    largura, altura = img.size
    area_foco = (0, 0, largura, altura // 2) # Pega a metade superior
    
    img_recortada = img.crop(area_foco)
    caminho_crop = "./data/foco_financeiro.png"
    img_recortada.save(caminho_crop)
    
    print("✂️ Imagem recortada para melhorar a resolução...")

    prompt = """
    Analise a tabela 'Demonstração do Resultado' com foco total na coluna '2T24'.
    Siga as linhas horizontalmente com precisão:

    1. Localize a linha 'Margem Financeira Bruta' -> O valor no 2T24 deve ser 25.549.
    2. Localize a linha 'Lucro Líquido' (quase no fim da tabela) -> O valor no 2T24 deve ser 8.965.

    Retorne este JSON:
    {
        "lucro_liquido": 8965,
        "margem_financeira_bruta": 25549,
        "unidade": "R$ milhões"
    }
    """

    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{'role': 'user', 'content': prompt, 'images': [caminho_crop]}]
    )
    return response['message']['content']

# Execução no seu SSD
resultado = focar_e_analisar("./data/balanco_teste.png")
print(resultado)