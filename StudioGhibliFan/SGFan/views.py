from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from .models import SGMovies
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SGMoviesForm, UserForm
from django.views.generic import View
from django.contrib.auth import authenticate, login

# View inside the website
# define to create movie
def movie_create(request):
	form = SGMoviesForm(request.POST or None)

	# if all the form filled out with how it supposed to be then it will 
	# go to validation and it will save to the database.
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
		"form" : form
	}
	# returning to render request, movie form to be filled out page, and context of form.
	return render(request, "SGFan/movie_form.html", context)

# movie detail that return request and movie id.
def movie_detail(request, id=None):
	# instance equals to getting the object or show error 404 page from SGMovies by id.
	instance = get_object_or_404(SGMovies, id=id)
	context = {
		"title" : instance.title,
		"instance" : instance
	}
	# returning to render request, show the movie detail page, and context of title and instance.
	return render(request, "SGFan/movie_detail.html", context)
	 
# movie list
def movie_list(request):

	# queryset equals to get all the objects in SGMovies order by number id.
	queryset = SGMovies.objects.all().order_by("id")

	# search bar, if the title contains the query that the user type show the title.
	query = request.GET.get("q")
	if query:
		queryset = queryset.filter(title__icontains=query)

	context = {
		"object_list":queryset,
		"title" : "List"
	}
	# returning to render request, show the main page, and context of object_list and title.
	return render(request, "SGFan/main.html", context)

# update or edit the movie
def movie_update(request, id=None):

	instance = get_object_or_404(SGMovies, id=id)
	
	form = SGMoviesForm(request.POST or None, instance=instance)

	# if all the form filled out with how it supposed to be then it will 
	# go to validation and it will save to the database.
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title" : instance.title,
		"instance" : instance,
		"form" : form
	}
	# returning to render request, show the movie detail page, and context of title, instance, form.
	return render(request, "SGFan/movie_detail.html", context)

class UserFormView(View):
	form_class = UserForm
	template_name = 'SGFan/registration_form.html'

	# display a blank form for the user to sign up
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})
	
	# process form data to the database
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			# return user object if credentials are correct
			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('SGFan/movie_detail.html')

		# if they are not login it will return to the blank form
		return render(request, self.template_name, {'form': form})

		