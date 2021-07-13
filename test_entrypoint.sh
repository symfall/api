#!/bin/sh

# Run migrations
poetry install

# Run server
python manage.py test
