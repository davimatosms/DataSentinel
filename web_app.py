"""
DataSentinel - Web Dashboard
Interface web para validação de qualidade de dados
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

from app.connectors import MockConnector, CSVConnector
from app.core.engine import DataValidator

# Configuração da página
st.set_page_config(
    page_title="DataSentinel - Validação de Qualidade",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado da sessão
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# CSS customizado profissional
st.markdown("""
<style>
    /* Remover padding padrão */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    /* Navbar */
    .navbar {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        padding: 1rem 5%;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 20px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2d3748;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 8rem 5% 6rem 5%;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') no-repeat bottom;
        opacity: 0.3;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        opacity: 0.95;
        margin-bottom: 2.5rem;
        font-weight: 300;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Buttons */
    .cta-primary {
        background: white;
        color: #667eea;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 700;
        border: none;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
    }
    
    .cta-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    /* Section Styling */
    .section {
        padding: 5rem 5%;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2d3748;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .section-subtitle {
        font-size: 1.2rem;
        color: #718096;
        text-align: center;
        margin-bottom: 4rem;
        font-weight: 300;
    }
    
    /* Stats Box */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .stat-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #718096;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 5px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-top: 4px solid #667eea;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #718096;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Testimonial / Benefits */
    .benefit-box {
        background: linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .benefit-box:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.1);
    }
    
    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 5rem 5%;
        color: white;
        text-align: center;
        margin-top: 4rem;
    }
    
    /* Footer */
    .footer {
        background: #2d3748;
        color: white;
        padding: 3rem 5%;
        text-align: center;
    }
    
    .footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
    }
    
    /* App page styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .success-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .error-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #764ba2;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)


def landing_page():
    """Renderiza a landing page profissional"""
    
    # Navbar
    st.markdown("""
    <div class="navbar">
        <div class="logo">🛡️ DataSentinel</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">
            Validação de Qualidade de Dados<br>Simples, Poderosa e Visual
        </div>
        <div class="hero-subtitle">
            Detecte problemas de qualidade antes que eles afetem suas análises.<br>
            Interface moderna, testes automatizados e relatórios em tempo real.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão CTA no hero
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Começar Gratuitamente", use_container_width=True, type="primary", key="hero_cta"):
            st.session_state.page = 'app'
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
    <div class="section">
        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-number">5+</div>
                <div class="stat-label">Tipos de Validação</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">3</div>
                <div class="stat-label">Conectores Integrados</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">96%</div>
                <div class="stat-label">Cobertura de Testes</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">100%</div>
                <div class="stat-label">Open Source</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # About Section
    st.markdown("""
    <div class="section">
        <div class="section-title">O que é o DataSentinel?</div>
        <div class="section-subtitle">
            Uma plataforma completa para garantir a qualidade dos seus dados
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div style="padding: 2rem;">
            <h3 style="color: #2d3748; font-size: 1.8rem; margin-bottom: 1.5rem;">
                Validação de Dados Nunca Foi Tão Fácil
            </h3>
            <p style="color: #718096; font-size: 1.1rem; line-height: 1.8;">
                O DataSentinel é uma ferramenta moderna de validação de qualidade de dados 
                que permite testar, validar e monitorar a integridade dos seus dados de 
                forma automatizada e visual.
            </p>
            <br>
            <p style="color: #718096; font-size: 1.1rem; line-height: 1.8;">
                Desenvolvido para <strong>analistas de dados</strong>, 
                <strong>engenheiros de dados</strong> e <strong>cientistas de dados</strong> 
                que precisam garantir a qualidade antes de análises críticas.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 2rem;">
            <div class="benefit-box">
                <h4 style="color: #2d3748; margin: 0 0 0.5rem 0;">✅ Sem Configuração Complexa</h4>
                <p style="margin: 0; color: #718096;">Interface intuitiva pronta para uso</p>
            </div>
            <div class="benefit-box">
                <h4 style="color: #2d3748; margin: 0 0 0.5rem 0;">⚡ Resultados em Tempo Real</h4>
                <p style="margin: 0; color: #718096;">Visualize problemas instantaneamente</p>
            </div>
            <div class="benefit-box">
                <h4 style="color: #2d3748; margin: 0 0 0.5rem 0;">📊 Relatórios Visuais</h4>
                <p style="margin: 0; color: #718096;">Gráficos interativos e dashboards</p>
            </div>
            <div class="benefit-box">
                <h4 style="color: #2d3748; margin: 0 0 0.5rem 0;">🔌 Múltiplas Fontes</h4>
                <p style="margin: 0; color: #718096;">PostgreSQL, CSV e dados simulados</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div class="section">
        <div class="section-title">Recursos Principais</div>
        <div class="section-subtitle">
            Tudo que você precisa para garantir a qualidade dos seus dados
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section">
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🎭</div>
                <div class="feature-title">Mock Connector</div>
                <div class="feature-description">
                    Teste suas validações sem necessidade de banco de dados real. 
                    Inclui 4 tabelas simuladas com dados realistas para desenvolvimento 
                    e testes rápidos.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">✅</div>
                <div class="feature-title">Validações Inteligentes</div>
                <div class="feature-description">
                    5 tipos de validação prontas: valores nulos, intervalos, 
                    unicidade, detecção de outliers e padrões regex. 
                    Configure em segundos.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <div class="feature-title">Visualizações Interativas</div>
                <div class="feature-description">
                    Dashboard moderno com gráficos de gauge, barras e sunburst. 
                    Entenda seus dados visualmente e exporte relatórios.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Detecção de Outliers</div>
                <div class="feature-description">
                    Identifique automaticamente valores anômalos usando 
                    Z-score ou IQR. Proteja suas análises de dados problemáticos.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">💾</div>
                <div class="feature-title">Múltiplas Fontes</div>
                <div class="feature-description">
                    Conecte-se a PostgreSQL, carregue arquivos CSV ou use dados 
                    simulados. Flexibilidade total para seu workflow.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📥</div>
                <div class="feature-title">Export & Relatórios</div>
                <div class="feature-description">
                    Exporte resultados em JSON ou CSV. Integre facilmente 
                    com suas ferramentas de BI e relatórios automatizados.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Cases Section
    st.markdown("""
    <div class="section" style="background: #f7fafc; padding: 5rem 5%; margin: 3rem -5%;">
        <div class="section-title">Para Quem é o DataSentinel?</div>
        <div class="section-subtitle">
            Profissionais de dados que precisam de qualidade e confiabilidade
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">👨‍💻</div>
            <h3 style="color: #2d3748; margin-bottom: 1rem;">Engenheiros de Dados</h3>
            <p style="color: #718096; line-height: 1.7;">
                Valide pipelines ETL/ELT, garanta qualidade em data warehouses 
                e automatize checks em processos de ingestão.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #2d3748; margin-bottom: 1rem;">Analistas de Dados</h3>
            <p style="color: #718096; line-height: 1.7;">
                Verifique a qualidade antes de análises críticas, 
                detecte inconsistências e garanta relatórios confiáveis.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔬</div>
            <h3 style="color: #2d3748; margin-bottom: 1rem;">Cientistas de Dados</h3>
            <p style="color: #718096; line-height: 1.7;">
                Prepare datasets para machine learning, identifique outliers 
                e garanta features de qualidade para seus modelos.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Final
    st.markdown("""
    <div class="cta-section">
        <div style="max-width: 800px; margin: 0 auto;">
            <h2 style="font-size: 2.5rem; margin-bottom: 1.5rem; font-weight: 800;">
                Pronto para Garantir a Qualidade dos Seus Dados?
            </h2>
            <p style="font-size: 1.2rem; margin-bottom: 2.5rem; opacity: 0.95;">
                Comece gratuitamente agora. Sem cartão de crédito, sem instalação complexa.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Testar Agora", use_container_width=True, type="primary", key="footer_cta"):
            st.session_state.page = 'app'
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div style="max-width: 1200px; margin: 0 auto;">
            <div style="margin-bottom: 2rem;">
                <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">
                    🛡️ DataSentinel
                </div>
                <p style="color: #a0aec0; font-size: 1rem;">
                    Validação Profissional de Qualidade de Dados
                </p>
            </div>
            
            <div style="padding: 2rem 0; border-top: 1px solid rgba(255,255,255,0.1);">
                <p style="margin: 0.5rem 0; color: #a0aec0;">
                    Open Source sob MIT License
                </p>
                <p style="margin: 0.5rem 0;">
                    <a href="https://github.com/davimatosms/DataSentinel" target="_blank">
                        GitHub Repository
                    </a>
                </p>
                <p style="margin: 1.5rem 0 0 0; color: #718096; font-size: 0.9rem;">
                    © 2026 DataSentinel. Todos os direitos reservados.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Inicializa variáveis de sessão"""
    if 'connector' not in st.session_state:
        st.session_state.connector = None
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'validator' not in st.session_state:
        st.session_state.validator = None
    if 'validation_done' not in st.session_state:
        st.session_state.validation_done = False


def create_gauge_chart(value, title):
    """Cria um gráfico de gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        delta={'reference': 100},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#ffcccb'},
                {'range': [50, 80], 'color': '#fff4cc'},
                {'range': [80, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig


def sidebar_configuration():
    """Configuração da sidebar"""
    st.sidebar.markdown("## ⚙️ Configuração")
    
    # Seleção de fonte de dados
    data_source = st.sidebar.selectbox(
        "Fonte de Dados",
        ["Mock (Simulado)", "CSV Local", "PostgreSQL (Em breve)"]
    )
    
    if data_source == "Mock (Simulado)":
        st.sidebar.info("🎭 Usando dados simulados para demonstração")
        
        # Opções do Mock
        simulate_delay = st.sidebar.checkbox("Simular latência de rede", value=False)
        
        config = {}
        if simulate_delay:
            delay_time = st.sidebar.slider("Tempo de delay (segundos)", 0.1, 2.0, 0.5, 0.1)
            config = {'simulate_delay': True, 'delay_seconds': delay_time}
        
        if st.sidebar.button("🔌 Conectar ao Mock"):
            with st.spinner("Conectando..."):
                connector = MockConnector(config if config else None)
                if connector.connect():
                    st.session_state.connector = connector
                    st.sidebar.success("✅ Conectado com sucesso!")
                else:
                    st.sidebar.error("❌ Falha na conexão")
    
    elif data_source == "CSV Local":
        st.sidebar.info("📁 Carregar arquivo CSV")
        uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV", type=['csv'])
        
        if uploaded_file is not None:
            st.session_state.data = pd.read_csv(uploaded_file)
            st.sidebar.success(f"✅ Arquivo carregado: {len(st.session_state.data)} linhas")
    
    else:
        st.sidebar.warning("🚧 PostgreSQL em desenvolvimento")
    
    st.sidebar.markdown("---")
    
    # Seleção de tabela (se conectado ao Mock)
    if st.session_state.connector and isinstance(st.session_state.connector, MockConnector):
        tables = st.session_state.connector.list_tables()
        selected_table = st.sidebar.selectbox("Selecione uma tabela", tables)
        
        if st.sidebar.button("📊 Carregar Dados"):
            with st.spinner("Carregando dados..."):
                st.session_state.data = st.session_state.connector.get_table_data(selected_table)
                st.sidebar.success(f"✅ Carregados {len(st.session_state.data)} registros")
    
    return data_source


def display_data_preview():
    """Exibe preview dos dados"""
    if st.session_state.data is not None:
        st.markdown("### 📋 Preview dos Dados")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total de Linhas", len(st.session_state.data))
        with col2:
            st.metric("📈 Total de Colunas", len(st.session_state.data.columns))
        with col3:
            memory_mb = st.session_state.data.memory_usage(deep=True).sum() / 1024 / 1024
            st.metric("💾 Memória", f"{memory_mb:.2f} MB")
        with col4:
            null_count = st.session_state.data.isnull().sum().sum()
            st.metric("⚠️ Valores Nulos", null_count)
        
        # Preview da tabela
        st.dataframe(
            st.session_state.data.head(10),
            use_container_width=True,
            height=300
        )
        
        # Informações das colunas
        with st.expander("ℹ️ Informações das Colunas"):
            col_info = pd.DataFrame({
                'Coluna': st.session_state.data.columns,
                'Tipo': st.session_state.data.dtypes.astype(str),
                'Não Nulos': st.session_state.data.count(),
                'Nulos': st.session_state.data.isnull().sum(),
                '% Nulos': (st.session_state.data.isnull().sum() / len(st.session_state.data) * 100).round(2)
            })
            st.dataframe(col_info, use_container_width=True)


def validation_configuration():
    """Configuração das validações"""
    if st.session_state.data is None:
        st.warning("⚠️ Carregue os dados primeiro!")
        return
    
    st.markdown("### 🔍 Configurar Validações")
    
    # Nome da tabela
    table_name = st.text_input("Nome da Tabela", value="dados_validacao")
    
    # Seleção de colunas para validar
    columns = st.session_state.data.columns.tolist()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔒 Valores Nulos", 
        "📏 Intervalos", 
        "🎯 Unicidade",
        "📊 Outliers"
    ])
    
    validations = {
        'not_null': [],
        'range': [],
        'unique': [],
        'outliers': []
    }
    
    with tab1:
        st.markdown("#### Validação de Valores Nulos")
        selected_cols_null = st.multiselect(
            "Selecione colunas para validar nulos",
            columns,
            key="null_cols"
        )
        
        if selected_cols_null:
            threshold = st.slider(
                "Threshold de nulos aceitável (%)",
                0.0, 100.0, 0.0, 0.5,
                key="null_threshold"
            )
            validations['not_null'] = [(col, threshold) for col in selected_cols_null]
    
    with tab2:
        st.markdown("#### Validação de Intervalos")
        numeric_cols = st.session_state.data.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            selected_col_range = st.selectbox("Selecione uma coluna", numeric_cols, key="range_col")
            
            col1, col2 = st.columns(2)
            with col1:
                min_val = st.number_input("Valor Mínimo", value=0.0, key="min_val")
            with col2:
                max_val = st.number_input("Valor Máximo", value=1000.0, key="max_val")
            
            if st.button("➕ Adicionar Validação de Intervalo"):
                validations['range'].append((selected_col_range, min_val, max_val))
                st.success(f"✅ Validação adicionada para {selected_col_range}")
    
    with tab3:
        st.markdown("#### Validação de Unicidade")
        selected_cols_unique = st.multiselect(
            "Selecione colunas que devem ser únicas",
            columns,
            key="unique_cols"
        )
        validations['unique'] = selected_cols_unique
    
    with tab4:
        st.markdown("#### Detecção de Outliers")
        numeric_cols = st.session_state.data.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            selected_cols_outliers = st.multiselect(
                "Selecione colunas para detectar outliers",
                numeric_cols,
                key="outlier_cols"
            )
            
            if selected_cols_outliers:
                z_threshold = st.slider(
                    "Z-Score Threshold",
                    1.0, 5.0, 3.0, 0.5,
                    key="z_threshold"
                )
                validations['outliers'] = [(col, z_threshold) for col in selected_cols_outliers]
    
    st.markdown("---")
    
    # Botão de executar validações
    if st.button("🚀 Executar Validações", type="primary", use_container_width=True):
        execute_validations(table_name, validations)


def execute_validations(table_name, validations):
    """Executa as validações configuradas"""
    with st.spinner("🔄 Executando validações..."):
        validator = DataValidator(st.session_state.data, table_name)
        
        # Validações de nulos
        for col, threshold in validations['not_null']:
            validator.expect_column_values_to_not_be_null(col, threshold=threshold)
        
        # Validações de intervalo
        for col, min_val, max_val in validations['range']:
            validator.expect_column_values_to_be_between(col, min_val, max_val)
        
        # Validações de unicidade
        for col in validations['unique']:
            validator.expect_column_values_to_be_unique(col)
        
        # Detecção de outliers
        for col, threshold in validations['outliers']:
            validator.detect_outliers_zscore(col, threshold=threshold)
        
        st.session_state.validator = validator
        st.session_state.validation_done = True
        
        st.success("✅ Validações concluídas!")
        st.rerun()


def display_validation_results():
    """Exibe os resultados das validações"""
    if not st.session_state.validation_done or st.session_state.validator is None:
        return
    
    validator = st.session_state.validator
    summary = validator.get_summary()
    
    st.markdown("## 📊 Resultados da Validação")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Verificações",
            summary['total_checks'],
            delta=None
        )
    
    with col2:
        st.metric(
            "Aprovadas",
            summary['passed'],
            delta=f"+{summary['passed']}"
        )
    
    with col3:
        st.metric(
            "Falharam",
            summary['failed'],
            delta=f"-{summary['failed']}" if summary['failed'] > 0 else None,
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Taxa de Sucesso",
            f"{summary['success_rate']}%",
            delta=f"{summary['success_rate'] - 100:.1f}%"
        )
    
    # Gauge de qualidade
    col1, col2 = st.columns(2)
    
    with col1:
        fig_gauge = create_gauge_chart(summary['success_rate'], "Taxa de Qualidade")
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Gráfico de pizza
        fig_pie = px.pie(
            values=[summary['passed'], summary['failed']],
            names=['Aprovadas', 'Falharam'],
            title="Distribuição dos Resultados",
            color_discrete_sequence=['#00cc96', '#ef553b']
        )
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Status geral
    if summary['failed'] == 0:
        st.success(f"### {summary['overall_status']}")
    else:
        st.error(f"### {summary['overall_status']}")
    
    # Detalhes das validações
    st.markdown("### 📋 Detalhes das Validações")
    
    # Separar por status
    passed_results = [r for r in validator.results if r.passed]
    failed_results = [r for r in validator.results if not r.passed]
    
    tab1, tab2 = st.tabs([f"✅ Aprovadas ({len(passed_results)})", f"❌ Falharam ({len(failed_results)})"])
    
    with tab1:
        if passed_results:
            for result in passed_results:
                with st.expander(f"✅ {result.check_name}"):
                    st.write(f"**Status:** {result.status}")
                    st.write(f"**Detalhes:** {result.details}")
                    st.write(f"**Severidade:** {result.severity}")
                    if result.metadata:
                        st.json(result.metadata)
        else:
            st.info("Nenhuma validação aprovada.")
    
    with tab2:
        if failed_results:
            for result in failed_results:
                with st.expander(f"❌ {result.check_name}", expanded=True):
                    st.write(f"**Status:** {result.status}")
                    st.write(f"**Detalhes:** {result.details}")
                    st.write(f"**Severidade:** {result.severity}")
                    if result.metadata:
                        st.json(result.metadata)
        else:
            st.success("🎉 Nenhuma validação falhou!")
    
    # Exportar relatório
    st.markdown("### 📥 Exportar Resultados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Exportar como JSON
        report_json = {
            'summary': summary,
            'results': [r.to_dict() for r in validator.results]
        }
        
        st.download_button(
            label="📄 Baixar Relatório JSON",
            data=json.dumps(report_json, indent=2, default=str),
            file_name=f"relatorio_validacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # Exportar como CSV
        results_df = pd.DataFrame([{
            'Check': r.check_name,
            'Status': r.status,
            'Passou': r.passed,
            'Detalhes': r.details,
            'Severidade': r.severity,
            'Timestamp': r.timestamp
        } for r in validator.results])
        
        st.download_button(
            label="📊 Baixar Resultados CSV",
            data=results_df.to_csv(index=False).encode('utf-8'),
            file_name=f"resultados_validacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


def main():
    """Função principal da aplicação"""
    # Navegação
    if st.session_state.page == 'home':
        landing_page()
    else:
        application_page()


def application_page():
    """Página da aplicação de validação"""
    initialize_session_state()
    
    # Header com botão de voltar
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown('<div class="main-header">🛡️ DataSentinel - Validação de Qualidade de Dados</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar
    data_source = sidebar_configuration()
    
    # Conteúdo principal
    if st.session_state.data is not None:
        # Preview dos dados
        display_data_preview()
        
        st.markdown("---")
        
        # Se já executou validações, mostra resultados
        if st.session_state.validation_done:
            display_validation_results()
            
            # Botão para nova validação
            if st.button("🔄 Nova Validação"):
                st.session_state.validation_done = False
                st.session_state.validator = None
                st.rerun()
        else:
            # Configuração de validações
            validation_configuration()
    
    else:
        # Tela inicial
        st.info("👈 Configure a fonte de dados na barra lateral e carregue os dados para começar!")
        
        # Cards de features
        st.markdown("### ✨ Recursos do DataSentinel")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="success-card">
                <h3>🎭 Dados Simulados</h3>
                <p>Teste sem necessidade de banco de dados real</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="success-card">
                <h3>📊 Validações Flexíveis</h3>
                <p>Múltiplas validações de qualidade de dados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="success-card">
                <h3>📈 Visualizações</h3>
                <p>Gráficos interativos e relatórios detalhados</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "DataSentinel © 2026 | Validação de Qualidade de Dados"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
