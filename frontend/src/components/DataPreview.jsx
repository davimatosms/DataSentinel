import React from 'react';
import { Table, ChevronRight } from 'lucide-react';

const DataPreview = ({ tables, onSelectTable, onBack }) => {
  return (
    <div className="max-w-5xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">Selecionar Tabela</h1>
        <p className="text-xl text-gray-600">Escolha uma tabela para validar</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tables.map((table) => (
          <button
            key={table}
            onClick={() => onSelectTable(table)}
            className="card text-left group hover:border-primary-500 border-2 border-transparent"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Table className="w-8 h-8 text-primary-500" />
                <div>
                  <h3 className="text-lg font-bold text-gray-900">{table}</h3>
                  <p className="text-sm text-gray-600">Clique para visualizar</p>
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-primary-500 transition-colors" />
            </div>
          </button>
        ))}
      </div>

      <div className="mt-8 text-center">
        <button
          onClick={onBack}
          className="text-gray-600 hover:text-gray-900 font-medium"
        >
          ← Voltar para conexão
        </button>
      </div>
    </div>
  );
};

export default DataPreview;
