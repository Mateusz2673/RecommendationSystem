#!/bin/bash

set -e

echo "Make migrations"
python manage.py makemigrations --noinput

echo "Apply database migrations"
python manage.py migrate --noinput

echo "Creating admin user"
python manage.py shell < create_superuser.py

echo "Starting server"
python manage.py runserver 0.0.0.0:8000