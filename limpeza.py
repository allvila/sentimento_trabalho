import pandas as pd
import re

# Lê o arquivo que você coletou
df = pd.read_csv("comentarios_g1.csv")

# 📢 PASSO 1: IMPRIMA OS NOMES DAS COLUNAS PARA VERIFICAR!
print("Nomes das Colunas no CSV:", df.columns.tolist())
# --------------------------------------------------------

def limpar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = re.sub(r"http\S+", "", texto) 
    texto = re.sub(r"[@#]\w+", "", texto) 
    
    # Versão alternativa que mantém alguns sinais de pontuação
    # Ex: exclui tudo que não seja letra, número, espaço ou os sinais !,?.'
    texto = re.sub(r"[^a-zA-ZÀ-ÿ\s\d!?.,]", "", texto) 
    
    return texto.strip()

# 📢 PASSO 2: Substitua 'texto_do_comentario' pelo nome correto que apareceu no terminal!
df["comentario"] = df["comentario"].apply(limpar_texto)

# Salva um novo arquivo limpo
df.to_csv("resultadosg1_limpos.csv", index=False, encoding="utf-8")

print("✅ Textos limpos e salvos em resultadosg1_limpos.csv")