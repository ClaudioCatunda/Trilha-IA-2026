import requests
import json
import os
import glob

# --- CONFIGURAÇÕES ---
# O M4 lida com o 8b com extrema facilidade
MODELO_PRODUCAO = "llama3.1:8b" 
URL_OLLAMA = "http://localhost:11434/api/chat"
CAMINHO_SSD = "/Volumes/Catunda_SSD/Developer"
ARQUIVO_SOLUCOES = f"{CAMINHO_SSD}/Documents/SOLUCOES_TECNICAS.md"
# PASTA_KB = f"{CAMINHO_SSD}/Knowledge_Base"
# Para (Caminho Relativo):
PASTA_KB = "Knowledge_Base"

def chamar_ollama(prompt, system_prompt, output_json=False):
    payload = {
        "model": MODELO_PRODUCAO,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    
    if output_json:
        payload["format"] = "json"

    try:
        response = requests.post(URL_OLLAMA, json=payload)
        response.raise_for_status()
        return response.json()['message']['content']
    except Exception as e:
        return f"Erro ao chamar Ollama: {e}"

def orquestrador_de_correcao(log_texto):
    # 1. DEFINIÇÃO DE VARIÁVEIS (Evita NameError)
    servico = "Desconhecido"
    problema = "Não identificado"
    conteudo_extra = ""

    # --- PASSO 1: ANÁLISE (Agente Analista) ---
    print(f"🔍 Analisando log com {MODELO_PRODUCAO}...")

    system_analise = (
        "Você é um especialista em logs. "
        "Sua saída deve ser EXCLUSIVAMENTE um objeto JSON válido. "
        "Não escreva nada antes ou depois do JSON. "
        "Estrutura: {\"servico\": \"nome_do_servico\", \"problema\": \"resumo_do_erro\"}"
    )
    
    resposta_analista = chamar_ollama(log_texto, system_analise, output_json=True)
    print(f"DEBUG Resposta: {resposta_analista}") # Adicione esta linha temporariamente

    try:
        dados = json.loads(resposta_analista)
        # Busca resiliente (Português/Inglês)
        servico = dados.get('servico', dados.get('service', servico))
        problema = dados.get('problema', dados.get('problem', problema))
    except Exception as e:
        print(f"⚠️ Falha no parsing do JSON: {e}. Usando valores padrão.")

# --- PASSO 2: RAG (Busca no SSD) ---
    print(f"📚 Consultando base de conhecimento para: {servico}...")
    
    arquivos_kb = glob.glob(f"{PASTA_KB}/*.txt")
    for caminho_arq in arquivos_kb:
        # Simplificamos a busca: se 'postgres' estiver no nome do arquivo, ele lê
        termo_busca = servico.lower().replace("sql", "").strip() 
        if termo_busca in caminho_arq.lower():
            print(f"✅ DOCUMENTO ENCONTRADO: {os.path.basename(caminho_arq)}")
            with open(caminho_arq, 'r', encoding='utf-8') as f:
                conteudo_extra += f"\n--- INSTRUÇÕES OBRIGATÓRIAS DO USUÁRIO ---\n{f.read()}\n"

    # --- PASSO 3: SOLUÇÃO (Agente Arquiteto) ---
    # Se encontramos algo no manual, usamos um System Prompt muito mais agressivo
    if conteudo_extra:
        system_solucao = (
            "Você é um Arquiteto Sênior. Você recebeu INSTRUÇÕES OBRIGATÓRIAS. "
            "Ignore qualquer solução padrão se ela contradizer o MANUAL DO USUÁRIO. "
            "Você DEVE mencionar o tempo de espera e os scripts citados no manual."
        )
    else:
        system_solucao = "Você é um Arquiteto de Software Sênior especializado em infraestrutura."

    prompt_solucao = (
        f"LOG DE ERRO: {log_texto}\n"
        f"BASE DE CONHECIMENTO DISPONÍVEL: {conteudo_extra if conteudo_extra else 'Nenhuma instrução específica.'}\n\n"
        "TAREFA: Gere um guia de correção. Se houver instruções obrigatórias acima, "
        "priorize-as sobre o seu conhecimento geral."
    )

    system_solucao = "Você é um Arquiteto de Software Sênior especializado em infraestrutura resiliente."
    
    solucao_markdown = chamar_ollama(prompt_solucao, system_solucao)

    # --- PASSO 4: PERSISTÊNCIA NO SSD ---
    with open(ARQUIVO_SOLUCOES, "a", encoding="utf-8") as f:
        f.write(f"\n\n# 🚨 Incidente: {servico}\n")
        f.write(f"**Problema Identificado:** {problema}\n")
        f.write(f"**Guia de Correção:**\n\n{solucao_markdown}\n")
        f.write("\n" + "="*40 + "\n")
    
    print(f"✅ Relatório salvo com sucesso no Catunda_SSD!")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    # Teste com o log do Postgres para validar o RAG manual
    log_bruto = "2026-02-04 20:00:00 [ERROR] PostgreSQL FATAL: database system is starting up"
    orquestrador_de_correcao(log_bruto)