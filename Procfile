release: cd CiudadConnect && python manage.py migrate
web: cd CiudadConnect && gunicorn CiudadConnect.wsgi:application --log-file - --workers 3 --timeout 60