import time
import os
import pandas as pd

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

# --- CONFIGURAÇÕES ---
USUARIO = "_____"  # ⚠️ Coloque seu usuário do X
SENHA = "____"       # ⚠️ Coloque sua senha do X
ARQUIVO_SAIDA = "comentarios_g1.csv"
URL_LOGIN = "https://x.com/i/flow/login"
URL_PERFIL = "https://x.com/g1" # Perfíl que será raspado
NOME_PERFIL = URL_PERFIL.split('/')[-1] # Extrai "g1"

def fazer_login(navegador):
    """Faz login automático no X usando credenciais do código"""
    print("🔗 Acessando página de login...")
    navegador.get(URL_LOGIN)
    time.sleep(5)

    try:
        campo_usuario = navegador.find_element(By.XPATH, "//input[@name='text']")
        campo_usuario.send_keys(USUARIO)
        campo_usuario.send_keys(Keys.ENTER)
        time.sleep(3)

        # Pode aparecer uma tela pedindo usuário de novo se o primeiro login falhar
        try:
            campo_senha = navegador.find_element(By.XPATH, "//input[@name='password']")
        except NoSuchElementException:
            # Tenta inserir o usuário novamente se for solicitado
            campo_usuario = navegador.find_element(By.XPATH, "//input[@name='text']")
            campo_usuario.send_keys(USUARIO)
            campo_usuario.send_keys(Keys.ENTER)
            time.sleep(3)
            campo_senha = navegador.find_element(By.XPATH, "//input[@name='password']")

        campo_senha.send_keys(SENHA)
        campo_senha.send_keys(Keys.ENTER)
        time.sleep(8)

        print("✅ Login realizado com sucesso!")
        return True
    except NoSuchElementException:
        print("❌ Não foi possível preencher os campos de login (pode ter captcha ou tela de verificação).")
        return False


def fechar_popup_views(navegador):
    """Fecha pop-ups modais, incluindo 'Views' e 'Login' (se logado)"""
    try:
        # Busca o botão "Dismiss" que aparece no pop-up da imagem
        botao_dismiss = navegador.find_element(By.XPATH, '//span[text()="Dismiss"]/ancestor::div[@role="button"]')
        if botao_dismiss:
            botao_dismiss.click()
            print("🪄 Popup 'Views' fechado automaticamente.")
            time.sleep(2)
    except NoSuchElementException:
        pass
    except Exception as e:
        # Tenta fechar o pop-up de login se ele aparecer no meio do caminho
        try:
            fechar_login = navegador.find_element(By.XPATH, '//div[@aria-label="Close"]')
            fechar_login.click()
            print("🪄 Popup de login fechado.")
            time.sleep(1)
        except NoSuchElementException:
            pass
        except Exception:
            pass


def coletar_ultimos_posts(navegador, limite=30):
    """Coleta links das últimas N postagens, navegando diretamente para o perfil."""
    print(f"📌 Acessando o perfil @{NOME_PERFIL}...")
    navegador.get(URL_PERFIL)
    time.sleep(5)

    links_unicos = set()
    
    # XPath mais específico: Busca por elementos ARTICLE que contêm a menção ao usuário correto
    xpath_articles = f'//article//a[starts-with(@href, "/{NOME_PERFIL}/status/")]'

    while len(links_unicos) < limite:
        fechar_popup_views(navegador)
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        fechar_popup_views(navegador)

        try:
            post_elements = navegador.find_elements(By.XPATH, xpath_articles)
            for el in post_elements:
                href = el.get_attribute("href")
                if href and f'/{NOME_PERFIL}/status/' in href:
                    # Filtra posts longos que terminam em /media (ex: /status/1234/media)
                    if not href.endswith('/photo') and not href.endswith('/video') and not href.endswith('/media'):
                        links_unicos.add(href.split('?')[0]) # Limpa parâmetros de query
        except StaleElementReferenceException:
            print("⚠️ Aviso: Elementos ficaram obsoletos, tentando novamente.")
            continue

        print(f"➡️ Já encontrados {len(links_unicos)} links de posts de @{NOME_PERFIL}...")

    return list(links_unicos)[:limite]


def raspar_comentarios(navegador, links_posts):
    """Entra em cada post e coleta comentários"""
    dados = []

    for i, link in enumerate(links_posts, start=1):
        print(f"\n📝 Coletando post {i}/{len(links_posts)}: {link}")
        navegador.get(link)
        time.sleep(5)

        fechar_popup_views(navegador)

        for _ in range(5): 
            navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            fechar_popup_views(navegador) 

        try:
            artigos = navegador.find_elements(By.TAG_NAME, "article")
            if len(artigos) < 2:
                print("⚠️ Nenhum comentário (artigo > 1) encontrado ou página não carregou.")
                continue

            texto_post = artigos[0].text  # O primeiro "article" é o post original

            for j, comentario in enumerate(artigos[1:], start=1):
                texto_comentario = comentario.text.strip()
                if texto_comentario:
                    dados.append([
                        f"P{i}_C{j}",
                        NOME_PERFIL, 
                        texto_post,
                        texto_comentario
                    ])

            print(f"✅ {len(artigos)-1} comentários coletados neste post.")

        except Exception as e:
            print(f"❌ Erro no post {link}: {e}")

    return dados


def salvar_csv(dados):
    """Salva em CSV"""
    if not dados:
        print("⚠️ Nenhum dado coletado.")
        return

    df = pd.DataFrame(dados, columns=["codigo", "perfil", "postagem", "comentario"])
    df.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8")
    print(f"\n💾 Dados salvos em {ARQUIVO_SAIDA} ({len(dados)} comentários).")


def main():
    navegador = None
    try:
        print("🚀 Iniciando navegador...")
        navegador = webdriver.Chrome()

        if not fazer_login(navegador):
            print("🚫 Abortando coleta devido a falha no login ou verificação.")
            return

        links = coletar_ultimos_posts(navegador, limite=30)
        print(f"\n📌 Total de {len(links)} posts coletados para análise de @{NOME_PERFIL}.")

        dados = raspar_comentarios(navegador, links)
        salvar_csv(dados)

    except TimeoutException:
        print("⏳ Timeout ao carregar página.")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
    finally:
        if navegador:
            navegador.quit()
            print("👋 Navegador fechado.")


if __name__ == "__main__":
    main()
