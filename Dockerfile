# Passo 1: A Base - Usar uma imagem oficial e leve do Python
FROM python:3.11-slim

# Passo 2: O Ambiente - Criar uma pasta de trabalho dentro do contêiner
WORKDIR /app

# Passo 3: As Dependências - Copiar o arquivo de requisitos e instalar tudo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Passo 4: O Código - Copiar todos o seus arquivos (.py, .csv) para o contêiner
COPY . .

# Passo 5: A Execução - Definir o comando para rodar o seu app quando o contêiner iniciar
# (Assumindo que o arquivo principal se chama app.py Se for outro nome, Se for outro nome, Troque aqui)
CMD ["streamlit", "run",  "app.py", "--server.port=8050", "--server.address=0.0.0.0", "--server.headless=true", "--browser.serverAddress=0.0.0.0" ]
