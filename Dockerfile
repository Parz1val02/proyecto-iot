FROM python:3.9-slim

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set timezone (optional, for the container environment)
ENV TZ=America/Lima

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY ./main.py .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir fastapi uvicorn psycopg2 

# Exponer el puerto 8000 para la aplicación FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
