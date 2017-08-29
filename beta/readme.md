## VisionMarker

This verison is designed specifically for vehicle labelling.

## Install
```
git clone https://github.com/wasit7/visionmarker.git
pip install django-extensions
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Dataset Preparation
  1. create MyUser in the Django Admin
  2. copy all images into /static/raw and then start Jupyter using notebook.bat, the import script is the main project directory (load_dataset.ipynb).

## Run Server
```
python manage.py runserver
```
