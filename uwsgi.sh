#!/bin/sh

uwsgi --chdir=/home/pi/chya \
    --module=chya.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=chya.settings \
    --env LANG='zh_CN.UTF-8' \
    --master  --pidfile=/var/django-chya.pid \
    --socket=127.0.0.1:9000 \
    --processes=1 \
    --uid=1000  --gid=2000 \
    --harakiri=20 \
    --max-requests=50 \
    --vacuum \
    --daemonize=/var/log/uwsgi/django-chya.log

