import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from utils.helpers import carregar_dados
from auth import login


# Verifica login antes de carregar qualquer conteúdo
if not st.session_state.get("logado", False):
    login()
    st.stop()

# Configuração da Página
st.set_page_config(
    page_title="Tabela Completa",
     page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS Customizado para um visual ainda mais bonito e sofisticado
st.markdown(
    """
    <style>
        /* Importa a fonte do Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap');
        :root {
            --primary-color: #0D0D0D;
            --accent-gradient: linear-gradient(45deg, #FF6B6B, #FFD93D);
            --text-color: #F0F0F0;
            --header-bg: #1A1A1A;
            --border-color: #444;
            --button-text: #FFFFFF;
            --card-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
            --hover-scale: 1.05;
            --transition-speed: 0.3s;
        }
        body {
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            font-family: 'Roboto Condensed', sans-serif;
            margin: 0;
            padding: 0;
        }
        h1, h2, h3 {
            color: var(--text-color);
            text-align: center;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .linha {
            border-top: 3px solid var(--accent-gradient);
            margin: 30px 10px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; }
            100% { opacity: 0.7; }
        }
        /* Estilização do AgGrid */
        .ag-theme-streamlit {
            height: auto;
            max-height: 650px;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: var(--card-shadow);
            border: 2px solid var(--border-color);
        }
        .ag-theme-streamlit .ag-header {
            background-color: var(--header-bg) !important;
            color: var(--text-color) !important;
            font-size: 18px !important;
            font-weight: 700;
        }
        .ag-theme-streamlit .ag-row {
            font-size: 16px !important;
            color: var(--text-color);
        }
        /* Customização do botão de download */
        div.stDownloadButton button {
            background: var(--accent-gradient);
            color: var(--button-text);
            border: none;
            padding: 14px 28px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: transform var(--transition-speed), box-shadow var(--transition-speed);
            display: block;
            margin: 20px auto;
        }
        div.stDownloadButton button:hover {
            transform: scale(var(--hover-scale));
            box-shadow: 0px 10px 20px rgba(255, 107, 107, 0.5);
        }
        /* Customização da sidebar */
        .sidebar .sidebar-content {
            background-color: var(--header-bg);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título da Página
st.title("Tabela Completa")
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Carregar os Dados
df = carregar_dados(st.session_state.get("uploaded_file"))
if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
    st.stop()

# Configurar as opções do AgGrid para uma experiência interativa
builder = GridOptionsBuilder.from_dataframe(df)
builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=15)
builder.configure_side_bar()  # Barra lateral para filtros
builder.configure_column(
    "Posição", sortable=True, filter=True, headerCheckboxSelection=True, checkboxSelection=True
)
builder.configure_column(
    "Observação", editable=True, filter=True, cellStyle={"color": "#333", "backgroundColor": "#FFD93D"}
)
grid_options = builder.build()

st.subheader("🔍 Dados Detalhados")
AgGrid(
    df,
    gridOptions=grid_options,
    height=650,
    theme="streamlit",
    enable_enterprise_modules=True,
    fit_columns_on_grid_load=True,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
    allow_unsafe_jscode=True,
)

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Botão para exportar os dados como CSV com visual impactante
st.download_button(
    label="📥 Baixar Dados como CSV",
    data=df.to_csv(index=False, sep=";", encoding="utf-8"),
    file_name="tabela_completa.csv",
    mime="text/csv",
    key="download-csv",
    help="Clique para baixar a tabela completa em formato CSV"
)
