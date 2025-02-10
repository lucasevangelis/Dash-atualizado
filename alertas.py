import smtplib
import json
import os
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# 🔐 Carregar variáveis de ambiente
if os.path.exists(".env"):
    load_dotenv()

# Configurações de e-mail (ajustável via .env ou Streamlit Secrets)
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE") or st.secrets["EMAIL_REMETENTE"]
SENHA_APP = os.getenv("EMAIL_SENHA_APP") or st.secrets["EMAIL_SENHA_APP"]

# Caminho para o arquivo JSON com destinatários
EMAILS_JSON = "emails_destinatarios.json"

# 📤 Função para carregar destinatários
def carregar_destinatarios():
    """
    Carrega os e-mails de destinatários do arquivo JSON.
    Retorna uma lista padrão se o arquivo não existir.
    """
    if os.path.exists(EMAILS_JSON):
        try:
            with open(EMAILS_JSON, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"❌ Erro ao carregar destinatários: {e}")
            return []
    return ["exemplo@destinatario.com"]  # E-mail padrão caso o arquivo JSON não exista

# 📧 Função para enviar e-mail de alerta
def enviar_alerta(piso_critico):
    """
    Envia um e-mail de alerta informando o piso crítico.
    """
    destinatarios = carregar_destinatarios()

    # Montar o corpo do e-mail
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = "⚠️ Alerta Crítico: Piso em Condição Crítica"

    corpo_email = f"""
    <html>
        <body>
            <h2 style='color: red;'>⚠️ ALERTA CRÍTICO</h2>
            <p>Olá,</p>
            <p><strong>O piso mais crítico atualmente é:</strong> {piso_critico}</p>
            <p>Por favor, verifique a situação o mais rápido possível.</p>
            <br>
            <p>🔍 <i>Este e-mail foi enviado automaticamente pelo sistema de monitoramento.</i></p>
        </body>
    </html>
    """
    msg.attach(MIMEText(corpo_email, "html"))

    # Conectar ao servidor SMTP e enviar o e-mail
    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_APP)
        servidor.sendmail(EMAIL_REMETENTE, destinatarios, msg.as_string())
        servidor.quit()

        st.success(f"✅ Alerta enviado com sucesso para {', '.join(destinatarios)}!")
    except Exception as e:
        st.error(f"❌ Erro ao enviar alerta: {e}")

# 🔎 Teste manual do envio no Streamlit
def interface_teste_envio():
    """
    Interface do Streamlit para testar o envio de alertas.
    """
    st.title("📢 Enviar Alerta Manualmente")
    st.markdown(
        """
        <style>
            h1 {
                text-align: center;
                color: #2C3E50;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Entrada para o piso crítico
    piso_critico = st.text_input("Digite o Piso Crítico:", placeholder="Exemplo: Piso A3")
    
    # Botão para envio do alerta
    if st.button("Enviar Alerta"):
        if piso_critico.strip():
            enviar_alerta(piso_critico)
        else:
            st.error("❌ Insira o nome do piso crítico antes de enviar o alerta.")

# 🔥 Executar o app Streamlit
if __name__ == "__main__":
    interface_teste_envio()
