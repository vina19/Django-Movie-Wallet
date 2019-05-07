from django.contrib import admin
from .models import SGMovies

class SGMoviesModelAdmin(admin.ModelAdmin):
	list_display = ["title", "release_date"]
	list_display_links = ["title"]
	list_filter = ["release_date"]
	search_fields = ["title", "description"]
	class Meta:
		model = SGMovies

admin.site.register(SGMovies, SGMoviesModelAdmin)
