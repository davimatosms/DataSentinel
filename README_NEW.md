# 🛡️ DataSentinel

<div align="center">

![DataSentinel Logo](https://img.shields.io/badge/DataSentinel-Quality%20Validation-blue?style=for-the-badge)

**Sistema Profissional de Validação de Qualidade de Dados**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-24%2F25%20Passing-brightgreen.svg)]()

[Demo](#-demo) • [Instalação](#-instalação) • [Uso](#-uso-rápido) • [Documentação](#-documentação)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Características](#-características)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Interface Web](#-interface-web)
- [Documentação](#-documentação)
- [Testes](#-testes)
- [Roadmap](#-roadmap)

---

## 🎯 Sobre o Projeto

**DataSentinel** é uma solução completa e profissional para validação de qualidade de dados, inspirada em ferramentas como Great Expectations. O projeto oferece uma interface web intuitiva e uma API Python poderosa para garantir a integridade dos seus dados.

### 💡 Por que DataSentinel?

- ✅ **Interface Web Moderna** - Dashboard interativo com Streamlit
- ✅ **Testes sem Infraestrutura** - MockConnector para desenvolvimento ágil
- ✅ **Múltiplas Fontes** - PostgreSQL, CSV, Mock e mais
- ✅ **Validações Flexíveis** - Nulos, ranges, unicidade, outliers
- ✅ **Visualizações Ricas** - Gráficos interativos com Plotly
- ✅ **Exportação** - Relatórios em JSON e CSV
- ✅ **100% Python** - Fácil integração em pipelines existentes

---

## ✨ Características

### 🔍 Validações de Qualidade

| Tipo | Descrição | Uso |
|------|-----------|-----|
| **Not Null** | Detecta valores nulos/vazios | Campos obrigatórios |
| **Range Check** | Valida intervalos numéricos | Preços, idades, quantidades |
| **Uniqueness** | Verifica valores duplicados | IDs, emails, chaves |
| **Outliers** | Detecta valores anômalos (Z-Score) | Análise estatística |
| **Data Types** | Valida tipos de dados | Consistência de schema |

### 🔌 Conectores Suportados

- **MockConnector** 🎭 - Dados simulados para testes e desenvolvimento
- **CSVConnector** 📁 - Arquivos CSV locais
- **PostgreSQLConnector** 🐘 - Banco de dados PostgreSQL
- **Extensível** 🔧 - Crie seus próprios conectores

### 📊 Interface Web

- Dashboard interativo e responsivo
- Configuração visual de validações
- Gráficos em tempo real
- Preview de dados
- Exportação de relatórios

---

## 🛠️ Tecnologias

- **Python 3.8+** - Linguagem principal
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica
- **Streamlit** - Interface web
- **Plotly** - Visualizações interativas
- **Pytest** - Testes automatizados
- **SQLAlchemy** - ORM para bancos de dados

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)

### Passo a Passo

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/DataSentinel.git
cd DataSentinel

# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

---

## 💻 Uso Rápido

### 1️⃣ Interface Web

```bash
streamlit run web_app.py
```

Acesse: `http://localhost:8501`

### 2️⃣ API Python

```python
from app.connectors import MockConnector
from app.core.engine import DataValidator

# Conecta aos dados
with MockConnector() as conn:
    data = conn.get_table_data('sales')
    
    # Cria validador
    validator = DataValidator(data, 'sales')
    
    # Executa validações
    validator.expect_column_values_to_not_be_null('price')
    validator.expect_column_values_to_be_between('price', 0, 10000)
    validator.expect_column_values_to_be_unique('sale_id')
    
    # Obtém resultados
    summary = validator.get_summary()
    print(f"Taxa de qualidade: {summary['success_rate']}%")
```

### 3️⃣ Linha de Comando

```bash
# Executa demonstração completa
python demo_mock.py

# Executa testes
pytest tests/ -v
```

---

## 🖥️ Interface Web

### Dashboard Principal

A interface web oferece uma experiência completa de validação:

1. **Conectar aos Dados**
   - Selecione a fonte (Mock, CSV, PostgreSQL)
   - Configure parâmetros de conexão
   - Carregue os dados

2. **Configurar Validações**
   - Valores Nulos: defina thresholds aceitáveis
   - Intervalos: configure min/max para campos numéricos
   - Unicidade: marque colunas que devem ser únicas
   - Outliers: ajuste sensibilidade do Z-Score

3. **Visualizar Resultados**
   - Métricas em tempo real
   - Gráficos interativos
   - Detalhes de cada validação
   - Exportação de relatórios

---

## 📚 Documentação

### Estrutura do Projeto

```
DataSentinel/
├── app/
│   ├── connectors/          # Conectores de dados
│   │   ├── base.py         # Interface base
│   │   ├── mock.py         # Conector simulado
│   │   ├── database.py     # PostgreSQL, etc
│   │   └── __init__.py
│   ├── core/               # Motor de validação
│   │   ├── engine.py       # DataValidator
│   │   ├── config.py       # Configurações
│   │   └── __init__.py
│   ├── tests_definitions/  # Definições de testes
│   │   └── sales_checks.py
│   └── utils/              # Utilitários
│       └── reporter.py     # Geração de relatórios
├── tests/                  # Testes automatizados
│   ├── test_engine.py
│   └── test_mock_connector.py
├── web_app.py             # Interface web Streamlit
├── demo_mock.py           # Demonstração
├── main.py                # Entry point CLI
├── requirements.txt       # Dependências
└── README.md             # Este arquivo
```

### Criando um Conector Customizado

```python
from app.connectors.base import BaseConnector
import pandas as pd

class MeuConector(BaseConnector):
    def connect(self) -> bool:
        # Implementar lógica de conexão
        return True
    
    def disconnect(self) -> bool:
        # Implementar lógica de desconexão
        return True
    
    def execute_query(self, query: str) -> pd.DataFrame:
        # Implementar execução de query
        pass
    
    def get_table_data(self, table_name: str, limit=None) -> pd.DataFrame:
        # Implementar busca de dados
        pass
    
    def get_table_metadata(self, table_name: str) -> dict:
        # Implementar busca de metadados
        pass
```

---

## 🧪 Testes

O projeto possui uma suíte completa de testes automatizados:

```bash
# Executar todos os testes
pytest tests/ -v

# Executar com cobertura
pytest tests/ --cov=app --cov-report=html

# Executar testes específicos
pytest tests/test_mock_connector.py -v
```

### Cobertura de Testes

- ✅ 20/20 testes do MockConnector
- ✅ 4/5 testes do DataValidator
- ✅ 96% de cobertura geral

---

## 🗺️ Roadmap

### Versão 1.0 (Atual)
- [x] Motor de validação
- [x] MockConnector
- [x] Interface web
- [x] Exportação de relatórios
- [x] Testes automatizados

### Versão 1.1 (Próximo)
- [ ] PostgreSQL totalmente integrado
- [ ] Suporte a MySQL
- [ ] Validações customizadas
- [ ] Agendamento de validações
- [ ] Notificações (Email, Slack)

### Versão 2.0 (Futuro)
- [ ] Machine Learning para detecção de anomalias
- [ ] API REST
- [ ] Dashboard de monitoramento contínuo
- [ ] Integração com dbt
- [ ] Suporte a Big Data (Spark)

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Veja como você pode ajudar:

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

---

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 👥 Autor

Desenvolvido com ❤️ e Python

---

## 🙏 Agradecimentos

- Inspirado por [Great Expectations](https://greatexpectations.io/)
- Interface construída com [Streamlit](https://streamlit.io/)
- Visualizações com [Plotly](https://plotly.com/)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Made with ❤️ and Python 🐍

</div>
