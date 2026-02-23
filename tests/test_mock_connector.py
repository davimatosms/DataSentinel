"""
Testes para o MockConnector
Valida que o conector mock funciona corretamente
"""
import pytest
import pandas as pd
import numpy as np
from app.connectors import MockConnector


class TestMockConnector:
    """Suite de testes para o MockConnector"""
    
    def test_connection_success(self):
        """Testa conexão bem-sucedida"""
        mock = MockConnector()
        assert mock.connect() == True
        assert mock.is_connected == True
        assert mock.disconnect() == True
        assert mock.is_connected == False
    
    def test_connection_failure(self):
        """Testa simulação de falha de conexão"""
        mock = MockConnector({'fail_connection': True})
        assert mock.connect() == False
        assert mock.is_connected == False
    
    def test_context_manager(self):
        """Testa uso como context manager"""
        with MockConnector() as mock:
            assert mock.is_connected == True
            tables = mock.list_tables()
            assert len(tables) > 0
        
        # Deve desconectar automaticamente
        assert mock.is_connected == False
    
    def test_list_tables(self):
        """Testa listagem de tabelas"""
        with MockConnector() as mock:
            tables = mock.list_tables()
            
            assert isinstance(tables, list)
            assert 'sales' in tables
            assert 'customers' in tables
            assert 'products' in tables
            assert len(tables) >= 3
    
    def test_get_table_data(self):
        """Testa recuperação de dados de tabela"""
        with MockConnector() as mock:
            # Sem limite
            sales_df = mock.get_table_data('sales')
            assert isinstance(sales_df, pd.DataFrame)
            assert len(sales_df) > 0
            assert 'sale_id' in sales_df.columns
            assert 'price' in sales_df.columns
            
            # Com limite
            limited_df = mock.get_table_data('sales', limit=5)
            assert len(limited_df) == 5
    
    def test_get_table_data_invalid_table(self):
        """Testa erro ao buscar tabela inexistente"""
        with MockConnector() as mock:
            with pytest.raises(ValueError, match="não existe"):
                mock.get_table_data('tabela_inexistente')
    
    def test_get_table_metadata(self):
        """Testa recuperação de metadados"""
        with MockConnector() as mock:
            metadata = mock.get_table_metadata('sales')
            
            assert isinstance(metadata, dict)
            assert 'table_name' in metadata
            assert 'total_rows' in metadata
            assert 'total_columns' in metadata
            assert 'columns' in metadata
            
            assert metadata['table_name'] == 'sales'
            assert metadata['total_rows'] > 0
            assert len(metadata['columns']) > 0
            
            # Verifica estrutura de coluna
            col_info = metadata['columns'][0]
            assert 'column_name' in col_info
            assert 'data_type' in col_info
            assert 'is_nullable' in col_info
    
    def test_execute_query(self):
        """Testa execução de queries"""
        with MockConnector() as mock:
            # Query simples
            result = mock.execute_query("SELECT * FROM sales")
            assert isinstance(result, pd.DataFrame)
            assert len(result) > 0
            
            # Query com LIMIT
            result = mock.execute_query("SELECT * FROM sales LIMIT 10")
            assert len(result) == 10
    
    def test_execute_query_invalid_table(self):
        """Testa erro ao executar query com tabela inválida"""
        with MockConnector() as mock:
            with pytest.raises(ValueError, match="Tabela não encontrada"):
                mock.execute_query("SELECT * FROM tabela_invalida")
    
    def test_add_custom_table(self):
        """Testa adição de tabela customizada"""
        custom_data = pd.DataFrame({
            'id': [1, 2, 3],
            'value': ['A', 'B', 'C']
        })
        
        with MockConnector() as mock:
            initial_count = len(mock.list_tables())
            
            mock.add_mock_table('custom_table', custom_data)
            
            assert len(mock.list_tables()) == initial_count + 1
            assert 'custom_table' in mock.list_tables()
            
            retrieved_data = mock.get_table_data('custom_table')
            pd.testing.assert_frame_equal(retrieved_data, custom_data)
    
    def test_clear_table(self):
        """Testa limpeza de tabela"""
        with MockConnector() as mock:
            # Verifica que tem dados
            sales_df = mock.get_table_data('sales')
            assert len(sales_df) > 0
            
            # Limpa tabela
            mock.clear_table('sales')
            
            # Verifica que está vazia
            empty_df = mock.get_table_data('sales')
            assert len(empty_df) == 0
    
    def test_reset_to_defaults(self):
        """Testa reset para dados padrão"""
        with MockConnector() as mock:
            # Limpa uma tabela
            mock.clear_table('sales')
            assert len(mock.get_table_data('sales')) == 0
            
            # Reseta
            mock.reset_to_defaults()
            
            # Verifica que os dados voltaram
            sales_df = mock.get_table_data('sales')
            assert len(sales_df) > 0
    
    def test_data_quality_issues(self):
        """Testa que os dados mock contêm problemas propositais para validação"""
        with MockConnector() as mock:
            sales_df = mock.get_table_data('sales')
            
            # Deve ter preços nulos
            assert sales_df['price'].isnull().any()
            
            # Deve ter preços negativos
            assert (sales_df['price'] < 0).any()
            
            # Deve ter emails nulos
            assert sales_df['customer_email'].isnull().any()
            
            # Deve ter quantidades zero
            assert (sales_df['quantity'] == 0).any()
    
    def test_customers_data_issues(self):
        """Testa problemas nos dados de clientes"""
        with MockConnector() as mock:
            customers_df = mock.get_table_data('customers')
            
            # Deve ter idades inválidas (muito altas ou negativas)
            assert (customers_df['age'] > 150).any() or (customers_df['age'] < 0).any()
            
            # Deve ter cidades nulas
            assert customers_df['city'].isnull().any()
    
    def test_connection_required_for_operations(self):
        """Testa que operações exigem conexão ativa"""
        mock = MockConnector()
        
        # Sem conectar, deve falhar
        with pytest.raises(ConnectionError, match="não está conectado"):
            mock.get_table_data('sales')
        
        with pytest.raises(ConnectionError, match="não está conectado"):
            mock.execute_query("SELECT * FROM sales")
        
        with pytest.raises(ConnectionError, match="não está conectado"):
            mock.get_table_metadata('sales')
    
    def test_network_delay_simulation(self):
        """Testa simulação de delay de rede"""
        import time
        
        mock = MockConnector({
            'simulate_delay': True,
            'delay_seconds': 0.1
        })
        
        # Conectar deve ter delay
        start = time.time()
        mock.connect()
        elapsed = time.time() - start
        assert elapsed >= 0.1
        
        # Operações devem ter delay
        start = time.time()
        mock.get_table_data('sales', limit=5)
        elapsed = time.time() - start
        assert elapsed >= 0.1
        
        mock.disconnect()
    
    def test_large_dataset(self):
        """Testa que há uma tabela com volume maior para testes de performance"""
        with MockConnector() as mock:
            transactions_df = mock.get_table_data('transactions')
            
            # Deve ter pelo menos 100 registros
            assert len(transactions_df) >= 100
            assert 'transaction_id' in transactions_df.columns
            assert 'amount' in transactions_df.columns
    
    def test_default_tables_structure(self):
        """Testa estrutura das tabelas padrão"""
        with MockConnector() as mock:
            # Sales deve ter colunas específicas
            sales_df = mock.get_table_data('sales')
            expected_cols = ['sale_id', 'product_name', 'price', 'quantity', 
                           'customer_email', 'sale_date', 'status']
            for col in expected_cols:
                assert col in sales_df.columns
            
            # Customers deve ter colunas específicas
            customers_df = mock.get_table_data('customers')
            expected_cols = ['customer_id', 'name', 'age', 'city', 'premium_customer']
            for col in expected_cols:
                assert col in customers_df.columns
            
            # Products deve ter colunas específicas
            products_df = mock.get_table_data('products')
            expected_cols = ['product_id', 'category', 'stock', 'min_stock', 'supplier']
            for col in expected_cols:
                assert col in products_df.columns


class TestMockConnectorIntegration:
    """Testes de integração com DataValidator"""
    
    def test_integration_with_validator(self):
        """Testa integração com o DataValidator"""
        from app.core.engine import DataValidator
        
        with MockConnector() as mock:
            sales_df = mock.get_table_data('sales')
            
            validator = DataValidator(sales_df, 'sales')
            
            # Executa algumas validações
            validator.expect_column_values_to_not_be_null('price', threshold=0.0)
            validator.expect_column_values_to_be_between('quantity', 1, 1000)
            
            summary = validator.get_summary()
            
            assert summary['total_checks'] == 2
            assert 'success_rate' in summary
            assert 'overall_status' in summary
    
    def test_multiple_tables_validation(self):
        """Testa validação de múltiplas tabelas"""
        from app.core.engine import DataValidator
        
        with MockConnector() as mock:
            results = {}
            
            for table_name in ['sales', 'customers', 'products']:
                df = mock.get_table_data(table_name)
                validator = DataValidator(df, table_name)
                
                # Validação genérica
                for col in df.columns:
                    if df[col].dtype in ['int64', 'float64']:
                        validator.expect_column_values_to_not_be_null(col, threshold=10.0)
                
                results[table_name] = validator.get_summary()
            
            # Todas as tabelas devem ter sido validadas
            assert len(results) == 3
            for table_name, summary in results.items():
                assert summary['total_checks'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
