import os
import pandas as pd
import streamlit as st

CAMINHO_ARQUIVO_PADRAO = "datasets/dados_checklist.csv"

@st.cache_data
def carregar_dados(uploaded_file=None):
    """
    Carrega os dados de um arquivo CSV, seja um arquivo carregado pelo usuário
    ou o arquivo padrão.
    """
    try:
        # Define os parâmetros de leitura do CSV
        read_params = {"sep": ";", "encoding": "latin1", "quotechar": "'"}

        if uploaded_file:
            # Se um arquivo foi carregado, usa-o
            df = pd.read_csv(uploaded_file, **read_params)
        else:
            # Caso contrário, usa o caminho padrão
            if not os.path.exists(CAMINHO_ARQUIVO_PADRAO):
                st.error(f"Arquivo padrão não encontrado: {CAMINHO_ARQUIVO_PADRAO}")
                return pd.DataFrame()
            df = pd.read_csv(CAMINHO_ARQUIVO_PADRAO, **read_params)

        # Limpeza e processamento dos dados
        df.columns = df.columns.str.strip().str.replace("�", "ç", regex=False)
        colunas_corrigidas = {
            "Posi��o": "Posição",
            "PosiÇão": "Posição",
            "Posição ": "Posição",
            "Observa��o": "Observação",
            "ObservaÇão": "Observação",
            "Observação ": "Observação",
        }
        df.rename(columns=colunas_corrigidas, inplace=True)

        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
        else:
            st.warning("A coluna 'Data' não foi encontrada no arquivo.")

        return df

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar ou processar o arquivo: {e}")
        return pd.DataFrame()

def load_css(file_name: str):
    """
    Carrega e injeta um arquivo CSS no aplicativo Streamlit.
    """
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo CSS não encontrado: {file_name}")
