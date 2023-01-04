from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import psycopg2

PESQUISA = "IMPROCEDÊNCIA DIREITO DO TRABALHO DECADÊNCIA BIENAL"

def open_browser():
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    return navegador

def pesquisa_google(navegador):
    navegador.get("https://www.google.com/")
    navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(PESQUISA, Keys.RETURN)

def resultado_pesquisa(navegador):
    titulos = []

    objTitulos = navegador.find_elements(By.XPATH,"//h3[contains(@class,'LC20lb')]")
    for el in objTitulos:
            if el.text != "":
                titulos.append(el.text)
    return titulos

def integracao_pg():
    conn = psycopg2.connect(
        database="Analise_CSV",
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    
    conn.autocommit = True

    cursor = conn.cursor()
    return cursor, conn

def renovacao_tabela(cursor):
    sql = 'DROP TABLE IF EXISTS pesquisa'
    cursor.execute(sql)

    sql2 = 'CREATE TABLE pesquisa ( objtitulos VARCHAR(100));'
    cursor.execute(sql2)

def insercao_db(titulos, cursor):
    for el in titulos:
        sql3 = f"INSERT INTO pesquisa (objtitulos) VALUES ('{el}')"
        cursor.execute(sql3)

def finalizar_operacao_pg(conn):
    conn.commit()

    conn.close()

def main():

    navegador = open_browser()

    pesquisa_google(navegador)

    titulos = resultado_pesquisa(navegador)

    cursor, conn = integracao_pg()

    renovacao_tabela(cursor)

    insercao_db(titulos, cursor)

    finalizar_operacao_pg(conn)

main()