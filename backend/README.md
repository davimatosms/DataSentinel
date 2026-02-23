# DataSentinel Backend API

FastAPI backend for data quality validation.

## Setup

```bash
# Install dependencies
pip install fastapi uvicorn[standard] python-multipart

# Run server
cd backend
python main.py
```

## API Endpoints

### Health Check
```
GET /api/health
```

### Connectors
```
POST /api/connect          - Connect to data source
GET  /api/tables           - List available tables
POST /api/data             - Get table data
GET  /api/disconnect       - Disconnect from source
```

### Validation
```
POST /api/validate         - Execute validations
GET  /api/results/{id}     - Get validation results (future)
```

## API Documentation

Access the interactive API docs at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Example Requests

### Connect to Mock Data
```json
POST /api/connect
{
  "connector_type": "mock",
  "config": {
    "network_delay": 0.0,
    "failure_rate": 0.0
  }
}
```

### Get Table Data
```json
POST /api/data
{
  "table_name": "sales",
  "limit": 100
}
```

### Execute Validation
```json
POST /api/validate
{
  "table_name": "sales",
  "rules": [
    {
      "type": "not_null",
      "column": "customer_id",
      "params": {"threshold": 0}
    },
    {
      "type": "range",
      "column": "amount",
      "params": {"min_value": 0, "max_value": 10000}
    }
  ]
}
```
