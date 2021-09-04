#!/bin/sh

if [ "$DEPLOYMENT_ARCHITECTURE" = "local" ]; then

  # Install dev requirements
  poetry export --without-hashes --dev | poetry run pip install -r /dev/stdin

fi

# Run migrations
python "$PWD"/manage.py migrate


# Run server
if [ "$DEPLOYMENT_ARCHITECTURE" = "local" ]; then

  python "$PWD"/manage.py runserver 0.0.0.0:8000

else

  daphne -b 0.0.0.0 -p 8000 src.server.asgi:application

fi

