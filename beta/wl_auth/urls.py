from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^signin/', views.signin, name='signin'),
	url(r'^signout/', views.signout, name='signout'),
	url(r'^change_password/', views.change_password, name='change_password'),
]