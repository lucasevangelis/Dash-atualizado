# Checklist Pisos
Este projeto é um **dashboard interativo** desenvolvido em **Python** usando **Streamlit**, **Plotly** e **Pandas**. Ele permite analisar dados relacionados a pisos, suas posições e observações críticas, fornecendo insights por meio de gráficos interativos e indicadores chave.

---

## 🚀 Funcionalidades
- **Resumo Geral:** 
  - Piso mais crítico
  - Data mais crítica
  - Total de posições e observações
- **Análise por Piso:** Visualização da distribuição e desempenho dos pisos em gráficos.
- **Análise por Data:** Filtrar os dados com base em datas específicas.
- **Análise Detalhada:** Gráficos hierárquicos (treemap) e outros detalhes por posição.

---

## 🔧 Instalação e Execução
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/lucasevangelis/Dash-atualizado.git
   cd Dash-atualizado

    Crie um ambiente virtual e ative:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

Instale as dependências:

pip install -r requirements.txt

Execute o dashboard:

    streamlit run app.py

🎥 Demonstração

    Insira um GIF ou captura de tela mostrando o funcionamento do dashboard.

🛠 Tecnologias Utilizadas

    Python 3.11
    Streamlit - Para criação de dashboards interativos
    Pandas - Manipulação e análise de dados
    Plotly - Visualização de gráficos interativos
    NumPy - Operações numéricas avançadas

📂 Estrutura do Projeto

📦 Checklist-pisos
│-- 📂 datasets            # Arquivos CSV com dados
│   └── data.csv           # Base de dados utilizada no projeto
│-- 📂 pages               # Arquivos para múltiplas páginas do app
│-- 📂 utils               # Scripts auxiliares (helpers, autenticação, etc.)
│   └── helpers.py         # Funções de suporte
│-- app.py                 # Arquivo principal do Streamlit
│-- requirements.txt       # Dependências do projeto
│-- README.md              # Documentação do projeto

🤝 Contribuição

Sinta-se à vontade para contribuir com este projeto!

    Faça um fork 🍴
    Crie um branch: git checkout -b minha-feature
    Faça o commit das suas alterações: git commit -m "Adicionei uma nova funcionalidade"
    Envie um pull request 🚀

👤 Autor

    Lucas Evangelista
    📩 Email: lucasevan14@hotmail.com
    🔗 GitHub: lucasevangelis

📜 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.


---

### 🚀 **Instruções para Subir o Novo README.md**
1. Salve o conteúdo acima em seu arquivo `README.md` local.
2. Faça o commit e push para o repositório:
   ```bash
   git add README.md
   git commit -m "Atualizado README.md"
   git push origin main
