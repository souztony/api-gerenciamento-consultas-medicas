# API de Gerenciamento de Consultas Médicas - Lacrei Saúde

[![CI/CD Pipeline](https://github.com/souztony/api-consultas-medicas/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/souztony/api-consultas-medicas/actions/workflows/ci-cd.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Django 6.0](https://img.shields.io/badge/django-6.0-green.svg)](https://www.djangoproject.com/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

API REST para gerenciamento de profissionais de saúde e consultas médicas, desenvolvida com foco em inclusão e segurança de dados sensíveis.

## 📋 Índice

- [Características](#-características)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
  - [Setup Local](#setup-local)
  - [Setup com Docker](#setup-com-docker)
- [Executando Testes](#-executando-testes)
- [Documentação da API](#-documentação-da-api)
- [CI/CD](#-cicd)
- [Estratégia de Rollback](#-estratégia-de-rollback)
- [Segurança](#-segurança)
- [Arquitetura](#-arquitetura)

## ✨ Características

- ✅ **Autenticação JWT** com tokens rotativos e expiração configurável
- ✅ **Validação robusta** de dados com sanitização contra XSS
- ✅ **Testes automatizados** com cobertura >90% usando APITestCase
- ✅ **Dockerização completa** para desenvolvimento e produção
- ✅ **Pipeline CI/CD** com lint, testes, segurança e deploy automatizado
- ✅ **Documentação interativa** com Swagger e ReDoc
- ✅ **CORS configurável** por ambiente
- ✅ **Logging estruturado** de todas as requisições

## 🛠 Tecnologias

- **Backend**: Django 6.0 + Django REST Framework 3.16
- **Autenticação**: JWT (djangorestframework-simplejwt)
- **Banco de Dados**: PostgreSQL 16
- **Servidor WSGI**: Gunicorn
- **Containerização**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Testes**: pytest + pytest-django + pytest-cov
- **Linting**: Ruff
- **Documentação**: drf-spectacular (OpenAPI 3.0)

## 📦 Pré-requisitos

### Para execução local:
- Python 3.12+
- Poetry 1.7+
- PostgreSQL 16+ (ou SQLite para desenvolvimento rápido)

### Para execução com Docker:
- Docker 24+
- Docker Compose 2.20+

## 🚀 Instalação e Configuração

### Setup Local

1. **Clone o repositório**
```bash
git clone https://github.com/souztony/api-consultas-medicas.git
cd api-consultas-medicas
```

2. **Instale as dependências com Poetry**
```bash
poetry install
```

3. **Configure as variáveis de ambiente**

Copie o arquivo de exemplo e ajuste conforme necessário:
```bash
cp .env.example .env
```

Variáveis principais:
```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=consultas_medicas
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

4. **Execute as migrações**
```bash
poetry run python manage.py migrate
```

5. **Crie um superusuário (opcional)**
```bash
poetry run python manage.py createsuperuser
```

6. **Inicie o servidor de desenvolvimento**
```bash
poetry run python manage.py runserver
```

A API estará disponível em `http://localhost:8000`

### Setup com Docker

#### Desenvolvimento

```bash
# Subir os containers
docker-compose up --build

# A API estará disponível em http://localhost:8000
# O PostgreSQL estará em localhost:5432
```

#### Produção

```bash
# Usar o arquivo de produção
docker-compose -f docker-compose.prod.yml up --build

# Ou com variáveis de ambiente customizadas
SECRET_KEY=your-secret-key docker-compose -f docker-compose.prod.yml up -d
```

**Importante**: Em produção, sempre defina:
- `SECRET_KEY` (chave única e segura)
- `DEBUG=False`
- `CORS_ALLOW_ALL_ORIGINS=False`
- `CORS_ALLOWED_ORIGINS` (apenas origens confiáveis)

## 🧪 Executando Testes

### Testes Unitários e de Integração

```bash
# Executar todos os testes
poetry run pytest

# Com verbosidade
poetry run pytest -v

# Com cobertura
poetry run pytest --cov=apps --cov-report=term --cov-report=html

# Executar testes específicos
poetry run pytest apps/professionals/tests.py
poetry run pytest apps/appointments/tests.py
```

### Cobertura de Testes

Após executar os testes com cobertura, abra o relatório HTML:
```bash
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

### Linting

```bash
# Verificar código
poetry run ruff check .

# Corrigir automaticamente
poetry run ruff check --fix .

# Verificar formatação
poetry run ruff format --check .

# Formatar código
poetry run ruff format .
```

## 📚 Documentação da API

A API possui documentação interativa disponível em:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **Schema OpenAPI**: `http://localhost:8000/api/schema/`

### Autenticação

1. **Obter token JWT**:
```bash
POST /api/token/
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

Resposta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

2. **Usar o token nas requisições**:
```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

3. **Renovar token**:
```bash
POST /api/token/refresh/
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Endpoints Principais

#### Profissionais
- `GET /api/professionals/` - Listar profissionais
- `POST /api/professionals/` - Criar profissional
- `GET /api/professionals/{id}/` - Detalhes do profissional
- `PUT /api/professionals/{id}/` - Atualizar profissional
- `DELETE /api/professionals/{id}/` - Deletar profissional

#### Consultas
- `GET /api/appointments/` - Listar consultas
- `POST /api/appointments/` - Criar consulta
- `GET /api/appointments/{id}/` - Detalhes da consulta
- `PATCH /api/appointments/{id}/` - Atualizar consulta
- `DELETE /api/appointments/{id}/` - Deletar consulta

## 🔄 CI/CD

O projeto utiliza GitHub Actions para automação completa do ciclo de desenvolvimento.

### Pipeline

O pipeline é executado em **push** e **pull requests** para as branches `main` e `staging`:

1. **Lint** (Ruff)
   - Verificação de estilo de código
   - Verificação de formatação

2. **Tests**
   - Execução de testes unitários e de integração
   - Geração de relatório de cobertura
   - Upload para Codecov

3. **Security**
   - Verificação de vulnerabilidades com Safety
   - Análise de dependências

4. **Build**
   - Build da imagem Docker
   - Teste da imagem

5. **Deploy** (apenas em push para main/staging)
   - Login no Amazon ECR
   - Push da imagem para ECR
   - Tag da versão deployada
   - Deploy automático (quando configurado)

### Configuração de Secrets

Para o deploy funcionar, configure os seguintes secrets no GitHub:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_APP_RUNNER_ARN_PROD` (opcional)
- `AWS_APP_RUNNER_ARN_STAGING` (opcional)

## 🔙 Estratégia de Rollback

### Rollback Manual (Recomendado)

Cada deploy cria uma tag com o SHA do commit no ECR. Para fazer rollback:

1. **Identificar a versão anterior**:
```bash
# Listar imagens no ECR
aws ecr describe-images --repository-name lacrei-saude-backend --query 'imageDetails[*].[imageTags[0],imagePushedAt]' --output table
```

2. **Fazer rollback para uma versão específica**:
```bash
# Atualizar o serviço com a imagem anterior
aws apprunner update-service \
  --service-arn <SERVICE_ARN> \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "<ECR_REGISTRY>/lacrei-saude-backend:<SHA_ANTERIOR>",
      "ImageConfiguration": {"Port": "8000"},
      "ImageRepositoryType": "ECR"
    }
  }'
```

### Rollback via Git

```bash
# Reverter o último commit
git revert HEAD

# Ou reverter para um commit específico
git revert <commit-sha>

# Push para disparar novo deploy
git push origin main
```

### Rollback de Banco de Dados

Para migrações de banco de dados:

```bash
# Listar migrações
poetry run python manage.py showmigrations

# Reverter para uma migração específica
poetry run python manage.py migrate <app_name> <migration_name>
```

**Importante**: Sempre teste rollbacks em staging antes de aplicar em produção.

## 🔒 Segurança

### Práticas Implementadas

1. **Autenticação JWT**
   - Tokens com expiração de 60 minutos
   - Refresh tokens rotativos
   - Blacklist de tokens após rotação

2. **Validação de Dados**
   - Sanitização de inputs
   - Validação de email e telefone
   - Validação de datas (consultas apenas no futuro)
   - Limites de tamanho de campos

3. **CORS**
   - Configuração restritiva por padrão
   - Whitelist de origens permitidas

4. **Docker**
   - Execução como usuário não-root
   - Multi-stage build para imagens menores
   - Healthchecks configurados

5. **Logging**
   - Registro de todas as requisições
   - IP do cliente e usuário autenticado
   - Tempo de resposta

### Recomendações Adicionais

- Sempre use HTTPS em produção
- Configure rate limiting (ex: django-ratelimit)
- Implemente monitoramento (ex: Sentry)
- Faça backups regulares do banco de dados
- Mantenha dependências atualizadas

## 🏗 Arquitetura

```
api-consultas-medicas/
├── apps/
│   ├── accounts/          # Autenticação e usuários
│   ├── professionals/     # Profissionais de saúde
│   └── appointments/      # Consultas médicas
├── backend/
│   └── core/
│       ├── settings/      # Configurações por ambiente
│       │   ├── base.py
│       │   ├── local.py
│       │   ├── staging.py
│       │   └── production.py
│       ├── middleware.py  # Middlewares customizados
│       ├── urls.py
│       └── wsgi.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # Pipeline CI/CD
├── docker-compose.yml     # Desenvolvimento
├── docker-compose.prod.yml # Produção
├── Dockerfile
├── pyproject.toml
└── README.md
```

### Configurações por Ambiente

- **local.py**: Desenvolvimento local (DEBUG=True, SQLite opcional)
- **staging.py**: Ambiente de homologação
- **production.py**: Produção (DEBUG=False, segurança máxima)

## 📄 Licença

Este projeto está sob a licença MIT.

## 👥 Contato

**Desenvolvedor**: Tony Souza  
**Email**: [seu-email]  
**LinkedIn**: [seu-linkedin]

---

Desenvolvido com ❤️ para a Lacrei Saúde
