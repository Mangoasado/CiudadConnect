#!/bin/bash
set -o errexit

pip install -r requirements.txt
cd CiudadConnect
python manage.py collectstatic --no-input
python manage.py migrate
