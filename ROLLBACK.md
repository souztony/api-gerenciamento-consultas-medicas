# Estratégia de Rollback - API Lacrei Saúde

## Visão Geral

Este documento descreve as estratégias de rollback para a API de Consultas Médicas em diferentes cenários de falha.

## 1. Rollback de Aplicação (Docker/ECR)

### Identificar Versões Disponíveis

```bash
# Listar todas as imagens no ECR
aws ecr describe-images \
  --repository-name lacrei-saude-backend \
  --query 'imageDetails[*].[imageTags[0],imagePushedAt]' \
  --output table
```

### Rollback Manual

```bash
# 1. Identificar o SHA da versão estável anterior
# 2. Atualizar o serviço App Runner
aws apprunner update-service \
  --service-arn arn:aws:apprunner:us-east-1:ACCOUNT_ID:service/lacrei-saude-backend/SERVICE_ID \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/lacrei-saude-backend:PREVIOUS_SHA",
      "ImageConfiguration": {"Port": "8000"},
      "ImageRepositoryType": "ECR"
    }
  }'
```

### Rollback via Git

```bash
# Reverter o último commit problemático
git revert HEAD
git push origin main

# Ou reverter para um commit específico
git revert <commit-sha>
git push origin main

# O pipeline CI/CD irá automaticamente fazer o deploy da versão revertida
```

## 2. Rollback de Banco de Dados

### Listar Migrações

```bash
# Ver todas as migrações aplicadas
python manage.py showmigrations

# Ver migrações de um app específico
python manage.py showmigrations professionals
```

### Reverter Migração

```bash
# Reverter para uma migração específica
python manage.py migrate professionals 0001_initial

# Reverter todas as migrações de um app
python manage.py migrate professionals zero
```

### Backup e Restore

```bash
# Criar backup antes de mudanças críticas
pg_dump -h localhost -U postgres consultas_medicas > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar de backup
psql -h localhost -U postgres consultas_medicas < backup_20260209_120000.sql
```

## 3. Rollback de Configuração

### Variáveis de Ambiente

Se uma mudança de configuração causou problemas:

```bash
# 1. Identificar a configuração anterior no histórico do Git
git log -- .env.example

# 2. Restaurar as variáveis de ambiente no serviço
# AWS App Runner: atualizar via console ou CLI
# Docker Compose: editar docker-compose.prod.yml e redeployar
```

## 4. Procedimento de Emergência

### Checklist de Rollback Rápido

1. **Identificar o Problema**
   - [ ] Verificar logs da aplicação
   - [ ] Verificar métricas de erro
   - [ ] Identificar o deploy que causou o problema

2. **Comunicar**
   - [ ] Notificar a equipe
   - [ ] Atualizar status page (se houver)

3. **Executar Rollback**
   - [ ] Fazer rollback da aplicação (método mais rápido)
   - [ ] Verificar se o problema foi resolvido
   - [ ] Se necessário, fazer rollback do banco de dados

4. **Validar**
   - [ ] Testar endpoints críticos
   - [ ] Verificar logs
   - [ ] Confirmar que métricas voltaram ao normal

5. **Post-Mortem**
   - [ ] Documentar o incidente
   - [ ] Identificar causa raiz
   - [ ] Criar plano de prevenção

## 5. Testes de Rollback

### Ambiente de Staging

Sempre teste rollbacks em staging antes de precisar em produção:

```bash
# 1. Deploy de uma versão
git checkout v1.0.0
git push staging main

# 2. Deploy de uma nova versão
git checkout v1.1.0
git push staging main

# 3. Praticar rollback
git revert HEAD
git push staging main
```

## 6. Monitoramento Pós-Rollback

Após um rollback, monitore:

- Taxa de erro (deve voltar ao normal)
- Tempo de resposta
- Uso de recursos (CPU, memória)
- Logs de erro
- Feedback de usuários

## 7. Prevenção

Para minimizar a necessidade de rollbacks:

1. **Testes Abrangentes**
   - Cobertura de testes >90%
   - Testes de integração
   - Testes de carga

2. **Deploy Gradual**
   - Canary deployments
   - Blue-green deployments
   - Feature flags

3. **Monitoramento**
   - Alertas automáticos
   - Dashboards em tempo real
   - Logs centralizados

4. **Revisão de Código**
   - Pull requests obrigatórios
   - Aprovação de pelo menos 1 revisor
   - Checklist de segurança

## Contatos de Emergência

- **DevOps Lead**: [nome] - [email]
- **Backend Lead**: [nome] - [email]
- **On-Call**: [rotação]
