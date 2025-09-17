#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- INICIANDO SCRIPT DE BUILD ---"

echo "--- Instalando dependências ---"
pip install -r requirements.txt
echo "--- Dependências instaladas ---"

# Adicionado apenas para diagnóstico
echo "--- Executando makemigrations (para diagnóstico) ---"
python manage.py makemigrations
echo "--- Makemigrations finalizado ---"


echo "--- Executando migrate ---"
python manage.py migrate
echo "--- Migrate finalizado ---"


echo "--- Executando collectstatic ---"
python manage.py collectstatic --no-input
echo "--- Collectstatic finalizado ---"


echo "--- SCRIPT DE BUILD CONCLUÍDO ---"