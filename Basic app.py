# Biblioteca responsavel por realizar a comunicação com o banco de dados 
from sqlalchemy import create_engine
# Biblioteca responsavel pela leitura do arquivo CSV
import pandas as pd
# Biblioteca para codificar os dados de login, evitando conflitos entre caracteres especiais
from urllib.parse import quote_plus as qp

# Dados de acesso ao banco
user = 'wirehouse'
password = qp('Br3ntw00d@WP25')
host = 'wirehouse'
database = 'wirehouse'

# Analisar qualidade do CSV
try:
    # Carregar arquivo CSV
    bd = pd.read_csv(r'C:\Users\csilva\Downloads\Base.CSV', encoding='latin1', sep=',')
    # Se tiver sucesso para carregar o CSV
    print('Arquivo carregado com sucesso')
    # print(bd.head(100))
    print(bd.columns.tolist())
# Se falhar o carregamento do CSV
except Exception as e:
        print("Erro", e)

# # Criar comunicação com o banco de dados
# engine = create_engine(
#     f"mysql+pymysql://{user}:{password}@{host}:3306/{database}"
#     )

# # Enviar informações do CSV para o SQL
# bd.to_sql('orcamento_site',con=engine, if_exists='append',index=False)