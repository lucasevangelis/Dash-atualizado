import streamlit as st
import plotly.express as px
import pandas as pd
from utils.helpers import carregar_dados
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

# Estilo CSS para Layout Moderno com Efeito Espelhado Aprimorado
def aplicar_estilo():
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
            .kpi-container { 
                display: flex; 
                flex-wrap: wrap; 
                justify-content: space-around; 
            }
            .kpi {
                display: flex; 
                align-items: center; 
                justify-content: space-between;
                padding: 20px; 
                margin: 10px;
                background: linear-gradient(145deg, #1E1E1E, #2A2A2A);
                border-radius: 15px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
                color: white;
                text-align: center;
                width: 100%;
                transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                position: relative;
                overflow: hidden;
            }
            .kpi:hover {
                transform: scale(1.05);
                box-shadow: 0 10px 20px rgba(255, 215, 0, 0.8);
            }
            /* Efeito espelhado aprimorado: reflexão com desvanecimento */
            .espelhado::after {
                content: "";
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                height: 100%;
                background: inherit;
                transform: scaleY(-1);
                opacity: 0.2;
                pointer-events: none;
                filter: blur(2px);
                mask-image: linear-gradient(to bottom, rgba(0,0,0,1), rgba(0,0,0,0));
            }
            /* Customização da sidebar */
            .sidebar .block-container {
                background: #2A2A2A;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
            }
            .sidebar .stMultiSelect, .sidebar .stButton {
                color: white;
                background: linear-gradient(145deg, #1E1E1E, #3A3A3A);
                border-radius: 8px;
                padding: 10px;
            }
            .sidebar .stButton:hover {
                background: linear-gradient(145deg, #3A3A3A, #1E1E1E);
                transform: scale(1.05);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

aplicar_estilo()

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

# Função para Exibir KPIs com efeito espelhado
def exibir_kpi(titulo, valor, detalhe, icon_url):
    st.markdown(
        f"""
        <div class='kpi espelhado'>
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

# Cálculo dos KPIs
piso_critico = df_filtrado["Piso"].value_counts().idxmax()
posicao_critica = df_filtrado["Posição"].value_counts().idxmax()
data_critica = df_filtrado["Data"].value_counts().idxmax().strftime("%d/%m/%Y")
observacao_critica = df_filtrado["Observação"].value_counts().idxmax()
total_posicoes = len(df_filtrado["Posição"])
total_observacoes = len(df_filtrado["Observação"])

st.subheader("📈 KPIs")
kpi_row1_col1, kpi_row1_col2, kpi_row1_col3 = st.columns(3)
kpi_row2_col1, kpi_row2_col2, kpi_row2_col3 = st.columns(3)

with kpi_row1_col1:
    exibir_kpi("Piso Mais Crítico", piso_critico, "Piso com maior quantidade de ocorrências.", "https://img.icons8.com/color/48/floor-plan.png")
with kpi_row1_col2:
    exibir_kpi("Posição Mais Crítica", posicao_critica, "Posição mais recorrente nos dados.", "https://img.icons8.com/color/48/marker.png")
with kpi_row1_col3:
    exibir_kpi("Data Mais Crítica", data_critica, "Data com maior número de ocorrências.", "https://img.icons8.com/color/48/calendar.png")
with kpi_row2_col1:
    exibir_kpi("Observação Mais Crítica", observacao_critica, "Observação mais registrada.", "https://img.icons8.com/color/48/idea.png")
with kpi_row2_col2:
    exibir_kpi("Total de Posições", total_posicoes, "Número total de registros de posições.", "https://img.icons8.com/color/48/pin.png")
with kpi_row2_col3:
    exibir_kpi("Total de Observações", total_observacoes, "Número total de registros de observações.", "https://img.icons8.com/color/48/document.png")

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
