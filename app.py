import streamlit as st
import pandas as pd
from datetime import date

# 🔗 Criar conexão com Google Sheets
st.write("🚀 Iniciando conexão com Google Sheets...")
try:
    conn = st.connection("gsheet", type="gspread", ttl=600)
    st.write("✅ Conexão bem-sucedida!")
except Exception as e:
    st.error(f"❌ Erro ao conectar com Google Sheets: {e}")
    st.stop()

# 🔥 Carregar os dados da planilha
try:
    df = conn.read(worksheet="NomeDaAba", usecols=list(range(5)), ttl=600)
    st.success("✅ Dados carregados com sucesso!")
except Exception as e:
    st.error(f"❌ Erro ao carregar dados do Google Sheets: {e}")
    st.stop()

# 📊 Exibir os primeiros dados para debug
st.write("📊 Primeiras linhas dos dados:")
st.dataframe(df.head())

# 🛠 Limpeza dos dados
df.columns = df.columns.astype(str).str.strip()  # Remove espaços extras nos nomes das colunas

# Verificar se a coluna "Data de Nascimento" existe
if "Data de Nascimento" in df.columns:
    df["Data de Nascimento"] = pd.to_datetime(df["Data de Nascimento"], format="%d/%m/%Y", errors="coerce").dt.date
    df = df.dropna(subset=["Data de Nascimento"])  # Remove linhas com datas vazias
else:
    st.error("⚠️ A coluna 'Data de Nascimento' não foi encontrada na planilha.")

# 📌 Entrada do usuário para busca
nome_filtro = st.text_input("Digite seu nome completo:")
data_nasc_filtro = st.date_input("Escolha sua data de nascimento:", value=date(2009, 2, 1), min_value=date(1900, 1, 1), max_value=date.today())

# 📌 Aplicando o filtro no DataFrame
if nome_filtro and data_nasc_filtro:
    df_filtrado = df[
        (df["Nome do Aluno"].str.lower() == nome_filtro.lower()) &
        (df["Data de Nascimento"] == data_nasc_filtro)
    ]

    if not df_filtrado.empty:
        email_usuarioG = df_filtrado["Email Google"].values[0]
        email_usuarioM = df_filtrado["Email Microsoft"].values[0]
                
        # 📧 Criando um campo de texto com o e-mail para copiar
        st.write("📧 **Seu e-mail Google:**")        
        st.code(email_usuarioG, language="text")

        st.write("📧 **Seu e-mail Microsoft:**")        
        st.code(email_usuarioM, language="text")
    else:
        st.error("Nenhum registro encontrado para esse nome e data de nascimento.")









