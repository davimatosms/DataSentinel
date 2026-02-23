# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o DataSentinel! Este documento fornece diretrizes para contribuições.

## 📋 Código de Conduta

Este projeto segue um Código de Conduta. Ao participar, você concorda em manter um ambiente respeitoso e acolhedor.

## 🚀 Como Contribuir

### 1. **Fork e Clone**

```bash
# Fork o projeto no GitHub
# Clone seu fork
git clone https://github.com/seu-usuario/DataSentinel.git
cd DataSentinel

# Adicione o repositório original como upstream
git remote add upstream https://github.com/original/DataSentinel.git
```

### 2. **Crie um Branch**

```bash
# Atualize sua main
git checkout main
git pull upstream main

# Crie um branch para sua feature
git checkout -b feature/minha-feature
```

### 3. **Faça suas Alterações**

- Escreva código claro e bem documentado
- Siga o estilo PEP 8
- Adicione/atualize testes quando necessário
- Atualize a documentação

### 4. **Teste suas Alterações**

```bash
# Execute os testes
pytest tests/ -v

# Verifique a cobertura
pytest tests/ --cov=app

# Execute o linter
flake8 app/ tests/

# Formate o código
black app/ tests/
```

### 5. **Commit e Push**

```bash
# Adicione suas alterações
git add .

# Commit com mensagem descritiva
git commit -m "feat: adiciona validação de email"

# Push para seu fork
git push origin feature/minha-feature
```

### 6. **Abra um Pull Request**

- Vá ao seu fork no GitHub
- Clique em "Pull Request"
- Descreva suas alterações claramente
- Referencie issues relacionadas

## 📝 Padrões de Commit

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança de código)
- `refactor`: Refatoração de código
- `test`: Adiciona/atualiza testes
- `chore`: Tarefas de manutenção

Exemplos:
```
feat: adiciona validação de formato de email
fix: corrige bug no cálculo de outliers
docs: atualiza README com novos exemplos
test: adiciona testes para CSVConnector
```

## 🧪 Escrevendo Testes

### Estrutura de Teste

```python
import pytest
from app.core.engine import DataValidator
import pandas as pd

def test_minha_feature():
    """Descrição clara do que está sendo testado"""
    # Arrange (preparar)
    df = pd.DataFrame({'col': [1, 2, 3]})
    validator = DataValidator(df, 'test')
    
    # Act (executar)
    result = validator.minha_feature()
    
    # Assert (verificar)
    assert result.passed == True
```

### Executando Testes

```bash
# Todos os testes
pytest tests/ -v

# Teste específico
pytest tests/test_engine.py::test_not_null_validation -v

# Com cobertura
pytest tests/ --cov=app --cov-report=html
```

## 📚 Documentação

### Docstrings

Use docstrings no formato Google:

```python
def minha_funcao(param1: str, param2: int) -> bool:
    """
    Descrição breve da função.
    
    Descrição mais detalhada se necessário.
    
    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2
    
    Returns:
        Descrição do retorno
    
    Raises:
        ValueError: Quando param2 é negativo
    
    Example:
        >>> minha_funcao("teste", 5)
        True
    """
    if param2 < 0:
        raise ValueError("param2 deve ser positivo")
    return True
```

## 🎨 Estilo de Código

### Python (PEP 8)

- Indentação: 4 espaços
- Linha máxima: 100 caracteres
- Use type hints quando possível
- Nomes descritivos para variáveis

```python
# Bom
def calculate_success_rate(passed: int, total: int) -> float:
    """Calcula taxa de sucesso em percentual"""
    if total == 0:
        return 0.0
    return (passed / total) * 100

# Evite
def calc(p, t):
    return (p/t)*100 if t else 0
```

### Formatação Automática

```bash
# Instale as ferramentas
pip install black flake8

# Formate o código
black app/ tests/

# Verifique estilo
flake8 app/ tests/
```

## 🐛 Reportando Bugs

### Antes de Reportar

- Verifique se o bug já foi reportado
- Tente reproduzir com a última versão
- Colete informações do ambiente

### Template de Bug Report

```markdown
**Descrição do Bug**
Descrição clara e concisa do problema.

**Para Reproduzir**
Passos para reproduzir:
1. Vá para '...'
2. Clique em '....'
3. Role até '....'
4. Veja o erro

**Comportamento Esperado**
O que você esperava que acontecesse.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
 - OS: [ex: Windows 10]
 - Python: [ex: 3.10.5]
 - Versão do DataSentinel: [ex: 1.0.0]

**Contexto Adicional**
Qualquer outra informação sobre o problema.
```

## 💡 Sugerindo Melhorias

### Template de Feature Request

```markdown
**Sua sugestão está relacionada a um problema?**
Descrição clara do problema. Ex: "Sempre fico frustrado quando..."

**Descreva a solução que você gostaria**
Descrição clara da solução desejada.

**Descreva alternativas consideradas**
Outras soluções ou features que você considerou.

**Contexto Adicional**
Qualquer outro contexto sobre a sugestão.
```

## 📦 Tipos de Contribuições

### Código

- Novas funcionalidades
- Correção de bugs
- Melhorias de performance
- Refatorações

### Documentação

- Melhoria do README
- Exemplos de uso
- Tutoriais
- API documentation

### Testes

- Novos casos de teste
- Melhoria de cobertura
- Testes de integração

### Design

- Interface web
- Visualizações
- UX improvements

## 🎯 Áreas que Precisam de Ajuda

- [ ] Implementação completa do PostgreSQLConnector
- [ ] Suporte a MySQL
- [ ] Validações customizadas
- [ ] Melhorias na interface web
- [ ] Mais exemplos e tutoriais
- [ ] Tradução da documentação
- [ ] Testes de performance

## ❓ Perguntas

Se tiver dúvidas sobre como contribuir:

1. Abra uma [Issue](https://github.com/seu-usuario/DataSentinel/issues)
2. Entre em contato via email
3. Participe das discussões

## 🙏 Reconhecimento

Todos os contribuidores serão reconhecidos:

- Adicionados ao AUTHORS.md
- Mencionados em release notes
- Badges de contribuidor

---

**Obrigado por contribuir com o DataSentinel!** 🎉
