# Generated by Django 3.2.8 on 2021-10-31 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_shops'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shop',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.shops'),
        ),
    ]
