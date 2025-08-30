import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from utils.helpers import carregar_dados, load_css
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

# Carrega o CSS centralizado
load_css("styles/style.css")

# Título da Página
st.markdown('<div class="tabela-completa-body">', unsafe_allow_html=True)
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

st.markdown('</div>', unsafe_allow_html=True)
