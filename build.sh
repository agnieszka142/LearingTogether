#!/usr/bin/env bash
# exit on error
set -o errexit

pip install poetry
pip install django
pip install dj_database_url
pip install whitenoise
pip install psycopg2

poetry add gunicorn

python manage.py collectstatic --no-input
python manage.py migrate