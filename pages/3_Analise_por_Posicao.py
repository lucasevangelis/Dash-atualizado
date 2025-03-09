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

# 🎨 Estilização CSS para um layout mais bonito, tipografia elegante e tabelas com visual UX aprimorado
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap');
        
        body {
            font-family: 'Montserrat', sans-serif;
            background: #f8f9fa;
            color: #2C3E50;
        }
        h1, h2, h3 {
            text-align: center;
            color: #2C3E50;
            font-weight: 600;
        }
        .linha {
            border-top: 3px solid #ccc;
            margin: 20px 0;
        }
        /* Estilização customizada para tabelas com visual moderno e UX aprimorado */
        table.dataframe {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 14px;
        }
        table.dataframe thead tr {
            background-color: #2980b9;
            color: #ffffff;
            text-align: center;
        }
        table.dataframe tbody tr {
            color: #2C3E50;
        }
        table.dataframe tbody tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        table.dataframe tbody tr:hover {
            background-color: #e6f2ff;
        }
        table.dataframe th, table.dataframe td {
            padding: 12px 15px;
            text-align: center;
            color: inherit;
        }
        /* Ajustes responsivos */
        @media screen and (max-width: 768px) {
            h1, h2, h3 {
                font-size: 18px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Função para exibir uma tabela estilizada sem índice
def display_styled_table(df):
    html = df.to_html(index=False, classes="dataframe", border=0)
    st.markdown(html, unsafe_allow_html=True)

# 📊 Carregar os dados
df = carregar_dados()

# 📌 Verificar se os dados foram carregados corretamente
if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
    st.stop()

# 📅 Barra lateral - Filtro de Data
st.sidebar.title("📅 Filtros")
datas_disponiveis = sorted(df["Data"].dt.strftime("%d/%m/%Y").unique())  # Converter datas para exibição
data_selecionada = st.sidebar.selectbox("Selecione uma Data", datas_disponiveis)

# 📌 Converter a string de data para datetime para filtrar corretamente
data_selecionada_dt = pd.to_datetime(data_selecionada, format="%d/%m/%Y")

# 🔍 Filtrar os dados pela data selecionada
df_filtrado = df[df["Data"] == data_selecionada_dt]

# 🏷️ Título da Página
st.title("📍 Análise por Posição")
st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# 🚨 Verificar se há dados disponíveis para a data
if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado para a data selecionada.")
    st.stop()

# 🏆 Top 10 Posições Mais Repetidas
st.subheader(f"🏆 Top 10 Posições Mais Repetidas ({data_selecionada})")

posicao_data = df_filtrado["Posição"].value_counts().head(10).reset_index()
posicao_data.columns = ["Posição", "Total"]

# Exibe a tabela estilizada em HTML para melhor visualização
display_styled_table(posicao_data)

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# 🔍 Detalhamento por Posição Selecionada
st.subheader("🔎 Detalhamento por Posição")

# Dropdown para selecionar uma posição
posicao_selecionada = st.selectbox(
    "Selecione uma Posição para visualizar as Observações:",
    posicao_data["Posição"],
    help="Escolha uma posição para ver suas observações associadas."
)

# Filtrar as observações para a posição selecionada
if posicao_selecionada:
    observacoes = df_filtrado[df_filtrado["Posição"] == posicao_selecionada][["Observação", "Piso"]]
    
    # 🔽 MELHORIA NA EXIBIÇÃO DAS INFORMAÇÕES (ANTES era apenas st.write)
    # Agora exibimos com ícones e um layout mais agradável:
    st.markdown(
        f"""
        <div style="margin: 10px 0;">
            <span style="font-size: 1.2rem;">🔴</span>
            <strong style="font-size: 1rem; color: #2C3E50; margin-left: 8px;">
                Posição Selecionada:
            </strong>
            <span style="font-size: 1rem; color: #2C3E50; margin-left: 5px;">
                {posicao_selecionada}
            </span>
        </div>
        <div style="margin: 10px 0;">
            <span style="font-size: 1.2rem;">📊</span>
            <strong style="font-size: 1rem; color: #2C3E50; margin-left: 8px;">
                Total de Observações Encontradas:
            </strong>
            <span style="font-size: 1rem; color: #2C3E50; margin-left: 5px;">
                {len(observacoes)}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Exibe a tabela de observações estilizada
    display_styled_table(observacoes)
