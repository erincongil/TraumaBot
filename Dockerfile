# 1. Usar una imagen base de Python con Debian, que es ligera y compatible.
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requisitos e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. (CRÍTICO) Instalar el navegador que zendriver necesita (ej. Chromium)
# Las versiones 'slim' de Python no traen estos paquetes.
RUN apt-get update && apt-get install -y \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar el código de la aplicación
COPY Worker.py .

# 6. Ejecutar la aplicación
# El CMD ejecuta tu script principal.
CMD ["python", "Worker.py"]