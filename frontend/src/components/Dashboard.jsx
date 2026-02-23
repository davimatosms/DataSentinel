import React, { useState } from 'react';
import { Shield, ArrowLeft, Database, CheckCircle, AlertCircle, Activity } from 'lucide-react';
import ConnectionPanel from './ConnectionPanel';
import DataPreview from './DataPreview';
import ValidationConfig from './ValidationConfig';
import ResultsPanel from './ResultsPanel';
import ResultsPanel from './ResultsPanel';
import api from '../services/api';

const Dashboard = ({ onBack }) => {
  const [step, setStep] = useState('connect'); // connect, preview, validate, results
  const [connectionData, setConnectionData] = useState(null);
  const [selectedTable, setSelectedTable] = useState(null);
  const [tableData, setTableData] = useState(null);
  const [validationResults, setValidationResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleConnect = async (connectorType, config) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.connect(connectorType, config);
      setConnectionData(response);
      setStep('preview');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTable = async (tableName) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await api.getTableData(tableName, 100);
      setSelectedTable(tableName);
      setTableData(data);
      setStep('validate');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteValidations = async (rules) => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await api.executeValidations(selectedTable, rules);
      setValidationResults(results);
      setStep('results');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setStep('connect');
    setConnectionData(null);
    setSelectedTable(null);
    setTableData(null);
    setValidationResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <button
                onClick={onBack}
                className="flex items-center space-x-2 text-gray-600 hover:text-primary-500 transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
                <span>Voltar</span>
              </button>
              <div className="h-6 w-px bg-gray-300"></div>
              <div className="flex items-center space-x-2">
                <Shield className="w-6 h-6 text-primary-500" />
                <span className="text-xl font-bold text-gray-900">DataSentinel</span>
              </div>
            </div>
            
            {/* Progress Steps */}
            <div className="flex items-center space-x-4">
              <StepIndicator icon={Database} label="Conectar" active={step === 'connect'} completed={['preview', 'validate', 'results'].includes(step)} />
              <StepIndicator icon={Activity} label="Dados" active={step === 'preview'} completed={['validate', 'results'].includes(step)} />
              <StepIndicator icon={CheckCircle} label="Validar" active={step === 'validate'} completed={step === 'results'} />
              <StepIndicator icon={AlertCircle} label="Resultados" active={step === 'results'} />
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
          </div>
        )}

        {!loading && (
          <>
            {step === 'connect' && (
              <ConnectionPanel onConnect={handleConnect} />
            )}

            {step === 'preview' && connectionData && (
              <DataPreview 
                tables={connectionData.tables} 
                onSelectTable={handleSelectTable}
                onBack={handleReset}
              />
            )}

            {step === 'validate' && tableData && (
              <ValidationConfig 
                tableData={tableData}
                onExecute={handleExecuteValidations}
                onBack={() => setStep('preview')}
              />
            )}

            {step === 'results' && validationResults && (
              <ResultsPanel 
                results={validationResults}
                onReset={handleReset}
              />
            )}
          </>
        )}
      </div>
    </div>
  );
};

const StepIndicator = ({ icon: Icon, label, active, completed }) => {
  return (
    <div className="flex items-center space-x-2">
      <div className={`flex items-center justify-center w-8 h-8 rounded-full transition-all ${
        completed ? 'bg-green-500 text-white' :
        active ? 'bg-primary-500 text-white' :
        'bg-gray-200 text-gray-500'
      }`}>
        <Icon className="w-4 h-4" />
      </div>
      <span className={`text-sm font-medium ${
        active ? 'text-primary-600' : 'text-gray-600'
      }`}>
        {label}
      </span>
    </div>
  );
};

export default Dashboard;
