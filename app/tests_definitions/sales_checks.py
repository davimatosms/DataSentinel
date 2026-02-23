"""
Definições de Testes para Dados de Vendas
Exemplo de como configurar regras de validação para uma tabela
"""
import pandas as pd
from app.core.engine import DataValidator


def validate_sales_data(df: pd.DataFrame) -> DataValidator:
    """
    Executa validações na tabela de vendas
    
    Args:
        df: DataFrame com dados de vendas
        
    Returns:
        DataValidator com resultados das validações
    """
    validator = DataValidator(df, table_name="sales")
    
    # ========== VALIDAÇÕES DE NULIDADE ==========
    print("\n🔍 Executando validações de nulidade...")
    validator.expect_column_values_to_not_be_null('product_id')
    validator.expect_column_values_to_not_be_null('price', threshold=0.0)
    validator.expect_column_values_to_not_be_null('email_contato', threshold=5.0)  # Permite até 5% de nulos
    
    # ========== VALIDAÇÕES DE INTERVALO ==========
    print("\n🔍 Executando validações de intervalo...")
    validator.expect_column_values_to_be_between('price', min_val=0, max_val=100000, allow_null=False)
    
    # ========== VALIDAÇÕES DE UNICIDADE ==========
    print("\n🔍 Executando validações de unicidade...")
    validator.expect_column_values_to_be_unique('product_id')
    
    # ========== VALIDAÇÕES DE FORMATO ==========
    print("\n🔍 Executando validações de formato...")
    # Regex para validar email básico
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    validator.expect_column_values_to_match_regex(
        'email_contato', 
        email_regex, 
        description="Email válido"
    )
    
    # ========== VALIDAÇÕES ESTATÍSTICAS ==========
    print("\n🔍 Executando validações estatísticas...")
    validator.expect_column_mean_to_be_between('price', min_val=50, max_val=200)
    
    # ========== DETECÇÃO DE ANOMALIAS ==========
    print("\n🔍 Detectando anomalias (outliers)...")
    validator.detect_outliers_zscore('price', threshold=3.0)
    
    return validator


def validate_customer_data(df: pd.DataFrame) -> DataValidator:
    """
    Exemplo de validações para dados de clientes
    
    Args:
        df: DataFrame com dados de clientes
        
    Returns:
        DataValidator com resultados
    """
    validator = DataValidator(df, table_name="customers")
    
    # Validações básicas de cliente
    validator.expect_column_values_to_not_be_null('customer_id')
    validator.expect_column_values_to_not_be_null('customer_name')
    validator.expect_column_values_to_be_unique('customer_id')
    
    # Validação de email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    validator.expect_column_values_to_match_regex('email', email_regex, "Email válido")
    
    return validator


def validate_financial_data(df: pd.DataFrame) -> DataValidator:
    """
    Validações específicas para dados financeiros
    
    Args:
        df: DataFrame com dados financeiros
        
    Returns:
        DataValidator com resultados
    """
    validator = DataValidator(df, table_name="financial")
    
    # Validações financeiras críticas
    validator.expect_column_values_to_not_be_null('transaction_id')
    validator.expect_column_values_to_not_be_null('amount')
    validator.expect_column_values_to_not_be_null('transaction_date')
    
    # Valores não podem ser negativos (dependendo da lógica de negócio)
    validator.expect_column_values_to_be_between('amount', min_val=0, max_val=1000000)
    
    # Unicidade de transações
    validator.expect_column_values_to_be_unique('transaction_id')
    
    # Detecção de transações anômalas
    validator.detect_outliers_zscore('amount', threshold=3.0)
    
    # Validações estatísticas
    validator.expect_column_mean_to_be_between('amount', min_val=100, max_val=50000)
    validator.expect_column_stdev_to_be_between('amount', min_val=10, max_val=100000)
    
    return validator
