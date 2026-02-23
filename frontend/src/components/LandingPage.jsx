import React from 'react';
import { ArrowRight, Shield, CheckCircle, BarChart3, Database, FileCheck, Download } from 'lucide-react';

const LandingPage = ({ onStart }) => {
  return (
    <div className="min-h-screen">
      {/* Navbar */}
      <nav className="bg-white/90 backdrop-blur-md fixed w-full z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Shield className="w-8 h-8 text-primary-500" />
            <span className="text-2xl font-bold text-gray-900">DataSentinel</span>
          </div>
          <button
            onClick={onStart}
            className="bg-primary-500 text-white px-6 py-2 rounded-full hover:bg-primary-600 transition-all duration-300 hover:shadow-lg"
          >
            Começar
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-600 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="max-w-6xl mx-auto text-center relative z-10">
          <h1 className="text-5xl md:text-7xl font-extrabold mb-6 leading-tight">
            Validação de Qualidade de Dados
            <br />
            <span className="text-primary-100">Simples, Poderosa e Visual</span>
          </h1>
          <p className="text-xl md:text-2xl mb-10 text-primary-50 max-w-3xl mx-auto">
            Detecte problemas de qualidade antes que eles afetem suas análises.
            Interface moderna, testes automatizados e relatórios em tempo real.
          </p>
          <button
            onClick={onStart}
            className="bg-white text-primary-600 px-10 py-4 rounded-full font-bold text-lg hover:shadow-2xl transition-all duration-300 hover:scale-105 inline-flex items-center space-x-2"
          >
            <span>🚀 Começar Gratuitamente</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8">
          {[
            { number: '5+', label: 'Tipos de Validação' },
            { number: '3', label: 'Conectores Integrados' },
            { number: '96%', label: 'Cobertura de Testes' },
            { number: '100%', label: 'Open Source' },
          ].map((stat, index) => (
            <div key={index} className="text-center p-6 rounded-xl bg-gradient-to-br from-primary-50 to-secondary-50 hover:shadow-xl transition-all duration-300">
              <div className="text-4xl font-extrabold bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent mb-2">
                {stat.number}
              </div>
              <div className="text-gray-600 font-medium">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* About Section */}
      <section className="section bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-extrabold text-center mb-4">
            O que é o DataSentinel?
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-3xl mx-auto">
            Uma plataforma completa para garantir a qualidade dos seus dados
          </p>
          
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h3 className="text-3xl font-bold mb-6 text-gray-900">
                Validação de Dados Nunca Foi Tão Fácil
              </h3>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                O DataSentinel é uma ferramenta moderna de validação de qualidade de dados
                que permite testar, validar e monitorar a integridade dos seus dados de
                forma automatizada e visual.
              </p>
              <p className="text-lg text-gray-600 leading-relaxed">
                Desenvolvido para <strong>analistas de dados</strong>,
                <strong> engenheiros de dados</strong> e <strong>cientistas de dados</strong>
                que precisam garantir a qualidade antes de análises críticas.
              </p>
            </div>
            
            <div className="space-y-4">
              {[
                { icon: <CheckCircle className="w-6 h-6" />, title: 'Sem Configuração Complexa', desc: 'Interface intuitiva pronta para uso' },
                { icon: <ArrowRight className="w-6 h-6" />, title: 'Resultados em Tempo Real', desc: 'Visualize problemas instantaneamente' },
                { icon: <BarChart3 className="w-6 h-6" />, title: 'Relatórios Visuais', desc: 'Gráficos interativos e dashboards' },
                { icon: <Database className="w-6 h-6" />, title: 'Múltiplas Fontes', desc: 'PostgreSQL, CSV e dados simulados' },
              ].map((benefit, index) => (
                <div key={index} className="bg-white p-4 rounded-lg border-l-4 border-primary-500 hover:shadow-lg transition-all duration-300">
                  <div className="flex items-start space-x-3">
                    <div className="text-primary-500 mt-1">{benefit.icon}</div>
                    <div>
                      <h4 className="font-bold text-gray-900">{benefit.title}</h4>
                      <p className="text-gray-600 text-sm">{benefit.desc}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-extrabold text-center mb-4">
            Recursos Principais
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-3xl mx-auto">
            Tudo que você precisa para garantir a qualidade dos seus dados
          </p>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: '🎭', title: 'Mock Connector', desc: 'Teste suas validações sem necessidade de banco de dados real. Inclui 4 tabelas simuladas com dados realistas.' },
              { icon: '✅', title: 'Validações Inteligentes', desc: '5 tipos de validação prontas: valores nulos, intervalos, unicidade, detecção de outliers e padrões regex.' },
              { icon: '📈', title: 'Visualizações Interativas', desc: 'Dashboard moderno com gráficos de gauge, barras e sunburst. Entenda seus dados visualmente.' },
              { icon: '🔍', title: 'Detecção de Outliers', desc: 'Identifique automaticamente valores anômalos usando Z-score ou IQR. Proteja suas análises.' },
              { icon: '💾', title: 'Múltiplas Fontes', desc: 'Conecte-se a PostgreSQL, carregue arquivos CSV ou use dados simulados. Flexibilidade total.' },
              { icon: '📥', title: 'Export & Relatórios', desc: 'Exporte resultados em JSON ou CSV. Integre facilmente com suas ferramentas de BI.' },
            ].map((feature, index) => (
              <div key={index} className="card border-t-4 border-primary-500">
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-3 text-gray-900">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="section bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-extrabold text-center mb-4">
            Para Quem é o DataSentinel?
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-3xl mx-auto">
            Profissionais de dados que precisam de qualidade e confiabilidade
          </p>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: '👨‍💻', title: 'Engenheiros de Dados', desc: 'Valide pipelines ETL/ELT, garanta qualidade em data warehouses e automatize checks em processos de ingestão.' },
              { icon: '📊', title: 'Analistas de Dados', desc: 'Verifique a qualidade antes de análises críticas, detecte inconsistências e garanta relatórios confiáveis.' },
              { icon: '🔬', title: 'Cientistas de Dados', desc: 'Prepare datasets para machine learning, identifique outliers e garanta features de qualidade para seus modelos.' },
            ].map((use, index) => (
              <div key={index} className="bg-white p-8 rounded-2xl text-center hover:shadow-2xl transition-all duration-300">
                <div className="text-6xl mb-6">{use.icon}</div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">{use.title}</h3>
                <p className="text-gray-600 leading-relaxed">{use.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section bg-gradient-to-r from-primary-500 to-secondary-600 text-white text-center">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-extrabold mb-6">
            Pronto para Garantir a Qualidade dos Seus Dados?
          </h2>
          <p className="text-xl mb-10 text-primary-50">
            Comece gratuitamente agora. Sem cartão de crédito, sem instalação complexa.
          </p>
          <button
            onClick={onStart}
            className="bg-white text-primary-600 px-12 py-4 rounded-full font-bold text-lg hover:shadow-2xl transition-all duration-300 hover:scale-105 inline-flex items-center space-x-2"
          >
            <span>🚀 Testar Agora</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Shield className="w-8 h-8" />
            <span className="text-2xl font-bold">DataSentinel</span>
          </div>
          <p className="text-gray-400 mb-6">
            Validação Profissional de Qualidade de Dados
          </p>
          <div className="border-t border-gray-800 pt-6">
            <p className="text-gray-500 text-sm mb-2">Open Source sob MIT License</p>
            <a
              href="https://github.com/davimatosms/DataSentinel"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-400 hover:text-primary-300 font-semibold"
            >
              GitHub Repository
            </a>
            <p className="text-gray-600 text-xs mt-4">© 2026 DataSentinel. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
