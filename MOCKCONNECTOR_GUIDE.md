# 🚀 DataSentinel - Guia de Setup e Uso do MockConnector

## ✅ Sistema de Simulação Implementado!

Criamos um **MockConnector** completo que permite testar toda a aplicação **SEM BANCO DE DADOS REAL**.

---

## 📦 O que foi criado:

### 1. **MockConnector** (`app/connectors/mock.py`)
Conector simulado com:
- ✅ 4 tabelas mockadas (sales, customers, products, transactions)
- ✅ Dados com erros propositais para validação
- ✅ Simulação de latência de rede
- ✅ Simulação de falhas de conexão
- ✅ Suporte a queries SQL básicas
- ✅ Adição de tabelas customizadas

### 2. **Script de Demonstração** (`demo_mock.py`)
6 exemplos práticos:
- Uso básico do MockConnector
- Validação de qualidade de dados
- Validação em múltiplas tabelas
- Simulação de falhas e latência
- Dados customizados
- Execução de queries

### 3. **Testes Automatizados** (`tests/test_mock_connector.py`)
Suite completa com 20+ testes cobrindo:
- Conexão/desconexão
- Busca de dados e metadados
- Queries SQL
- Integração com DataValidator
- Simulação de erros

---

## 🔧 Como Usar (depois de instalar Python):

### Instalação do Python:
1. Baixe Python 3.8+ em: https://www.python.org/downloads/
2. **IMPORTANTE**: Marque "Add Python to PATH" durante instalação
3. Reinicie o terminal

### Instalar Dependências:
```powershell
pip install -r requirements.txt
```

### Executar Demonstração:
```powershell
python demo_mock.py
```

### Executar Testes:
```powershell
pytest tests/test_mock_connector.py -v
```

---

## 💡 Exemplos de Uso no Código:

### Exemplo 1: Uso Básico
```python
from app.connectors import MockConnector

# Cria e conecta
with MockConnector() as mock:
    # Lista tabelas
    tables = mock.list_tables()
    print(f"Tabelas: {tables}")
    
    # Busca dados
    sales = mock.get_table_data('sales', limit=10)
    print(sales)
```

### Exemplo 2: Validação de Qualidade
```python
from app.connectors import MockConnector
from app.core.engine import DataValidator

with MockConnector() as mock:
    # Carrega dados
    df = mock.get_table_data('sales')
    
    # Valida
    validator = DataValidator(df, 'sales')
    validator.expect_column_values_to_not_be_null('price')
    validator.expect_column_values_to_be_between('price', 0, 10000)
    
    # Resultados
    summary = validator.get_summary()
    print(f"Taxa de sucesso: {summary['success_rate']}%")
```

### Exemplo 3: Dados Customizados
```python
import pandas as pd
from app.connectors import MockConnector

# Cria seus próprios dados
custom_data = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['A', 'B', 'C'],
    'value': [100, 200, 300]
})

with MockConnector() as mock:
    # Adiciona ao mock
    mock.add_mock_table('minha_tabela', custom_data)
    
    # Usa normalmente
    data = mock.get_table_data('minha_tabela')
    print(data)
```

### Exemplo 4: Simular Falhas
```python
# Simula falha de conexão
mock = MockConnector({'fail_connection': True})
result = mock.connect()  # Retorna False

# Simula latência
mock = MockConnector({
    'simulate_delay': True,
    'delay_seconds': 0.5
})
```

---

## 🎯 Vantagens do MockConnector:

✅ **Testes Rápidos** - Sem esperar banco de dados  
✅ **Desenvolvimento Offline** - Trabalhe em qualquer lugar  
✅ **Dados Controlados** - Resultados reproduzíveis  
✅ **Simula Erros** - Teste edge cases facilmente  
✅ **CI/CD Simples** - Sem infraestrutura nos pipelines  
✅ **Prototipagem Rápida** - Teste ideias rapidamente  

---

## 📊 Dados Mockados Inclusos:

### Tabela: `sales` (20 registros)
- Vendas com preços (alguns negativos/nulos ❌)
- Quantidades (algumas zeradas ❌)
- Emails (alguns inválidos/nulos ❌)
- Datas e status

### Tabela: `customers` (10 registros)
- Clientes com idades (algumas inválidas ❌)
- Cidades (algumas nulas ❌)
- Flag premium

### Tabela: `products` (15 registros)
- Produtos com estoque
- Estoque mínimo
- Categorias e fornecedores

### Tabela: `transactions` (1000 registros)
- Grande volume para testes de performance
- Valores aleatórios
- Status variados

---

## 🧪 Estrutura dos Testes:

```
tests/
├── test_engine.py           # Testes do motor de validação
└── test_mock_connector.py   # Testes do MockConnector (NOVO!)
```

---

## 🔄 Workflow de Desenvolvimento:

1. **Desenvolvimento Local**
   ```python
   mock = MockConnector()
   # Desenvolva e teste rapidamente
   ```

2. **Testes Automatizados**
   ```bash
   pytest tests/test_mock_connector.py
   ```

3. **Integração/Produção**
   ```python
   # Troque para conector real
   from app.connectors import PostgreSQLConnector
   conn = PostgreSQLConnector(config)
   ```

---

## 📝 Próximos Passos:

1. Instale o Python (se ainda não tem)
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute a demo: `python demo_mock.py`
4. Execute os testes: `pytest tests/test_mock_connector.py -v`
5. Integre o MockConnector no seu workflow!

---

## 🆘 Suporte:

Se precisar de ajuda ou quiser customizar o MockConnector, é só pedir!

**Arquivos criados:**
- ✅ `app/connectors/mock.py` (320 linhas)
- ✅ `demo_mock.py` (290 linhas)
- ✅ `tests/test_mock_connector.py` (280 linhas)
- ✅ `app/connectors/__init__.py` (atualizado)

**Total:** ~900 linhas de código para testes sem banco de dados! 🎉
