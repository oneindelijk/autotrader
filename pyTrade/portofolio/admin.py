from django.contrib import admin

# Register your models here.

from .models import Portofolio,Balance,Operation,Company,StockData,Statistic


admin.site.register(Portofolio)
admin.site.register(Balance)
admin.site.register(Operation)
admin.site.register(Company)
admin.site.register(StockData)
admin.site.register(Statistic)
