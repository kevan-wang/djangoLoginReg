from django.conf.urls import url
from . import views           # This line is new!


urlpatterns = [
	url(r'^$', views.index),	# This line has changed! Notice that urlpatterns is a list, the comma is in anticipation of all the routes that will be coming soon
	url(r'^dashboard$', views.dashboard),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^wish_items/(?P<id>\d+)/$', views.showItem),	
	url(r'^wish_items/create$', views.create),
	url(r'^create_item$', views.createItem),
	url(r'^add_wish$', views.addWish),
	url(r'^remove$', views.remove),
	url(r'^delete$', views.delete)
	
]


# /{{number}}/delete - Have this be handled by a method named 'destroy'. For now, have this url redirect to /. 
