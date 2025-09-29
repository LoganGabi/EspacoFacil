#!/bin/sh
python manage.py migrate
python manage.py collectstatic --no-input
exec "$@"

# caso não esteja sendo encontrado durante up build, execulte no GIT BASH: dos2unix entrypoint.sh