"""
Configuration Management
Gerenciamento de configurações e variáveis de ambiente
"""
import os
from typing import Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


@dataclass
class DatabaseConfig:
    """Configuração de conexão com banco de dados"""
    host: str
    port: int
    database: str
    user: str
    password: str
    
    @classmethod
    def from_env(cls, prefix: str = "DB"):
        """
        Cria configuração a partir de variáveis de ambiente
        
        Exemplo de variáveis:
        - DB_HOST=localhost
        - DB_PORT=5432
        - DB_DATABASE=mydb
        - DB_USER=user
        - DB_PASSWORD=pass
        """
        return cls(
            host=os.getenv(f"{prefix}_HOST", "localhost"),
            port=int(os.getenv(f"{prefix}_PORT", "5432")),
            database=os.getenv(f"{prefix}_DATABASE", ""),
            user=os.getenv(f"{prefix}_USER", ""),
            password=os.getenv(f"{prefix}_PASSWORD", "")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password
        }


@dataclass
class AppConfig:
    """Configurações gerais da aplicação"""
    
    # Configurações de execução
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Configurações de relatórios
    report_output_dir: str = os.getenv("REPORT_OUTPUT_DIR", "./reports")
    report_format: str = os.getenv("REPORT_FORMAT", "json")  # json, html, csv
    
    # Configurações de alertas
    enable_slack_alerts: bool = os.getenv("ENABLE_SLACK_ALERTS", "false").lower() == "true"
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")
    
    enable_email_alerts: bool = os.getenv("ENABLE_EMAIL_ALERTS", "false").lower() == "true"
    email_recipients: str = os.getenv("EMAIL_RECIPIENTS", "")
    
    # Configurações de thresholds
    max_null_percentage: float = float(os.getenv("MAX_NULL_PERCENTAGE", "5.0"))
    outlier_zscore_threshold: float = float(os.getenv("OUTLIER_ZSCORE_THRESHOLD", "3.0"))
    
    def __post_init__(self):
        """Cria diretório de relatórios se não existir"""
        os.makedirs(self.report_output_dir, exist_ok=True)


# Instância global de configuração
config = AppConfig()


def get_postgres_config() -> Dict[str, Any]:
    """Retorna configuração do PostgreSQL"""
    return DatabaseConfig.from_env("POSTGRES").to_dict()


def get_sqlserver_config() -> Dict[str, Any]:
    """Retorna configuração do SQL Server"""
    return {
        'server': os.getenv("SQLSERVER_HOST", "localhost"),
        'database': os.getenv("SQLSERVER_DATABASE", ""),
        'user': os.getenv("SQLSERVER_USER", ""),
        'password': os.getenv("SQLSERVER_PASSWORD", "")
    }


def get_csv_config(file_path: str) -> Dict[str, Any]:
    """Retorna configuração para CSV"""
    return {
        'file_path': file_path
    }
