# Generated by Django 3.1.7 on 2021-11-23 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zayavki', '0004_delete_filters'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiltersOfZayavok',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30)),
                ('link', models.CharField(max_length=10)),
                ('status1', models.BooleanField(default=False)),
                ('status2', models.BooleanField(default=False)),
                ('status3', models.BooleanField(default=False)),
                ('status4', models.BooleanField(default=False)),
                ('status5', models.BooleanField(default=False)),
                ('status6', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Фильтр заявок',
                'verbose_name_plural': 'Фильтры заявок',
            },
        ),
        migrations.AlterField(
            model_name='zayavka',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
