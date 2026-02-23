# 🛡️ DataSentinel

**Data Quality Ops & Data Observability Tool**

Uma ferramenta profissional para monitoramento e validação automática da qualidade de dados em múltiplas fontes.

## 🎯 Objetivo

O DataSentinel é um serviço agendado que "escaneia" suas tabelas e gera relatórios de saúde dos dados, detectando:

- ✅ Valores nulos e missing data
- ✅ Valores fora de intervalos esperados
- ✅ Duplicatas e violações de unicidade
- ✅ Formatos inválidos (emails, datas, etc)
- ✅ Anomalias estatísticas (outliers via Z-Score)
- ✅ Desvios de padrões históricos

## 🏗️ Arquitetura

O projeto segue uma arquitetura modular e escalável:

```
DataSentinel/
├── app/
│   ├── connectors/       # Conexões com diferentes fontes de dados
│   │   ├── base.py       # Interface abstrata
│   │   └── database.py   # PostgreSQL, SQL Server, CSV
│   ├── core/
│   │   ├── config.py     # Configurações e variáveis de ambiente
│   │   └── engine.py     # Motor de validação (DataValidator)
│   ├── tests_definitions/
│   │   └── sales_checks.py  # Definição de regras de negócio
│   └── utils/
│       └── reporter.py   # Geração de relatórios (JSON, HTML, CSV)
├── tests/                # Testes unitários
├── reports/              # Relatórios gerados
├── requirements.txt
├── main.py               # Ponto de entrada
└── README.md
```

## 🚀 Instalação

### 1. Clone ou crie o projeto

```bash
cd DataSentinel
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais de banco de dados.

## 📊 Uso Básico

### Executar Demo com Dados de Exemplo

```bash
python main.py
```

Isso irá:
1. Criar dados de exemplo (vendas com erros propositais)
2. Executar validações de qualidade
3. Gerar relatórios em JSON, HTML e CSV
4. Exibir resumo no console

### Usar com Seus Próprios Dados

```python
from app.core.engine import DataValidator
import pandas as pd

# Carregar seus dados
df = pd.read_csv('seu_arquivo.csv')

# Criar validador
validator = DataValidator(df, table_name="sua_tabela")

# Definir expectativas
validator.expect_column_values_to_not_be_null('email')
validator.expect_column_values_to_be_between('preco', 0, 10000)
validator.expect_column_values_to_be_unique('id_produto')

# Obter relatório
report = validator.get_report()
summary = validator.get_summary()
```

## 🔍 Tipos de Validações Disponíveis

### Validações de Nulidade
```python
validator.expect_column_values_to_not_be_null('coluna', threshold=5.0)
```

### Validações de Intervalo
```python
validator.expect_column_values_to_be_between('preco', min_val=0, max_val=1000)
```

### Validações de Unicidade
```python
validator.expect_column_values_to_be_unique('id_cliente')
```

### Validações de Formato (Regex)
```python
validator.expect_column_values_to_match_regex(
    'email', 
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    description="Email válido"
)
```

### Validações Estatísticas
```python
validator.expect_column_mean_to_be_between('faturamento', 1000, 50000)
validator.expect_column_stdev_to_be_between('faturamento', 100, 10000)
```

### Detecção de Anomalias (Z-Score)
```python
validator.detect_outliers_zscore('vendas_diarias', threshold=3.0)
```

## 📄 Formatos de Relatório

### JSON
Estrutura completa com metadados para integração com outras ferramentas.

### HTML
Relatório visual com tabelas e métricas destacadas. Abra no navegador!

### CSV
Para análises no Excel ou BI tools.

### Slack (opcional)
Envie alertas automáticos para seu canal do Slack.

## 🔌 Conectores Disponíveis

### PostgreSQL
```python
from app.connectors.database import PostgreSQLConnector

config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydb',
    'user': 'user',
    'password': 'pass'
}

with PostgreSQLConnector(config) as conn:
    df = conn.get_table_data('sales')
```

### SQL Server
```python
from app.connectors.database import SQLServerConnector

config = {
    'server': 'localhost',
    'database': 'mydb',
    'user': 'user',
    'password': 'pass'
}

with SQLServerConnector(config) as conn:
    df = conn.get_table_data('sales')
```

### CSV
```python
from app.connectors.database import CSVConnector

config = {'file_path': 'data/sales.csv'}

with CSVConnector(config) as conn:
    df = conn.get_table_data('sales')
```

## 🎯 Próximos Passos (Roadmap)

### Fase 2: Otimização para Big Data
- [ ] Validações direto no banco (SQL) sem carregar no Pandas
- [ ] Suporte para Spark/Dask para grandes volumes

### Fase 3: Dashboard Interativo
- [ ] Interface web com Streamlit
- [ ] Gráficos de evolução temporal da qualidade
- [ ] Histórico de execuções

### Fase 4: Machine Learning
- [ ] Detecção automática de anomalias com algoritmos ML
- [ ] Predição de problemas futuros
- [ ] Alertas inteligentes baseados em padrões

### Fase 5: Integração com Airflow
- [ ] DAGs para execução agendada
- [ ] Integração com pipelines de dados

## 🧪 Testes

```bash
# Executar testes unitários
pytest tests/

# Com cobertura
pytest --cov=app tests/
```

## 📝 Licença

Este projeto é open-source e está disponível sob a licença MIT.

## 👨‍💻 Autor

Desenvolvido como projeto de portfólio de Data Quality & Data Engineering.

---

**DataSentinel** - Porque dados saudáveis são dados confiáveis! 🛡️
