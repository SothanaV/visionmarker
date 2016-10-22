## VisionMarker

This verison is designed specifically for vehicle labelling.

## Install
```
git clone https://github.com/wasit7/visionmarker.git
pipinstal django-extensions
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Dataset Preparation
  copy all images into /raw and then start Jupyter using notebook.bat, the import script is the main project directory.

## Run Server
```
python manage.py runserver
```
