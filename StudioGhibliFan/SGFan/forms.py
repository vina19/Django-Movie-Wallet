from django import forms
from .models import SGMovies
from django.contrib.auth.models import User

# form that we can fill out with data on a webpage 
# and it will save the data into database for us.
class SGMoviesForm(forms.ModelForm):
	class Meta:
		model = SGMovies
		fields = [
			"title",
			"image",
			"description",
			"director",
			"producer",
			"release_date",
		]

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			"username",
		 	"email", 
		 	"password",
		]
