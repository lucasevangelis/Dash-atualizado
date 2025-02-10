import streamlit as st
import pandas as pd
from utils.helpers import carregar_dados
from auth import login

# 🛑 Verifica login antes de carregar qualquer conteúdo
if not st.session_state.get("logado", False):
    login()
    st.stop()

# 🔧 Configuração da Página
st.set_page_config(
    page_title="📍 Análise por Posição",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🎨 Estilização CSS para melhorar a apresentação e responsividade
st.markdown(
    """
    <style>
        h1, h2, h3 {
            color: #2C3E50;
            text-align: center;
            font-weight: bold;
        }
        .linha {
            border-top: 3px solid #ccc;
            margin: 20px 0;
        }
        @media screen and (max-width: 768px) {
            h1, h2, h3 {
                font-size: 18px;
            }
            .stMetric {
                font-size: 14px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 📊 Carregar os dados
df = carregar_dados()

# 📌 Verificar se os dados foram carregados corretamente
if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
    st.stop()  # Interrompe a execução se não houver dados

# 📅 Barra lateral - Filtro de Data
st.sidebar.title("📅 Filtros")
datas_disponiveis = sorted(df["Data"].dt.strftime("%d/%m/%Y").unique())  # Convertendo para string para exibição
data_selecionada = st.sidebar.selectbox("Selecione uma Data", datas_disponiveis)

# 📌 Converter string de data para datetime para filtrar corretamente
data_selecionada_dt = pd.to_datetime(data_selecionada, format="%d/%m/%Y")

# 🔍 Filtrar os dados pela data selecionada
df_filtrado = df[df["Data"] == data_selecionada_dt]

# 🏷️ Título da Página
st.title("📍 Análise por Posição")
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# 🚨 Verificar se há dados disponíveis
if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado para a data selecionada.")
    st.stop()

# 🏆 **Top 10 Posições Mais Repetidas**
st.subheader(f"🏆 **Top 10 Posições Mais Repetidas ({data_selecionada})**")

posicao_data = df_filtrado["Posição"].value_counts().head(10).reset_index()
posicao_data.columns = ["Posição", "Total"]

# 📊 Exibir a tabela estilizada
st.dataframe(
    posicao_data,
    use_container_width=True,
    height=400,
)

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# 🔍 **Detalhamento por Posição Selecionada**
st.subheader("🔎 Detalhamento por Posição")

# 🎯 Criar um Dropdown para Selecionar uma Posição
posicao_selecionada = st.selectbox(
    "Selecione uma Posição para visualizar as Observações:",
    posicao_data["Posição"],
    help="Escolha uma posição para ver suas observações associadas.",
)

# 📌 Filtrar Observações para a Posição Selecionada
if posicao_selecionada:
    observacoes = df_filtrado[df_filtrado["Posição"] == posicao_selecionada][["Observação", "Piso"]]

    # 📍 Exibir as Informações
    st.write(f"**📍 Posição Selecionada:** `{posicao_selecionada}`")
    st.write(f"**📊 Total de Observações Encontradas:** `{len(observacoes)}`")

    # 📊 Exibir a Tabela sem Índice
    st.dataframe(
        observacoes.reset_index(drop=True),
        use_container_width=True,
        height=400,
    )
