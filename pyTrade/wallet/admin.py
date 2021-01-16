from django.contrib import admin

# Register your models here.

from .models import Wallet, Currency, Operation, Balance

admin.site.register(Wallet)
admin.site.register(Currency)
admin.site.register(Operation) # Do not allow Operations to be manually altered because it won't reflect in the Wallets's balances
admin.site.register(Balance)
