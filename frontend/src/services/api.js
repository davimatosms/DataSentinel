/**
 * API Service - HTTP client for DataSentinel backend
 */

const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
  /**
   * Connect to a data source
   */
  async connect(connectorType, config = {}) {
    const response = await fetch(`${API_BASE_URL}/connect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        connector_type: connectorType,
        config: config,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Connection failed');
    }

    return response.json();
  }

  /**
   * Get list of available tables
   */
  async getTables() {
    const response = await fetch(`${API_BASE_URL}/tables`);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get tables');
    }

    return response.json();
  }

  /**
   * Get data from a table
   */
  async getTableData(tableName, limit = 100) {
    const response = await fetch(`${API_BASE_URL}/data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        table_name: tableName,
        limit: limit,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get table data');
    }

    return response.json();
  }

  /**
   * Execute validations
   */
  async executeValidations(tableName, rules) {
    const response = await fetch(`${API_BASE_URL}/validate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        table_name: tableName,
        rules: rules,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Validation failed');
    }

    return response.json();
  }

  /**
   * Disconnect from data source
   */
  async disconnect() {
    const response = await fetch(`${API_BASE_URL}/disconnect`);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Disconnect failed');
    }

    return response.json();
  }

  /**
   * Health check
   */
  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  }
}

export default new ApiService();
