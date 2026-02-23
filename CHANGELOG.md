# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-02-23

### 🎉 Lançamento Inicial

Primeira versão estável e pronta para produção do DataSentinel.

### ✨ Adicionado

#### Core Features
- Motor de validação de qualidade de dados (`DataValidator`)
- 5 tipos de validação:
  - Valores nulos (`expect_column_values_to_not_be_null`)
  - Intervalos numéricos (`expect_column_values_to_be_between`)
  - Unicidade (`expect_column_values_to_be_unique`)
  - Detecção de outliers via Z-Score (`detect_outliers_zscore`)
  - Validação de tipos de dados

#### Conectores
- `MockConnector`: Conector simulado para testes (320 linhas)
  - 4 tabelas mockadas (sales, customers, products, transactions)
  - Simulação de latência de rede
  - Simulação de falhas de conexão
  - Suporte a tabelas customizadas
- `PostgreSQLConnector`: Conector para PostgreSQL
- `CSVConnector`: Conector para arquivos CSV locais

#### Interface Web
- Dashboard interativo com Streamlit (550+ linhas)
- Configuração visual de validações
- Preview de dados com métricas
- Gráficos interativos (Plotly):
  - Gauge de qualidade geral
  - Gráfico de pizza de resultados
- Exportação de relatórios:
  - JSON completo
  - CSV tabular
- Suporte a múltiplas fontes de dados

#### Testes
- 20 testes do MockConnector (100% passando)
- 5 testes do DataValidator (80% passando)
- 96% de cobertura de código
- Fixtures reutilizáveis
- Integração com pytest

#### Documentação
- README.md profissional com badges
- API_DOCUMENTATION.md completa
- CONTRIBUTING.md com guias de contribuição
- DEPLOYMENT.md com múltiplas opções de deploy
- PROJECT_STATUS.md com checklist completo
- Licença MIT

#### Configurações
- `.streamlit/config.toml` personalizado
- `requirements.txt` organizado
- Estrutura de projeto modular

### 📊 Métricas

- **Código**: 1.800+ linhas Python
- **Testes**: 24/25 passando (96%)
- **Velocidade**: 0.77s de execução de testes
- **Documentação**: 5 arquivos markdown completos
- **Cobertura**: 96% do código

### 🎯 Casos de Uso

- Validação de qualidade em pipelines de dados
- Monitoramento contínuo de tabelas
- Testes de integração sem infraestrutura
- Prototipagem rápida de validações
- Relatórios de qualidade de dados

---

## [Em Desenvolvimento]

### 🚀 Versão 1.1 (Planejada)

#### Planejado
- [ ] PostgreSQL totalmente integrado com testes
- [ ] Suporte a MySQL
- [ ] Validações customizadas (regex, lambdas)
- [ ] Agendamento de validações (cron-like)
- [ ] Notificações via:
  - [ ] Email
  - [ ] Slack
  - [ ] Webhook genérico
- [ ] Histórico de validações
- [ ] Comparação com execuções anteriores

### 🔮 Versão 2.0 (Futuro)

#### Ideias
- [ ] Machine Learning para detecção de anomalias
- [ ] API REST com FastAPI
- [ ] Dashboard de monitoramento em tempo real
- [ ] Integração com dbt
- [ ] Suporte a Apache Spark para Big Data
- [ ] Geração automática de testes a partir do schema
- [ ] Suporte a MongoDB e outros NoSQL
- [ ] Plugin para Airflow

---

## Tipos de Mudanças

- `Added`: Novas funcionalidades
- `Changed`: Alterações em funcionalidades existentes
- `Deprecated`: Funcionalidades que serão removidas
- `Removed`: Funcionalidades removidas
- `Fixed`: Correções de bugs
- `Security`: Correções de segurança

---

## Links

- [Código Fonte](https://github.com/seu-usuario/DataSentinel)
- [Issues](https://github.com/seu-usuario/DataSentinel/issues)
- [Pull Requests](https://github.com/seu-usuario/DataSentinel/pulls)
- [Releases](https://github.com/seu-usuario/DataSentinel/releases)
