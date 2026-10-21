# 1. Usar una computadora Linux con Python 3.10
FROM python:3.10-slim

# 2. Instalar el motor de SWI-Prolog en el sistema
RUN apt-get update && apt-get install -y swi-prolog

# 3. Copiar tu código al servidor
WORKDIR /app
COPY . .

# 4. Instalar las librerías de Python
RUN pip install flask pyswip gunicorn

# 5. Comando para encender tu aplicación web en la nube
CMD gunicorn app:app --bind 0.0.0.0:$PORT