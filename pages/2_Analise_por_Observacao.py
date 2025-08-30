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

# 🎨 Estilização CSS personalizada para um layout mais elegante e tipografia aprimorada
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap');
        
        body {
            font-family: 'Montserrat', sans-serif;
            background: linear-gradient(to right, #ece9e6, #ffffff);
            color: #2C3E50;
        }
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
        /* Estilização customizada dos cards de KPI com efeito 3D, hover e cores profissionais */
        .kpi-card {
            background-color: #ffffff;
            border: 2px solid #d1dce5;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            text-align: center;
        }
        .kpi-card:hover {
            transform: scale(1.05);
            box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
        }
        .kpi-icon {
            font-size: 40px;
            margin-bottom: 10px;
            color: #2980b9;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.15);
        }
        .kpi-title {
            font-size: 16px;
            color: #34495e;
            text-align: center;
            margin-bottom: 10px;
            font-weight: 600;
        }
        .kpi-value {
            font-size: 26px;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Função para exibir os KPIs como cards bonitos com ícones profissionais
def display_kpi(label, value, icon):
    html = f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-title">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# 🏷️ Título da Página
st.title("📊 Comparação de Observações por Data")

# 📊 Carregar os dados
df = carregar_dados(st.session_state.get("uploaded_file"))

# 📌 Verificar se os dados foram carregados corretamente
if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
    st.stop()  # Interrompe a execução se não houver dados

# 📅 Barra lateral para filtros
st.sidebar.title("📅 Filtros")
datas_disponiveis = sorted(df["Data"].dt.strftime("%d/%m/%Y").unique())
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

# 🚀 Função para obter a observação/posição mais crítica
def obter_mais_critico(df, coluna):
    return df[coluna].value_counts().idxmax() if not df[coluna].empty else "N/A"

observacao_critica_data1 = obter_mais_critico(df_data1, "Observação")
posicao_critica_data1 = obter_mais_critico(df_data1, "Posição")
observacao_critica_data2 = obter_mais_critico(df_data2, "Observação")
posicao_critica_data2 = obter_mais_critico(df_data2, "Posição")

# 🚨 Exibir KPIs com cards customizados, ícones e novo layout tipográfico
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)
st.subheader("🚨 **Principais Ofensores (KPIs)**")

col1, col2, col3, col4 = st.columns(4)
with col1:
    display_kpi(f"Obs. Mais Crítica ({data1})", observacao_critica_data1, '<i class="fas fa-exclamation-circle"></i>')
with col2:
    display_kpi(f"Posição Mais Crítica ({data1})", posicao_critica_data1, '<i class="fas fa-map-pin"></i>')
with col3:
    display_kpi(f"Obs. Mais Crítica ({data2})", observacao_critica_data2, '<i class="fas fa-exclamation-circle"></i>')
with col4:
    display_kpi(f"Posição Mais Crítica ({data2})", posicao_critica_data2, '<i class="fas fa-map-pin"></i>')

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# 📊 Gráficos de barras lado a lado com textos mais visíveis
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
        xaxis=dict(
            title="Total de Ocorrências", 
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title="Observações", 
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        height=500,
        margin=dict(l=100, r=50, t=50, b=50)
    )
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        textfont=dict(color="black", size=12)
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
