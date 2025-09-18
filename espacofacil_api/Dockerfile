# 1. Imagem base
FROM python:3.11-slim

# 2. Variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Define o diretório de trabalho
WORKDIR /app

# 4. Copia e instala as dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copia todo o código do projeto
COPY . .

# 6. Executa os comandos de build DENTRO da imagem
#    Isso garante que as tabelas sejam criadas durante o build.
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

# 7. Expõe a porta que o Gunicorn vai usar
EXPOSE 8000

# 8. Define o comando para iniciar o servidor em produção
#    Substitua 'espacofacil_api' pelo nome do seu projeto (a pasta com o wsgi.py)
CMD ["gunicorn", "espacofacil_api.wsgi:application", "--bind", "0.0.0.0:8000"]