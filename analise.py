import pandas as pd
from LeIA.leia import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt # Importação necessária para o gráfico

# --- Configurações de Arquivo ---
# O seu script de limpeza deve ter gerado este arquivo
ARQUIVO_ENTRADA = "resultadosg1_limpos.csv" # Nome de exemplo! CONFIRA o nome exato do seu CSV limpo
ARQUIVO_SAIDA_ANALISE = "resultados_com_sentimento_g1.csv"
# --------------------------------

try:
    # 1. Carrega os textos já limpos
    df = pd.read_csv(ARQUIVO_ENTRADA)

    # 2. Análise de Sentimento com LeIA
    analyzer = SentimentIntensityAnalyzer()
    sentimentos = []

    for comentario in df["comentario"]: # Coluna 'comentario' conforme conversamos
        score = analyzer.polarity_scores(str(comentario))
        
        if score["compound"] >= 0.05:
            sentimentos.append("POSITIVO")
        elif score["compound"] <= -0.05:
            sentimentos.append("NEGATIVO")
        else:
            sentimentos.append("NEUTRO")

    df["sentimento"] = sentimentos

    # Salva o CSV com a nova coluna 'sentimento'
    df.to_csv(ARQUIVO_SAIDA_ANALISE, index=False, encoding="utf-8")
    print(f"✅ Análise de sentimentos concluída! Arquivo salvo como {ARQUIVO_SAIDA_ANALISE}")

    # ----------------------------------------------------
    # 3. Geração do Gráfico (Análise Gráfica)
    # ----------------------------------------------------
    
    # Contagem dos sentimentos (inclui NaN por segurança, mas não deve aparecer)
    contagem = df["sentimento"].value_counts(dropna=False)
    
    # Mapeamento de cores garantido para POSITIVO, NEGATIVO, NEUTRO
    cores_map = {
        'POSITIVO': 'green',
        'NEGATIVO': 'red',
        'NEUTRO': 'blue',
        float('nan'): 'gray' # Para qualquer valor nulo
    }
    
    # Obtém a lista de cores na ordem dos sentimentos contados
    cores_barras = [cores_map.get(s, 'gray') for s in contagem.index] 

    plt.figure(figsize=(8, 6))
    plt.bar(contagem.index, contagem.values, color=cores_barras)
    plt.xlabel("Sentimento")
    plt.ylabel("Quantidade")
    plt.title("Análise de Sentimentos dos Comentários do Portal @g1")

    # Adiciona os rótulos de quantidade em cima das barras
    for i, valor in enumerate(contagem.values):
        plt.text(i, valor + 0.5, str(valor), ha='center', va='bottom')

    # Salva o gráfico
    plt.savefig("analise_sentimentos.png")

    plt.close()
    print("✅ Gráfico de análise de sentimentos salvo como analise_sentimentos.png")

except KeyError as e:
    print(f"❌ ERRO DE COLUNA: A coluna {e} não foi encontrada. Verifique o seu script de limpeza.")
except FileNotFoundError:
    print(f"❌ ERRO DE ARQUIVO: O arquivo de entrada '{ARQUIVO_ENTRADA}' não foi encontrado. Execute o script de limpeza (limpeza.py) primeiro.")
except Exception as e:
    print(f"❌ Ocorreu um erro inesperado: {e}")