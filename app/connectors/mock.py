"""
Mock Connector
Conector simulado para testes sem necessidade de banco de dados real
"""
import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, Any, List
from .base import BaseConnector
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockConnector(BaseConnector):
    """
    Conector Mock para testes e desenvolvimento
    Simula um banco de dados em memória sem necessidade de infraestrutura real
    """
    
    def __init__(self, connection_config: Dict[str, Any] = None):
        """
        Args:
            connection_config: Configurações opcionais como:
                - 'simulate_delay': bool - Simula latência de rede (padrão: False)
                - 'delay_seconds': float - Tempo de delay em segundos (padrão: 0.1)
                - 'fail_connection': bool - Simula falha de conexão (padrão: False)
                - 'mock_data': Dict - Dados mockados por tabela
        """
        config = connection_config or {}
        super().__init__(config)
        
        self.simulate_delay = config.get('simulate_delay', False)
        self.delay_seconds = config.get('delay_seconds', 0.1)
        self.fail_connection = config.get('fail_connection', False)
        self.mock_tables = config.get('mock_data', self._default_mock_data())
        self.is_connected = False
    
    def _default_mock_data(self) -> Dict[str, pd.DataFrame]:
        """Cria dados mockados padrão para várias tabelas"""
        np.random.seed(42)
        
        # Tabela de vendas com alguns erros propositais
        sales_data = pd.DataFrame({
            'sale_id': range(1, 21),
            'product_name': [
                'Notebook', 'Mouse', 'Teclado', 'Monitor', 'Webcam',
                'Headset', 'SSD', 'RAM', 'Processador', 'Placa de Vídeo',
                'Gabinete', 'Fonte', 'Cooler', 'Mousepad', 'Hub USB',
                'Cabo HDMI', 'Adaptador', 'HD Externo', 'Pendrive', 'Roteador'
            ],
            'price': [
                3500.00, 150.00, 350.00, 1200.00, 250.00,
                400.00, 800.00, 600.00, 1500.00, 2800.00,
                500.00, 450.00, 120.00, 80.00, 150.00,
                50.00, -30.00, 400.00, np.nan, 350.00  # Erros: preço negativo e nulo
            ],
            'quantity': [
                5, 10, 8, 3, 7,
                6, 12, 15, 4, 2,
                8, 9, 20, 25, 10,
                30, 15, 8, 0, 5  # Erro: quantidade zero
            ],
            'customer_email': [
                'cliente1@email.com', 'cliente2@email.com', 'cliente3@email.com',
                'invalido.com', 'cliente5@email.com',  # Erro: email inválido
                'cliente6@email.com', None, 'cliente8@email.com',  # Erro: email nulo
                'cliente9@email.com', 'cliente10@email.com',
                'cliente11@email.com', 'cliente12@email.com', 'cliente13@email.com',
                'cliente14@email.com', 'cliente15@email.com', 'cliente16@email.com',
                'cliente17@email.com', 'cliente18@email.com', 'cliente19@email.com',
                'cliente20@email.com'
            ],
            'sale_date': pd.date_range('2026-01-01', periods=20, freq='D'),
            'status': ['completed'] * 15 + ['pending'] * 3 + ['cancelled'] * 2
        })
        
        # Tabela de clientes
        customers_data = pd.DataFrame({
            'customer_id': range(1, 11),
            'name': [
                'João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Lima',
                'Carlos Souza', 'Juliana Oliveira', 'Roberto Alves', 
                'Fernanda Rocha', 'Lucas Martins', 'Patricia Fernandes'
            ],
            'age': [25, 32, 28, 45, 38, 29, 150, 31, 26, -5],  # Erros: idade 150 e -5
            'city': [
                'São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba',
                'Porto Alegre', None, 'Salvador', 'Recife',  # Erro: cidade nula
                'Fortaleza', 'Brasília'
            ],
            'premium_customer': [True, True, False, True, False, True, False, True, False, True]
        })
        
        # Tabela de produtos
        products_data = pd.DataFrame({
            'product_id': range(1, 16),
            'category': [
                'Eletrônicos', 'Eletrônicos', 'Eletrônicos', 'Eletrônicos', 'Eletrônicos',
                'Acessórios', 'Hardware', 'Hardware', 'Hardware', 'Hardware',
                'Periféricos', 'Periféricos', 'Periféricos', 'Cabos', 'Rede'
            ],
            'stock': [100, 250, 150, 45, 80, 200, 75, 90, 30, 15, 180, 220, 500, 800, 120],
            'min_stock': [20, 50, 30, 10, 15, 40, 15, 20, 10, 5, 30, 40, 100, 150, 25],
            'supplier': [
                'Fornecedor A', 'Fornecedor B', 'Fornecedor A', 'Fornecedor C',
                'Fornecedor B', 'Fornecedor A', 'Fornecedor D', 'Fornecedor D',
                'Fornecedor C', 'Fornecedor E', 'Fornecedor A', 'Fornecedor B',
                'Fornecedor C', 'Fornecedor A', 'Fornecedor B'
            ]
        })
        
        # Tabela de transações (para testar volumes maiores)
        transactions_data = pd.DataFrame({
            'transaction_id': range(1, 1001),
            'amount': np.random.uniform(10, 5000, 1000),
            'transaction_date': pd.date_range('2025-01-01', periods=1000, freq='h'),
            'status': np.random.choice(['approved', 'pending', 'rejected'], 1000, p=[0.8, 0.15, 0.05])
        })
        
        return {
            'sales': sales_data,
            'customers': customers_data,
            'products': products_data,
            'transactions': transactions_data
        }
    
    def _simulate_network_delay(self):
        """Simula latência de rede"""
        if self.simulate_delay:
            time.sleep(self.delay_seconds)
    
    def connect(self) -> bool:
        """Simula conexão com banco de dados"""
        self._simulate_network_delay()
        
        if self.fail_connection:
            logger.error("❌ Simulação de falha de conexão ativada")
            return False
        
        self.is_connected = True
        logger.info("✅ Mock Connector: Conexão simulada estabelecida com sucesso")
        logger.info(f"📊 Tabelas disponíveis: {list(self.mock_tables.keys())}")
        return True
    
    def disconnect(self) -> bool:
        """Simula desconexão"""
        self._simulate_network_delay()
        
        if not self.is_connected:
            logger.warning("⚠️ Tentativa de desconectar quando já está desconectado")
            return False
        
        self.is_connected = False
        logger.info("✅ Mock Connector: Conexão simulada fechada")
        return True
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Simula execução de query SQL
        Suporta queries básicas como SELECT, WHERE, LIMIT
        """
        if not self.is_connected:
            raise ConnectionError("Mock Connector não está conectado. Execute connect() primeiro.")
        
        self._simulate_network_delay()
        
        # Parse simples de query (básico para demonstração)
        query_lower = query.lower().strip()
        
        # Identifica a tabela na query
        table_name = None
        for table in self.mock_tables.keys():
            if f'from {table}' in query_lower or f'from `{table}`' in query_lower:
                table_name = table
                break
        
        if not table_name:
            raise ValueError(f"Tabela não encontrada na query. Tabelas disponíveis: {list(self.mock_tables.keys())}")
        
        df = self.mock_tables[table_name].copy()
        
        # Aplica LIMIT se presente
        if 'limit' in query_lower:
            try:
                limit_value = int(query_lower.split('limit')[-1].strip())
                df = df.head(limit_value)
            except:
                pass
        
        logger.info(f"✅ Query executada: retornando {len(df)} linhas da tabela '{table_name}'")
        return df
    
    def get_table_data(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """Retorna dados de uma tabela mockada"""
        if not self.is_connected:
            raise ConnectionError("Mock Connector não está conectado. Execute connect() primeiro.")
        
        self._simulate_network_delay()
        
        if table_name not in self.mock_tables:
            available = ', '.join(self.mock_tables.keys())
            raise ValueError(f"Tabela '{table_name}' não existe. Disponíveis: {available}")
        
        df = self.mock_tables[table_name].copy()
        
        if limit:
            df = df.head(limit)
        
        logger.info(f"✅ Dados recuperados da tabela '{table_name}': {len(df)} linhas")
        return df
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """Retorna metadados simulados da tabela"""
        if not self.is_connected:
            raise ConnectionError("Mock Connector não está conectado. Execute connect() primeiro.")
        
        if table_name not in self.mock_tables:
            raise ValueError(f"Tabela '{table_name}' não existe")
        
        self._simulate_network_delay()
        
        df = self.mock_tables[table_name]
        
        columns_info = []
        for col in df.columns:
            columns_info.append({
                'column_name': col,
                'data_type': str(df[col].dtype),
                'is_nullable': df[col].isnull().any(),
                'null_count': int(df[col].isnull().sum()),
                'unique_count': int(df[col].nunique())
            })
        
        metadata = {
            'table_name': table_name,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': columns_info,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
        }
        
        logger.info(f"✅ Metadados recuperados para '{table_name}'")
        return metadata
    
    def add_mock_table(self, table_name: str, data: pd.DataFrame):
        """Adiciona uma nova tabela mockada dinamicamente"""
        self.mock_tables[table_name] = data.copy()
        logger.info(f"✅ Tabela '{table_name}' adicionada ao mock ({len(data)} linhas)")
    
    def list_tables(self) -> List[str]:
        """Lista todas as tabelas disponíveis"""
        if not self.is_connected:
            raise ConnectionError("Mock Connector não está conectado")
        
        return list(self.mock_tables.keys())
    
    def clear_table(self, table_name: str):
        """Limpa os dados de uma tabela mockada"""
        if table_name in self.mock_tables:
            self.mock_tables[table_name] = pd.DataFrame()
            logger.info(f"✅ Tabela '{table_name}' limpa")
    
    def reset_to_defaults(self):
        """Reseta todas as tabelas para os dados padrão"""
        self.mock_tables = self._default_mock_data()
        logger.info("✅ Todas as tabelas resetadas para dados padrão")
