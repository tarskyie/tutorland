release: python manage.py migrate
web: gunicorn newcubebackend.wsgi:application --bind 0.0.0.0:$PORT
