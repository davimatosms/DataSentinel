"""
Validation routes - Handle data quality validations
"""
from fastapi import APIRouter, HTTPException
from typing import List
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from app.core.engine import DataValidator
from backend.api.schemas import (
    ValidationRequest,
    ValidationResponse,
    ValidationResult,
    ValidationType
)

router = APIRouter()

# Import active connections from connectors
from backend.api.routes.connectors import active_connections


@router.post("/validate", response_model=ValidationResponse)
async def execute_validation(request: ValidationRequest):
    """
    Execute data quality validations
    """
    if "current" not in active_connections:
        raise HTTPException(status_code=400, detail="No active connection")
    
    try:
        # Get data
        connector = active_connections["current"]
        df = connector.get_table_data(request.table_name)
        
        # Create validator
        validator = DataValidator(df)
        
        # Execute each validation rule
        results: List[ValidationResult] = []
        
        for rule in request.rules:
            try:
                if rule.type == ValidationType.NOT_NULL:
                    threshold = rule.params.get("threshold", 0.0)
                    result = validator.expect_column_values_to_not_be_null(
                        rule.column,
                        threshold=threshold
                    )
                    
                    results.append(ValidationResult(
                        rule_type=rule.type.value,
                        column=rule.column,
                        passed=result["success"],
                        message=result["message"],
                        details={
                            "null_count": result.get("null_count"),
                            "null_percentage": result.get("null_percentage"),
                            "threshold": threshold
                        }
                    ))
                
                elif rule.type == ValidationType.RANGE:
                    min_val = rule.params.get("min_value")
                    max_val = rule.params.get("max_value")
                    
                    result = validator.expect_column_values_to_be_between(
                        rule.column,
                        min_value=min_val,
                        max_value=max_val
                    )
                    
                    results.append(ValidationResult(
                        rule_type=rule.type.value,
                        column=rule.column,
                        passed=result["success"],
                        message=result["message"],
                        details={
                            "min_value": min_val,
                            "max_value": max_val,
                            "out_of_range_count": result.get("out_of_range_count")
                        }
                    ))
                
                elif rule.type == ValidationType.UNIQUE:
                    result = validator.expect_column_values_to_be_unique(rule.column)
                    
                    results.append(ValidationResult(
                        rule_type=rule.type.value,
                        column=rule.column,
                        passed=result["success"],
                        message=result["message"],
                        details={
                            "duplicate_count": result.get("duplicate_count"),
                            "unique_percentage": result.get("unique_percentage")
                        }
                    ))
                
                elif rule.type == ValidationType.OUTLIERS:
                    method = rule.params.get("method", "zscore")
                    threshold = rule.params.get("threshold", 3.0)
                    
                    result = validator.detect_outliers_zscore(
                        rule.column,
                        threshold=threshold
                    )
                    
                    results.append(ValidationResult(
                        rule_type=rule.type.value,
                        column=rule.column,
                        passed=result["success"],
                        message=result["message"],
                        details={
                            "outlier_count": result.get("outlier_count"),
                            "outlier_percentage": result.get("outlier_percentage"),
                            "method": method
                        }
                    ))
                
                elif rule.type == ValidationType.PATTERN:
                    pattern = rule.params.get("pattern")
                    if not pattern:
                        raise ValueError("Pattern is required for pattern validation")
                    
                    result = validator.expect_column_values_to_match_regex(
                        rule.column,
                        pattern=pattern
                    )
                    
                    results.append(ValidationResult(
                        rule_type=rule.type.value,
                        column=rule.column,
                        passed=result["success"],
                        message=result["message"],
                        details={
                            "pattern": pattern,
                            "match_count": result.get("match_count"),
                            "match_percentage": result.get("match_percentage")
                        }
                    ))
            
            except Exception as e:
                # If a single validation fails, add error result
                results.append(ValidationResult(
                    rule_type=rule.type.value,
                    column=rule.column,
                    passed=False,
                    message=f"Validation error: {str(e)}",
                    details={"error": str(e)}
                ))
        
        # Calculate summary
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        success_rate = (passed / len(results) * 100) if results else 0
        
        return ValidationResponse(
            table_name=request.table_name,
            total_rules=len(results),
            passed=passed,
            failed=failed,
            success_rate=round(success_rate, 2),
            results=results
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/{validation_id}")
async def get_validation_results(validation_id: str):
    """
    Get stored validation results (future implementation with database)
    """
    raise HTTPException(
        status_code=501,
        detail="Persistent storage not yet implemented"
    )
