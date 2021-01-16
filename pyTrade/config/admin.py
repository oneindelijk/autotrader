from django.contrib import admin
from .models import SettingsPage, Setting

# Register your models here.

admin.site.register(SettingsPage)
admin.site.register(Setting)