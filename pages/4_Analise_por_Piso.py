import streamlit as st
import plotly.express as px
import pandas as pd
from utils.helpers import carregar_dados
from auth import login
from utils.helpers import carregar_dados




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

# Estilo CSS para Melhorar o Layout
st.markdown(
    """
    <style>
        h1, h2, h3 {
            color: white;
            text-align: center;
            font-weight: bold;
        }
        .linha {
            border-top: 2px dashed #ccc;
            margin: 20px 0;
        }
        .kpi {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px;
            margin: 5px;
            background-color: #1E1E1E;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .kpi-icon {
            margin-right: 15px;
        }
        .kpi h5 {
            margin: 0;
            font-size: 16px;
            color: #FFD700;
        }
        .kpi h3 {
            margin: 0;
            font-size: 24px;
            color: white;
        }
        .kpi p {
            margin: 5px 0 0;
            font-size: 14px;
            color: #ccc;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


df = carregar_dados()

if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
else:
    st.dataframe(df, use_container_width=True)
    
# Carregar os Dados
df = carregar_dados()

# Barra Lateral - Filtros
st.sidebar.title("📅 Filtros")
datas_disponiveis = sorted(df["Data"].dt.strftime("%d/%m/%Y").unique())
col1, col2 = st.sidebar.columns(2)
data_1 = col1.selectbox("Data 1", datas_disponiveis, index=0)
data_2 = col2.selectbox("Data 2", datas_disponiveis, index=1)

# Filtrar os Dados pelas Datas Selecionadas
df_data1 = df[df["Data"] == pd.to_datetime(data_1, format="%d/%m/%Y")]
df_data2 = df[df["Data"] == pd.to_datetime(data_2, format="%d/%m/%Y")]

# Título da Página
st.title("📊 Análise por Piso")
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Função para Exibir KPIs
def exibir_kpi(titulo, valor, detalhe, icon_url):
    st.markdown(
        f"""
        <div class='kpi'>
            <img class='kpi-icon' src='{icon_url}' width='40'/>
            <div>
                <h5>{titulo}</h5>
                <h3>{valor}</h3>
                <p>{detalhe}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Verificar Disponibilidade de Dados
if df_data1.empty or df_data2.empty:
    st.warning("⚠️ Dados insuficientes para análise. Verifique as datas selecionadas.")
else:
    # KPIs para o Piso Mais Crítico
    piso_critico_data1 = df_data1["Piso"].value_counts().idxmax()
    piso_critico_data2 = df_data2["Piso"].value_counts().idxmax()

    # Determinar a Posição e Observação Mais Críticas
    posicao_critica_data1 = (
        df_data1[df_data1["Piso"] == piso_critico_data1]["Posição"]
        .value_counts()
        .idxmax()
    )
    observacao_critica_data1 = (
        df_data1[df_data1["Piso"] == piso_critico_data1]["Observação"]
        .value_counts()
        .idxmax()
    )

    posicao_critica_data2 = (
        df_data2[df_data2["Piso"] == piso_critico_data2]["Posição"]
        .value_counts()
        .idxmax()
    )
    observacao_critica_data2 = (
        df_data2[df_data2["Piso"] == piso_critico_data2]["Observação"]
        .value_counts()
        .idxmax()
    )

    # Exibir KPIs
    st.subheader("📈 Indicadores Chave de Desempenho (KPIs)")
    kpi_col1, kpi_col2 = st.columns(2)
    with kpi_col1:
        exibir_kpi(
            f"Piso Mais Crítico (Data 1: {data_1})",
            piso_critico_data1,
            f"📍 Posição Crítica: {posicao_critica_data1}\n🔎 Observação: {observacao_critica_data1}",
            "https://img.icons8.com/color/48/floor-plan.png",
        )
    with kpi_col2:
        exibir_kpi(
            f"Piso Mais Crítico (Data 2: {data_2})",
            piso_critico_data2,
            f"📍 Posição Crítica: {posicao_critica_data2}\n🔎 Observação: {observacao_critica_data2}",
            "https://img.icons8.com/color/48/floor-plan.png",
        )

    st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

    # Comparativo de Pisos (Gráfico)
    piso_comparativo = pd.concat(
        [
            df_data1["Piso"].value_counts().rename(f"Ocorrências ({data_1})"),
            df_data2["Piso"].value_counts().rename(f"Ocorrências ({data_2})"),
        ],
        axis=1,
    ).fillna(0).reset_index().rename(columns={"index": "Piso"})

    fig_piso = px.bar(
        piso_comparativo,
        x="Piso",
        y=[f"Ocorrências ({data_1})", f"Ocorrências ({data_2})"],
        barmode="group",
        title="Comparativo de Ocorrências por Piso",
        text_auto=True,
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
        # Posição e Observação mais críticas no piso selecionado
        df_piso = df_data1[df_data1["Piso"] == piso_selecionado]
        posicao_critica = df_piso["Posição"].value_counts().idxmax()
        observacao_critica = df_piso["Observação"].value_counts().idxmax()

        st.write(f"**📍 Posição Mais Crítica no Piso {piso_selecionado}:** `{posicao_critica}`")
        st.write(f"**🔎 Observação Mais Crítica no Piso {piso_selecionado}:** `{observacao_critica}`")

        # Tabela detalhada
        st.dataframe(
            df_piso[["Posição", "Observação"]].reset_index(drop=True),
            use_container_width=True,
        )
