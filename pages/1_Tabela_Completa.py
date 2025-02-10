import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from utils.helpers import carregar_dados
from auth import login

# 🛑 Verifica login antes de carregar qualquer conteúdo
if not st.session_state.get("logado", False):
    login()
    st.stop()

# 🔧 Configuração da Página
st.set_page_config(
    page_title="📋 Tabela Completa",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🎨 Estilo CSS Personalizado (Responsivo)
st.markdown(
    """
    <style>
        h1, h2, h3 {
            color: #2C3E50;
            text-align: center;
            font-weight: bold;
        }
        .linha {
            border-top: 2px dashed #ccc;
            margin: 20px 10px;
        }
        .ag-theme-streamlit .ag-header {
            background-color: #2C3E50 !important;
            color: white !important;
            font-size: 16px !important;
        }
        .ag-theme-streamlit .ag-row {
            font-size: 14px !important;
        }
        .ag-theme-streamlit {
            height: auto;
            max-height: 600px;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        /* Responsividade para dispositivos móveis */
        @media screen and (max-width: 768px) {
            .ag-theme-streamlit {
                font-size: 12px !important;
            }
            .stButton > button {
                font-size: 14px !important;
                padding: 10px !important;
            }
            h1, h2 {
                font-size: 20px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🏷️ Título da Página
st.title("📋 Tabela Completa")
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# 📊 Carregar os Dados
df = carregar_dados()

# 📌 Verificar se os dados foram carregados corretamente
if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
    st.stop()  # Interrompe a execução se não houver dados

# 🔍 Exibir os dados como DataFrame no Streamlit
st.dataframe(df, use_container_width=True)

# 🛠️ Personalizar as Opções da Tabela
builder = GridOptionsBuilder.from_dataframe(df)
builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=15)
builder.configure_side_bar()  # Adiciona barra lateral para filtros
builder.configure_column(
    "Posição", sortable=True, filter=True, headerCheckboxSelection=True, checkboxSelection=True
)
builder.configure_column(
    "Observação", editable=True, filter=True, cellStyle={"color": "#333", "backgroundColor": "#FFD700"}
)

grid_options = builder.build()

# 🖥️ Renderizar a Tabela com Ag-Grid
st.subheader("🔍 **Dados Detalhados**")
AgGrid(
    df,
    gridOptions=grid_options,
    height=600,
    theme="streamlit",  # Temas disponíveis: "streamlit", "light", "dark", "blue", "fresh"
    enable_enterprise_modules=True,
    fit_columns_on_grid_load=True,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
    allow_unsafe_jscode=True,  # Permite estilos personalizados
)

# 🔹 Linha Divisória
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# 📥 Botão para exportar os dados como CSV
st.download_button(
    label="📥 Baixar Dados como CSV",
    data=df.to_csv(index=False, sep=";", encoding="utf-8"),
    file_name="tabela_completa.csv",
    mime="text/csv",
)
