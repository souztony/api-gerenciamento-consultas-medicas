# Usar a imagem oficial do Python como base
FROM python:3.12-slim

# Evitar que o Python gere arquivos .pyc e que o stdout/stderr fiquem em buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências do sistema necessárias para o psycopg2 e Poetry
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock* /app/

# Configurar o Poetry para não criar ambientes virtuais dentro do container
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copiar o restante do código do projeto
COPY . /app/

# Expor a porta que o Django usará
EXPOSE 8000

# Comando para rodar a aplicação (usando o servidor de desenvolvimento para simplificar, 
# mas em produção deve ser usado um Gunicorn/Uvicorn)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
