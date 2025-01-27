import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carregar os dados
df = pd.read_csv("datasets/data.csv", sep=";", encoding="Windows-1252", parse_dates=["Data"], dayfirst=True)
df["Mês"] = df["Data"].dt.month
df["Dia"] = df["Data"].dt.day

# Barra lateral
st.sidebar.header("Filtros")
pagina = st.sidebar.radio(
    "Escolha a página",
    ["Resumo Geral", "Análise Total", "Análise por Piso", "Análise por Posição", "Análise por Observação", "Tabela Completa"]
)

# Filtro de Data (exceto para "Análise Total")
if pagina != "Análise Total":
    data_selecionada = st.sidebar.selectbox("Selecione uma Data", sorted(df["Data"].dt.strftime("%d/%m/%Y").unique()))
    df_filtrado = df[df["Data"] == pd.to_datetime(data_selecionada, format="%d/%m/%Y")]
else:
    df_filtrado = df  # Para Análise Total, considera todos os dados

# Função para criar KPIs com ícones
def exibir_kpi(icon_url, label, value):
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; padding: 10px; background-color: #f4f4f4; border-radius: 8px;'>
            <img src='{icon_url}' width='40' height='40' style='margin-right: 15px;'/>
            <div>
                <h5 style='margin: 0; font-size: 16px; color: #333;'>{label}</h5>
                <h3 style='margin: 0; font-size: 24px; color: #2C3E50;'>{value}</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# URLs de ícones para KPIs
ICONES = {
    "piso_critico": "https://img.icons8.com/color/48/floor-plan.png",
    "data_critica": "https://img.icons8.com/color/48/calendar.png",
    "total_posicoes": "https://img.icons8.com/color/48/marker.png",
    "total_observacoes": "https://img.icons8.com/color/48/document.png",
}

# Páginas
if pagina == "Resumo Geral":
    st.title("Resumo Geral")
    if not df_filtrado.empty:
        piso_critico = df_filtrado["Piso"].value_counts().idxmax()
        data_critica = data_selecionada
        total_posicoes = len(df_filtrado["Posição"].unique())
        total_observacoes = len(df_filtrado["Observação"])

        # KPIs com ícones
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            exibir_kpi(ICONES["piso_critico"], "Piso Mais Crítico", piso_critico)
        with col2:
            exibir_kpi(ICONES["data_critica"], "Data Mais Crítica", data_critica)
        with col3:
            exibir_kpi(ICONES["total_posicoes"], "Total de Posições", total_posicoes)
        with col4:
            exibir_kpi(ICONES["total_observacoes"], "Total de Observações", total_observacoes)

        # Gráfico de Tendência
        tendencia = df.groupby("Data").size().reset_index(name="Ocorrências")
        tendencia_fig = px.line(
            tendencia,
            x="Data",
            y="Ocorrências",
            title="Tendência de Melhoras ou Piora (Resumo Geral)",
            markers=True,
        )
        st.plotly_chart(tendencia_fig, use_container_width=True)
    else:
        st.error("Nenhum dado encontrado para a data selecionada.")

elif pagina == "Análise Total":
    st.title("Análise Total")
    if not df.empty:
        piso_critico = df["Piso"].value_counts().idxmax()
        data_critica = df["Data"].value_counts().idxmax().strftime("%d/%m/%Y")
        total_posicoes = len(df["Posição"].unique())
        total_observacoes = len(df["Observação"])

        # KPIs com ícones
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            exibir_kpi(ICONES["piso_critico"], "Piso Mais Crítico", piso_critico)
        with col2:
            exibir_kpi(ICONES["data_critica"], "Data Mais Crítica", data_critica)
        with col3:
            exibir_kpi(ICONES["total_posicoes"], "Total de Posições", total_posicoes)
        with col4:
            exibir_kpi(ICONES["total_observacoes"], "Total de Observações", total_observacoes)

        # Treemap para análise dos pisos
        treemap_fig = px.treemap(
            df,
            path=["Piso"],
            values="Posição",
            title="Distribuição dos Pisos",
        )
        st.plotly_chart(treemap_fig, use_container_width=True)

        # Gráfico de Tendência
        tendencia = df.groupby("Data").size().reset_index(name="Ocorrências")
        tendencia_fig = px.line(
            tendencia,
            x="Data",
            y="Ocorrências",
            title="Tendência Geral de Ocorrências",
            markers=True,
        )
        st.plotly_chart(tendencia_fig, use_container_width=True)

        # Tabela de Top 5 Posições
        st.subheader("Top 5 Posições Mais Repetidas")
        top_5_posicoes = df["Posição"].value_counts().head(5).reset_index()
        top_5_posicoes.columns = ["Posição", "Total"]
        st.table(top_5_posicoes)
    else:
        st.error("Nenhum dado disponível para análise total.")

elif pagina == "Análise por Piso":
    st.title("Análise por Piso")
    piso_data = df_filtrado["Piso"].value_counts().reset_index()
    piso_data.columns = ["Piso", "Total"]
    if not piso_data.empty:
        fig_piso = px.bar(piso_data, x="Piso", y="Total", title="Ocorrências por Piso", text="Total")
        st.plotly_chart(fig_piso, use_container_width=True)

        # Observações mais comuns por Piso
        st.subheader("Observações Mais Comuns por Piso")
        observacoes_por_piso = df_filtrado.groupby("Piso")["Observação"].value_counts().reset_index(name="Total")
        st.dataframe(observacoes_por_piso, use_container_width=True)
    else:
        st.warning("Nenhum dado para análise por piso.")

elif pagina == "Análise por Posição":
    st.title("Análise por Posição")
    posicao_data = df_filtrado["Posição"].value_counts().reset_index()
    posicao_data.columns = ["Posição", "Total"]
    posicao_data = posicao_data.head(10)  # Mostrar apenas o top 10
    if not posicao_data.empty:
        st.subheader("Top 10 Posições Mais Repetidas")
        st.table(posicao_data)
    else:
        st.warning("Nenhum dado para análise por posição.")

elif pagina == "Análise por Observação":
    st.title("Análise por Observação")
    observacao_data = df_filtrado["Observação"].value_counts().reset_index()
    observacao_data.columns = ["Observação", "Total"]
    if not observacao_data.empty:
        fig_observacao = px.bar(
            observacao_data,
            x="Observação",
            y="Total",
            title="Ocorrências por Observação",
            text="Total",
            width=1000,
            height=600,
        )
        st.plotly_chart(fig_observacao, use_container_width=True)
    else:
        st.warning("Nenhum dado para análise por observação.")

elif pagina == "Tabela Completa":
    st.title("Tabela Completa")
    st.dataframe(df, width=1200, height=600)
