# Generated by Django 3.2.8 on 2021-11-02 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20211102_1226'),
        ('zayavki', '0008_rename_who_zayavka_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zayavka',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.category'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]