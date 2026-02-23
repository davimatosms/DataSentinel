"""
Connector routes - Handle data source connections
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from app.connectors import MockConnector, CSVConnector
from backend.api.schemas import (
    ConnectionRequest,
    ConnectionResponse,
    TableDataRequest,
    TableDataResponse,
    ConnectorType
)

router = APIRouter()

# Store active connections (in production, use proper state management)
active_connections: Dict[str, Any] = {}


@router.post("/connect", response_model=ConnectionResponse)
async def connect_to_source(request: ConnectionRequest):
    """
    Connect to a data source
    """
    try:
        connector = None
        
        if request.connector_type == ConnectorType.MOCK:
            # Create MockConnector
            connector = MockConnector(
                network_delay=request.config.get("network_delay", 0.0),
                failure_rate=request.config.get("failure_rate", 0.0)
            )
            connector.connect()
            tables = connector.list_tables()
            
            # Store connector
            active_connections["current"] = connector
            
            return ConnectionResponse(
                success=True,
                message="Successfully connected to Mock data source",
                tables=tables
            )
        
        elif request.connector_type == ConnectorType.CSV:
            # CSV connector
            file_path = request.config.get("file_path")
            if not file_path:
                raise HTTPException(status_code=400, detail="CSV file_path is required")
            
            connector = CSVConnector(file_path=file_path)
            connector.connect()
            
            active_connections["current"] = connector
            
            return ConnectionResponse(
                success=True,
                message=f"Successfully connected to CSV file: {file_path}",
                tables=[os.path.basename(file_path)]
            )
        
        elif request.connector_type == ConnectorType.POSTGRESQL:
            raise HTTPException(
                status_code=501,
                detail="PostgreSQL connector not yet implemented in API"
            )
        
        else:
            raise HTTPException(status_code=400, detail="Invalid connector type")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables")
async def list_tables():
    """
    List available tables from the active connection
    """
    if "current" not in active_connections:
        raise HTTPException(status_code=400, detail="No active connection")
    
    try:
        connector = active_connections["current"]
        tables = connector.list_tables()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data", response_model=TableDataResponse)
async def get_table_data(request: TableDataRequest):
    """
    Get data from a specific table
    """
    if "current" not in active_connections:
        raise HTTPException(status_code=400, detail="No active connection")
    
    try:
        connector = active_connections["current"]
        df = connector.get_table_data(request.table_name)
        
        # Limit rows
        if request.limit:
            df = df.head(request.limit)
        
        # Convert to dict
        data = df.to_dict(orient='records')
        columns = df.columns.tolist()
        
        return TableDataResponse(
            table_name=request.table_name,
            columns=columns,
            data=data,
            row_count=len(df)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/disconnect")
async def disconnect():
    """
    Disconnect from the current data source
    """
    if "current" in active_connections:
        try:
            connector = active_connections["current"]
            connector.disconnect()
            del active_connections["current"]
            return {"success": True, "message": "Disconnected successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return {"success": True, "message": "No active connection"}
