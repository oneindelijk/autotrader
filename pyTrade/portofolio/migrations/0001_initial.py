# Generated by Django 3.1.5 on 2021-01-16 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portofolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=200, verbose_name='Symbol')),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
