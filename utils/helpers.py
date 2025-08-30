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
        if uploaded_file:
            # Se um arquivo foi carregado, usa-o
            df = pd.read_csv(uploaded_file, sep=";", encoding="latin1")
        else:
            # Caso contrário, usa o caminho padrão
            if not os.path.exists(CAMINHO_ARQUIVO_PADRAO):
                st.error(f"Arquivo padrão não encontrado: {CAMINHO_ARQUIVO_PADRAO}")
                return pd.DataFrame()
            df = pd.read_csv(CAMINHO_ARQUIVO_PADRAO, sep=";", encoding="latin1")

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
