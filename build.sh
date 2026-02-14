#!/bin/bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

python manage.py auto_createsuperuser --username ivantarsky --email tarsky2@example.com --password securepassword