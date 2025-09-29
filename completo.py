import subprocess
import time
import os

# --- Etapas do Pipeline ---
# 1. COLETAR (Selenium)
# 2. LIMPEZA (Pandas/Regex)
# 3. ANÁLISE (LeIA)
# 4. QUALIDADE/RELATÓRIO FINAL (Pandas)

def executar_script(nome_script):
    """Executa um script Python e verifica o código de retorno."""
    print(f"\n==================================================")
    print(f"| 🚀 Iniciando o processo: {nome_script} ")
    print(f"==================================================")
    
    # O comando "python nome_script.py"
    processo = subprocess.run(["python", nome_script])
    
    if processo.returncode == 0:
        print(f"✅ SUCESSO: {nome_script} concluído sem erros.")
        # Pequena pausa para garantir que os arquivos sejam salvos antes do próximo passo
        time.sleep(2) 
        return True
    else:
        print(f"❌ ERRO FATAL: {nome_script} falhou.")
        print("   Verifique o Traceback acima para detalhes do erro.")
        return False

# ------------------------------------------------------------------
# Execução da Sequência
# ------------------------------------------------------------------

print("INICIANDO A PIPELINE DE ANÁLISE DE SENTIMENTO.")

# 1. Coleta de Dados (Selenium)
if not executar_script("coleta.py"):
    exit()

# 2. Limpeza de Dados
if not executar_script("limpeza.py"):
    exit()

# 3. Análise de Sentimento (LeIA)
if not executar_script("analise.py"):
    exit()

# 4. Qualidade e Relatório Final
if not executar_script("qualidade.py"):
    exit()

# Fim da Pipeline
print("\n🎉🎉🎉 PIPELINE CONCLUÍDA! 🎉🎉🎉")
print(f"O relatório final foi salvo como 'relatorio_final_g1.csv'.")