# API Documentation - DataSentinel

## 📚 Documentação da API

### BaseConnector

Interface base para todos os conectores de dados.

```python
from app.connectors.base import BaseConnector

class BaseConnector(ABC):
    """Classe abstrata para conectores de fonte de dados"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Estabelece conexão com a fonte de dados"""
        
    @abstractmethod
    def disconnect(self) -> bool:
        """Fecha a conexão com a fonte de dados"""
        
    @abstractmethod
    def execute_query(self, query: str) -> pd.DataFrame:
        """Executa uma query e retorna os resultados"""
        
    @abstractmethod
    def get_table_data(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """Recupera dados de uma tabela específica"""
        
    @abstractmethod
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """Retorna metadados da tabela"""
```

---

### MockConnector

Conector simulado para testes e desenvolvimento.

#### Inicialização

```python
from app.connectors import MockConnector

# Configuração padrão
mock = MockConnector()

# Com simulação de latência
mock = MockConnector({
    'simulate_delay': True,
    'delay_seconds': 0.5
})

# Simulando falha
mock = MockConnector({
    'fail_connection': True
})
```

#### Métodos

##### `connect() -> bool`
Estabelece conexão simulada.

```python
with MockConnector() as mock:
    # Conexão automática via context manager
    data = mock.get_table_data('sales')
```

##### `list_tables() -> List[str]`
Lista todas as tabelas disponíveis.

```python
tables = mock.list_tables()
# Retorna: ['sales', 'customers', 'products', 'transactions']
```

##### `get_table_data(table_name: str, limit: Optional[int] = None) -> pd.DataFrame`
Busca dados de uma tabela.

```python
# Todos os dados
data = mock.get_table_data('sales')

# Com limite
data = mock.get_table_data('sales', limit=10)
```

##### `add_mock_table(table_name: str, data: pd.DataFrame)`
Adiciona uma tabela customizada.

```python
import pandas as pd

custom_data = pd.DataFrame({
    'id': [1, 2, 3],
    'value': [100, 200, 300]
})

mock.add_mock_table('minha_tabela', custom_data)
```

##### `reset_to_defaults()`
Reseta todas as tabelas para os dados padrão.

```python
mock.reset_to_defaults()
```

---

### DataValidator

Motor de validação de qualidade de dados.

#### Inicialização

```python
from app.core.engine import DataValidator
import pandas as pd

df = pd.DataFrame({...})
validator = DataValidator(df, table_name='minha_tabela')
```

#### Métodos de Validação

##### `expect_column_values_to_not_be_null(column: str, threshold: float = 0.0) -> ValidationResult`

Valida que uma coluna não contenha valores nulos.

```python
result = validator.expect_column_values_to_not_be_null('email', threshold=5.0)
# threshold: percentual aceitável de nulos (0.0 = nenhum nulo)
```

##### `expect_column_values_to_be_between(column: str, min_val: float, max_val: float, allow_null: bool = False) -> ValidationResult`

Valida que valores estejam dentro de um intervalo.

```python
result = validator.expect_column_values_to_be_between('age', 18, 120)
result = validator.expect_column_values_to_be_between('price', 0, 10000, allow_null=True)
```

##### `expect_column_values_to_be_unique(column: str) -> ValidationResult`

Valida que todos os valores de uma coluna sejam únicos.

```python
result = validator.expect_column_values_to_be_unique('user_id')
```

##### `detect_outliers_zscore(column: str, threshold: float = 3.0) -> ValidationResult`

Detecta outliers usando Z-Score.

```python
result = validator.detect_outliers_zscore('salary', threshold=2.5)
# threshold: número de desvios padrão (padrão: 3.0)
```

##### `get_summary() -> Dict[str, Any]`

Retorna resumo executivo das validações.

```python
summary = validator.get_summary()

print(summary)
# {
#     'table_name': 'sales',
#     'total_checks': 5,
#     'passed': 3,
#     'failed': 2,
#     'success_rate': 60.0,
#     'overall_status': '❌ ISSUES DETECTED'
# }
```

---

### ValidationResult

Resultado de uma validação individual.

#### Atributos

```python
result.check_name    # Nome da verificação
result.status        # Status visual ("✅ PASS" ou "❌ FAIL")
result.passed        # Boolean indicando sucesso
result.details       # Descrição detalhada
result.severity      # "INFO", "WARNING", "ERROR", "CRITICAL"
result.timestamp     # Datetime da execução
result.metadata      # Dicionário com dados adicionais
```

#### Métodos

##### `to_dict() -> Dict[str, Any]`

Converte resultado para dicionário.

```python
result_dict = result.to_dict()
```

---

## 🔧 Exemplos Avançados

### Validação Completa de uma Tabela

```python
from app.connectors import MockConnector
from app.core.engine import DataValidator

with MockConnector() as conn:
    # Carrega dados
    sales_data = conn.get_table_data('sales')
    
    # Cria validador
    validator = DataValidator(sales_data, 'sales')
    
    # Executa múltiplas validações
    validator.expect_column_values_to_not_be_null('product_name')
    validator.expect_column_values_to_not_be_null('price', threshold=5.0)
    validator.expect_column_values_to_be_between('price', 0, 100000)
    validator.expect_column_values_to_be_between('quantity', 1, 1000)
    validator.expect_column_values_to_be_unique('sale_id')
    validator.detect_outliers_zscore('price', threshold=3.0)
    
    # Analisa resultados
    summary = validator.get_summary()
    
    if summary['failed'] > 0:
        print(f"⚠️  {summary['failed']} validações falharam!")
        
        for result in validator.results:
            if not result.passed:
                print(f"  ❌ {result.check_name}: {result.details}")
    else:
        print("✅ Todos os testes passaram!")
```

### Pipeline de Validação

```python
def validate_data_pipeline(connector, table_name):
    """Pipeline de validação reutilizável"""
    
    # Carrega dados
    data = connector.get_table_data(table_name)
    
    # Cria validador
    validator = DataValidator(data, table_name)
    
    # Validações automáticas baseadas em tipos
    for column in data.columns:
        # Verifica nulos
        validator.expect_column_values_to_not_be_null(column, threshold=10.0)
        
        # Para colunas numéricas, detecta outliers
        if data[column].dtype in ['int64', 'float64']:
            validator.detect_outliers_zscore(column)
    
    # Retorna resumo
    return validator.get_summary()

# Uso
with MockConnector() as conn:
    summary = validate_data_pipeline(conn, 'sales')
    print(f"Qualidade: {summary['success_rate']}%")
```

### Exportação de Relatórios

```python
import json
from datetime import datetime

# Executa validações
validator = DataValidator(df, 'sales')
validator.expect_column_values_to_not_be_null('price')
validator.expect_column_values_to_be_between('price', 0, 10000)

# Gera relatório
report = {
    'timestamp': datetime.now().isoformat(),
    'table': 'sales',
    'summary': validator.get_summary(),
    'results': [r.to_dict() for r in validator.results]
}

# Salva JSON
with open('relatorio.json', 'w') as f:
    json.dump(report, indent=2, default=str)

# Salva CSV
import pandas as pd
results_df = pd.DataFrame([r.to_dict() for r in validator.results])
results_df.to_csv('resultados.csv', index=False)
```

---

## 🎯 Melhores Práticas

1. **Use Context Managers**
   ```python
   with MockConnector() as conn:
       # Garante desconexão automática
       data = conn.get_table_data('sales')
   ```

2. **Configure Thresholds Adequados**
   ```python
   # Permite até 5% de nulos para campos opcionais
   validator.expect_column_values_to_not_be_null('optional_field', threshold=5.0)
   ```

3. **Trate Erros Apropriadamente**
   ```python
   try:
       result = validator.expect_column_values_to_be_between('age', 0, 150)
   except KeyError:
       print("Coluna 'age' não existe!")
   ```

4. **Monitore Resultados**
   ```python
   summary = validator.get_summary()
   if summary['success_rate'] < 80:
       # Alerta para equipe
       send_alert(f"Qualidade baixa: {summary['success_rate']}%")
   ```

---

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no GitHub.
