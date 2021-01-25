#!/bin/sh

# Run migrations
python /code/symfall/manage.py migrate

# Run server
python /code/symfall/manage.py runserver 0.0.0.0:8000
