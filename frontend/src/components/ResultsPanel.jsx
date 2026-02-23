import React from 'react';
import { CheckCircle, XCircle, RotateCcw, Download } from 'lucide-react';

const ResultsPanel = ({ results, onReset }) => {
  const exportJSON = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    const exportFileDefaultName = `validation_results_${new Date().toISOString()}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const successRate = results.success_rate;
  const gaugeColor = successRate >= 80 ? 'text-green-500' : successRate >= 50 ? 'text-yellow-500' : 'text-red-500';

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">Resultados da Validação</h1>
        <p className="text-xl text-gray-600">Tabela: <span className="font-bold text-primary-600">{results.table_name}</span></p>
      </div>

      {/* Summary Cards */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <p className="text-gray-600 mb-2">Total de Regras</p>
          <p className="text-4xl font-bold text-gray-900">{results.total_rules}</p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <p className="text-gray-600 mb-2">Aprovadas</p>
          <p className="text-4xl font-bold text-green-500">{results.passed}</p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <p className="text-gray-600 mb-2">Reprovadas</p>
          <p className="text-4xl font-bold text-red-500">{results.failed}</p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <p className="text-gray-600 mb-2">Taxa de Sucesso</p>
          <p className={`text-4xl font-bold ${gaugeColor}`}>{results.success_rate}%</p>
        </div>
      </div>

      {/* Gauge Visual */}
      <div className="bg-white p-8 rounded-xl shadow-lg mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-6 text-center">Taxa de Sucesso</h3>
        <div className="relative w-full h-8 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className={`h-full ${successRate >= 80 ? 'bg-green-500' : successRate >= 50 ? 'bg-yellow-500' : 'bg-red-500'} transition-all duration-1000`}
            style={{ width: `${successRate}%` }}
          ></div>
        </div>
        <div className="flex justify-between mt-2 text-sm text-gray-600">
          <span>0%</span>
          <span>50%</span>
          <span>100%</span>
        </div>
      </div>

      {/* Results Details */}
      <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-6">Detalhes das Validações</h3>
        
        <div className="space-y-4">
          {results.results.map((result, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg border-l-4 ${
                result.passed ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    {result.passed ? (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-500" />
                    )}
                    <h4 className="font-bold text-gray-900">
                      {result.rule_type.replace('_', ' ').toUpperCase()}
                    </h4>
                    <span className="text-sm text-gray-600">• {result.column}</span>
                  </div>
                  
                  <p className={`text-sm ${result.passed ? 'text-green-700' : 'text-red-700'}`}>
                    {result.message}
                  </p>
                  
                  {result.details && (
                    <div className="mt-2 text-xs text-gray-600 bg-white bg-opacity-50 p-2 rounded">
                      {Object.entries(result.details).map(([key, value]) => (
                        <span key={key} className="mr-4">
                          <strong>{key}:</strong> {JSON.stringify(value)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={exportJSON}
          className="px-8 py-3 bg-primary-500 text-white rounded-full hover:bg-primary-600 transition-colors flex items-center space-x-2"
        >
          <Download className="w-5 h-5" />
          <span>Exportar JSON</span>
        </button>
        
        <button
          onClick={onReset}
          className="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition-colors flex items-center space-x-2"
        >
          <RotateCcw className="w-5 h-5" />
          <span>Nova Validação</span>
        </button>
      </div>
    </div>
  );
};

export default ResultsPanel;
