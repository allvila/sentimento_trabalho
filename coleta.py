from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
import os

# --- Opção de Login: Perguntar ao usuário ---
login_manual = input("Você já inseriu suas credenciais no código (digite 'c') ou prefere fazer o login manualmente no navegador (digite 'm')? ").lower()

if login_manual == 'c':
    # Informações de login (substitua com seus dados)
    USUARIO = "alvilaray"
    SENHA = "Anaclara8615*"
else:
    # Apenas para o script não dar erro
    USUARIO = ""
    SENHA = ""

# Abre o navegador
navegador = webdriver.Chrome()

# --- Etapa 1: Fazer o login ---
try:
    navegador.get("https://x.com/i/flow/login")
    time.sleep(5)
    
    if login_manual == 'c':
        print("Preenchendo credenciais do código...")
        campo_usuario = navegador.find_element(By.XPATH, "//input[@name='text']")
        campo_usuario.send_keys(USUARIO)
        campo_usuario.send_keys(Keys.ENTER)
        time.sleep(3)

        campo_senha = navegador.find_element(By.XPATH, "//input[@name='password']")
        campo_senha.send_keys(SENHA)
        campo_senha.send_keys(Keys.ENTER)
        time.sleep(10)
        print("✅ Login realizado com sucesso!")
    else:
        print("Por favor, faça o login manualmente na janela do navegador que se abriu.")
        input("Pressione Enter quando o login estiver completo e você estiver na tela inicial...")
        
        # --- NOVO TRECHO ADICIONADO ---
        # Garante que estamos na página inicial e espera ela carregar
        navegador.get("https://x.com/home")
        time.sleep(5) 
        print("✅ Continuando...")

    # --- Etapa 2: Coletar os links dos posts no feed ---
    print("Coletando links de posts...")
    
    # Rola a página para carregar os primeiros posts
    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Coleta todos os links de posts na página
    post_links = navegador.find_elements(By.XPATH, '//a[contains(@href, "/status/")]')
    
    links_unicos = []
    for link in post_links:
        href = link.get_attribute('href')
        if "/status/" in href and href not in links_unicos:
            links_unicos.append(href)
    
    print(f"✅ {len(links_unicos)} links de posts encontrados.")

    if not links_unicos:
        print("❌ Nenhum post encontrado. Verifique se o feed está carregado corretamente.")
        navegador.quit()
        exit()

    # --- Etapa 3: Entrar em cada post com a sua permissão ---
    dados_finais = []
    i = 0
    while i < len(links_unicos):
        link_post = links_unicos[i]
        
        continuar = input(f"Processar o post {i+1} de {len(links_unicos)}? (S/N) ").lower()
        if continuar != 's':
            print("Processo interrompido pelo usuário.")
            break

        try:
            print(f"Coletando dados do post {i+1}: {link_post}")
            navegador.get(link_post)
            time.sleep(5)

            for _ in range(3):
                navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            post_original = navegador.find_element(By.TAG_NAME, "article")
            texto_da_postagem = post_original.text
            
            comentarios = navegador.find_elements(By.TAG_NAME, "article")
            
            for j, comentario in enumerate(comentarios[1:]):
                texto_comentario = comentario.text
                dados_finais.append([
                    f"{i+1}-{j+1}",
                    "@",
                    texto_da_postagem,
                    texto_comentario
                ])

            print(f"✅ Post {i+1} processado. Comentários coletados.")

        except Exception as e:
            print(f"❌ Erro ao processar o post {link_post}: {e}")
            
        i += 1
    
    # --- Etapa 4: Salvar em CSV ---
    df = pd.DataFrame(dados_finais, columns=["codigo_da_postagem", "nome_portal", "texto_da_postagem", "texto_do_comentario"])
    
    if os.path.exists("resultados_com_comentarios.csv"):
        df.to_csv("resultados_com_comentarios.csv", mode='a', header=False, index=False, encoding="utf-8")
    else:
        df.to_csv("resultados_com_comentarios.csv", index=False, encoding="utf-8")

    print(f"✅ Dados de {len(dados_finais)} comentários salvos ou adicionados.")

except Exception as e:
    print(f"❌ Ocorreu um erro no processo: {e}")

finally:
    navegador.quit()