# 🚀 Guia de Deploy - DataSentinel

Este guia cobre diferentes opções de deployment para o DataSentinel.

## 📋 Índice

- [Deploy Local](#-deploy-local)
- [Streamlit Cloud](#-streamlit-cloud)
- [Docker](#-docker)
- [Heroku](#-heroku)
- [AWS/Azure/GCP](#-cloud-providers)

---

## 🏠 Deploy Local

### Para Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/DataSentinel.git
cd DataSentinel

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run web_app.py
```

### Para Produção Local

```bash
# Instale dependências de produção
pip install -r requirements.txt --no-dev

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# Execute em modo headless
streamlit run web_app.py --server.headless=true
```

---

## ☁️ Streamlit Cloud

O Streamlit Cloud oferece deploy gratuito e fácil.

### Passo a Passo

1. **Prepare o Repositório**
   ```bash
   # Certifique-se de ter:
   # - requirements.txt
   # - web_app.py
   # - .streamlit/config.toml (opcional)
   ```

2. **Faça Push para GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud"
   git push origin main
   ```

3. **Deploy no Streamlit Cloud**
   - Acesse [share.streamlit.io](https://share.streamlit.io)
   - Conecte sua conta GitHub
   - Selecione o repositório DataSentinel
   - Escolha o arquivo principal: `web_app.py`
   - Clique em "Deploy"

4. **Configure Secrets (Opcional)**
   - No dashboard do Streamlit Cloud
   - Vá em "Settings" > "Secrets"
   - Adicione suas credenciais:
   ```toml
   [database]
   host = "seu-host"
   port = 5432
   database = "seu-db"
   user = "seu-usuario"
   password = "sua-senha"
   ```

### URL Customizada

Seu app ficará disponível em:
```
https://share.streamlit.io/seu-usuario/datasentinel/main/web_app.py
```

---

## 🐳 Docker

### Dockerfile

Crie um `Dockerfile` na raiz do projeto:

```dockerfile
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta do Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando para executar a aplicação
CMD ["streamlit", "run", "web_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  datasentinel:
    build: .
    container_name: datasentinel
    ports:
      - "8501:8501"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./app:/app/app
      - ./tests:/app/tests
    restart: unless-stopped
    networks:
      - datasentinel-network

  # PostgreSQL (opcional)
  postgres:
    image: postgres:15-alpine
    container_name: datasentinel-db
    environment:
      POSTGRES_DB: datasentinel
      POSTGRES_USER: sentinel_user
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - datasentinel-network

volumes:
  postgres_data:

networks:
  datasentinel-network:
    driver: bridge
```

### Comandos Docker

```bash
# Build da imagem
docker build -t datasentinel:latest .

# Run container
docker run -d -p 8501:8501 --name datasentinel datasentinel:latest

# Usando docker-compose
docker-compose up -d

# Ver logs
docker logs -f datasentinel

# Parar
docker-compose down
```

---

## 🔧 Heroku

### Preparação

1. **Crie `Procfile`**:
   ```
   web: streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Crie `runtime.txt`**:
   ```
   python-3.10.11
   ```

3. **Instale Heroku CLI**:
   ```bash
   # Windows (Chocolatey)
   choco install heroku-cli
   
   # Linux/Mac
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

### Deploy

```bash
# Login no Heroku
heroku login

# Crie um novo app
heroku create datasentinel-app

# Configure buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Abra a aplicação
heroku open

# Ver logs
heroku logs --tail
```

### Configurar Variáveis de Ambiente

```bash
heroku config:set DB_HOST=seu-host
heroku config:set DB_USER=seu-usuario
heroku config:set DB_PASSWORD=sua-senha
```

---

## ☁️ Cloud Providers

### AWS (Elastic Beanstalk)

```bash
# Instale EB CLI
pip install awsebcli

# Inicialize
eb init -p python-3.10 datasentinel

# Crie ambiente
eb create datasentinel-env

# Deploy
eb deploy

# Abra
eb open
```

### Azure (App Service)

```bash
# Instale Azure CLI
az login

# Crie resource group
az group create --name datasentinel-rg --location eastus

# Crie app service plan
az appservice plan create --name datasentinel-plan \
    --resource-group datasentinel-rg --sku B1

# Crie web app
az webapp create --name datasentinel \
    --resource-group datasentinel-rg \
    --plan datasentinel-plan --runtime "PYTHON|3.10"

# Deploy
az webapp up --name datasentinel
```

### Google Cloud (App Engine)

1. **Crie `app.yaml`**:
   ```yaml
   runtime: python310
   
   entrypoint: streamlit run web_app.py --server.port $PORT
   
   instance_class: F2
   
   automatic_scaling:
     target_cpu_utilization: 0.65
     min_instances: 1
     max_instances: 10
   ```

2. **Deploy**:
   ```bash
   # Autentique
   gcloud auth login
   
   # Configure projeto
   gcloud config set project seu-projeto-id
   
   # Deploy
   gcloud app deploy
   
   # Abra
   gcloud app browse
   ```

---

## 🔒 Segurança

### Variáveis de Ambiente

Nunca commite credenciais! Use variáveis de ambiente:

**`.env.example`**:
```env
# Banco de Dados
DB_HOST=localhost
DB_PORT=5432
DB_NAME=datasentinel
DB_USER=seu_usuario
DB_PASSWORD=sua_senha

# API Keys (se necessário)
API_KEY=sua_api_key
```

**No código**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
```

### HTTPS

Para produção, sempre use HTTPS:

- **Streamlit Cloud**: HTTPS automático
- **Heroku**: HTTPS automático
- **Outros**: Configure certificado SSL

---

## 📊 Monitoramento

### Logs

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('datasentinel.log'),
        logging.StreamHandler()
    ]
)
```

### Health Check

Adicione endpoint de health check:

```python
import requests

def check_health():
    try:
        response = requests.get('http://localhost:8501/_stcore/health')
        return response.status_code == 200
    except:
        return False
```

---

## 🚀 CI/CD

### GitHub Actions

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest tests/ -v
```

---

## 📝 Checklist de Deploy

- [ ] Testes passando localmente
- [ ] Requirements.txt atualizado
- [ ] Variáveis de ambiente configuradas
- [ ] Logs configurados
- [ ] Health check implementado
- [ ] Documentação atualizada
- [ ] README com instruções de deploy
- [ ] .gitignore configurado (não commitar .env)
- [ ] HTTPS habilitado
- [ ] Monitoramento configurado

---

## 🆘 Troubleshooting

### Erro: Module not found

```bash
# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

### Erro: Port already in use

```bash
# Mude a porta
streamlit run web_app.py --server.port=8502
```

### Erro de memória

```bash
# Aumente recursos do container/instância
# Ou otimize o código para usar menos memória
```

---

## 📞 Suporte

Para problemas de deploy, abra uma issue no GitHub com:
- Plataforma de deploy
- Logs de erro
- Steps para reproduzir

---

**Boa sorte com o deploy!** 🚀
