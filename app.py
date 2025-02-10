import streamlit as st
import json
import os
import auth  # ✅ Corrigido para autenticação


# 📌 Verifica login antes de carregar qualquer conteúdo
if not st.session_state.get("logado", False):
    auth.login()
    st.stop()

# 📌 Configuração inicial da página
st.set_page_config(
    layout="wide",
    page_title="📋 Checklist de Pisos",
    page_icon="📊"
)

# 📌 Bem-vindo
usuario = st.session_state.get('usuario', '').capitalize()
st.title(f"Bem-vindo, {usuario}! 🎉")

# 📌 Opção de logout
if st.sidebar.button("🔓 Sair"):
    st.session_state.clear()  # Reseta a sessão para deslogar
    st.rerun()

# 📌 Caminho para armazenar os destinatários dos alertas
EMAILS_JSON = "emails_destinatarios.json"

# 📌 Função para carregar destinatários do JSON
def carregar_destinatarios():
    if os.path.exists(EMAILS_JSON):
        with open(EMAILS_JSON, "r") as f:
            return json.load(f)
    return ["lucasevan14@hotmail.com"]  # Destinatário padrão

# 📌 Função para salvar destinatários
def salvar_destinatarios(destinatarios):
    with open(EMAILS_JSON, "w") as f:
        json.dump(destinatarios, f)

# 📌 Estilização avançada para um visual premium
st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #F8F9FA;
            color: #2C3E50;
        }
        .container {
            max-width: 1100px;
            margin: 20px auto;
            padding: 40px;
            background: linear-gradient(to bottom, #FFFFFF, #F8F9FA);
            border-radius: 12px;
            box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.15);
            text-align: center;
            opacity: 0;
            animation: fadeIn 1.2s ease-in-out forwards;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        .title {
            font-size: 44px;
            font-weight: bold;
            color: #2C3E50;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        .subtitle {
            font-size: 24px;
            color: #34495E;
            margin-top: -10px;
        }
        .description {
            font-size: 18px;
            color: #566573;
            margin: 20px auto;
            max-width: 900px;
            line-height: 1.6;
        }
        .features {
            display: flex;
            justify-content: center;
            margin-top: 30px;
            gap: 25px;
            flex-wrap: wrap;
        }
        .feature {
            flex: 1;
            background: #FFFFFF;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.12);
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
            text-align: center;
            max-width: 300px;
            margin: 10px;
        }
        .feature:hover {
            transform: translateY(-8px);
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.15);
        }
        .feature img {
            width: 80px;
            margin-bottom: 15px;
        }
        .feature h3 {
            font-size: 20px;
            color: #2C3E50;
        }
        .feature p {
            font-size: 16px;
            color: #566573;
        }
        .gif-container {
            text-align: center;
            margin-top: 40px;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 15px;
            color: #7F8C8D;
            font-style: italic;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 📌 Layout principal
st.markdown("<div class='container'>", unsafe_allow_html=True)

st.markdown("<h1 class='title'>📋 Checklist de Pisos</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Monitoramento Inteligente da Infraestrutura Operacional</h2>", unsafe_allow_html=True)

st.markdown(
    """
    <p class='description'>
        O <strong>Dashboard de Checklist de Pisos</strong> é uma solução poderosa para análise e gestão da infraestrutura operacional. 
        Com gráficos interativos, dados detalhados e filtros inteligentes, 
        você pode tomar decisões mais assertivas e garantir uma infraestrutura eficiente e segura.
    </p>
    """,
    unsafe_allow_html=True,
)

# 📌 Seção de Recursos
st.markdown(
    """
    <div class="features">
        <div class="feature">
            <img src="https://img.icons8.com/fluency/96/data-configuration.png" alt="Análise de Dados">
            <h3>🔍 Análise Detalhada</h3>
            <p>Visualize rapidamente as áreas mais críticas e tome ações corretivas de forma eficaz.</p>
        </div>
        <div class="feature">
            <img src="https://img.icons8.com/fluency/96/combo-chart.png" alt="Gráficos Interativos">
            <h3>📊 Dashboards Interativos</h3>
            <p>Explore tendências e padrões com gráficos dinâmicos e relatórios completos.</p>
        </div>
        <div class="feature">
            <img src="https://img.icons8.com/fluency/96/document.png" alt="Relatórios Inteligentes">
            <h3>📥 Relatórios Personalizados</h3>
            <p>Gere e exporte relatórios profissionais para monitoramento detalhado.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 📌 GIF ilustrativo
st.markdown(
    """
    <div class="gif-container">
        <img src="https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif" alt="GIF de Análise de Dados" width="550px">
    </div>
    """,
    unsafe_allow_html=True,
)

# 📌 Apenas ADMIN pode gerenciar destinatários
if st.session_state.get("tipo") == "admin":
    st.markdown("---")
    st.subheader("✉️ **Gerenciar Destinatários dos Alertas**")

    destinatarios = carregar_destinatarios()
    novo_email = st.text_input("Adicionar novo e-mail", placeholder="Digite um e-mail válido")

    if st.button("Adicionar"):
        if novo_email and "@" in novo_email:
            destinatarios.append(novo_email)
            salvar_destinatarios(destinatarios)
            st.success(f"✅ {novo_email} foi adicionado!")
            st.rerun()
        else:
            st.error("❌ E-mail inválido.")

    st.subheader("📋 Destinatários Atuais")
    for email in destinatarios:
        st.write(f"📧 {email}")

    if st.button("🗑️ Remover Todos"):
        salvar_destinatarios(["lucasevan14@hotmail.com"])
        st.success("✅ Lista redefinida!")
        st.rerun()

# 📌 Rodapé
st.markdown(
    """
    <div class="footer">
        Desenvolvido por Evangelistalp
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
