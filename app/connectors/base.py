"""
Base Connector Interface
Define a interface abstrata para todos os conectores de dados
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, Dict, Any


class BaseConnector(ABC):
    """
    Classe abstrata para conectores de fonte de dados.
    Todos os conectores devem implementar esta interface.
    """
    
    def __init__(self, connection_config: Dict[str, Any]):
        """
        Inicializa o conector com configurações de conexão
        
        Args:
            connection_config: Dicionário com parâmetros de conexão
        """
        self.connection_config = connection_config
        self.connection = None
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Estabelece conexão com a fonte de dados
        
        Returns:
            True se conectado com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        Fecha a conexão com a fonte de dados
        
        Returns:
            True se desconectado com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Executa uma query e retorna os resultados como DataFrame
        
        Args:
            query: String SQL ou consulta equivalente
            
        Returns:
            DataFrame com os resultados
        """
        pass
    
    @abstractmethod
    def get_table_data(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Recupera dados de uma tabela específica
        
        Args:
            table_name: Nome da tabela
            limit: Número máximo de linhas (opcional)
            
        Returns:
            DataFrame com os dados da tabela
        """
        pass
    
    @abstractmethod
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """
        Retorna metadados da tabela (colunas, tipos, etc)
        
        Args:
            table_name: Nome da tabela
            
        Returns:
            Dicionário com metadados da tabela
        """
        pass
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
