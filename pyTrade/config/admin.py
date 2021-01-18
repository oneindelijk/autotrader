from django.contrib import admin
from .models import SettingsPage, Setting, Parameter

# Register your models here.

admin.site.register(SettingsPage)
admin.site.register(Setting)
admin.site.register(Parameter)