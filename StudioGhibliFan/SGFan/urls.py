from django.conf.urls import url
from django.contrib import admin
from .views import (
	movie_list,
	movie_create,
	movie_detail,
	movie_update,
    UserFormView,
	)

urlpatterns = [
    #login path
    url(r'^register/$', UserFormView, name='register'),

	# movie list path.
    url(r'^$', movie_list, name='list'),

    # creating movie path.
    url(r'^create/$', movie_create, name='create'),

    # movie detail path.
    url(r'^(?P<id>\d+)/$', movie_detail, name='detail'),
    
    # editing movie path.
   	url(r'^(?P<id>\d+)/edit/$', movie_update, name='update'),
]
