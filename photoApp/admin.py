from django.contrib import admin
from .models import Profile, Photo, Tag
# Register your models here.
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(Profile)