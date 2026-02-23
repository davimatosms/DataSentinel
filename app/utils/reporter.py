"""
Reporter Module
Gera relatórios em diferentes formatos (JSON, HTML, Slack)
"""
import json
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Gerador de relatórios de qualidade de dados"""
    
    def __init__(self, output_dir: str = "./reports"):
        """
        Args:
            output_dir: Diretório onde os relatórios serão salvos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_json_report(
        self, 
        summary: Dict[str, Any], 
        results_df: pd.DataFrame,
        filename: str = None
    ) -> str:
        """
        Gera relatório em formato JSON
        
        Returns:
            Caminho do arquivo gerado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_quality_report_{timestamp}.json"
        
        report_data = {
            'summary': summary,
            'checks': results_df.to_dict('records') if not results_df.empty else []
        }
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 Relatório JSON salvo em: {output_path}")
        return str(output_path)
    
    def generate_html_report(
        self, 
        summary: Dict[str, Any], 
        results_df: pd.DataFrame,
        filename: str = None
    ) -> str:
        """
        Gera relatório em formato HTML com estilo
        
        Returns:
            Caminho do arquivo gerado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_quality_report_{timestamp}.html"
        
        # Template HTML
        html_template = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DataSentinel - Relatório de Qualidade</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                }}
                .summary {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .metric-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .metric-card.success {{
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                }}
                .metric-card.danger {{
                    background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
                }}
                .metric-card h3 {{
                    margin: 0 0 10px 0;
                    font-size: 14px;
                    opacity: 0.9;
                }}
                .metric-card .value {{
                    font-size: 32px;
                    font-weight: bold;
                    margin: 0;
                }}
                .status-badge {{
                    display: inline-block;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 14px;
                }}
                .status-pass {{
                    background-color: #d4edda;
                    color: #155724;
                }}
                .status-fail {{
                    background-color: #f8d7da;
                    color: #721c24;
                }}
                .status-error {{
                    background-color: #fff3cd;
                    color: #856404;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                }}
                td {{
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛡️ DataSentinel - Relatório de Qualidade de Dados</h1>
                
                <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <strong>Tabela:</strong> {summary.get('table_name', 'N/A')}<br>
                    <strong>Execução:</strong> {summary.get('execution_time', 'N/A')}<br>
                    <strong>Status Geral:</strong> <span class="status-badge {'status-pass' if summary.get('failed', 1) == 0 else 'status-fail'}">
                        {summary.get('overall_status', 'UNKNOWN')}
                    </span>
                </div>
                
                <h2>📊 Resumo Executivo</h2>
                <div class="summary">
                    <div class="metric-card">
                        <h3>Total de Verificações</h3>
                        <p class="value">{summary.get('total_checks', 0)}</p>
                    </div>
                    <div class="metric-card success">
                        <h3>✅ Aprovadas</h3>
                        <p class="value">{summary.get('passed', 0)}</p>
                    </div>
                    <div class="metric-card danger">
                        <h3>❌ Reprovadas</h3>
                        <p class="value">{summary.get('failed', 0)}</p>
                    </div>
                    <div class="metric-card">
                        <h3>Taxa de Sucesso</h3>
                        <p class="value">{summary.get('success_rate', 0):.1f}%</p>
                    </div>
                </div>
                
                <h2>🔍 Detalhes das Verificações</h2>
                {self._generate_html_table(results_df)}
                
                <div class="footer">
                    <p>Gerado por DataSentinel em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                    <p>Data Quality Ops & Data Observability Tool</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        logger.info(f"📄 Relatório HTML salvo em: {output_path}")
        return str(output_path)
    
    def _generate_html_table(self, df: pd.DataFrame) -> str:
        """Gera tabela HTML a partir do DataFrame"""
        if df.empty:
            return "<p>Nenhuma verificação executada.</p>"
        
        # Seleciona colunas relevantes
        display_columns = ['check_name', 'status', 'details', 'severity']
        available_columns = [col for col in display_columns if col in df.columns]
        
        html = "<table>\n<thead>\n<tr>\n"
        
        # Cabeçalhos
        for col in available_columns:
            html += f"<th>{col.replace('_', ' ').title()}</th>\n"
        html += "</tr>\n</thead>\n<tbody>\n"
        
        # Linhas
        for _, row in df.iterrows():
            html += "<tr>\n"
            for col in available_columns:
                value = row.get(col, '')
                html += f"<td>{value}</td>\n"
            html += "</tr>\n"
        
        html += "</tbody>\n</table>"
        return html
    
    def generate_csv_report(
        self, 
        results_df: pd.DataFrame,
        filename: str = None
    ) -> str:
        """
        Gera relatório em formato CSV
        
        Returns:
            Caminho do arquivo gerado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_quality_report_{timestamp}.csv"
        
        output_path = self.output_dir / filename
        
        results_df.to_csv(output_path, index=False, encoding='utf-8')
        
        logger.info(f"📄 Relatório CSV salvo em: {output_path}")
        return str(output_path)
    
    def send_slack_notification(
        self, 
        webhook_url: str,
        summary: Dict[str, Any]
    ) -> bool:
        """
        Envia notificação para o Slack
        
        Args:
            webhook_url: URL do webhook do Slack
            summary: Resumo da validação
            
        Returns:
            True se enviado com sucesso
        """
        try:
            import requests
            
            # Determina cor baseado no status
            color = "#36a64f" if summary.get('failed', 1) == 0 else "#ff0000"
            
            # Monta mensagem
            message = {
                "attachments": [
                    {
                        "color": color,
                        "title": f"🛡️ DataSentinel - {summary.get('table_name', 'Unknown')}",
                        "text": summary.get('overall_status', 'UNKNOWN'),
                        "fields": [
                            {
                                "title": "Total de Verificações",
                                "value": str(summary.get('total_checks', 0)),
                                "short": True
                            },
                            {
                                "title": "Taxa de Sucesso",
                                "value": f"{summary.get('success_rate', 0):.1f}%",
                                "short": True
                            },
                            {
                                "title": "✅ Aprovadas",
                                "value": str(summary.get('passed', 0)),
                                "short": True
                            },
                            {
                                "title": "❌ Reprovadas",
                                "value": str(summary.get('failed', 0)),
                                "short": True
                            }
                        ],
                        "footer": "DataSentinel",
                        "ts": int(datetime.now().timestamp())
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=message)
            
            if response.status_code == 200:
                logger.info("✅ Notificação enviada para o Slack com sucesso")
                return True
            else:
                logger.error(f"❌ Erro ao enviar notificação: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao enviar notificação Slack: {e}")
            return False
    
    def generate_report(
        self,
        summary: Dict[str, Any],
        results_df: pd.DataFrame,
        formats: List[str] = ['json']
    ) -> Dict[str, str]:
        """
        Gera relatórios em múltiplos formatos
        
        Args:
            summary: Resumo executivo
            results_df: DataFrame com resultados
            formats: Lista de formatos ('json', 'html', 'csv')
            
        Returns:
            Dicionário com caminhos dos arquivos gerados
        """
        output_files = {}
        
        for fmt in formats:
            if fmt == 'json':
                output_files['json'] = self.generate_json_report(summary, results_df)
            elif fmt == 'html':
                output_files['html'] = self.generate_html_report(summary, results_df)
            elif fmt == 'csv':
                output_files['csv'] = self.generate_csv_report(results_df)
            else:
                logger.warning(f"Formato '{fmt}' não reconhecido")
        
        return output_files
