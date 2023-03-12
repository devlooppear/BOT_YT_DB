from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import psycopg2

PESQUISA = "Michael Jackson"

def iniciar_sele_webdriver():
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    return navegador

def insercao_pesquisa(navegador):
    navegador.get(f'https://www.youtube.com//results?search_query={PESQUISA}')

def iniciar_psycopg():
    conn = psycopg2.connect(
        database="Analise_YT",
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
        )
    conn.autocommit = True
    return conn

def excluir_tabela_se_existe(cursor):
    cursor.execute('DROP TABLE IF EXISTS youtube')

def criar_tabela(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS youtube (
        id SERIAL PRIMARY KEY,
        titulo VARCHAR (500) NOT NULL,
        link VARCHAR (500) NOT NULL,
        nome_canal VARCHAR (500) NOT NULL,
        url VARCHAR (500) NOT NULL
    )''')

def pegar_dados(navegador):
    titulos = [el.text.replace("'", "") for el in navegador.find_elements(By.ID, 'video-title')]
    links = [el.get_attribute('href').replace('https://www.youtube.com', '') for el in navegador.find_elements(By.XPATH, '//div[@id="dismissible"]//a[@href][@id="thumbnail"]')]
    nome_canal = [el.text for el in navegador.find_elements(By.XPATH, '//ytd-channel-name[@id="channel-name"][@class="long-byline style-scope ytd-video-renderer"]')]
    urls = [el.get_attribute('href') for el in navegador.find_elements(By.XPATH, '//div[@id="dismissible"]//a[@href][@id="thumbnail"]')]
    return titulos, links, nome_canal, urls

def inserir_itens(dados, cursor):
    sql = 'INSERT INTO youtube (titulo, link, nome_canal, url) VALUES (%s, %s, %s, %s)'
    cursor.executemany(sql, dados)

def main():
    navegador = iniciar_sele_webdriver()
    insercao_pesquisa(navegador)
    conn = iniciar_psycopg()
    with conn, conn.cursor() as cursor:
        excluir_tabela_se_existe(cursor)
        criar_tabela(cursor)
        dados = list(zip(*pegar_dados(navegador)))
        inserir_itens(dados, cursor)

if __name__ == '__main__':
    main()