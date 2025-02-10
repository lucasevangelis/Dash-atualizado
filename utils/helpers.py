import os
import pandas as pd
import streamlit as st

CAMINHO_ARQUIVO = "datasets/dados_checklist.csv"

@st.cache_data
def carregar_dados():
    df = pd.read_csv(CAMINHO_ARQUIVO, sep=";", encoding="latin1")
    
    # 🔍 Remover espaços e caracteres estranhos dos nomes das colunas
    df.columns = df.columns.str.strip().str.replace("�", "ç", regex=False)

    # 🔄 Renomear colunas corretamente (caso necessário)
    colunas_corrigidas = {
        "Posi��o": "Posição",
        "PosiÇão": "Posição",
        "Posição ": "Posição",
        "Observa��o": "Observação",
        "ObservaÇão": "Observação",
        "Observação ": "Observação"
    }
    df.rename(columns=colunas_corrigidas, inplace=True)

    # 📅 Converter coluna "Data" para formato datetime
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")

    return df
