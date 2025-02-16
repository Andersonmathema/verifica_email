import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 🔑 Autenticação com escopos corretos
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

secrets_dict = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(secrets_dict, scopes=SCOPE)
client = gspread.authorize(creds)

# 📄 Obtém o ID da planilha do secrets
SPREADSHEET_ID = st.secrets["google_sheets"]["spreadsheet_id"]

# 🏫 Lista de salas disponíveis
salas_disponiveis = ["2A_PROC","2A_RED", "2C_MAT", "2C_EF", "3A_MAT","3B_MAT", "3B_PRG", "3C_MAT", "3D_MAT", "3D_PRG"]

# 🎨 Interface do Streamlit
st.title("📚 Consulta de Notas")

# 🔽 Dropdown para escolher a sala
sala_escolhida = st.selectbox("🏫 Escolha sua sala", salas_disponiveis)

# 👤 Inputs para Nome e RA
nome = st.text_input("👤 Digite seu Nome Completo").upper()
ra = st.text_input("🆔 Digite seu RA (0000'RA'SP)")

if st.button("🔍 Buscar"):
    if sala_escolhida and nome and ra:
        try:
            # 📌 Acessar a aba correspondente à sala escolhida
            worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(sala_escolhida)
            
            # 📊 Carregar os dados completos para encontrar a linha do aluno
            raw_data = worksheet.get_all_values()
            headers = raw_data[0]  # Pega os cabeçalhos
            df = pd.DataFrame(raw_data[1:], columns=headers)  # Ignora a primeira linha (cabeçalho)

            # 🔎 Filtrar pelo Nome e RA
            resultado = df[(df['Aluno'] == nome) & (df['RA'] == ra)]

            if not resultado.empty:
                # 📌 Pega o número da linha do aluno na planilha (considerando o cabeçalho)
                linha_aluno = resultado.index[0] + 2  # Índice do DataFrame começa em 0, mas no Google Sheets começa em 2

                # 🔢 Definir intervalo C até O na linha do aluno
                intervalo = f"C{linha_aluno}:O{linha_aluno}"
                valores = worksheet.range(intervalo)

                # 📋 Transformar os valores em DataFrame
                dados_filtrados = [celula.value for celula in valores]
                colunas_desejadas = headers[2:15]  # Pegando os cabeçalhos de C até O

                df_resultado = pd.DataFrame([dados_filtrados], columns=colunas_desejadas)

                st.success("✅ Resultado encontrado!")
                st.dataframe(df_resultado)
            else:
                st.warning("⚠ Nenhum aluno encontrado com essas informações.")
        
        except Exception as e:
            st.error(f"❌ Erro ao acessar a planilha: {e}")
    
    else:
        st.error("❌ Por favor, preencha todos os campos.")












