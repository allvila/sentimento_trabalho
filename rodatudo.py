import subprocess
import os
import time

# Passo 1: Executar o script de coleta de dados (com Selenium)
print("Iniciando a coleta de dados...")
# O primeiro 'python' é o comando para executar o script
# O segundo argumento é o nome do arquivo que será executado
processo_coleta = subprocess.run(["python", "coleta.py"])
# O código de retorno 0 indica que o script foi executado com sucesso
if processo_coleta.returncode == 0:
    print("✅ Coleta de dados concluída com sucesso!")
else:
    print("❌ Erro na coleta de dados. Verifique o seu script do Selenium.")
    exit() # Interrompe a execução se houver um erro

# Adiciona uma pequena pausa para garantir que o arquivo foi salvo
time.sleep(2) 

# Passo 2: Executar o script de limpeza de dados
print("Iniciando a limpeza dos dados...")
# Garanta que 'resultados.csv' seja o arquivo de entrada de limpeza.py
processo_limpeza = subprocess.run(["python", "limpeza.py"])
if processo_limpeza.returncode == 0:
    print("✅ Limpeza de dados concluída!")
else:
    print("❌ Erro na limpeza dos dados. Verifique o seu script de limpeza.")
    exit()

# Passo 3: Executar o script de análise
print("Iniciando a análise dos dados...")
# Garanta que o arquivo de entrada seja o de saída do script de limpeza
processo_analise = subprocess.run(["python", "analise.py"])
if processo_analise.returncode == 0:
    print("✅ Análise dos dados concluída!")
else:
    print("❌ Erro na análise dos dados. Verifique o seu script de análise.")
    exit()

# Passo 4: Executar o script de qualidade
print("Iniciando a verificação de qualidade dos dados...")
processo_qualidade = subprocess.run(["python", "qualidade.py"])
if processo_qualidade.returncode == 0:
    print("✅ Verificação de qualidade concluída! Pipeline finalizado.")
else:
    print("❌ Erro na verificação de qualidade. Verifique o seu script de qualidade.")
    exit()