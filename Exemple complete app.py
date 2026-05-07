# Biblioteca responsavel por realizar a comunicação com o banco de dados 
from sqlalchemy import create_engine
# Biblioteca responsavel pela leitura do arquivo CSV
import pandas as pd
# Biblioteca para codificar os dados de login, evitando conflitos entre caracteres especiais
from urllib.parse import quote_plus as qp
# Biblioteca que coleta a data
from datetime import datetime as data
# Bibliotecas responsavel por criar a interface grafica
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import sys


# Dados de acesso ao banco
user = 'usuario do banco'
password = qp('Senha do banco')
host = 'Endereço do host do banco'
database = 'nome do banco'

# Armazenar o arquivo em uma pasta de destino
pasta_destino = os.path.join(os.path.dirname(__file__),'uploads')

# Se a pasta de destino não existir
if not os.path.exists(pasta_destino):
    # Criar pasta de destino
    os.makedirs(pasta_destino)

arquivo_selecionado = None

# Selecionar aruqivo
def selecionar_arquivo():
    global arquivo_selecionado

    caminho = filedialog.askopenfilename(
          filetypes=[('arquivos CSV','*.csv')]
    )

    if caminho:
        arquivo_selecionado = caminho
        label_arquivo.config(text=os.path.basename)

def processar_arquivo():
    global arquivo_selecionado

    if not arquivo_selecionado:
        messagebox.showerror("Erro","Arquivo não selecionado")
        return

    try:
        # Copiar arquivos para a pasta de sistema
        destino = os.path.join(pasta_destino, os.path.basename(arquivo_selecionado))
        shutil.copy(arquivo_selecionado, destino)

        # Chamar o ETL
        resultado = executar_etl(destino)

        messagebox.showinfo("Sucesso", resultado)
    
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Executar ETL
def executar_etl(caminho_arquivo):
    bd = pd.read_csv(caminho_arquivo, encoding='utf-8')
    bd.columns = bd.columns.str.strip()

    erros = []
    # Validação dos campos obrigatórios
    def validar_obrigatorio(df, coluna, mensagem):
        # Coletar colunas que estão com informações invalidas
            # isna() verifica se informação da coluna é NaN
            # astype(str) converte qualquer informação para string
            # .str.strip() elimina os espaços no começo e no final
            # =='' se o resultado final for vazio ou NaN, a variavel 'faltantes' ficará com o resultado vazio
        faltantes = df[df[coluna].isna() | (df[coluna].astype(str).str.strip()=='')]

        # Se existirem linhas invalidas
        if not faltantes.empty:
                # Looping para percorrer cada linha do banco
                # o i represent o Indice, i+1 garante o looping para a proxima linha do indice
                for i, linha in faltantes.iterrows():
                    # Criar lista com mesangens de erro
                    erros.append(f'Linha {i+1}: {mensagem}')

        return df.drop(faltantes.index)

    # Aplicar Validação dos campos obrigatórios
    bd = validar_obrigatorio(bd,'Cliente','o campo - Nome do cliente - é obrigatório')
    bd = validar_obrigatorio(bd,'Telefone','o campo - Telefone - é obrigatório')
    bd = validar_obrigatorio(bd,'Loja','o campo - Loja - é obrigatório')

    # Campos sem obrigatoriedade
    bd['Email'] = bd['Email'].fillna('Whatsapp')
    bd['OrcamentoSolicitado'] = bd['OrcamentoSolicitado'].fillna('Whatsapp')
    bd['AutorizacaoDeContato'] = bd['AutorizacaoDeContato'].fillna('Whatsapp')

    # Tratar o Vazio
    bd['Email'] = bd['Email'].replace('','Whatsapp')
    bd['OrcamentoSolicitado'] = bd['OrcamentoSolicitado'].replace('','Whatsapp')
    bd['AutorizacaoDeContato'] = bd['AutorizacaoDeContato'].replace('','Whatsapp')

    # Campo Fixo
    bd['Status'] = 'Enviado ao gerente'

    # Tratando campo de data
    bd['DataSolicita'] = bd['DataSolicita'].fillna(data.now().date())

    # Campo Livre
    bd['VendedorAssociado'] = None
    
    # Criar comunicação com o banco de dados
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:3306/{database}"
        )
    
    # Enviar informações do CSV para o SQL
    bd.to_sql('orcamento_site',con=engine, if_exists='append',index=False)

    # Apresentação do erro
    if erros:
        return 'Processado com erro:\n'+'\n'.join(erros)
    return 'Processado com sucesso'

# Interface grafica
# tabela de cores
background = '#1e1e2f'
textcolor = '#ffffff'
card_color = '#2a2a40'
primary = '#3a86ff'

# janela principal
janela = tk.Tk()
janela.title("Database Brentwood.com.br")
janela.configure(bg=background)
janela.geometry("400x300")

# container principal
container = tk.Frame(janela, bg=background)
container.pack(fill="both", expand=True, padx=20, pady=20)

# header
header = tk.Frame(container, bg=background)
header.pack(fill="x")

label_titulo = tk.Label(
    header,
    text='Upload do CSV',
    font=("Segoe UI", 14),
    bg=background,
    fg=textcolor
)
label_titulo.pack(pady=(0, 10))

# body
body = tk.Frame(container, bg=background)
body.pack(fill="both", expand=True)

# Personalização do card
card_frame = tk.Frame(
    body,
    bg=card_color,
    bd=0,
    highlightthickness=0,
    padx=15,
    pady=15
)
card_frame.pack(fill="x", pady=10)

# Personalização do título do card
label = tk.Label(
    card_frame,
    text="Upload de arquivo",
    bg=card_color,
    fg=textcolor,
    font=("Segoe UI", 12)
)
label.pack(pady=(0, 10))

# Personalização do botão upload
botao_upload = tk.Button(
    card_frame,
    text='Selecionar arquivo',
    command=selecionar_arquivo,
    bg=primary,
    fg="white",
    activebackground="#2f6edc",
    activeforeground="white",
    bd=0,
    padx=15,
    pady=8,
    cursor="hand2"
)
botao_upload.pack(pady=5)

# Personalização da label com o nome do arquivo
label_arquivo = tk.Label(
    card_frame,
    text='Nenhum arquivo selecionado',
    fg=textcolor,
    bg=card_color,
    wraplength=300,
    justify="center"
)
label_arquivo.pack(pady=5)

# Personalização do botão processar
botao_processar = tk.Button(
    card_frame,
    text='Enviar dados',
    command=processar_arquivo,
    bg=primary,
    fg="white",
    activebackground="#2f6edc",
    activeforeground="white",
    bd=0,
    padx=15,
    pady=8,
    cursor="hand2"
)
botao_processar.pack(pady=10)

janela.mainloop()