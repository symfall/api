#!/bin/sh

# Run migrations
python /code/src/manage.py migrate

# Run server
python /code/src/manage.py runserver 0.0.0.0:8000
