"""
DataSentinel - Main Entry Point
Ponto de entrada principal da aplicação
"""
import pandas as pd
import numpy as np
from app.core.engine import DataValidator
from app.core.config import config
from app.utils.reporter import ReportGenerator
from app.tests_definitions.sales_checks import validate_sales_data
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_sample_data() -> pd.DataFrame:
    """
    Cria dados de exemplo para demonstração
    Simula uma tabela de vendas com alguns erros propositais
    """
    np.random.seed(42)
    
    data = {
        'product_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'product_name': [
            'Shampoo', 'Condicionador', 'Sabonete', 'Creme Dental',
            'Desodorante', 'Hidratante', 'Protetor Solar', 'Perfume',
            'Shampoo Anticaspa', 'Máscara Capilar'
        ],
        'price': [
            100.50,      # Normal
            -5.00,       # ❌ ERRO: Preço negativo
            200.00,      # Normal
            np.nan,      # ❌ ERRO: Nulo
            150.75,      # Normal
            89.90,       # Normal
            250.00,      # Normal
            500.00,      # Normal (pode ser outlier)
            120.00,      # Normal
            180.50       # Normal
        ],
        'email_contato': [
            'vendas@jj.com',
            'erro.com',              # ❌ ERRO: Email inválido
            None,                     # ❌ ERRO: Nulo
            'suporte@jj.com',
            'comercial@jj.com',
            'atendimento@jj.com',
            'produtos@jj.com',
            'marketing@jj.com',
            'ti@jj.com',
            'financeiro@jj.com'
        ],
        'quantidade_estoque': [100, 50, 200, 75, 120, 90, 150, 30, 80, 110],
        'categoria': [
            'Cabelo', 'Cabelo', 'Corpo', 'Higiene',
            'Corpo', 'Corpo', 'Corpo', 'Perfumaria',
            'Cabelo', 'Cabelo'
        ]
    }
    
    return pd.DataFrame(data)


def run_validation_demo():
    """
    Executa demonstração completa do DataSentinel
    """
    print("\n" + "="*70)
    print("🛡️  DATASENTINEL - Data Quality Ops & Data Observability")
    print("="*70)
    
    # 1. Criar/Carregar dados
    print("\n📊 Carregando dados de exemplo...")
    df_vendas = create_sample_data()
    print(f"✅ {len(df_vendas)} registros carregados")
    print("\nPrimeiras linhas:")
    print(df_vendas.head())
    
    # 2. Executar validações
    print("\n" + "="*70)
    print("🔍 INICIANDO VALIDAÇÕES DE QUALIDADE")
    print("="*70)
    
    validator = validate_sales_data(df_vendas)
    
    # 3. Obter resultados
    print("\n" + "="*70)
    print("📋 RESULTADOS DAS VALIDAÇÕES")
    print("="*70)
    
    report_df = validator.get_report()
    print("\n" + report_df[['check_name', 'status', 'details']].to_string(index=False))
    
    # 4. Gerar resumo
    print("\n" + "="*70)
    print("📊 RESUMO EXECUTIVO")
    print("="*70)
    
    summary = validator.get_summary()
    print(f"\n{'Tabela:':<25} {summary['table_name']}")
    print(f"{'Execução:':<25} {summary['execution_time']}")
    print(f"{'Total de Verificações:':<25} {summary['total_checks']}")
    print(f"{'✅ Aprovadas:':<25} {summary['passed']}")
    print(f"{'❌ Reprovadas:':<25} {summary['failed']}")
    print(f"{'Taxa de Sucesso:':<25} {summary['success_rate']:.2f}%")
    print(f"{'Status Geral:':<25} {summary['overall_status']}")
    
    # 5. Gerar relatórios
    print("\n" + "="*70)
    print("📄 GERANDO RELATÓRIOS")
    print("="*70)
    
    reporter = ReportGenerator(output_dir=config.report_output_dir)
    
    # Gerar em múltiplos formatos
    output_files = reporter.generate_report(
        summary=summary,
        results_df=report_df,
        formats=['json', 'html', 'csv']
    )
    
    print(f"\n✅ Relatórios gerados:")
    for fmt, path in output_files.items():
        print(f"   - {fmt.upper()}: {path}")
    
    # 6. Enviar notificação Slack (se configurado)
    if config.enable_slack_alerts and config.slack_webhook_url:
        print("\n📢 Enviando notificação para o Slack...")
        reporter.send_slack_notification(
            webhook_url=config.slack_webhook_url,
            summary=summary
        )
    
    print("\n" + "="*70)
    print("✅ PROCESSO CONCLUÍDO COM SUCESSO")
    print("="*70 + "\n")


def run_with_custom_data(file_path: str, file_type: str = 'csv'):
    """
    Executa validações em dados customizados
    
    Args:
        file_path: Caminho para o arquivo de dados
        file_type: Tipo do arquivo ('csv', 'excel', etc)
    """
    logger.info(f"Carregando dados de: {file_path}")
    
    # Carregar dados
    if file_type == 'csv':
        df = pd.read_csv(file_path)
    elif file_type == 'excel':
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Tipo de arquivo não suportado: {file_type}")
    
    logger.info(f"✅ {len(df)} registros carregados")
    
    # Criar validador
    validator = DataValidator(df, table_name=file_path)
    
    # Executar validações básicas automáticas
    print("\n🔍 Executando validações automáticas...")
    
    for column in df.columns:
        # Verificar nulidade
        validator.expect_column_values_to_not_be_null(column, threshold=10.0)
        
        # Para colunas numéricas, fazer validações adicionais
        if pd.api.types.is_numeric_dtype(df[column]):
            validator.detect_outliers_zscore(column, threshold=3.0)
    
    # Gerar relatório
    summary = validator.get_summary()
    report_df = validator.get_report()
    
    reporter = ReportGenerator(output_dir=config.report_output_dir)
    output_files = reporter.generate_report(
        summary=summary,
        results_df=report_df,
        formats=['json', 'html']
    )
    
    print(f"\n✅ Relatórios gerados: {output_files}")


if __name__ == "__main__":
    # Executar demonstração
    run_validation_demo()
    
    # Para usar com seus próprios dados, descomente:
    # run_with_custom_data('caminho/para/seu/arquivo.csv', file_type='csv')
