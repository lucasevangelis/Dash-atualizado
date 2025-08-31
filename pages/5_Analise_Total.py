import streamlit as st
import plotly.express as px
import pandas as pd
from utils.helpers import carregar_dados, load_css
import auth  # ✅ Verificação de login

# Verifica login antes de carregar qualquer conteúdo
if not st.session_state.get("logado", False):
    auth.login()
    st.stop()

# Configuração da Página
st.set_page_config(
    page_title="📊 Análise Total",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Carrega o CSS centralizado
load_css("styles/style.css")

# Carregar os Dados
df = carregar_dados(st.session_state.get("uploaded_file"))

# Filtros de Comparação no Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Filtros de Comparação")
    meses_unicos = df["Data"].dt.strftime("%Y-%m").unique()
    mes_filtro = st.multiselect("📆 Selecione os meses para comparar", meses_unicos)
    dias_unicos = df["Data"].dt.strftime("%d-%m-%Y").unique()
    dia_filtro = st.multiselect("📅 Selecione os dias para comparar", dias_unicos)

df_filtrado = df.copy()
if mes_filtro:
    df_filtrado = df_filtrado[df_filtrado["Data"].dt.strftime("%Y-%m").isin(mes_filtro)]
if dia_filtro:
    df_filtrado = df_filtrado[df_filtrado["Data"].dt.strftime("%d-%m-%Y").isin(dia_filtro)]

if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique o arquivo CSV.")
    st.stop()

# Função para ajustar os gráficos
def ajustar_grafico(fig):
    fig.update_layout(
        title_font_size=22,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
        legend_title_font_size=18,
        legend_font_size=16,
        margin=dict(l=20, r=20, t=50, b=20),
        template="plotly_dark",
        hoverlabel=dict(font_size=16),
        scene=dict(camera=dict(eye=dict(x=1.2, y=1.2, z=1.2)))
    )
    fig.update_traces(marker=dict(line=dict(width=1.5, color='DarkSlateGrey')), selector=dict(type="bar"))
    fig.update_traces(marker=dict(line=dict(width=2, color='black')), selector=dict(type="pie"))
    return fig

# Função para Exibir KPIs com o novo estilo unificado
def exibir_kpi(titulo, valor, icon):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div>
                <div class="kpi-title">{titulo}</div>
                <div class="kpi-value">{valor}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Cálculo dos KPIs
piso_critico = df_filtrado["Piso"].value_counts().idxmax()
posicao_critica = df_filtrado["Posição"].value_counts().idxmax()
data_critica = df_filtrado["Data"].value_counts().idxmax().strftime("%d/%m/%Y")
observacao_critica = df_filtrado["Observação"].value_counts().idxmax()
total_posicoes = len(df_filtrado["Posição"])
total_observacoes = len(df_filtrado["Observação"])

st.subheader("📈 Indicadores Chave de Performance")
kpi_row1_col1, kpi_row1_col2, kpi_row1_col3 = st.columns(3)
kpi_row2_col1, kpi_row2_col2, kpi_row2_col3 = st.columns(3)

with kpi_row1_col1:
    exibir_kpi("Piso Mais Crítico", piso_critico, "🏢")
with kpi_row1_col2:
    exibir_kpi("Posição Mais Crítica", posicao_critica, "📍")
with kpi_row1_col3:
    exibir_kpi("Data Mais Crítica", data_critica, "📅")
with kpi_row2_col1:
    exibir_kpi("Observação Mais Crítica", observacao_critica, "❗️")
with kpi_row2_col2:
    exibir_kpi("Total de Posições", f"{total_posicoes:,}", "🔢")
with kpi_row2_col3:
    exibir_kpi("Total de Observações", f"{total_observacoes:,}", "🔢")

st.markdown("<div class='linha'></div>", unsafe_allow_html=True)

# Gráficos de Distribuição
st.subheader("📊 Distribuição de Ocorrências")
col1, col2 = st.columns(2)

with col1:
    piso_data = df_filtrado["Piso"].value_counts().reset_index()
    piso_data.columns = ["Piso", "Total"]
    fig_pizza_piso = px.pie(
        piso_data, names="Piso", values="Total", title="📍 Distribuição de Ocorrências por Piso", 
        hole=0.3, color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_pizza_piso.update_traces(pull=[0.1] * len(piso_data), textinfo="percent+label", hoverinfo="label+percent", scalegroup='one')
    st.plotly_chart(ajustar_grafico(fig_pizza_piso), use_container_width=True)

with col2:
    observacao_data = df_filtrado["Observação"].value_counts().nlargest(5).reset_index()
    observacao_data.columns = ["Observação", "Total"]
    fig_pizza_obs = px.pie(
        observacao_data, names="Observação", values="Total", title="⚠️ Top 5 Observações Mais Críticas", 
        hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pizza_obs.update_traces(pull=[0.1] * len(observacao_data), textinfo="percent+label", hoverinfo="label+percent", scalegroup='one')
    st.plotly_chart(ajustar_grafico(fig_pizza_obs), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    mes_data = df_filtrado["Data"].dt.strftime("%Y-%m").value_counts().reset_index()
    mes_data.columns = ["Mês", "Total"]
    fig_bar_mes = px.bar(
        mes_data, x="Mês", y="Total", title="📆 Ocorrências por Mês", 
        color="Mês", color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar_mes.update_traces(marker=dict(line=dict(width=1.5, color='DarkSlateGrey')), hoverinfo="x+y")
    st.plotly_chart(ajustar_grafico(fig_bar_mes), use_container_width=True)

with col2:
    dia_data = df_filtrado["Data"].dt.strftime("%d-%m-%Y").value_counts().reset_index()
    dia_data.columns = ["Dia", "Total"]
    fig_bar_dia = px.bar(
        dia_data, x="Dia", y="Total", title="📅 Ocorrências por Dia", 
        color="Dia", color_discrete_sequence=px.colors.qualitative.Pastel1
    )
    fig_bar_dia.update_traces(marker=dict(line=dict(width=1.5, color='DarkSlateGrey')), hoverinfo="x+y")
    st.plotly_chart(ajustar_grafico(fig_bar_dia), use_container_width=True)
