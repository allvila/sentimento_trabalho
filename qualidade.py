import pandas as pd
import matplotlib.pyplot as plt

# A leitura do arquivo está correta
df = pd.read_csv("resultados_com_sentimento.csv")

# A contagem agora inclui valores nulos (NaN)
contagem = df["sentimento"].value_counts(dropna=False)

# O restante do seu código para gerar o gráfico
plt.figure(figsize=(8, 6))
plt.bar(contagem.index, contagem.values, color=['green', 'red', 'blue', 'gray']) 
plt.xlabel("Sentimento")
plt.ylabel("Quantidade")
plt.title("Análise de Sentimentos dos Comentários")

for i, valor in enumerate(contagem.values):
    plt.text(i, valor + 0.5, str(valor), ha='center', va='bottom')

plt.savefig("analise_sentimentos.png")

plt.cla()
plt.close()