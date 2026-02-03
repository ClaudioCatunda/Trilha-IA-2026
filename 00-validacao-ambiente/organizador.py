import requests

def organizar_ideias(texto_bruto):
    url = "http://localhost:11434/api/chat" # Mudamos para /api/chat que é mais moderno
    
    payload = {
        "model": "llama3.2:1b",
        "messages": [
            {
                "role": "system", 
                "content": "Você é um assistente sênior focado em produtividade. Sua tarefa é transformar textos bagunçados em uma lista de tópicos limpa e profissional."
            },
            {
                "role": "user", 
                "content": f"Organize isso para mim: {texto_bruto}"
            }
        ],
        "stream": False
    }

    response = requests.post(url, json=payload)
    return response.json()['message']['content']

# Teste com uma ideia qualquer
ideia = "Preciso comprar leite, mas também tenho que terminar o relatório do SSD e não posso esquecer de configurar o Git no Mac Mini."
print(organizar_ideias(ideia))