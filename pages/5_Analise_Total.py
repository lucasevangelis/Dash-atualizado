import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import carregar_dados
import pandas as pd
import auth  # ✅ Corrigido
from utils.helpers import carregar_dados




# 📌 Verifica login antes de carregar qualquer conteúdo
if not st.session_state.get("logado", False):
    auth.login()
    st.stop()



# Configuração da Página
st.set_page_config(
    page_title="📊 Análise Total",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo CSS para Melhorar o Layout
st.markdown(
    """
    <style>
        /* Estilo do Título e Subtítulos */
        h1, h2, h3 {
            color: white;
            text-align: center;
            font-weight: bold;
        }

        /* Linha divisória */
        .linha {
            border-top: 2px dashed #ccc;
            margin: 20px 0;
        }

        /* KPIs customizados */
        .kpi {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            margin: 10px;
            background: linear-gradient(145deg, #1E1E1E, #2A2A2A);
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        }
        .kpi-icon {
            margin-right: 20px;
        }
        .kpi h5 {
            margin: 0;
            font-size: 18px;
            color: #FFD700;
        }
        .kpi h3 {
            margin: 0;
            font-size: 26px;
            color: white;
        }
        .kpi p {
            margin: 5px 0 0;
            font-size: 14px;
            color: #ddd;
        }

        /* Estilo dos gráficos */
        .plotly-graph {
            margin: 20px 0;
            border: 2px solid #2A2A2A;
            border-radius: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Carregar os Dados
df = carregar_dados()

# Título da Página
st.title("📊 Análise Total")
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Função para Exibir KPIs
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

    df = carregar_dados()

if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
else:
    st.dataframe(df, use_container_width=True)

# Calcular KPIs
piso_critico = df["Piso"].value_counts().idxmax()
posicao_critica = df["Posição"].value_counts().idxmax()
data_critica = df["Data"].value_counts().idxmax().strftime("%d/%m/%Y")
observacao_critica = df["Observação"].value_counts().idxmax()

# Exibir KPIs
st.subheader("📈 Indicadores Chave de Desempenho (KPIs)")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
with kpi_col1:
    exibir_kpi(
        "Piso Mais Crítico",
        piso_critico,
        "Piso com maior quantidade de ocorrências.",
        "https://img.icons8.com/color/48/floor-plan.png",
    )
with kpi_col2:
    exibir_kpi(
        "Posição Mais Crítica",
        posicao_critica,
        "Posição mais recorrente nos dados.",
        "https://img.icons8.com/color/48/marker.png",
    )
with kpi_col3:
    exibir_kpi(
        "Data Mais Crítica",
        data_critica,
        "Data com maior número de ocorrências.",
        "https://img.icons8.com/color/48/calendar.png",
    )
with kpi_col4:
    exibir_kpi(
        "Observação Mais Crítica",
        observacao_critica,
        "Observação mais registrada.",
        "https://img.icons8.com/color/48/idea.png",
    )

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Gráfico de Pizza - Representação por Piso
st.subheader("🍕 Distribuição de Ocorrências por Piso")
piso_data = df["Piso"].value_counts().reset_index()
piso_data.columns = ["Piso", "Total"]

fig_pizza = px.pie(
    piso_data,
    names="Piso",
    values="Total",
    title="Distribuição de Ocorrências por Piso",
    color_discrete_sequence=px.colors.sequential.Tealgrn,
    hole=0.4,
)
fig_pizza.update_traces(
    textinfo="percent+label",
    pull=[0.1, 0.05, 0, 0.05],  # Destaca os setores
    hoverinfo="label+percent+value",
)
fig_pizza.update_layout(
    height=500,
    margin=dict(l=40, r=40, t=40, b=40),
    legend_title="Pisos",
    font=dict(size=14),
)
st.plotly_chart(fig_pizza, use_container_width=True)

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Gráfico de Tendência - Melhora ou Piora
st.subheader("📈 Tendência de Ocorrências")
tendencia = df.groupby("Data").size().reset_index(name="Ocorrências")
fig_tendencia = px.line(
    tendencia,
    x="Data",
    y="Ocorrências",
    title="Tendência Geral de Ocorrências",
    markers=True,
    line_shape="spline",
)
fig_tendencia.update_traces(
    line=dict(width=4, color="#FFD700"),
    marker=dict(size=10, symbol="circle"),
)
fig_tendencia.update_layout(
    xaxis_title="Data",
    yaxis_title="Total de Ocorrências",
    legend_title="Tendência",
    height=500,
    font=dict(size=14),
    margin=dict(l=40, r=40, t=40, b=40),
)
st.plotly_chart(fig_tendencia, use_container_width=True)

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Tabela de Dados Detalhados
st.subheader("📋 Dados Detalhados")
st.dataframe(df, use_container_width=True, height=400)
