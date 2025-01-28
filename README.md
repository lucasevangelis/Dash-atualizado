# Checklist Pisos

Este projeto é um **dashboard interativo** desenvolvido em Python usando Streamlit, Plotly e Pandas. Ele permite analisar dados relacionados a pisos, suas posições e observações críticas, fornecendo insights por meio de gráficos interativos e indicadores chave.

## 🚀 Funcionalidades

- **Resumo Geral:** Mostra informações como:
  - Piso mais crítico
  - Data mais crítica
  - Total de posições e observações
- **Análise por Piso:** Visualiza a distribuição e desempenho dos pisos em gráficos.
- **Análise por Data:** Permite filtrar os dados com base em datas específicas.
- **Análise Detalhada:** Gráficos de treemap e outros, exibindo dados de maneira hierárquica.

## 🛠 Tecnologias Utilizadas

- **Python 3.11**
- **Streamlit** - Para a criação de dashboards interativos.
- **Pandas** - Para manipulação e análise de dados.
- **Plotly** - Para gráficos interativos e visuais avançados.
- **NumPy** - Para cálculos matemáticos e operações numéricas.

## 📂 Estrutura do Projeto

```plaintext
.
├── datasets/
│   └── data.csv      # Base de dados utilizada no projeto
├── app.py            # Código principal da aplicação
├── requirements.txt  # Dependências do projeto
├── .devcontainer/    # Configurações do ambiente de desenvolvimento
└── README.md         # Documentação do projeto
