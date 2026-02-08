# Decisões Técnicas e Melhorias

Este documento detalha as escolhas técnicas, desafios e propostas de melhoria para o projeto **API de Consultas Médicas**.

## 🛠️ Decisões Técnicas

### 1. Python + Django + DRF
Escolhemos o Django devido à sua robustez e ao princípio "batteries included". O Django REST Framework (DRF) foi utilizado para agilizar a criação da API RESTful, garantindo serialização eficiente e autenticação robusta.

### 2. PostgreSQL
Utilizado como banco de dados relacional para garantir a integridade dos dados e suporte nativo a tipos complexos, atendendo aos padrões de produção.

### 3. JWT (JSON Web Token)
Implementado via `djangorestframework-simplejwt` para garantir um controle de autenticação seguro e stateless, facilitando a escalabilidade.

### 4. Docker & Docker Compose
A containerização foi aplicada para garantir que o ambiente de desenvolvimento seja idêntico ao de produção, facilitando o setup para novos desenvolvedores e o deploy.

### 5. drf-spectacular
Utilizado para auto-geração da documentação Swagger/OpenAPI, permitindo que a API seja facilmente testada e compreendida por outras equipes.

## 🛡️ Segurança

- **SQL Injection**: Proteção nativa através do Django ORM, que utiliza consultas parametrizadas.
- **Sanitização de Dados**: Validada rigorosamente através dos Serializers do DRF.
- **CORS**: Configurado via `django-cors-headers` para permitir apenas origens autorizadas em produção.
- **Logs**: Middleware customizado registra cada acesso à API (IP, Usuário, Path, Status), garantindo rastreabilidade.

## 🚀 Melhorias Propostas e Desafios

### Desafios Encontrados
- **Configuração de Ambientes**: A separação de `settings` para local, staging e produção exigiu uma estrutura modular para evitar duplicação de código.
- **Mock da Asaas**: Simular um fluxo de split de pagamentos exigiu uma abstração via `Service Layer` para manter a lógica de negócio separada das Views.

### Melhorias Futuras
- **Testes de Integração com Asaas**: Implementar uma sandbox real da Asaas.
- **Cache**: Utilizar Redis para cache de listagens de profissionais que não mudam com frequência.
- **Monitoramento**: Integrar com Sentry para rastreamento de erros em tempo real e Prometheus/Grafana para métricas.

## 🔄 Fluxo de Rollback

Em um ambiente AWS (App Runner/ECS), o rollback é facilitado:
1. **GitHub Actions Revert**: Ao reverter um commit, a pipeline gera uma nova imagem baseada no código estável.
2. **Blue/Green**: O tráfego só é direcionado para a nova versão após health checks passarem. Em caso de erro, o AWS App Runner mantém a versão anterior ativa, permitindo um rollback instantâneo se a nova versão falhar no runtime.
