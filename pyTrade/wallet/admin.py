from django.contrib import admin

# Register your models here.

from .models import Wallet, Currency, Operation

admin.site.register(Wallet)
admin.site.register(Currency)
admin.site.register(Operation)
