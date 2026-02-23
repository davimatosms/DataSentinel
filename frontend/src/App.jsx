import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import './index.css';

function App() {
  const [currentPage, setCurrentPage] = useState('landing');

  return (
    <div className="App">
      {currentPage === 'landing' && (
        <LandingPage onStart={() => setCurrentPage('dashboard')} />
      )}
      {currentPage === 'dashboard' && (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
          <div className="text-center p-12 bg-white rounded-2xl shadow-2xl max-w-2xl">
            <div className="text-6xl mb-6">🚧</div>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Dashboard em Desenvolvimento
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              A interface de validação de dados está sendo construída.
              <br />
              Em breve você poderá testar todas as validações!
            </p>
            <button
              onClick={() => setCurrentPage('landing')}
              className="bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-8 py-3 rounded-full hover:shadow-xl transition-all duration-300 hover:-translate-y-1 font-bold"
            >
              ← Voltar para Home
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
