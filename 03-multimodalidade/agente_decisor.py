import json
import os

def carregar_dados_ia():
    # Aqui simulamos a leitura do JSON que você acabou de gerar
    return {
        "lucro_liquido": 9812.0,
        "margem_bruta": 20.9,
        "inadimplencia_perc": 42.1, # Valor que a IA extraiu
        "data_referencia": "4Q23"
    }

def tomar_decisao(dados):
    print(f"🧐 Analisando dados de {dados['data_referencia']}...")
    
    decisao = ""
    # Lógica de Especialista
    if dados['lucro_liquido'] > 9000 and dados['inadimplencia_perc'] < 5.0:
        decisao = "🟢 COMPRA: Lucro acima da meta e risco controlado."
    elif dados['inadimplencia_perc'] > 10.0:
        decisao = "🔴 ALERTA CRÍTICO: Inadimplência muito alta! Revisar carteira de crédito."
    else:
        decisao = "🟡 NEUTRO: Aguardar próximos indicadores."
    
    return decisao

# Execução
dados_extraidos = carregar_dados_ia()
resultado = tomar_decisao(dados_extraidos)

print("\n--- VEREDITO DO AGENTE ---")
print(resultado)