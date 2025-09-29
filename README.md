📊 Análise de Comentários do X (Twitter) - Portal G1
Este repositório contém um pipeline de análise de dados completo, que vai desde a raspagem automática de comentários do perfil @g1 no X (anteriormente Twitter) até a classificação do sentimento desses comentários e a visualização dos resultados.

🚀 Estrutura do Projeto
O projeto é dividido em três etapas principais, representadas por diferentes scripts:

Coleta de Dados: Utiliza Selenium para logar e raspar os últimos posts e seus comentários.

Pré-processamento: Utiliza Pandas e Expressões Regulares para limpar os textos brutos.

Análise e Visualização: Utiliza LeIA (Análise de Sentimento em Português), Pandas e Matplotlib para classificar os comentários e gerar um gráfico.

Visualização Final (Terminal): Usa a biblioteca Rich para apresentar os resultados em uma tabela colorida no terminal.

⚙️ Pré-requisitos
Para rodar o projeto, você precisa ter:

Python 3.x instalado.

ChromeDriver compatível com a sua versão do Google Chrome (necessário apenas para a etapa de coleta).

1. Instalação das Bibliotecas
Instale todas as dependências necessárias com um único comando:

Bash

pip install pandas selenium leia matplotlib rich
2. Configuração do Selenium (Coleta)
Certifique-se de que o ChromeDriver está corretamente configurado no seu ambiente para que o script de coleta possa controlar o navegador Chrome.

🛠️ Instruções de Uso (Passo a Passo)
1. Etapa de Coleta (Rastreamento)
O primeiro passo é coletar os dados do perfil desejado.

Configure Credenciais: No script de coleta, preencha as variáveis de configuração com seu usuário e senha do X:

Python

USUARIO = "seu_usuario"     # ⚠️ Coloque seu usuário do X
SENHA = "sua_senha_secreta" # ⚠️ Coloque sua senha do X
URL_PERFIL = "https://x.com/g1" # Mude se quiser outro perfil
Execute o Script:

Bash

python script_coleta.py
Saída: comentarios_g1.csv (dados brutos).

2. Etapa de Limpeza (Pré-processamento)
Essa etapa remove ruídos como links, menções, hashtags e caracteres especiais, preparando o texto para a análise.

Verifique a Entrada: Certifique-se de que o arquivo comentarios_g1.csv está na mesma pasta.

Execute o Script:

Bash

python script_limpeza.py
Saída: resultadosg1_limpos.csv (dados prontos para análise).

3. Etapa de Análise de Sentimento e Gráfico
Aplica a Análise de Sentimento em Português e gera a primeira visualização.

Execute o Script:

Bash

python script_analise_sentimento.py
Saídas:

resultados_com_sentimento_g1.csv (CSV final com a nova coluna sentimento).

analise_sentimentos.png (Gráfico de barras da distribuição dos sentimentos).

4. Etapa de Visualização no Terminal (Opcional)
Use este script para inspecionar os resultados finais diretamente na sua linha de comando, com destaque de cores para o sentimento.

Execute o Script:

Bash

python script_visualizacao_rich.py
Saída: Uma tabela formatada e colorida no terminal, com Positivo em verde, Negativo em vermelho e Neutro em amarelo.

📊 Estrutura dos Dados Finais
O arquivo final resultados_com_sentimento_g1.csv possui as seguintes colunas:

Coluna	Descrição
codigo	ID da postagem e comentário (Ex: P1_C5).
perfil	O nome do perfil rastreado (@g1).
postagem	O texto limpo da postagem original.
comentario	O texto limpo do comentário.
sentimento	A classificação do sentimento: POSITIVO, NEGATIVO, ou NEUTRO.

Exportar para as Planilhas
