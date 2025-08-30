import streamlit as st
import pandas as pd
from utils.helpers import carregar_dados, load_css
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

# Carrega o CSS centralizado
load_css("styles/style.css")

# Adiciona a classe de corpo específica da página
st.markdown('<div class="analise-posicao-body">', unsafe_allow_html=True)


# Função para exibir uma tabela estilizada sem índice
def display_styled_table(df):
    html = df.to_html(index=False, classes="dataframe", border=0)
    st.markdown(html, unsafe_allow_html=True)

# 📊 Carregar os dados
df = carregar_dados(st.session_state.get("uploaded_file"))

# 📌 Verificar se os dados foram carregados corretamente
if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
    st.stop()

# 📅 Barra lateral - Filtro de Data
st.sidebar.title("📅 Filtros")
datas_disponiveis = sorted(df["Data"].dropna().dt.strftime("%d/%m/%Y").unique())  # Converter datas para exibição
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

st.markdown('</div>', unsafe_allow_html=True)
