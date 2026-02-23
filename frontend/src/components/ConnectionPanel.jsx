import React, { useState } from 'react';
import { Database, Upload, TestTube } from 'lucide-react';

const ConnectionPanel = ({ onConnect }) => {
  const [selectedType, setSelectedType] = useState('mock');
  const [config, setConfig] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    onConnect(selectedType, config);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">Conectar Fonte de Dados</h1>
        <p className="text-xl text-gray-600">Escolha como deseja conectar aos seus dados</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Connector Type Selection */}
        <div className="grid md:grid-cols-3 gap-4">
          <ConnectorCard
            icon={TestTube}
            title="Mock Data"
            description="Dados simulados para testes"
            selected={selectedType === 'mock'}
            onClick={() => setSelectedType('mock')}
          />
          
          <ConnectorCard
            icon={Upload}
            title="CSV File"
            description="Carregar arquivo CSV"
            selected={selectedType === 'csv'}
            onClick={() => setSelectedType('csv')}
          />
          
          <ConnectorCard
            icon={Database}
            title="PostgreSQL"
            description="Banco de dados PostgreSQL"
            selected={selectedType === 'postgresql'}
            onClick={() => setSelectedType('postgresql')}
            disabled={true}
          />
        </div>

        {/* Configuration based on type */}
        <div className="bg-white p-6 rounded-xl shadow-lg">
          {selectedType === 'mock' && (
            <MockConfig config={config} setConfig={setConfig} />
          )}
          
          {selectedType === 'csv' && (
            <CsvConfig config={config} setConfig={setConfig} />
          )}
          
          {selectedType === 'postgresql' && (
            <PostgresConfig config={config} setConfig={setConfig} />
          )}
        </div>

        {/* Submit Button */}
        <div className="flex justify-center">
          <button
            type="submit"
            className="btn-primary text-lg px-12 py-4"
          >
            Conectar
          </button>
        </div>
      </form>
    </div>
  );
};

const ConnectorCard = ({ icon: Icon, title, description, selected, onClick, disabled }) => {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`p-6 rounded-xl border-2 transition-all text-left ${
        disabled
          ? 'opacity-50 cursor-not-allowed bg-gray-50 border-gray-200'
          : selected
          ? 'border-primary-500 bg-primary-50'
          : 'border-gray-200 bg-white hover:border-primary-300 hover:bg-primary-50'
      }`}
    >
      <Icon className={`w-10 h-10 mb-3 ${selected ? 'text-primary-500' : 'text-gray-400'}`} />
      <h3 className="text-lg font-bold text-gray-900 mb-1">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
      {disabled && <span className="text-xs text-gray-500 mt-2 inline-block">Em breve</span>}
    </button>
  );
};

const MockConfig = ({ config, setConfig }) => {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Configuração de Dados Simulados</h3>
      <p className="text-gray-600 mb-4">
        Os dados simulados incluem 4 tabelas pré-configuradas: vendas, clientes, produtos e transações.
      </p>
      
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Latência de Rede (segundos)
          </label>
          <input
            type="number"
            step="0.1"
            min="0"
            max="5"
            value={config.network_delay || 0}
            onChange={(e) => setConfig({ ...config, network_delay: parseFloat(e.target.value) })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Taxa de Falha (0-1)
          </label>
          <input
            type="number"
            step="0.1"
            min="0"
            max="1"
            value={config.failure_rate || 0}
            onChange={(e) => setConfig({ ...config, failure_rate: parseFloat(e.target.value) })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
      </div>
    </div>
  );
};

const CsvConfig = ({ config, setConfig }) => {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Configuração CSV</h3>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Caminho do Arquivo
        </label>
        <input
          type="text"
          placeholder="C:/path/to/file.csv"
          value={config.file_path || ''}
          onChange={(e) => setConfig({ ...config, file_path: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <p className="text-sm text-gray-500 mt-2">
          Digite o caminho completo do arquivo CSV
        </p>
      </div>
    </div>
  );
};

const PostgresConfig = ({ config, setConfig }) => {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Configuração PostgreSQL</h3>
      <p className="text-gray-600">
        Conexão PostgreSQL estará disponível em breve.
      </p>
    </div>
  );
};

export default ConnectionPanel;
