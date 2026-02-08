# API de Consultas Médicas

API RESTful desenvolvida com o objetivo de facilitar o gerenciamento de profissionais e consultas médicas, promovendo a inclusão e acessibilidade.

## 🚀 Tecnologias Utilizadas

- **Python 3.12+**
- **Django & Django REST Framework**
- **Poetry** (Gerenciamento de dependências)
- **PostgreSQL** (Banco de dados)
- **Docker & Docker Compose** (Containerização)
- **GitHub Actions** (CI/CD)
- **drf-spectacular** (Documentação Swagger/OpenAPI)

---

## 🛠️ Configuração do Ambiente

### Local (com Poetry)

1. **Instale o Poetry** (se não tiver):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. **Instale as dependências**:
   ```bash
   poetry install
   ```
3. **Configure as variáveis de ambiente**:
   Crie um arquivo `.env` baseado no `.env.example`.
4. **Rode as migrações**:
   ```bash
   poetry run python manage.py migrate
   ```
5. **Inicie o servidor**:
   ```bash
   poetry run python manage.py runserver
   ```

### Docker (Recomendado)

Inicie toda a infraestrutura (API + Banco de Dados) com um comando:
```bash
docker-compose up --build
```
A API estará disponível em `http://localhost:8000`.

---

## 🧪 Testes Automatizados

Os testes foram desenvolvidos utilizando o `APITestCase` do Django.

Para rodar os testes localmente:
```bash
poetry run python manage.py test
```
Via Docker:
```bash
docker-compose exec web python manage.py test
```

---

---

## 📖 Documentação da API (Swagger)

A documentação interativa está disponível nos seguintes endpoints:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **Redoc**: `http://localhost:8000/api/redoc/`

Para detalhes sobre decisões técnicas, desafios e melhoria de arquitetura, consulte o [DECISIONS.md](file:///c:/Users/tonys/OneDrive/Área de Trabalho/api-consultas-medicas/DECISIONS.md).

---

## ⚙️ CI/CD e Deploy

A pipeline do GitHub Actions (.github/workflows/ci-cd.yml) automatiza o fluxo:
1. **Lint**: Verificação de qualidade de código com `ruff`.
2. **Testes**: Execução dos testes automatizados.
3. **Build**: Criação da imagem Docker e push para o Amazon ECR.
4. **Deploy**: Configurado para AWS App Runner via GitHub Actions.
   > [!NOTE]
   > O step de deploy final (`aws apprunner update-service`) está comentado no arquivo `ci-cd.yml` para evitar falha por falta de credenciais AWS em repositórios pessoais, mas a lógica de build e tag de imagem está 100% pronta.

### Estratégia de Rollback 🔄

Propomos a utilização de **Blue/Green Deployment** via AWS App Runner.
Em caso de falha:
1. **Reverter Commit**: O pipeline detecta o revert e faz o push da imagem estável anterior.
2. **Health Checks**: O AWS App Runner mantém a versão anterior ativa até que os novos containers estejam saudáveis.

---

## 🛡️ Segurança e Logs

1. **Autenticação**: Foi implementado JWT para todas as rotas da API. Use `/api/token/` para obter as credenciais.
2. **Middleware de Logs**: Todas as requisições são logadas contendo IP, usuário, método e path.
3. **Segurança de Dados**: 
   - **SQL Injection**: Proteção nativa garantida pelo uso do Django ORM.
   - **Sanitização**: Implementada via Serializers do DRF para todos os inputs.
   - **CORS**: Configurado para aceitar apenas domínios autorizados.

---

## 💳 Integração Assas (Mock)

A API conta com um serviço de mock (`AsaasService`) que demonstra o fluxo de split de pagamento entre o profissional e a Lacrei Saúde.

---

*Desenvolvido por Tony Souza*
