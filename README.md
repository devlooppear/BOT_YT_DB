# BOT_YT_DB

- Esse código é uma automação da criação de um Banco de Dados, com valores do YouTube, tais como: títulos, links dos vídeos, nome dos canais e URLs.

- Como usar: no arquivo principal "main.py", você pode escolher escrever uma determinada pesquisa, na variável `PESQUISA` e o valor recebido será usado para que seja retirado do navegador os valores supracitados dessa pesquisa e eles viram os elementos que serão usados para a criação do Banco de Dados.

- O arquivo que executa o código é o ``main.py``.

## Ferramentas

- O arquivo de output é o Banco de Dados "youtube", que será criado com o código, dentro do Sistema Gerenciador de Banco de Dados (SGBD): Postgres.

- Como configurar no Postgres: para a integração com o Postgres, o código Python deve estar com as informações de acesso coincidentes, podendo serem definidas na função ``IniciarPsycopg()``, como é ilustrado a baixo:

```python
def IniciarPsycopg():
    conn = psycopg2.connect(
        database="Analise_YT",
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
        )
```

- Por isso, é possível tanto alterar essas informações para a integração, quanto criar o Banco de Dados (database)usuario 'postgres', senha 'postgres' e as outras informações, a não ser que tenham sido alteradas, já são as de padrão do postgres, como o 'localhost' e a posta escolhida ser '5432'.

## Bibliotecas

- Para utilizar o código, é necessário instalar as bibliotecas, com a escrita, no Terminal: pip install -r requirements.txt, que irá instalar todas as biblíotecas necessárias.

| Command | Description |
| --- | --- |
| pip install -r requirements.txt | Irá instalar todas as biblíotecas necessárias |