"""
Exemplo de uso do MockConnector
Demonstra como testar a aplicação sem banco de dados real
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from app.connectors import MockConnector
from app.core.engine import DataValidator
from app.utils.reporter import ReportGenerator
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def exemplo_basico():
    """Exemplo 1: Uso básico do MockConnector"""
    print("\n" + "="*80)
    print("EXEMPLO 1: Uso Básico do MockConnector")
    print("="*80 + "\n")
    
    # Cria conector mock
    mock = MockConnector()
    
    # Conecta (simulado)
    mock.connect()
    
    # Lista tabelas disponíveis
    print(f"📋 Tabelas disponíveis: {mock.list_tables()}\n")
    
    # Busca dados de uma tabela
    sales_df = mock.get_table_data('sales', limit=5)
    print("📊 Primeiras 5 vendas:")
    print(sales_df)
    print()
    
    # Busca metadados
    metadata = mock.get_table_metadata('sales')
    print(f"\n📈 Metadados da tabela 'sales':")
    print(f"  - Total de linhas: {metadata['total_rows']}")
    print(f"  - Total de colunas: {metadata['total_columns']}")
    print(f"  - Uso de memória: {metadata['memory_usage_mb']:.2f} MB")
    
    # Desconecta
    mock.disconnect()


def exemplo_validacao_qualidade():
    """Exemplo 2: Validação de qualidade de dados com MockConnector"""
    print("\n" + "="*80)
    print("EXEMPLO 2: Validação de Qualidade de Dados")
    print("="*80 + "\n")
    
    # Usa context manager
    with MockConnector() as mock:
        # Carrega dados da tabela de vendas
        sales_df = mock.get_table_data('sales')
        
        print(f"✅ Carregados {len(sales_df)} registros de vendas\n")
        
        # Cria validador
        validator = DataValidator(sales_df, table_name='sales')
        
        # Executa validações
        print("🔍 Executando validações...\n")
        
        # 1. Validar preços não nulos
        validator.expect_column_values_to_not_be_null('price', threshold=0.0)
        
        # 2. Validar preços positivos
        validator.expect_column_values_to_be_between('price', min_val=0, max_val=10000)
        
        # 3. Validar emails não nulos
        validator.expect_column_values_to_not_be_null('customer_email', threshold=5.0)
        
        # 4. Validar quantidades
        validator.expect_column_values_to_be_between('quantity', min_val=1, max_val=1000)
        
        # 5. Detectar outliers nos preços
        validator.detect_outliers_zscore('price', threshold=2.5)
        
        # Gera resumo
        summary = validator.get_summary()
        
        print("\n" + "="*80)
        print("📊 RESUMO DA VALIDAÇÃO")
        print("="*80)
        print(f"Total de verificações: {summary['total_checks']}")
        print(f"Aprovadas: {summary['passed']} [OK]")
        print(f"Falharam: {summary['failed']} [X]")
        print(f"Taxa de sucesso: {summary['success_rate']:.1f}%")
        print(f"Status geral: {summary['overall_status']}")
        print()
        
        # Mostra detalhes dos problemas
        print("🔍 Problemas detectados:")
        for result in validator.results:
            if not result.passed:
                print(f"\n❌ {result.check_name}")
                print(f"   {result.details}")


def exemplo_multiplas_tabelas():
    """Exemplo 3: Validação em múltiplas tabelas"""
    print("\n" + "="*80)
    print("EXEMPLO 3: Validação em Múltiplas Tabelas")
    print("="*80 + "\n")
    
    with MockConnector() as mock:
        # Valida tabela de clientes
        print("👥 Validando tabela de CLIENTES...")
        customers_df = mock.get_table_data('customers')
        
        validator_customers = DataValidator(customers_df, 'customers')
        validator_customers.expect_column_values_to_not_be_null('name')
        validator_customers.expect_column_values_to_not_be_null('city', threshold=5.0)
        validator_customers.expect_column_values_to_be_between('age', 18, 120)
        
        summary_customers = validator_customers.get_summary()
        print(f"[OK] Clientes: {summary_customers['passed']}/{summary_customers['total_checks']} checks passaram")
        
        # Valida tabela de produtos
        print("\n📦 Validando tabela de PRODUTOS...")
        products_df = mock.get_table_data('products')
        
        validator_products = DataValidator(products_df, 'products')
        validator_products.expect_column_values_to_not_be_null('category')
        validator_products.expect_column_values_to_be_between('stock', 0, 10000)
        
        # Verifica se estoque está abaixo do mínimo
        low_stock = products_df[products_df['stock'] < products_df['min_stock']]
        if len(low_stock) > 0:
            print(f"⚠️  ALERTA: {len(low_stock)} produtos com estoque abaixo do mínimo!")
        
        summary_products = validator_products.get_summary()
        print(f"[OK] Produtos: {summary_products['passed']}/{summary_products['total_checks']} checks passaram")


def exemplo_simulacao_falhas():
    """Exemplo 4: Simulando falhas e latência"""
    print("\n" + "="*80)
    print("EXEMPLO 4: Simulando Falhas e Latência de Rede")
    print("="*80 + "\n")
    
    # Simula falha de conexão
    print("🔌 Testando falha de conexão...")
    mock_fail = MockConnector({'fail_connection': True})
    result = mock_fail.connect()
    print(f"Resultado da conexão: {result}\n")
    
    # Simula latência de rede
    print("⏱️  Testando com latência de rede (0.5s)...")
    import time
    mock_slow = MockConnector({
        'simulate_delay': True,
        'delay_seconds': 0.5
    })
    
    start = time.time()
    mock_slow.connect()
    elapsed = time.time() - start
    print(f"Tempo de conexão: {elapsed:.2f}s")
    
    start = time.time()
    data = mock_slow.get_table_data('sales', limit=5)
    elapsed = time.time() - start
    print(f"Tempo para buscar dados: {elapsed:.2f}s")
    
    mock_slow.disconnect()


def exemplo_dados_customizados():
    """Exemplo 5: Adicionando dados customizados"""
    print("\n" + "="*80)
    print("EXEMPLO 5: Dados Customizados")
    print("="*80 + "\n")
    
    import pandas as pd
    import numpy as np
    
    # Cria dados customizados
    custom_data = pd.DataFrame({
        'user_id': range(1, 11),
        'username': [f'user_{i}' for i in range(1, 11)],
        'score': np.random.randint(0, 100, 10),
        'active': np.random.choice([True, False], 10)
    })
    
    with MockConnector() as mock:
        # Adiciona tabela customizada
        mock.add_mock_table('users', custom_data)
        
        print(f"📋 Tabelas disponíveis: {mock.list_tables()}\n")
        
        # Busca dados customizados
        users_df = mock.get_table_data('users')
        print("👤 Dados de usuários customizados:")
        print(users_df)
        
        # Valida dados customizados
        validator = DataValidator(users_df, 'users')
        validator.expect_column_values_to_be_unique('user_id')
        validator.expect_column_values_to_be_between('score', 0, 100)
        
        summary = validator.get_summary()
        print(f"\n✅ Validação: {summary['overall_status']}")


def exemplo_queries():
    """Exemplo 6: Executando queries simuladas"""
    print("\n" + "="*80)
    print("EXEMPLO 6: Executando Queries SQL Simuladas")
    print("="*80 + "\n")
    
    with MockConnector() as mock:
        # Query simples
        print("🔍 SELECT * FROM sales LIMIT 3")
        result = mock.execute_query("SELECT * FROM sales LIMIT 3")
        print(result)
        print()
        
        # Query em outra tabela
        print("🔍 SELECT * FROM customers LIMIT 5")
        result = mock.execute_query("SELECT * FROM customers LIMIT 5")
        print(result[['customer_id', 'name', 'city', 'age']])


def main():
    """Executa todos os exemplos"""
    print("\n" + "="*80)
    print("DEMONSTRACAO DO MOCKCONNECTOR - TESTES SEM BANCO DE DADOS")
    print("="*80)
    
    try:
        exemplo_basico()
        exemplo_validacao_qualidade()
        exemplo_multiplas_tabelas()
        exemplo_simulacao_falhas()
        exemplo_dados_customizados()
        exemplo_queries()
        
        print("\n" + "="*80)
        print("TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("="*80 + "\n")
        
        print("VANTAGENS DO MOCKCONNECTOR:")
        print("   [OK] Testes rapidos sem infraestrutura")
        print("   [OK] Dados controlados e reproduziveis")
        print("   [OK] Simula erros e edge cases")
        print("   [OK] Desenvolvimento offline")
        print("   [OK] CI/CD sem dependencias externas")
        print()
        
    except Exception as e:
        logger.error(f"❌ Erro durante execução: {e}", exc_info=True)


if __name__ == "__main__":
    main()
