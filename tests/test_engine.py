"""
Testes unitários para o DataValidator
"""
import pytest
import pandas as pd
import numpy as np
from app.core.engine import DataValidator


@pytest.fixture
def sample_dataframe():
    """Fixture com dados de teste"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', None, 'David', 'Eve'],
        'age': [25, 30, 35, -5, 40],
        'email': ['alice@test.com', 'bob@test.com', 'invalid', 'david@test.com', 'eve@test.com'],
        'salary': [50000, 60000, 70000, 80000, 1000000]  # Último é outlier
    })


def test_not_null_validation(sample_dataframe):
    """Testa validação de não nulos"""
    validator = DataValidator(sample_dataframe, "test_table")
    result = validator.expect_column_values_to_not_be_null('name', threshold=0.0)
    
    assert result.passed == False
    assert result.metadata['null_count'] == 1


def test_range_validation(sample_dataframe):
    """Testa validação de intervalo"""
    validator = DataValidator(sample_dataframe, "test_table")
    result = validator.expect_column_values_to_be_between('age', 0, 100)
    
    assert result.passed == False
    assert result.metadata['invalid_count'] == 1  # -5 está fora do intervalo


def test_uniqueness_validation():
    """Testa validação de unicidade"""
    df = pd.DataFrame({
        'id': [1, 2, 2, 3, 4]
    })
    
    validator = DataValidator(df, "test_table")
    result = validator.expect_column_values_to_be_unique('id')
    
    assert result.passed == False
    assert result.metadata['duplicate_count'] == 1


def test_outlier_detection(sample_dataframe):
    """Testa detecção de outliers"""
    validator = DataValidator(sample_dataframe, "test_table")
    result = validator.detect_outliers_zscore('salary', threshold=2.0)
    
    # O salário de 1.000.000 deve ser detectado como outlier
    assert result.metadata['outlier_count'] > 0


def test_summary_generation(sample_dataframe):
    """Testa geração de resumo"""
    validator = DataValidator(sample_dataframe, "test_table")
    validator.expect_column_values_to_not_be_null('name')
    validator.expect_column_values_to_be_between('age', 0, 100)
    
    summary = validator.get_summary()
    
    assert summary['total_checks'] == 2
    assert 'success_rate' in summary
    assert 'overall_status' in summary
