from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

serviço = Service(ChromeDriverManager().install()) 
navegador = webdriver.Chrome(service=serviço)

def chama_pagina(url):
    navegador.get(url)

    try:
        botao_inicial = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[1]/div[5]/a'))
        )
        botao_inicial.click()
    except Exception as e:
        print(f"Erro ao encontrar o elemento inicial: {e}")
        navegador.quit()

    time.sleep(3)

def carrega_imagens():
    divs = navegador.find_elements(By.XPATH, "/html/body/div[9]/div/div[1]/div")
    total_divs = len(divs)

    for i in range(total_divs):
        try:
            proximo_botao = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/div/div[3]/button[2]"))
            )
            proximo_botao.click()
            time.sleep(2)
        except Exception as e:
            print(f"Erro ao clicar no botão: {e}")
            break

def gera_html_e_coleta_imagens():
    urls_imagens = []
    divs = navegador.find_elements(By.XPATH, "/html/body/div[9]/div/div[1]/div")
    total_divs = len(divs)

    try:
        for i in range(total_divs):
            div_imagem = navegador.find_element(By.XPATH, f"/html/body/div[9]/div/div[1]/div[{i+1}]")
            
            img_element = div_imagem.find_element(By.TAG_NAME, "img")
            
            urls_imagens.append(f"{i+1}. {img_element.get_attribute('src')}")
            
            navegador.execute_script("arguments[0].scrollIntoView();", div_imagem)
        

    except Exception as e:
        print(f"Erro ao coletar imagens: {e}")

    with open("div_content.html", "w", encoding="utf-8") as file:
        file.write("\n".join(urls_imagens))

    print("HTML das divs foi salvo em 'div_content.html'.")
    return urls_imagens

def salvar_em_excel(urls):
    colunas = ["Foto Frontal", "Foto Lateral", "Foto Interior", "Foto Traseira"]

    if os.path.exists("fotos_veiculos.xlsx"):
        df = pd.read_excel("fotos_veiculos.xlsx")
    else:
        df = pd.DataFrame(columns=colunas)

    novo_dado = pd.DataFrame([urls], columns=colunas)
    df = pd.concat([df, novo_dado], ignore_index=True)

    df.to_excel("fotos_veiculos.xlsx", index=False)
    print("Planilha atualizada com sucesso!")

while True:
    url = input("Insira a URL do carro (ou pressione Enter para sair): ")
    
    if url == '':
        break  # Sai do loop se a entrada for vazia
    
    if url == '0':
        salvar_em_excel(["-"])  # Adiciona uma linha com "-"

    else:
        print(f"Processando URL: {url}")
        chama_pagina(url)
        carrega_imagens()
        urls = gera_html_e_coleta_imagens()

        if urls:  # Verifica se há URLs coletadas
            print("salvar_em_excel(urls)")

input("Pressione Enter para fechar o navegador...")
navegador.quit()
