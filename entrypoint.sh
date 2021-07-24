#!/bin/sh

if [ $ENVIROMENT = "local" ]; then
# Install dev requirements
poetry export --without-hashes --dev | poetry run pip install -r /dev/stdin
fi

# Run migrations
python $PWD/manage.py migrate

# Run server
python $PWD/manage.py runserver 0.0.0.0:8000
