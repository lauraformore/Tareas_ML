# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requisitos primero (para aprovechar la caché)
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto al contenedor
COPY app/ ./app/
COPY frontend/ ./frontend/

# Exponer el puerto 8000
EXPOSE 8000

# Comando para iniciar el servidor Uvicorn
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]