# Configuração de Banco de Dados em Nuvem

Este documento explica como configurar o banco de dados em nuvem para o projeto API de Consultas Médicas.

## Visão Geral

O projeto agora suporta configuração de banco de dados através de variáveis de ambiente, permitindo fácil migração entre ambientes locais e em nuvem.

## Pré-requisitos

1. Python 3.12+
2. Poetry instalado
3. Conta em um provedor de banco de dados em nuvem (AWS RDS, Google Cloud SQL, Azure, Supabase, Neon, Railway, etc.)

## Configuração Inicial

### 1. Instalar Dependências

```bash
poetry install --no-root
```

### 2. Criar Banco de Dados no Provedor de Nuvem

Escolha um dos provedores abaixo e siga as instruções específicas:

#### Supabase (Recomendado para começar)

1. Acesse [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Vá em **Settings** → **Database**
4. Copie as credenciais de conexão:
   - Host
   - Database name
   - User
   - Password
   - Port (geralmente 5432)

#### AWS RDS PostgreSQL

1. Acesse o console AWS RDS
2. Crie uma nova instância PostgreSQL
3. Configure security groups para permitir conexões
4. Anote o endpoint, porta, nome do banco, usuário e senha

#### Google Cloud SQL

1. Acesse o console do Google Cloud
2. Crie uma nova instância Cloud SQL PostgreSQL
3. Configure conexões autorizadas
4. Obtenha as credenciais de conexão

#### Neon

1. Acesse [neon.tech](https://neon.tech)
2. Crie um novo projeto
3. Copie a connection string fornecida
4. Extraia host, database, user, password e port

### 3. Configurar Variáveis de Ambiente

#### Para Desenvolvimento Local

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env.local
   ```

2. Edite `.env.local` com suas credenciais:
   ```env
   DJANGO_SETTINGS_MODULE=backend.core.settings.local
   SECRET_KEY=sua-chave-secreta-aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Credenciais do seu banco de dados em nuvem
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=nome_do_seu_banco
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_HOST=seu-host.provider.com
   DB_PORT=5432
   
   DB_CONN_MAX_AGE=0
   DB_SSL_REQUIRE=True
   ```

#### Para Staging

Crie `.env.staging` com configurações de homologação:
```env
DJANGO_SETTINGS_MODULE=backend.core.settings.staging
SECRET_KEY=chave-secreta-staging
DEBUG=False
ALLOWED_HOSTS=staging.seudominio.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=consultas_medicas_staging
DB_USER=staging_user
DB_PASSWORD=senha_staging
DB_HOST=staging-db.provider.com
DB_PORT=5432

DB_CONN_MAX_AGE=300
DB_SSL_REQUIRE=True

CORS_ALLOWED_ORIGINS=https://staging.seudominio.com
```

#### Para Produção

Crie `.env.production` com configurações de produção:
```env
DJANGO_SETTINGS_MODULE=backend.core.settings.production
SECRET_KEY=chave-secreta-producao-muito-segura
DEBUG=False
ALLOWED_HOSTS=api.seudominio.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=consultas_medicas_prod
DB_USER=prod_user
DB_PASSWORD=senha_producao_segura
DB_HOST=prod-db.provider.com
DB_PORT=5432

DB_CONN_MAX_AGE=600
DB_SSL_REQUIRE=True

CORS_ALLOWED_ORIGINS=https://seudominio.com,https://www.seudominio.com
```

## Executar Migrações

### Desenvolvimento Local

```bash
# Carregar variáveis de ambiente
$env:DJANGO_SETTINGS_MODULE="backend.core.settings.local"

# Verificar configuração
python manage.py check

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

### Staging/Production

```bash
# Para staging
$env:DJANGO_SETTINGS_MODULE="backend.core.settings.staging"

# Para production
$env:DJANGO_SETTINGS_MODULE="backend.core.settings.production"

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

## Configurações de SSL/TLS

### Quando usar SSL

- **Desenvolvimento Local**: `DB_SSL_REQUIRE=False` (se usando banco local)
- **Staging**: `DB_SSL_REQUIRE=True` (sempre)
- **Produção**: `DB_SSL_REQUIRE=True` (sempre)

### Provedores que requerem SSL

A maioria dos provedores de nuvem **requer** SSL:
- Supabase: Sim
- AWS RDS: Sim (recomendado)
- Google Cloud SQL: Sim
- Azure: Sim
- Neon: Sim

## Troubleshooting

### Erro: "FATAL: password authentication failed"

- Verifique se as credenciais em `.env.local` estão corretas
- Confirme que o usuário tem permissões no banco de dados

### Erro: "could not connect to server"

- Verifique se o host está correto
- Confirme que o firewall/security group permite conexões do seu IP
- Verifique se a porta está correta (geralmente 5432)

### Erro: "SSL connection required"

- Defina `DB_SSL_REQUIRE=True` no arquivo `.env`

### Erro: "relation does not exist"

- Execute as migrações: `python manage.py migrate`

### Erro ao carregar variáveis de ambiente

- Certifique-se de que `python-decouple` está instalado
- Verifique se o arquivo `.env.local` existe
- Confirme que `DJANGO_SETTINGS_MODULE` está definido

## Segurança

### ⚠️ IMPORTANTE

1. **NUNCA** commite arquivos `.env*` (exceto `.env.example`)
2. Use senhas fortes e únicas para cada ambiente
3. Rotacione credenciais regularmente
4. Use SSL/TLS em produção
5. Mantenha `DEBUG=False` em produção
6. Configure `ALLOWED_HOSTS` corretamente

### Gerando SECRET_KEY Segura

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Estrutura de Arquivos

```
api-consultas-medicas/
├── .env.example          # Template de variáveis de ambiente
├── .env.local            # Desenvolvimento (não commitado)
├── .env.staging          # Staging (não commitado)
├── .env.production       # Produção (não commitado)
├── backend/
│   └── core/
│       └── settings/
│           ├── base.py       # Configurações compartilhadas
│           ├── local.py      # Configurações de desenvolvimento
│           ├── staging.py    # Configurações de staging
│           └── production.py # Configurações de produção
└── manage.py
```

## Próximos Passos

1. Configure seu banco de dados no provedor de nuvem
2. Preencha o arquivo `.env.local` com as credenciais
3. Execute as migrações
4. Teste a conexão localmente
5. Configure CI/CD para deploy automático
