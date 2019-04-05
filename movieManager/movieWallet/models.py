from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class userInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	password = models.CharField()
	email = models.CharField()
	movie_rating = models.CharField()
	movie_fav_list = models.CharField()
	movie_watched_list = models.CharField()
	

