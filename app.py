import streamlit as st
import json
import os
import auth  # ✅ Corrigido para autenticação
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv  # Para carregar variáveis do .env

# Tenta importar carregar_dados; se não houver, define um placeholder para testes
try:
    from utils.helpers import carregar_dados
except ImportError:
    def carregar_dados():
        # Exemplo: carrega dados de um CSV chamado 'dados.csv'
        return pd.read_csv('dados.csv')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o e-mail remetente e a senha (sem expor no código)
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP")

# Função para envio de e-mail utilizando o Gmail, suportando conteúdo HTML
def enviar_email(destinatarios, assunto, mensagem, is_html=False):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = ", ".join(destinatarios)
        msg['Subject'] = assunto
        
        if is_html:
            msg.attach(MIMEText(mensagem, 'html'))
        else:
            msg.attach(MIMEText(mensagem, 'plain'))
        
        # Conecta ao servidor SMTP do Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA_APP)
        server.sendmail(EMAIL_REMETENTE, destinatarios, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False

# Verifica login antes de carregar qualquer conteúdo
if not st.session_state.get("logado", False):
    auth.login()
    st.stop()

# Configuração inicial da página
st.set_page_config(
    layout="wide",
    page_title="📋 Checklist de Pisos",
    page_icon="📊"
)

# Bem-vindo
usuario = st.session_state.get('usuario', '').capitalize()
st.title(f"Bem-vindo, {usuario}! 🎉")

# Opção de logout
if st.sidebar.button("🔓 Sair"):
    st.session_state.clear()  # Reseta a sessão para deslogar
    st.rerun()

# Caminho para armazenar os destinatários dos alertas
EMAILS_JSON = "emails_destinatarios.json"

# Função para carregar destinatários do JSON
def carregar_destinatarios():
    if os.path.exists(EMAILS_JSON):
        with open(EMAILS_JSON, "r") as f:
            return json.load(f)
    return ["lucasevan14@hotmail.com"]  # Destinatário padrão

# Função para salvar destinatários
def salvar_destinatarios(destinatarios):
    with open(EMAILS_JSON, "w") as f:
        json.dump(destinatarios, f)

# Estilização avançada para um visual premium
st.markdown(
    """
    <style>
        /* Importa fonte do Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
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
        .linha {
            border-top: 3px solid linear-gradient(45deg, #FF6B6B, #FFD93D);
            margin: 30px 10px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; }
            100% { opacity: 0.7; }
        }
        .button-custom {
            background: linear-gradient(45deg, #FF6B6B, #FFD93D);
            color: #FFFFFF;
            border: none;
            padding: 14px 28px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .button-custom:hover {
            transform: scale(1.05);
            box-shadow: 0px 10px 20px rgba(255, 107, 107, 0.5);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout principal
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

# Seção de Recursos (exemplo ilustrativo)
st.markdown(
    """
    <div style="display:flex; justify-content:center; gap:25px; flex-wrap:wrap; margin-top:30px;">
        <div style="background:#FFFFFF; padding:25px; border-radius:12px; box-shadow: 0px 5px 15px rgba(0,0,0,0.12); max-width:300px; text-align:center;">
            <img src="https://img.icons8.com/fluency/96/data-configuration.png" alt="Análise de Dados">
            <h3 style="color:#2C3E50;">🔍 Análise Detalhada</h3>
            <p style="color:#566573; font-size:16px;">Visualize rapidamente as áreas mais críticas e tome ações corretivas de forma eficaz.</p>
        </div>
        <div style="background:#FFFFFF; padding:25px; border-radius:12px; box-shadow: 0px 5px 15px rgba(0,0,0,0.12); max-width:300px; text-align:center;">
            <img src="https://img.icons8.com/fluency/96/combo-chart.png" alt="Gráficos Interativos">
            <h3 style="color:#2C3E50;">📊 Dashboards Interativos</h3>
            <p style="color:#566573; font-size:16px;">Explore tendências e padrões com gráficos dinâmicos e relatórios completos.</p>
        </div>
        <div style="background:#FFFFFF; padding:25px; border-radius:12px; box-shadow: 0px 5px 15px rgba(0,0,0,0.12); max-width:300px; text-align:center;">
            <img src="https://img.icons8.com/fluency/96/document.png" alt="Relatórios Inteligentes">
            <h3 style="color:#2C3E50;">📥 Relatórios Personalizados</h3>
            <p style="color:#566573; font-size:16px;">Gere e exporte relatórios profissionais para monitoramento detalhado.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# GIF ilustrativo
st.markdown(
    """
    <div style="text-align:center; margin-top:40px;">
        <img src="https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif" alt="GIF de Análise de Dados" width="550px">
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# GERENCIAMENTO DE E-MAILS (Apenas ADMIN)
# =============================================================================
if st.session_state.get("tipo") == "admin":
    st.markdown("<hr>")
    st.subheader("✉️ Gerenciar Destinatários dos Alertas")

    destinatarios = carregar_destinatarios()
    novo_email = st.text_input("Adicionar novo e-mail", placeholder="Digite um e-mail válido")

    col_add, col_test = st.columns([2, 1])
    with col_add:
        if st.button("Adicionar"):
            if novo_email and "@" in novo_email:
                if novo_email not in destinatarios:
                    destinatarios.append(novo_email)
                    salvar_destinatarios(destinatarios)
                    st.success(f"✅ {novo_email} foi adicionado!")
                    st.rerun()
                else:
                    st.error("❌ E-mail já existe.")
            else:
                st.error("❌ E-mail inválido.")
    with col_test:
        if st.button("Teste de Envio"):
            if enviar_email(destinatarios, "Teste de E-mail", "Este é um e-mail de teste para verificar o envio.", is_html=True):
                st.success("✅ E-mail de teste enviado!")
            else:
                st.error("❌ Falha no envio do e-mail de teste.")

    st.subheader("📋 Destinatários Atuais")
    for email in destinatarios:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"📧 {email}")
        with col2:
            if st.button("Remover", key=email):
                destinatarios.remove(email)
                salvar_destinatarios(destinatarios)
                st.success(f"✅ {email} removido!")
                st.rerun()

    if st.button("🗑️ Remover Todos"):
        salvar_destinatarios([])
        st.success("✅ Todos os destinatários foram removidos!")
        st.rerun()

# =============================================================================
# VERIFICAÇÃO DE OCORRÊNCIAS E ENVIO DO DASHBOARD POR E-MAIL COM OS DADOS DA DATA MAIS RECENTE
# =============================================================================
try:
    df_pisos = carregar_dados()
    # Se existir a coluna "Data", filtra os dados pela data mais recente
    if "Data" in df_pisos.columns:
        recent_date = df_pisos["Data"].max()
        df_recent = df_pisos[df_pisos["Data"] == recent_date]
    else:
        df_recent = df_pisos
    
    ocorrencias = df_recent["Piso"].value_counts()
    pisos_alert = ocorrencias[ocorrencias > 15]
    
    if not pisos_alert.empty:
        st.info("⚠️ Alerta: Alguns pisos possuem mais de 15 ocorrências na data mais recente.")
        if st.button("Enviar Dashboard por E-mail"):
            assunto = f"Dashboard de Pisos - Alerta de Ocorrências ({recent_date})" if "recent_date" in locals() else "Dashboard de Pisos - Alerta de Ocorrências"
            # Cria um conteúdo HTML para o dashboard da data mais recente
            html_content = f"""
            <html>
              <head>
                <style>
                  body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; color: #2c3e50; }}
                  .dashboard-container {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: #ffffff; box-shadow: 0px 4px 8px rgba(0,0,0,0.1); }}
                  h2 {{ text-align: center; color: #2c3e50; }}
                  table {{ width: 100%; border-collapse: collapse; }}
                  th, td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                  th {{ background-color: #ff6b6b; color: #ffffff; }}
                </style>
              </head>
              <body>
                <div class="dashboard-container">
                  <h2>Dashboard de Pisos - Alertas</h2>
                  <p>Data: {recent_date if 'recent_date' in locals() else 'N/A'}</p>
                  <p>Os seguintes pisos possuem mais de 15 ocorrências:</p>
                  <table>
                    <tr>
                      <th>Piso</th>
                      <th>Ocorrências</th>
                    </tr>
            """
            for piso, qtd in pisos_alert.items():
                html_content += f"<tr><td>{piso}</td><td>{qtd}</td></tr>"
            html_content += """
                  </table>
                  <p style="text-align:center; margin-top:20px;">Por favor, acesse o dashboard para mais detalhes.</p>
                </div>
              </body>
            </html>
            """
            if enviar_email(carregar_destinatarios(), assunto, html_content, is_html=True):
                st.success("✅ Dashboard enviado por e-mail!")
            else:
                st.error("❌ Falha ao enviar o dashboard por e-mail.")
except Exception as e:
    st.error(f"Erro ao verificar ocorrências: {e}")

# =============================================================================
# RODAPÉ
# =============================================================================
st.markdown(
    """
    <div style="text-align:center; margin-top:40px; font-size:15px; color:#7F8C8D; font-style:italic;">
        Desenvolvido por Evangelistalp
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
