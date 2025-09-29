import pandas as pd
from rich.console import Console
from rich.table import Table

ARQUIVO_ENTRADA = "resultados_com_sentimento_g1.csv"
ARQUIVO_SAIDA_CSV = "resultados_padronizados_g1.csv" # Novo arquivo CSV
NOME_PORTAL_FINAL = "@g1"

# Carregar e renomear colunas
df = pd.read_csv(ARQUIVO_ENTRADA)
df = df.rename(columns={
    'codigo': 'codigo_da_postagem',
    'perfil': 'nome_portal',
    'postagem': 'texto_da_postagem',
    'comentario': 'texto_do_comentario'
})
df['nome_portal'] = NOME_PORTAL_FINAL

# Limpar quebras de linha e espaços múltiplos
for coluna in ["texto_da_postagem", "texto_do_comentario"]:
    df[coluna] = df[coluna].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()

# Função para cortar texto longo (usada apenas para exibição no terminal)
def truncar(texto, limite=60):
    return texto[:limite] + "..." if len(texto) > limite else texto

# ----------------------------------------------------------------------
# 1. SALVAR O NOVO CSV COM COLUNAS PADRONIZADAS
# ----------------------------------------------------------------------
df.to_csv(ARQUIVO_SAIDA_CSV, index=False, encoding="utf-8")
print(f"✅ Arquivo padronizado salvo em: {ARQUIVO_SAIDA_CSV}")

# ----------------------------------------------------------------------
# 2. VISUALIZAÇÃO COLORIDA NO TERMINAL (RICH)
# ----------------------------------------------------------------------

# Criar tabela colorida
console = Console()
table = Table(show_header=True, header_style="bold cyan", title="\nVisualização dos Resultados Finais")

# Definir largura máxima das colunas
table.add_column("codigo_da_postagem", style="white", no_wrap=True)
table.add_column("nome_portal", style="magenta", no_wrap=True)
table.add_column("texto_da_postagem", style="green", max_width=60, overflow="fold")
table.add_column("texto_do_comentario", style="yellow", max_width=40, overflow="fold")
table.add_column("sentimento", style="bold")

# Adicionar linhas com truncamento
for _, row in df.iterrows():
    sentimento = row["sentimento"]
    if sentimento == "POSITIVO":
        cor = f"[green]{sentimento}[/green]"
    elif sentimento == "NEGATIVO":
        cor = f"[red]{sentimento}[/red]"
    else:
        cor = f"[yellow]{sentimento}[/yellow]"

    table.add_row(
        str(row["codigo_da_postagem"]),
        row["nome_portal"],
        truncar(row["texto_da_postagem"], 60),
        truncar(row["texto_do_comentario"], 40),
        cor
    )

# Mostrar tabela no terminal
console.print(table)