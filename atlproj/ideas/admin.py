from django.contrib import admin
from .models import Idea, Client, Pitch, Platform

# Register your models here.

admin.site.register(Idea)
admin.site.register(Pitch)
admin.site.register(Client)
admin.site.register(Platform)