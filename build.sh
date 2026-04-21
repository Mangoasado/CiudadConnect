#!/bin/bash
pip install -r requirements.txt
cd CiudadConnect
python manage.py migrate
python manage.py collectstatic --no-input
