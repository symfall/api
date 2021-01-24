#!/bin/sh

# Run migrations
python /code/symfall/manage.py migrate

python /code/symfall/manage.py test messenger
# Run server

python /code/symfall/manage.py runserver 0.0.0.0:8000
