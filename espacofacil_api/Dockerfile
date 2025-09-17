# Use a mesma base que você já tem
FROM python:3.11-slim

# Define variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o resto do código do projeto para o contêiner
COPY . .

# Coleta os arquivos estáticos para serem servidos pelo WhiteNoise
# O --no-input evita prompts interativos durante o build
RUN python manage.py collectstatic --no-input

# Expõe a porta que o Gunicorn irá usar
EXPOSE 8000

# Comando para iniciar o servidor Gunicorn
# Substitua 'espacofacil_api' pelo nome do seu projeto (a pasta que contém o wsgi.py)
CMD ["gunicorn", "espacofacil_api.wsgi:application", "--bind", "0.0.0.0:8000"]