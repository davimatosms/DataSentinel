"""
Database Connectors
Implementações concretas para diferentes bancos de dados
"""
import pandas as pd
import logging
from typing import Optional, Dict, Any
from .base import BaseConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostgreSQLConnector(BaseConnector):
    """Conector para PostgreSQL usando SQLAlchemy"""
    
    def __init__(self, connection_config: Dict[str, Any]):
        """
        Args:
            connection_config: Deve conter 'host', 'port', 'database', 'user', 'password'
        """
        super().__init__(connection_config)
        self.engine = None
    
    def connect(self) -> bool:
        """Conecta ao PostgreSQL"""
        try:
            from sqlalchemy import create_engine
            
            conn_string = (
                f"postgresql://{self.connection_config['user']}:"
                f"{self.connection_config['password']}@"
                f"{self.connection_config['host']}:"
                f"{self.connection_config['port']}/"
                f"{self.connection_config['database']}"
            )
            
            self.engine = create_engine(conn_string)
            self.connection = self.engine.connect()
            logger.info("✅ Conectado ao PostgreSQL com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao PostgreSQL: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Desconecta do PostgreSQL"""
        try:
            if self.connection:
                self.connection.close()
            if self.engine:
                self.engine.dispose()
            logger.info("Conexão PostgreSQL fechada")
            return True
        except Exception as e:
            logger.error(f"Erro ao desconectar: {e}")
            return False
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Executa query SQL"""
        try:
            df = pd.read_sql(query, self.connection)
            logger.info(f"Query executada com sucesso. Retornadas {len(df)} linhas")
            return df
        except Exception as e:
            logger.error(f"Erro ao executar query: {e}")
            raise
    
    def get_table_data(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """Recupera dados de uma tabela"""
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        return self.execute_query(query)
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """Retorna metadados da tabela"""
        query = f"""
        SELECT 
            column_name, 
            data_type, 
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        """
        
        metadata_df = self.execute_query(query)
        
        return {
            'table_name': table_name,
            'columns': metadata_df.to_dict('records'),
            'total_columns': len(metadata_df)
        }


class CSVConnector(BaseConnector):
    """Conector para arquivos CSV"""
    
    def __init__(self, connection_config: Dict[str, Any]):
        """
        Args:
            connection_config: Deve conter 'file_path'
        """
        super().__init__(connection_config)
        self.file_path = connection_config['file_path']
        self.data = None
    
    def connect(self) -> bool:
        """Carrega o arquivo CSV"""
        try:
            self.data = pd.read_csv(self.file_path)
            logger.info(f"✅ CSV carregado: {len(self.data)} linhas")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao carregar CSV: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Libera memória do DataFrame"""
        self.data = None
        return True
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Executa query usando Pandas (limitado)"""
        # Para CSVs, implementação simplificada
        # Em produção, pode-se usar pandasql
        logger.warning("execute_query em CSV tem funcionalidade limitada")
        return self.data
    
    def get_table_data(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """Retorna dados do CSV"""
        if limit:
            return self.data.head(limit)
        return self.data
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """Retorna metadados do CSV"""
        return {
            'file_path': self.file_path,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'total_columns': len(self.data.columns),
            'total_rows': len(self.data)
        }


class SQLServerConnector(BaseConnector):
    """Conector para SQL Server usando pyodbc"""
    
    def __init__(self, connection_config: Dict[str, Any]):
        """
        Args:
            connection_config: Deve conter 'server', 'database', 'user', 'password'
        """
        super().__init__(connection_config)
        self.engine = None
    
    def connect(self) -> bool:
        """Conecta ao SQL Server"""
        try:
            from sqlalchemy import create_engine
            import urllib.parse
            
            params = urllib.parse.quote_plus(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.connection_config['server']};"
                f"DATABASE={self.connection_config['database']};"
                f"UID={self.connection_config['user']};"
                f"PWD={self.connection_config['password']}"
            )
            
            self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
            self.connection = self.engine.connect()
            logger.info("✅ Conectado ao SQL Server com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao SQL Server: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Desconecta do SQL Server"""
        try:
            if self.connection:
                self.connection.close()
            if self.engine:
                self.engine.dispose()
            logger.info("Conexão SQL Server fechada")
            return True
        except Exception as e:
            logger.error(f"Erro ao desconectar: {e}")
            return False
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Executa query SQL"""
        try:
            df = pd.read_sql(query, self.connection)
            logger.info(f"Query executada. Retornadas {len(df)} linhas")
            return df
        except Exception as e:
            logger.error(f"Erro ao executar query: {e}")
            raise
    
    def get_table_data(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """Recupera dados de uma tabela"""
        query = f"SELECT * FROM {table_name}"
        if limit:
            query = f"SELECT TOP {limit} * FROM {table_name}"
        return self.execute_query(query)
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """Retorna metadados da tabela"""
        query = f"""
        SELECT 
            COLUMN_NAME as column_name,
            DATA_TYPE as data_type,
            IS_NULLABLE as is_nullable,
            COLUMN_DEFAULT as column_default
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        """
        
        metadata_df = self.execute_query(query)
        
        return {
            'table_name': table_name,
            'columns': metadata_df.to_dict('records'),
            'total_columns': len(metadata_df)
        }
