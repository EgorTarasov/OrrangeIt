#!/usr/bin/env bash
cd /orrangeit_app/ || exit 1
python3 manage.py migrate
python3 manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8005 --access-log /var/log/orrangeit_app/daphne_access.log marketplace.asgi:application
