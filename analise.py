import pandas as pd
from LeIA.leia import SentimentIntensityAnalyzer

# Carrega os textos já limpos
df = pd.read_csv("resultados_limpos.csv")

# Cria o analisador de sentimentos
analyzer = SentimentIntensityAnalyzer()

# Lista para guardar os resultados
sentimentos = []

# Analisa cada comentário
for comentario in df["texto_do_comentario"]:
    score = analyzer.polarity_scores(str(comentario))
    
    if score["compound"] >= 0.05:
        sentimentos.append("POSITIVO")
    elif score["compound"] <= -0.05:
        sentimentos.append("NEGATIVO")
    else:
        sentimentos.append("NEUTRO")

# Cria uma nova coluna com o resultado
df["sentimento"] = sentimentos

# Salva em um novo CSV
df.to_csv("resultados_com_sentimento.csv", index=False, encoding="utf-8")

print("✅ Análise de sentimentos concluída! Arquivo salvo como resultados_com_sentimento.csv")
