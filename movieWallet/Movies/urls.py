from django.conf.urls import url
from Movies import api
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    Detail_movie,
    Play_movie,
    Favorite,
    Watched,
    )

app_name='Movies'

urlpatterns = [
    #movies/<movie_id>
    url(r'^(?P<movie_id>\d+)/$', Detail_movie, name="detail_movie"),
    #movies/<movie_id>/play/
    url(r'^(?P<movie_id>\d+)/play/$', Play_movie, name="play"),
    #movies/<movie_id>/watched/
    url(r'^(?P<movie_id>\d+)/watched/$', Favorite, name="favorite"),
    #movies/<movie_id>/watched/
    url(r'^(?P<movie_id>\d+)/watched/stay=True$', Watched, name="watched"),
    #movies/api/name=<name>
    url(r'^api/name=(?P<name>[A-Z,a-z," ",""]+|)?&y=(?P<year>[0-9]+|)$',api.API_res,name="api"),
]
