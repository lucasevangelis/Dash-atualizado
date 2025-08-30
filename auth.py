import streamlit as st
from dotenv import load_dotenv
import os

import bcrypt

# Carrega variáveis do .env (caso exista localmente)
if os.path.exists(".env"):
    load_dotenv()

# =============================================================================
# 1. CARREGAMENTO DE CREDENCIAIS E CONFIGURAÇÕES
# =============================================================================

def get_credential(key: str) -> str:
    """
    Obtém uma credencial do ambiente ou dos segredos do Streamlit de forma segura.
    """
    value = os.getenv(key)
    if value:
        return value
    if hasattr(st, "secrets") and key in st.secrets:
        return st.secrets[key]
    # Retorna string vazia para evitar erros NoneType
    return ""

# Obtém as credenciais usando a função auxiliar
USUARIO_ADMIN = get_credential("USUARIO_ADMIN")
SENHA_ADMIN = get_credential("SENHA_ADMIN")
USUARIO_GESTOR = get_credential("USUARIO_GESTOR")
SENHA_GESTOR = get_credential("SENHA_GESTOR")
EMAIL_REMETENTE = get_credential("EMAIL_REMETENTE")
EMAIL_SENHA_APP = get_credential("EMAIL_SENHA_APP")

# =============================================================================
# 2. ESTRUTURA DE DADOS DE USUÁRIOS
# =============================================================================

# As senhas (hashes) são carregadas do ambiente
USUARIOS = {
    USUARIO_ADMIN: {"senha_hash": SENHA_ADMIN, "tipo": "admin"},
    USUARIO_GESTOR: {"senha_hash": SENHA_GESTOR, "tipo": "gestor"},
}

# =============================================================================
# 3. FUNÇÕES DE AUTENTICAÇÃO E LÓGICA
# =============================================================================

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """
    Verifica se a senha fornecida (em texto plano) corresponde ao hash armazenado.
    """
    try:
        # A senha fornecida e o hash armazenado devem ser codificados para bytes
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
    except (ValueError, TypeError):
        # Retorna False se o hash for inválido ou ocorrer outro erro
        return False

# =============================================================================
# 4. INTERFACE DE LOGIN (UI)
# =============================================================================

def login():
    """
    Renderiza a interface de login e gerencia o estado da sessão.
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
            user_data = USUARIOS.get(usuario)
            if user_data and verificar_senha(senha, user_data["senha_hash"]):
                st.session_state["logado"] = True
                st.session_state["usuario"] = usuario
                st.session_state["tipo"] = user_data["tipo"]
                st.success(f"✅ Bem-vindo, {usuario}! Redirecionando...")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos. Tente novamente.")

if "logado" not in st.session_state:
    st.session_state["logado"] = False
