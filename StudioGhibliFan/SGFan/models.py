from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

#Put what data we want in database
#class SGMovies inherit from models.Model
class SGMovies(models.Model):
	title = models.CharField(max_length = 100)
	image = models.FileField(default='default.jpg', upload_to='profile_pics')
	description = models.CharField(max_length=5000)
	director = models.CharField(max_length = 100)
	producer = models.CharField(max_length = 100)
	release_date = models.IntegerField(default = 0)
	likes = models.ManyToManyField(User, related_name='likes', blank=True)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("detail", kwargs={"id": self.id})
