import streamlit as st
import plotly.express as px
import pandas as pd
from utils.helpers import carregar_dados, load_css
from auth import login

# Verifica login antes de carregar qualquer conteúdo
if not st.session_state.get("logado", False):
    login()
    st.stop()

# Configuração da Página
st.set_page_config(
    page_title="📊 Análise por Piso",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Carrega o CSS centralizado
load_css("styles/style.css")

# Adiciona a classe de corpo específica da página
st.markdown('<div class="analise-piso-body">', unsafe_allow_html=True)

# Carrega os dados com feedback visual e tratamento de exceção
with st.spinner("Carregando dados..."):
    try:
        df = carregar_dados(st.session_state.get("uploaded_file"))
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.stop()

if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
    st.stop()

# Barra Lateral - Filtros
st.sidebar.title("📅 Filtros")
st.sidebar.markdown("Selecione as datas para comparação:")
datas_disponiveis = sorted(df["Data"].dt.strftime("%d/%m/%Y").unique())
col1, col2 = st.sidebar.columns(2)
data_1 = col1.selectbox("Data 1", datas_disponiveis, index=0)
data_2 = col2.selectbox("Data 2", datas_disponiveis, index=1)

# Filtra os dados conforme as datas selecionadas
df_data1 = df[df["Data"] == pd.to_datetime(data_1, format="%d/%m/%Y")]
df_data2 = df[df["Data"] == pd.to_datetime(data_2, format="%d/%m/%Y")]

# Cabeçalho da Página e Separador
st.title("📊 Análise por Piso")
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Função para exibir os KPIs com layout aprimorado
def exibir_kpi(titulo, valor, detalhe, icon_url):
    st.markdown(
        f"""
        <div class='kpi'>
            <img class='kpi-icon' src='{icon_url}' width='50'/>
            <div>
                <h5>{titulo}</h5>
                <h3>{valor}</h3>
                <p>{detalhe}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if df_data1.empty or df_data2.empty:
    st.warning("⚠️ Dados insuficientes para análise nas datas selecionadas.")
    st.stop()

# Cálculo dos KPIs para o piso mais crítico em cada data
piso_critico_data1 = df_data1["Piso"].value_counts().idxmax()
piso_critico_data2 = df_data2["Piso"].value_counts().idxmax()

posicao_critica_data1 = df_data1[df_data1["Piso"] == piso_critico_data1]["Posição"].value_counts().idxmax()
observacao_critica_data1 = df_data1[df_data1["Piso"] == piso_critico_data1]["Observação"].value_counts().idxmax()

posicao_critica_data2 = df_data2[df_data2["Piso"] == piso_critico_data2]["Posição"].value_counts().idxmax()
observacao_critica_data2 = df_data2[df_data2["Piso"] == piso_critico_data2]["Observação"].value_counts().idxmax()

# Exibição dos KPIs em duas colunas
st.subheader("📈 Indicadores Chave de Desempenho (KPIs)")
kpi_col1, kpi_col2 = st.columns(2)
with kpi_col1:
    exibir_kpi(
        f"Piso Crítico ({data_1})",
        piso_critico_data1,
        f"Posição: {posicao_critica_data1} | Obs: {observacao_critica_data1}",
        "https://img.icons8.com/color/48/floor-plan.png",
    )
with kpi_col2:
    exibir_kpi(
        f"Piso Crítico ({data_2})",
        piso_critico_data2,
        f"Posição: {posicao_critica_data2} | Obs: {observacao_critica_data2}",
        "https://img.icons8.com/color/48/floor-plan.png",
    )

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Gráfico Comparativo de Ocorrências por Piso
piso_comparativo = pd.concat([
    df_data1["Piso"].value_counts().rename(f"Ocorrências ({data_1})"),
    df_data2["Piso"].value_counts().rename(f"Ocorrências ({data_2})")
], axis=1).fillna(0).reset_index().rename(columns={"index": "Piso"})

fig_piso = px.bar(
    piso_comparativo,
    x="Piso",
    y=[f"Ocorrências ({data_1})", f"Ocorrências ({data_2})"],
    barmode="group",
    title="Comparativo de Ocorrências por Piso",
    text_auto=True,
    template="plotly_dark"
)
fig_piso.update_layout(
    xaxis_title="Piso",
    yaxis_title="Total de Ocorrências",
    legend_title="Datas",
    height=500,
    margin=dict(l=40, r=40, t=40, b=40),
)
st.plotly_chart(fig_piso, use_container_width=True)

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Detalhamento por Piso
st.subheader("🔍 Detalhamento por Piso")
piso_selecionado = st.selectbox("Selecione um Piso para detalhar:", sorted(df["Piso"].unique()))

if piso_selecionado:
    df_piso = df_data1[df_data1["Piso"] == piso_selecionado]
    if df_piso.empty:
        st.info("Nenhum dado disponível para o piso selecionado na Data 1.")
    else:
        posicao_critica = df_piso["Posição"].value_counts().idxmax()
        observacao_critica = df_piso["Observação"].value_counts().idxmax()
        st.markdown(f"**📍 Posição Crítica no Piso {piso_selecionado}:** `{posicao_critica}`")
        st.markdown(f"**🔎 Observação Crítica no Piso {piso_selecionado}:** `{observacao_critica}`")
        st.dataframe(df_piso[["Posição", "Observação"]].reset_index(drop=True), use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
