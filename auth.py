import streamlit as st
from dotenv import load_dotenv
import os

# 🔹 Carregar variáveis do .env (Somente local)
if os.path.exists(".env"):
    load_dotenv()

# 🔹 Obtendo credenciais do ambiente (Local e Streamlit Cloud)
USUARIO_ADMIN = os.getenv("USUARIO_ADMIN") or st.secrets["USUARIO_ADMIN"]
SENHA_ADMIN = os.getenv("SENHA_ADMIN") or st.secrets["SENHA_ADMIN"]

USUARIO_GESTOR = os.getenv("USUARIO_GESTOR") or st.secrets["USUARIO_GESTOR"]
SENHA_GESTOR = os.getenv("SENHA_GESTOR") or st.secrets["SENHA_GESTOR"]

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE") or st.secrets["EMAIL_REMETENTE"]
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP") or st.secrets["EMAIL_SENHA_APP"]

# 🔹 Dicionário de usuários atualizado
USUARIOS = {
    USUARIO_ADMIN: {"senha": SENHA_ADMIN, "tipo": "admin"},
    USUARIO_GESTOR: {"senha": SENHA_GESTOR, "tipo": "gestor"},
}

# 🔹 Função de Login
def login():
    st.markdown(
        """
        <style>
            .login-container {
                max-width: 400px;
                margin: auto;
                padding: 40px;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.2);
                text-align: center;
            }
            .login-title {
                font-size: 34px;
                color: #2C3E50;
                font-weight: 900;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                margin-bottom: 20px;
            }
            .stTextInput input {
                font-size: 16px !important;
                padding: 12px !important;
            }
            .stButton>button {
                width: 100%;
                background-color: #2C3E50;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                cursor: pointer;
                margin-top: 20px;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #1A252F;
                transform: scale(1.05);
            }
        </style>
        <div class='login-container'>
            <h2 class='login-title'>🔑 Acesso ao Dashboard</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    usuario = st.text_input("Usuário", key="login_usuario")
    senha = st.text_input("Senha", type="password", key="login_senha")

    if st.button("Entrar"):
        if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["tipo"] = USUARIOS[usuario]["tipo"]
            st.success(f"✅ Bem-vindo, {usuario}! Redirecionando...")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos. Tente novamente.")

if "logado" not in st.session_state:
    st.session_state["logado"] = False
