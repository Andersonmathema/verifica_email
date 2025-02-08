import streamlit as st
import pandas as pd
import pygsheets
from dotenv import load_dotenv
from datetime import date
import json
import os

load_dotenv()

# Carregar o link da planilha do Google Sheets
meu_arquivo_GS = st.secrets["google_sheets"]["spreadsheet_url"]

# Carregar as credenciais de autenticação do Google Sheets
creds_dict = st.secrets["google_sheets_credentials"]

# Autenticar com Google Sheets
credenciais = pygsheets.authorize(service_account_info=creds_dict)

# Acessar a planilha pelo link armazenado no secrets
arquivo = credenciais.open_by_url(meu_arquivo_GS)

st.success("Conexão com Google Sheets realizada com sucesso!")

abas = {
    "Nenhum": arquivo.worksheet_by_title('Vazio'),
    "2A": arquivo.worksheet_by_title('2A tec'),
    "2C": arquivo.worksheet_by_title('2C MEF'),
    "3A": arquivo.worksheet_by_title('3A M'),
    "3B": arquivo.worksheet_by_title('3B MP'),
    "3C": arquivo.worksheet_by_title('3C M'),
    "3D": arquivo.worksheet_by_title('3D MP'),
}

st.title("Seu email institucional")
st.write("Preencha")

opcoes = list(abas.keys())
escolha = st.selectbox("Sua sala:", opcoes)

aba = abas[escolha]

df = pd.DataFrame(aba)

# Transformar a primeira linha em cabeçalho
df.columns = df.iloc[0]  # Define a primeira linha como cabeçalho
df = df[1:].reset_index(drop=True)  # Remove a primeira linha e reseta o índice

# Remover espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# Verificar se a coluna "Data de Nascimento" existe
if "Data de Nascimento" in df.columns:
    df["Data de Nascimento"] = df["Data de Nascimento"].replace("", pd.NA)  # Corrigir valores vazios
    df["Data de Nascimento"] = pd.to_datetime(df["Data de Nascimento"], format="%d/%m/%Y", errors="coerce").dt.date
    df = df.dropna(subset=["Data de Nascimento"])  # Remove linhas com datas vazias
else:
    st.error("⚠️ A coluna 'Data de Nascimento' não foi encontrada na aba selecionada.")

# Entrada do usuário
nome_filtro = st.text_input("Digite seu nome completo:")
data_nasc_filtro = st.date_input("Escolha sua data de nascimento:",
                                  value=date(2009, 2, 1),
                                  min_value=date(1900, 1, 1),
                                  max_value=date.today()
                                )

# Aplicando o filtro
if nome_filtro and data_nasc_filtro:
    df_filtrado = df[
        (df["Nome do Aluno"].str.lower() == nome_filtro.lower()) &
        (df["Data de Nascimento"] == data_nasc_filtro)
    ]

    if not df_filtrado.empty:
        email_usuarioG = df_filtrado["Email Google"].values[0]
        email_usuarioM = df_filtrado["Email Microsoft"].values[0]
                
        # Criando um campo de texto com o e-mail para copiar
        st.write("📧 **Seu e-mail Google:**")        
        st.code(email_usuarioG, language="text")

        st.write("📧 **Seu e-mail Microsoft:**")        
        st.code(email_usuarioM, language="text")

    else:
        st.error("Nenhum registro encontrado para esse nome e data de nascimento.")






