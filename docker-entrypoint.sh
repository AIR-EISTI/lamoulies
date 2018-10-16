#!/bin/sh

/venv/bin/python manage.py makemigrations polls
/venv/bin/python manage.py migrate

exec "$@"
