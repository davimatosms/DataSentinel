"""
Pydantic schemas for API requests and responses
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ConnectorType(str, Enum):
    """Types of data connectors"""
    MOCK = "mock"
    CSV = "csv"
    POSTGRESQL = "postgresql"


class ConnectionRequest(BaseModel):
    """Request to connect to a data source"""
    connector_type: ConnectorType
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "connector_type": "mock",
                "config": {
                    "network_delay": 0.1,
                    "failure_rate": 0.0
                }
            }
        }


class ConnectionResponse(BaseModel):
    """Response from connection attempt"""
    success: bool
    message: str
    tables: Optional[List[str]] = None


class TableDataRequest(BaseModel):
    """Request to get table data"""
    table_name: str
    limit: Optional[int] = 100


class TableDataResponse(BaseModel):
    """Response with table data"""
    table_name: str
    columns: List[str]
    data: List[Dict[str, Any]]
    row_count: int


class ValidationType(str, Enum):
    """Types of validations"""
    NOT_NULL = "not_null"
    RANGE = "range"
    UNIQUE = "unique"
    OUTLIERS = "outliers"
    PATTERN = "pattern"


class ValidationRule(BaseModel):
    """A single validation rule"""
    type: ValidationType
    column: str
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "not_null",
                "column": "customer_id",
                "params": {"threshold": 0}
            }
        }


class ValidationRequest(BaseModel):
    """Request to execute validations"""
    table_name: str
    rules: List[ValidationRule]


class ValidationResult(BaseModel):
    """Result of a single validation"""
    rule_type: str
    column: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None


class ValidationResponse(BaseModel):
    """Response with validation results"""
    table_name: str
    total_rules: int
    passed: int
    failed: int
    success_rate: float
    results: List[ValidationResult]


class ExportFormat(str, Enum):
    """Export formats"""
    JSON = "json"
    CSV = "csv"


class ExportRequest(BaseModel):
    """Request to export results"""
    format: ExportFormat
    results: ValidationResponse
