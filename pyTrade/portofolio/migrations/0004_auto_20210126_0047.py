# Generated by Django 3.1.5 on 2021-01-26 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portofolio', '0003_auto_20210126_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Industry'),
        ),
        migrations.AlterField(
            model_name='company',
            name='ipo_year',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='IPO Year'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='sector',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Sector'),
        ),
    ]