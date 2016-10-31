#!/bin/sh

##source activate django3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell_plus --notebook
