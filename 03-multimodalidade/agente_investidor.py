import json

# Simulando os dados que sua IA extraiu com o Crop
dados_ia = {
    "inadimplencia": 17.38,
    "lucro_liquido": 32708,
    "trimestre": "4Q23"
}

def analisar_saude_financeira(dados):
    print(f"📊 Relatório de Análise - {dados['trimestre']}")
    print("-" * 30)
    
    # Regras de Negócio (Hardcoded por enquanto, depois faremos dinâmico)
    LIMITE_INADIMPLENCIA = 5.0
    META_LUCRO = 30000

    alertas = []
    
    if dados['inadimplencia'] > LIMITE_INADIMPLENCIA:
        alertas.append(f"⚠️ RISCO: Inadimplência de {dados['inadimplencia']}% está acima do limite de {LIMITE_INADIMPLENCIA}%!")
    
    if dados['lucro_liquido'] >= META_LUCRO:
        print(f"✅ PERFORMANCE: Lucro de {dados['lucro_liquido']} superou a meta!")
    else:
        alertas.append("❌ PERFORMANCE: Lucro abaixo do esperado.")

    if not alertas:
        return "💎 VEREDITO: Empresa sólida. Sugestão: MANTER/COMPRAR."
    else:
        print("\n".join(alertas))
        return "🚨 VEREDITO: Atenção redobrada. Sugestão: AGUARDAR."

# Execução
veredito = analisar_saude_financeira(dados_ia)
print(f"\n{veredito}")

# Salvando o log no seu SSD
with open("./data/log_decisao.txt", "a") as f:
    f.write(f"Trimestre: {dados_ia['trimestre']} - Veredito: {veredito}\n")