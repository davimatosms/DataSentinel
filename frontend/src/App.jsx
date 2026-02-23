import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';
import './index.css';

function App() {
  const [currentPage, setCurrentPage] = useState('landing');

  return (
    <div className="App">
      {currentPage === 'landing' && (
        <LandingPage onStart={() => setCurrentPage('dashboard')} />
      )}
      {currentPage === 'dashboard' && (
        <Dashboard onBackToHome={() => setCurrentPage('landing')} />
      )}
    </div>
  );
}

export default App;
