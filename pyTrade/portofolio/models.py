from django.db import models

# Create your models here.

class Portofolio(models.Model):

    owner = models.CharField('Symbol', max_length = 200)
    updated = models.DateTimeField(auto_now_add=True)