from django.contrib import admin
from .models import Collection, Movie, User
# Register your models here.
admin.site.register(Collection)
admin.site.register(Movie)
admin.site.register(User)
