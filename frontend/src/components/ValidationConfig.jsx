import React, { useState } from 'react';
import { Plus, Trash2, Play } from 'lucide-react';

const ValidationConfig = ({ tableData, onExecute, onBack }) => {
  const [rules, setRules] = useState([]);
  const [currentRule, setCurrentRule] = useState({
    type: 'not_null',
    column: tableData.columns[0] || '',
    params: {}
  });

  const addRule = () => {
    setRules([...rules, currentRule]);
    setCurrentRule({
      type: 'not_null',
      column: tableData.columns[0] || '',
      params: {}
    });
  };

  const removeRule = (index) => {
    setRules(rules.filter((_, i) => i !== index));
  };

  const handleExecute = () => {
    if (rules.length === 0) {
      alert('Adicione pelo menos uma regra de validação');
      return;
    }
    onExecute(rules);
  };

  const validationTypes = [
    { value: 'not_null', label: 'Valores Nulos' },
    { value: 'range', label: 'Intervalo' },
    { value: 'unique', label: 'Unicidade' },
    { value: 'outliers', label: 'Outliers' },
    { value: 'pattern', label: 'Padrão Regex' }
  ];

  return (
    <div className="max-w-5xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">Configurar Validações</h1>
        <p className="text-xl text-gray-600">Tabela: <span className="font-bold text-primary-600">{tableData.table_name}</span></p>
        <p className="text-gray-600">{tableData.row_count} linhas, {tableData.columns.length} colunas</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Add Rule Form */}
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Nova Regra de Validação</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Tipo</label>
              <select
                value={currentRule.type}
                onChange={(e) => setCurrentRule({ ...currentRule, type: e.target.value, params: {} })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                {validationTypes.map(vt => (
                  <option key={vt.value} value={vt.value}>{vt.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Coluna</label>
              <select
                value={currentRule.column}
                onChange={(e) => setCurrentRule({ ...currentRule, column: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                {tableData.columns.map(col => (
                  <option key={col} value={col}>{col}</option>
                ))}
              </select>
            </div>

            {/* Parameters based on type */}
            {currentRule.type === 'not_null' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Threshold (%)</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={currentRule.params.threshold || 0}
                  onChange={(e) => setCurrentRule({
                    ...currentRule,
                    params: { threshold: parseFloat(e.target.value) }
                  })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            )}

            {currentRule.type === 'range' && (
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Mínimo</label>
                  <input
                    type="number"
                    value={currentRule.params.min_value || ''}
                    onChange={(e) => setCurrentRule({
                      ...currentRule,
                      params: { ...currentRule.params, min_value: parseFloat(e.target.value) }
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Máximo</label>
                  <input
                    type="number"
                    value={currentRule.params.max_value || ''}
                    onChange={(e) => setCurrentRule({
                      ...currentRule,
                      params: { ...currentRule.params, max_value: parseFloat(e.target.value) }
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>
            )}

            {currentRule.type === 'pattern' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Regex Pattern</label>
                <input
                  type="text"
                  placeholder="^[A-Z0-9]+"
                  value={currentRule.params.pattern || ''}
                  onChange={(e) => setCurrentRule({
                    ...currentRule,
                    params: { pattern: e.target.value }
                  })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg font-mono text-sm"
                />
              </div>
            )}

            {currentRule.type === 'outliers' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Threshold Z-score</label>
                <input
                  type="number"
                  step="0.5"
                  value={currentRule.params.threshold || 3}
                  onChange={(e) => setCurrentRule({
                    ...currentRule,
                    params: { threshold: parseFloat(e.target.value), method: 'zscore' }
                  })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            )}

            <button
              onClick={addRule}
              className="w-full bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors flex items-center justify-center space-x-2"
            >
              <Plus className="w-5 h-5" />
              <span>Adicionar Regra</span>
            </button>
          </div>
        </div>

        {/* Rules List */}
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Regras Configuradas ({rules.length})</h3>
          
          {rules.length === 0 ? (
            <p className="text-gray-500 text-center py-8">Nenhuma regra adicionada ainda</p>
          ) : (
            <div className="space-y-3">
              {rules.map((rule, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-semibold text-gray-900">
                      {validationTypes.find(vt => vt.value === rule.type)?.label}
                    </p>
                    <p className="text-sm text-gray-600">Coluna: {rule.column}</p>
                  </div>
                  <button
                    onClick={() => removeRule(index)}
                    className="text-red-500 hover:text-red-700 transition-colors"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="mt-8 flex justify-center space-x-4">
        <button
          onClick={onBack}
          className="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition-colors"
        >
          ← Voltar
        </button>
        <button
          onClick={handleExecute}
          className="btn-primary px-8 py-3 flex items-center space-x-2"
          disabled={rules.length === 0}
        >
          <Play className="w-5 h-5" />
          <span>Executar Validações</span>
        </button>
      </div>
    </div>
  );
};

export default ValidationConfig;
