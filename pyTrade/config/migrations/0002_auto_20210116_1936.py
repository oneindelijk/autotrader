# Generated by Django 3.1.5 on 2021-01-16 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='settingsComment',
            field=models.TextField(blank=True, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='settingsFloatValue',
            field=models.FloatField(blank=True, verbose_name='Float Value'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='settingsIntValue',
            field=models.IntegerField(blank=True, verbose_name='Integer Value'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='settingsValue',
            field=models.CharField(blank=True, max_length=512, verbose_name='Value'),
        ),
    ]
