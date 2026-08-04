web: gunicorn chatapp.wsgi:application --bind 0.0.0.0:$PORT
web: python manage.py migrate && gunicorn chatapp.wsgi:application --bind 0.0.0.0:$PORT