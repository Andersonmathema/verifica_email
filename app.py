import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 🔑 Autenticação no Google Sheets
secrets_dict = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(secrets_dict)
client = gspread.authorize(creds)

# 📄 Obtém o ID da planilha do secrets
SPREADSHEET_ID = st.secrets["google_sheets"]["spreadsheet_id"]

# 🏫 Lista de salas disponíveis
salas_disponiveis = ["2A", "2C", "3A", "3B", "3C", "3D"]

# 🎨 Interface do Streamlit
st.title("📚 Consulta de Notas")

# 🔽 Dropdown para escolher a sala
sala_escolhida = st.selectbox("🏫 Escolha sua sala", salas_disponiveis)

# 👤 Inputs para Nome e RA
nome = st.text_input("👤 Digite seu Nome Completo")
ra = st.text_input("🆔 Digite seu RA")

if st.button("🔍 Buscar"):
    if sala_escolhida and nome and ra:
        try:
            # 📌 Acessar a aba correspondente à sala escolhida
            worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(sala_escolhida)
            
            # 📊 Converter dados para DataFrame
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)

            # 🔎 Filtrar os dados do aluno
            resultado = df[(df['Nome'] == nome) & (df['RA'] == ra)]
            
            if not resultado.empty:
                st.success("✅ Resultado encontrado!")
                st.dataframe(resultado)
            else:
                st.warning("⚠ Nenhum aluno encontrado com essas informações.")
        
        except Exception as e:
            st.error(f"❌ Erro ao acessar a planilha: {e}")
    
    else:
        st.error("❌ Por favor, preencha todos os campos.")











