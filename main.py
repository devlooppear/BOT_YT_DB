from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import psycopg2

PESQUISA = "agronomia"

def IniciarSeleWebdriver():
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    
    return navegador

def InsercaoPesquisa(navegador):
    navegador.get(f'https://www.youtube.com//results?search_query={PESQUISA}')

#Iniciando psycopg2
def IniciarPsycopg():
    conn = psycopg2.connect(
        database="Analise_YT",
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
        )
        
    conn.autocommit = True

    cursor = conn.cursor()
    
    return cursor, conn

def ExcluirtabelaSeExiste(cursor):
    sql = 'DROP TABLE IF EXISTS youtube'
    cursor.execute(sql)

def CriarTabela(cursor):
    sql2 = '''CREATE TABLE IF NOT EXISTS youtube (
        identificacao SERIAL PRIMARY KEY,
        titulos VARCHAR (500),
        links VARCHAR (500),
        nome_canal VARCHAR (500),
        url VARCHAR (500)
    );'''
    cursor.execute(sql2)

def PegarTitulos(navegador):
    titulos = []

    ElTitulos = navegador.find_elements(By.ID, 'video-title')

    titulos = ElTitulos
    
    return titulos

def PegarLinks(navegador):
    links = []

    ItensLinks = navegador.find_elements(By.XPATH, '//div[@id="dismissible"]//a[@href][@id="thumbnail"]')

    links = ItensLinks
    
    return links

def PegarNomeCanal(navegador):
    NomeCanal = []

    ObjNomeCanal = navegador.find_elements(By.XPATH, '//ytd-channel-name[@id="channel-name"][@class="long-byline style-scope ytd-video-renderer"]')

    NomeCanal = ObjNomeCanal
    
    return NomeCanal

def PegarUrl(navegador):
    Url = []

    VlrsUrl = navegador.find_elements(By.XPATH, '//div[@id="dismissible"]//a[@href][@id="thumbnail"]')

    Url = VlrsUrl
    
    return Url

def InserirItens(titulos,links,NomeCanal,Url,cursor):
    for el,i,obj,vlr in list(zip(titulos, links, NomeCanal, Url)):
        el = str(el.text)
        for crt in el:    
            crt.strip("'")
        if el == " ":
            titulos.append(el)

        i = str(i.get_attribute("href").replace("https://www.youtube.com",""))
        if i == " ":
            links.remove(i)
        
        obj = str(obj.text)
        if obj == " ":
            NomeCanal.append(obj)
            
        vlr = str(vlr.get_attribute("href"))    
        sql3 = f"""INSERT INTO youtube (titulos, links, nome_canal, url) VALUES ('{el}','{i}','{obj}','{vlr}');"""
        cursor.execute(sql3)

def FecharConeccaoSql(conn):
    conn.commit()

    conn.close()

def main():

    navegador = IniciarSeleWebdriver()

    InsercaoPesquisa(navegador)

    cursor, conn = IniciarPsycopg()

    ExcluirtabelaSeExiste(cursor)

    CriarTabela(cursor)

    titulos = PegarTitulos(navegador)

    links = PegarLinks(navegador)

    NomeCanal = PegarNomeCanal(navegador)

    Url = PegarUrl(navegador)

    InserirItens(titulos,links,NomeCanal,Url,cursor)

    FecharConeccaoSql(conn)

main()