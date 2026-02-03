import requests
import json
import os

def chamar_ollama(prompt, system_prompt, output_json=False):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3.2:1b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    if output_json:
        payload["format"] = "json"
        
    response = requests.post(url, json=payload)
    return response.json()['message']['content']

def orquestrador_de_correcao(log_texto):
    # --- PASSO 1: ANÁLISE (Agente Analista) ---
    print("🧠 Agente Analista: Decompondo o erro...")
    prompt_analise = f"Analise este log e extraia o erro e o servico: {log_texto}"
    system_analise = (
    "Você é um parser. Responda APENAS JSON puro. "
    "Não use explicações. Se houver aspas no texto, ignore-as. "
    "Estrutura: {\"problema\": \"...\", \"servico\": \"...\"}"
)
    resposta_analista = chamar_ollama(prompt_analise, system_analise, output_json=True)
    
    try:
        dados = json.loads(resposta_analista)
    except json.JSONDecodeError:
        dados = {"problema": "Erro desconhecido", "servico": "Sistema"}

    servico = dados.get('servico', dados.get('service', 'Serviço Indefinido'))
    problema = dados.get('problema', 'Problema não identificado')

    # --- PASSO 2: SOLUÇÃO (Agente Arquiteto) ---
    print(f"🛠️ Agente Arquiteto: Projetando solução para {servico}...")
    prompt_solucao = (
        f"O serviço {servico} apresentou o problema: {problema}. "
        "Como engenheiro sênior, escreva um guia rápido em Markdown de como resolver isso."
    )
    system_solucao = "Você é um arquiteto de infraestrutura experiente. Responda em Markdown."
    
    solucao_markdown = chamar_ollama(prompt_solucao, system_solucao)

    # --- PASSO 3: PERSISTÊNCIA (Onde estava faltando!) ---
    diretorio = "/Volumes/Catunda_SSD/Developer/Documents"
    caminho_solucoes = os.path.join(diretorio, "SOLUCOES_TECNICAS.md")

    # Garante que a pasta existe no SSD
    os.makedirs(diretorio, exist_ok=True)

def limpar_json(texto):
    # Remove possíveis blocos de código markdown que a IA insiste em colocar
    texto = texto.replace("```json", "").replace("```", "").strip()
    return texto
    
    try:
        with open(caminho_solucoes, "a", encoding='utf-8') as f:
            f.write(f"\n\n# 🚨 Incidente: {servico}\n")
            f.write(f"**Problema Identificado:** {problema}\n")
            f.write(f"**Guia de Correção:**\n\n{solucao_markdown}\n")
            f.write("\n" + "="*40 + "\n")
        print(f"✅ Sucesso! Solução imortalizada em: {caminho_solucoes}")
    except Exception as e:
        print(f"❌ Erro ao gravar no SSD: {e}")

if __name__ == "__main__":
    #log_bruto = "FATAL: database system is starting up - Connection refused on PostgreSQL port 5432"
    log_bruto = "CRITICAL: Kubernetes Pod 'nginx-proxy-01' is stuck in CrashLoopBackOff due to Liveness probe failure"
    orquestrador_de_correcao(log_bruto)