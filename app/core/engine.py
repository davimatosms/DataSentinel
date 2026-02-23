"""
Data Validation Engine
Motor principal de validação de qualidade de dados
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationResult:
    """Classe para armazenar resultado de uma validação"""
    
    def __init__(
        self, 
        check_name: str, 
        status: str, 
        passed: bool,
        details: str,
        severity: str = "ERROR",
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.check_name = check_name
        self.status = status
        self.passed = passed
        self.details = details
        self.severity = severity
        self.timestamp = datetime.now()
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte resultado para dicionário"""
        return {
            'check_name': self.check_name,
            'status': self.status,
            'passed': self.passed,
            'details': self.details,
            'severity': self.severity,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


class DataValidator:
    """
    Motor de validação de dados com expectativas configuráveis.
    Inspirado no Great Expectations.
    """
    
    def __init__(self, df: pd.DataFrame, table_name: str = "unknown"):
        """
        Inicializa o validador com um DataFrame
        
        Args:
            df: DataFrame a ser validado
            table_name: Nome da tabela (para relatórios)
        """
        self.df = df
        self.table_name = table_name
        self.results: List[ValidationResult] = []
        self.execution_time = datetime.now()
    
    # ========== EXPECTATIVAS DE NULIDADE ==========
    
    def expect_column_values_to_not_be_null(
        self, 
        column: str,
        threshold: float = 0.0
    ) -> ValidationResult:
        """
        Valida que uma coluna não contenha valores nulos
        
        Args:
            column: Nome da coluna
            threshold: Percentual aceitável de nulos (0.0 = nenhum nulo aceito)
        """
        try:
            null_count = self.df[column].isnull().sum()
            total_count = len(self.df)
            null_percentage = (null_count / total_count) * 100 if total_count > 0 else 0
            
            passed = null_percentage <= threshold
            status = "✅ PASS" if passed else "❌ FAIL"
            
            result = ValidationResult(
                check_name=f"Not Null: {column}",
                status=status,
                passed=passed,
                details=f"Encontrados {null_count} nulos ({null_percentage:.2f}%) de {total_count} registros",
                severity="ERROR" if not passed else "INFO",
                metadata={
                    'column': column,
                    'null_count': int(null_count),
                    'total_count': int(total_count),
                    'null_percentage': float(null_percentage),
                    'threshold': threshold
                }
            )
            
            self.results.append(result)
            logger.info(f"{status} - {result.check_name}: {result.details}")
            return result
            
        except KeyError:
            result = ValidationResult(
                check_name=f"Not Null: {column}",
                status="⚠️ ERROR",
                passed=False,
                details=f"Coluna '{column}' não encontrada no DataFrame",
                severity="CRITICAL"
            )
            self.results.append(result)
            return result
    
    # ========== EXPECTATIVAS DE INTERVALO ==========
    
    def expect_column_values_to_be_between(
        self, 
        column: str, 
        min_val: float, 
        max_val: float,
        allow_null: bool = False
    ) -> ValidationResult:
        """
        Valida que valores de uma coluna estejam dentro de um intervalo
        
        Args:
            column: Nome da coluna
            min_val: Valor mínimo permitido
            max_val: Valor máximo permitido
            allow_null: Se True, ignora valores nulos
        """
        try:
            if allow_null:
                working_df = self.df[self.df[column].notna()]
            else:
                working_df = self.df
            
            out_of_range = working_df[
                (working_df[column] < min_val) | 
                (working_df[column] > max_val)
            ]
            
            total_count = len(working_df)
            invalid_count = len(out_of_range)
            invalid_percentage = (invalid_count / total_count) * 100 if total_count > 0 else 0
            
            passed = invalid_count == 0
            status = "✅ PASS" if passed else "❌ FAIL"
            
            result = ValidationResult(
                check_name=f"Range Check: {column}",
                status=status,
                passed=passed,
                details=f"{invalid_count} valores fora do intervalo [{min_val}, {max_val}] ({invalid_percentage:.2f}%)",
                severity="ERROR" if not passed else "INFO",
                metadata={
                    'column': column,
                    'min_val': min_val,
                    'max_val': max_val,
                    'invalid_count': int(invalid_count),
                    'total_count': int(total_count),
                    'invalid_percentage': float(invalid_percentage)
                }
            )
            
            self.results.append(result)
            logger.info(f"{status} - {result.check_name}: {result.details}")
            return result
            
        except Exception as e:
            result = ValidationResult(
                check_name=f"Range Check: {column}",
                status="⚠️ ERROR",
                passed=False,
                details=f"Erro ao executar validação: {str(e)}",
                severity="CRITICAL"
            )
            self.results.append(result)
            return result
    
    # ========== EXPECTATIVAS DE UNICIDADE ==========
    
    def expect_column_values_to_be_unique(self, column: str) -> ValidationResult:
        """Valida que valores de uma coluna sejam únicos"""
        try:
            duplicate_count = self.df[column].duplicated().sum()
            total_count = len(self.df)
            duplicate_percentage = (duplicate_count / total_count) * 100 if total_count > 0 else 0
            
            passed = duplicate_count == 0
            status = "✅ PASS" if passed else "❌ FAIL"
            
            result = ValidationResult(
                check_name=f"Uniqueness: {column}",
                status=status,
                passed=passed,
                details=f"{duplicate_count} valores duplicados ({duplicate_percentage:.2f}%)",
                severity="WARNING" if not passed else "INFO",
                metadata={
                    'column': column,
                    'duplicate_count': int(duplicate_count),
                    'total_count': int(total_count)
                }
            )
            
            self.results.append(result)
            logger.info(f"{status} - {result.check_name}: {result.details}")
            return result
            
        except Exception as e:
            result = ValidationResult(
                check_name=f"Uniqueness: {column}",
                status="⚠️ ERROR",
                passed=False,
                details=f"Erro: {str(e)}",
                severity="CRITICAL"
            )
            self.results.append(result)
            return result
    
    # ========== EXPECTATIVAS DE FORMATO ==========
    
    def expect_column_values_to_match_regex(
        self, 
        column: str, 
        regex_pattern: str,
        description: str = ""
    ) -> ValidationResult:
        """
        Valida que valores correspondam a um padrão regex
        
        Args:
            column: Nome da coluna
            regex_pattern: Padrão regex para validação
            description: Descrição do padrão (ex: "Email válido")
        """
        try:
            matches = self.df[column].astype(str).str.match(regex_pattern, na=False)
            invalid_count = (~matches).sum()
            total_count = len(self.df)
            invalid_percentage = (invalid_count / total_count) * 100 if total_count > 0 else 0
            
            passed = invalid_count == 0
            status = "✅ PASS" if passed else "❌ FAIL"
            
            check_desc = description if description else f"Regex: {regex_pattern}"
            
            result = ValidationResult(
                check_name=f"Format Check: {column} ({check_desc})",
                status=status,
                passed=passed,
                details=f"{invalid_count} valores inválidos ({invalid_percentage:.2f}%)",
                severity="ERROR" if not passed else "INFO",
                metadata={
                    'column': column,
                    'regex_pattern': regex_pattern,
                    'invalid_count': int(invalid_count),
                    'total_count': int(total_count)
                }
            )
            
            self.results.append(result)
            logger.info(f"{status} - {result.check_name}: {result.details}")
            return result
            
        except Exception as e:
            result = ValidationResult(
                check_name=f"Format Check: {column}",
                status="⚠️ ERROR",
                passed=False,
                details=f"Erro: {str(e)}",
                severity="CRITICAL"
            )
            self.results.append(result)
            return result
    
    # ========== EXPECTATIVAS ESTATÍSTICAS ==========
    
    def expect_column_mean_to_be_between(
        self, 
        column: str, 
        min_val: float, 
        max_val: float
    ) -> ValidationResult:
        """Valida que a média de uma coluna esteja dentro de um intervalo"""
        try:
            mean_value = self.df[column].mean()
            passed = min_val <= mean_value <= max_val
            status = "✅ PASS" if passed else "❌ FAIL"
            
            result = ValidationResult(
                check_name=f"Mean Check: {column}",
                status=status,
                passed=passed,
                details=f"Média = {mean_value:.2f} (esperado: [{min_val}, {max_val}])",
                severity="WARNING" if not passed else "INFO",
                metadata={
                    'column': column,
                    'mean_value': float(mean_value),
                    'min_expected': min_val,
                    'max_expected': max_val
                }
            )
            
            self.results.append(result)
            logger.info(f"{status} - {result.check_name}: {result.details}")
            return result
            
        except Exception as e:
            result = ValidationResult(
                check_name=f"Mean Check: {column}",
                status="⚠️ ERROR",
                passed=False,
                details=f"Erro: {str(e)}",
                severity="CRITICAL"
            )
            self.results.append(result)
            return result
    
    def expect_column_stdev_to_be_between(
        self, 
        column: str, 
        min_val: float, 
        max_val: float
    ) -> ValidationResult:
        """Valida que o desvio padrão esteja dentro de um intervalo"""
        try:
            std_value = self.df[column].std()
            passed = min_val <= std_value <= max_val
            status = "✅ PASS" if passed else "❌ FAIL"
            
            result = ValidationResult(
                check_name=f"StdDev Check: {column}",
                status=status,
                passed=passed,
                details=f"Desvio Padrão = {std_value:.2f} (esperado: [{min_val}, {max_val}])",
                severity="WARNING" if not passed else "INFO",
                metadata={
                    'column': column,
                    'std_value': float(std_value),
                    'min_expected': min_val,
                    'max_expected': max_val
                }
            )
            
            self.results.append(result)
            logger.info(f"{status} - {result.check_name}: {result.details}")
            return result
            
        except Exception as e:
            result = ValidationResult(
                check_name=f"StdDev Check: {column}",
                status="⚠️ ERROR",
                passed=False,
                details=f"Erro: {str(e)}",
                severity="CRITICAL"
            )
            self.results.append(result)
            return result
    
    # ========== DETECÇÃO DE ANOMALIAS (Z-SCORE) ==========
    
    def detect_outliers_zscore(
        self, 
        column: str, 
        threshold: float = 3.0
    ) -> ValidationResult:
        """
        Detecta outliers usando Z-Score
        
        Args:
            column: Nome da coluna numérica
            threshold: Limite de Z-Score (padrão: 3.0 = 99.7% dos dados)
        """
        try:
            mean = self.df[column].mean()
            std = self.df[column].std()
            
            z_scores = np.abs((self.df[column] - mean) / std)
            outliers = z_scores > threshold
            outlier_count = outliers.sum()
            
            total_count = len(self.df)
            outlier_percentage = (outlier_count / total_count) * 100 if total_count > 0 else 0
            
            passed = outlier_count == 0
            status = "✅ PASS" if passed else "⚠️ WARNING"
            
            result = ValidationResult(
                check_name=f"Outlier Detection (Z-Score): {column}",
                status=status,
                passed=passed,
                details=f"Detectados {outlier_count} outliers ({outlier_percentage:.2f}%) com threshold={threshold}",
                severity="WARNING" if not passed else "INFO",
                metadata={
                    'column': column,
                    'outlier_count': int(outlier_count),
                    'total_count': int(total_count),
                    'threshold': threshold,
                    'mean': float(mean),
                    'std': float(std)
                }
            )
            
            self.results.append(result)
            logger.info(f"{status} - {result.check_name}: {result.details}")
            return result
            
        except Exception as e:
            result = ValidationResult(
                check_name=f"Outlier Detection: {column}",
                status="⚠️ ERROR",
                passed=False,
                details=f"Erro: {str(e)}",
                severity="CRITICAL"
            )
            self.results.append(result)
            return result
    
    # ========== RELATÓRIOS ==========
    
    def get_report(self) -> pd.DataFrame:
        """Retorna relatório de validações em formato DataFrame"""
        if not self.results:
            return pd.DataFrame()
        
        return pd.DataFrame([r.to_dict() for r in self.results])
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo executivo das validações"""
        total_checks = len(self.results)
        passed_checks = sum(1 for r in self.results if r.passed)
        failed_checks = total_checks - passed_checks
        
        success_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        severity_counts = {}
        for r in self.results:
            severity_counts[r.severity] = severity_counts.get(r.severity, 0) + 1
        
        return {
            'table_name': self.table_name,
            'execution_time': self.execution_time.isoformat(),
            'total_checks': total_checks,
            'passed': passed_checks,
            'failed': failed_checks,
            'success_rate': round(success_rate, 2),
            'severity_breakdown': severity_counts,
            'overall_status': '✅ HEALTHY' if failed_checks == 0 else '❌ ISSUES DETECTED'
        }
    
    def clear_results(self):
        """Limpa resultados acumulados"""
        self.results = []
