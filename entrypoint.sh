#!/bin/sh

if [ "$DEPLOYMENT_ARCHITECTURE" = "local" ] || [ "$DEPLOYMENT_ARCHITECTURE" = "test" ]; then

  # Install dev requirements
  poetry export --without-hashes --dev | poetry run pip install -r /dev/stdin

fi

if [ "$DEPLOYMENT_ARCHITECTURE" = "test" ]; then

  coverage -m

fi


if [ "$DEPLOYMENT_ARCHITECTURE" = "local" ]; then

  # Run migrations
  python "$PWD"/manage.py migrate

  # Run server
  python "$PWD"/manage.py runserver 0.0.0.0:8000

fi

