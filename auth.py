import streamlit as st
from dotenv import load_dotenv
import os

# Carrega variáveis do .env (caso exista localmente)
if os.path.exists(".env"):
    load_dotenv()

# Obtém credenciais do ambiente (local ou Streamlit Cloud)
USUARIO_ADMIN = os.getenv("USUARIO_ADMIN") or st.secrets["USUARIO_ADMIN"]
SENHA_ADMIN = os.getenv("SENHA_ADMIN") or st.secrets["SENHA_ADMIN"]

USUARIO_GESTOR = os.getenv("USUARIO_GESTOR") or st.secrets["USUARIO_GESTOR"]
SENHA_GESTOR = os.getenv("SENHA_GESTOR") or st.secrets["SENHA_GESTOR"]

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE") or st.secrets["EMAIL_REMETENTE"]
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP") or st.secrets["EMAIL_SENHA_APP"]

# Dicionário de usuários
USUARIOS = {
    USUARIO_ADMIN: {"senha": SENHA_ADMIN, "tipo": "admin"},
    USUARIO_GESTOR: {"senha": SENHA_GESTOR, "tipo": "gestor"},
}

def login():
    """
    Função de login com um design escuro e profissional.
    """
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

            :root {
                --primary-bg: #1E1E1E;
                --secondary-bg: #2C2C2C;
                --primary-accent: #007AFF;
                --primary-text: #F0F0F0;
                --secondary-text: #A0A0A0;
                --border-color: #444444;
                --font-family: 'Inter', sans-serif;
            }

            /* Força o tema escuro na página de login */
            body {
                background-color: var(--primary-bg) !important;
            }

            /* Container de login centralizado */
            .login-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            /* Card de login */
            .login-card {
                background-color: var(--secondary-bg);
                padding: 3rem;
                border-radius: 16px;
                border: 1px solid var(--border-color);
                width: 100%;
                max-width: 450px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }

            .login-title {
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--primary-text);
                text-align: center;
                margin-bottom: 2rem;
            }

            /* Estilo dos inputs */
            .stTextInput label {
                color: var(--secondary-text) !important;
                font-weight: 600 !important;
                margin-bottom: 0.5rem !important;
            }
            .stTextInput input {
                background-color: var(--primary-bg) !important;
                color: var(--primary-text) !important;
                border: 1px solid var(--border-color) !important;
                border-radius: 8px !important;
                padding: 0.75rem !important;
            }
            .stTextInput input:focus {
                border-color: var(--primary-accent) !important;
                box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.5) !important;
            }

            /* Botão de login */
            .stButton>button {
                width: 100%;
                background-color: var(--primary-accent);
                color: white;
                padding: 0.75rem 0;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                border: none;
                margin-top: 1.5rem;
                transition: background-color 0.2s, transform 0.2s;
            }
            .stButton>button:hover {
                background-color: #0056b3;
                transform: scale(1.02);
            }

        </style>
        <div class="login-container">
            <div class="login-card">
                <h2 class="login-title">Bem-vindo</h2>
    """,
        unsafe_allow_html=True
    )

    # Formulário de login
    with st.form(key="login_form"):
        usuario = st.text_input("Usuário", key="login_usuario")
        senha = st.text_input("Senha", type="password", key="login_senha")
        submit = st.form_submit_button("Entrar")

        if submit:
            if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
                st.session_state["logado"] = True
                st.session_state["usuario"] = usuario
                st.session_state["tipo"] = USUARIOS[usuario]["tipo"]
                st.success(f"✅ Bem-vindo, {usuario}! Redirecionando...")
                st.rerun()  # Substituindo st.experimental_rerun() por st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos. Tente novamente.")

    # Fechamento das divs do container
    st.markdown("</div></div>", unsafe_allow_html=True)

if "logado" not in st.session_state:
    st.session_state["logado"] = False
