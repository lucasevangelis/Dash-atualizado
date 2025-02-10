import streamlit as st
import pandas as pd
import plotly.express as px
import auth
from utils.helpers import carregar_dados

# 🛑 Verifica login antes de carregar qualquer conteúdo
if not st.session_state.get("logado", False):
    auth.login()
    st.stop()

# 🔧 Configuração inicial da página
st.set_page_config(
    page_title="📊 Comparação por Observação",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🎨 Estilização CSS personalizada para responsividade
st.markdown(
    """
    <style>
        h1, h2, h3 {
            text-align: center;
            color: #2C3E50;
        }
        .linha {
            border-top: 3px dashed #ccc;
            margin: 20px 0;
        }
        .stMetric {
            text-align: center;
        }
        @media screen and (max-width: 768px) {
            h1, h2, h3 {
                font-size: 20px;
            }
            .stMetric {
                font-size: 14px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🏷️ Título da Página
st.title("📊 Comparação de Observações por Data")

# 📊 Carregar os dados
df = carregar_dados()

# 📌 Verificar se os dados foram carregados corretamente
if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
    st.stop()  # Interrompe a execução se não houver dados

# 📅 Barra lateral para filtros
st.sidebar.title("📅 Filtros")
datas_disponiveis = sorted(df["Data"].dt.strftime("%d/%m/%Y").unique())  # Convertendo para string para exibição
data1 = st.sidebar.selectbox("Selecione a 1ª Data", datas_disponiveis, key="data1")
data2 = st.sidebar.selectbox("Selecione a 2ª Data", datas_disponiveis, key="data2")

# 🚨 Verificar se as duas datas são iguais
if data1 == data2:
    st.warning("⚠️ As duas datas selecionadas são iguais. Por favor, escolha datas diferentes para comparação.")
    st.stop()

# 📌 Converter strings de data para datetime para filtrar corretamente
data1_dt = pd.to_datetime(data1, format="%d/%m/%Y")
data2_dt = pd.to_datetime(data2, format="%d/%m/%Y")

# 🔍 Filtrar os dados para as duas datas selecionadas
df_data1 = df[df["Data"] == data1_dt]
df_data2 = df[df["Data"] == data2_dt]

if df_data1.empty or df_data2.empty:
    st.warning("⚠️ Nenhum dado encontrado para uma das datas selecionadas.")
    st.stop()

# 🚀 KPIs: Observação e Posição mais críticas
def obter_mais_critico(df, coluna):
    return df[coluna].value_counts().idxmax() if not df[coluna].empty else "N/A"

observacao_critica_data1 = obter_mais_critico(df_data1, "Observação")
posicao_critica_data1 = obter_mais_critico(df_data1, "Posição")
observacao_critica_data2 = obter_mais_critico(df_data2, "Observação")
posicao_critica_data2 = obter_mais_critico(df_data2, "Posição")

# 🚨 Exibir KPIs
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)
st.subheader("🚨 **Principais Ofensores (KPIs)**")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label=f"🔍 Obs. Mais Crítica ({data1})", value=observacao_critica_data1)
with col2:
    st.metric(label=f"📍 Posição Mais Crítica ({data1})", value=posicao_critica_data1)
with col3:
    st.metric(label=f"🔍 Obs. Mais Crítica ({data2})", value=observacao_critica_data2)
with col4:
    st.metric(label=f"📍 Posição Mais Crítica ({data2})", value=posicao_critica_data2)

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# 📊 Gráficos de barras lado a lado
st.subheader("📊 **Top 10 Observações por Data**")

def criar_grafico_observacoes(df, data):
    obs_data = df["Observação"].value_counts().head(10).reset_index()
    obs_data.columns = ["Observação", "Total"]
    fig = px.bar(
        obs_data,
        x="Total",
        y="Observação",
        orientation="h",
        color="Observação",
        title=f"Top 10 Observações - {data}",
        text="Total",
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )
    fig.update_layout(
        title_font=dict(size=16),
        xaxis=dict(title="Total de Ocorrências", title_font=dict(size=14)),
        yaxis=dict(title="Observações", title_font=dict(size=14)),
        height=500,
    )
    return fig

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(criar_grafico_observacoes(df_data1, data1), use_container_width=True)

with col2:
    st.plotly_chart(criar_grafico_observacoes(df_data2, data2), use_container_width=True)

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# 🔍 Detalhamento por Observação
st.subheader("🔍 **Detalhamento por Observação**")

observacao_selecionada = st.selectbox(
    "Selecione uma Observação para comparar as Posições:",
    df["Observação"].unique(),
    help="Escolha uma observação para visualizar as posições relacionadas em ambas as datas.",
)

if observacao_selecionada:
    posicoes_data1 = df_data1[df_data1["Observação"] == observacao_selecionada][["Posição", "Piso"]]
    posicoes_data2 = df_data2[df_data2["Observação"] == observacao_selecionada][["Posição", "Piso"]]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**📅 Posições - {data1}**")
        st.dataframe(posicoes_data1.reset_index(drop=True), use_container_width=True, height=400)

    with col2:
        st.markdown(f"**📅 Posições - {data2}**")
        st.dataframe(posicoes_data2.reset_index(drop=True), use_container_width=True, height=400)
