from django.conf.urls import url
from . import views           # This line is new!


urlpatterns = [
	url(r'^$', views.index),	# This line has changed! Notice that urlpatterns is a list, the comma is in anticipation of all the routes that will be coming soon
	url(r'^success$', views.success),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout)
]


# /{{number}}/delete - Have this be handled by a method named 'destroy'. For now, have this url redirect to /. 
