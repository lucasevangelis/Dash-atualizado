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
    Função de login com layout e design inspirados no Figma.
    Remove subtítulo e força tema claro para evitar contraste baixo em modo escuro.
    """
    st.markdown(
        """
        <style>
            /* Força modo claro para evitar problemas de contraste em tema escuro */
            :root {
                color-scheme: light;
            }
            /* Fundo gradiente suave */
            body {
                background: linear-gradient(135deg, #F0F2F5, #C9D6FF) !important;
            }
            /* Container de login */
            .login-container {
                max-width: 420px;
                margin: 120px auto;
                padding: 48px;
                background: #FFFFFF;
                border-radius: 16px;
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
                text-align: center;
                font-family: 'Inter', sans-serif;
                color: #333333;
            }
            .login-title {
                font-size: 36px;
                font-weight: 700;
                color: #333333;
                margin-bottom: 20px;
            }
            /* Inputs */
            .stTextInput input {
                font-size: 16px !important;
                padding: 12px !important;
                border: 1px solid #E0E0E0 !important;
                border-radius: 8px !important;
                background-color: #F9F9F9 !important;
                color: #333333 !important;
            }
            .stTextInput label {
                color: #333333 !important;
                font-weight: 500 !important;
                margin-bottom: 8px !important;
            }
            /* Botão de login */
            .stButton>button {
                width: 100%;
                background-color: #007AFF;
                color: #FFFFFF;
                padding: 14px 0;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                border: none;
                cursor: pointer;
                margin-top: 30px;
                transition: background-color 0.3s, transform 0.3s;
            }
            .stButton>button:hover {
                background-color: #005BB5;
                transform: scale(1.02);
            }
        </style>
        <div class="login-container">
            <h2 class="login-title">Bem-vindo ao Dashboard</h2>
        </div>
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

if "logado" not in st.session_state:
    st.session_state["logado"] = False
