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
    Analise APENAS os números desta tabela recortada.
    Localize a coluna '4Q23' e me dê:
    - O valor exato de 'Inadimplência > 90d'.
    - O valor exato de 'Lucro Líquido'.
    Responda apenas o JSON.
    """

    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{'role': 'user', 'content': prompt, 'images': [caminho_crop]}]
    )
    return response['message']['content']

# Execução no seu SSD
resultado = focar_e_analisar("./data/balanco_teste.png")
print(resultado)