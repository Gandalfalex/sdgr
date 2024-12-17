#!/bin/bash
# this might need to be updated for shell...
# Start the Daphne server
#exec daphne djangoProject.asgi:application -u /tmp/daphne.sock --bind 0.0.0.0:8000

#python manage.py runserver
ls -l /usr/src/app/entrypoint.sh

daphne -b 0.0.0.0 -p 8000 djangoProject.asgi:application