FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario sin privilegios
RUN useradd -m -d /home/appuser -s /bin/bash appuser

# Copiar e instalar requerimientos como root
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código y cambiar propiedad
COPY --chown=appuser:appuser . .

# Copiar y preparar el script de arranque
COPY --chown=appuser:appuser run.sh /run.sh
RUN chmod +x /run.sh

# Cambiar de usuario
USER appuser

# Comando de arranque
CMD run.sh
