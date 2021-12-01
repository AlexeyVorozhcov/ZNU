# Generated by Django 3.2.8 on 2021-12-01 11:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='recipient',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
