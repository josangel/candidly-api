# Usa una imagen base liviana con Python
FROM python:3.11-slim

# Evita archivos .pyc y logs innecesarios en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar y conectar
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry de forma global (versión fija para evitar futuros errores)
ENV POETRY_VERSION=2.1.2
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Desactiva creación de entornos virtuales (instala en sistema)
ENV POETRY_VIRTUALENVS_CREATE=false

# Copia los archivos de dependencias primero para aprovechar cache
COPY pyproject.toml poetry.lock* ./

# Instala dependencias del proyecto (main)
RUN poetry install --only main --no-interaction --no-ansi --no-root

# Copia el resto del código fuente
COPY . .

# Expone el puerto de FastAPI
EXPOSE 8000

# Comando por defecto al iniciar el contenedor (API)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
