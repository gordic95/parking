#!/bin/sh

python manage.py migrate
#python manage.py create_admin --username=$ADMIN_LOGIN --email=$ADMIN_EMAIL --password=$ADMIN_PASSWORD --first_name=Admin --last_name=Adminov
#python manage.py loaddata sample
#python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
exec "$@"
