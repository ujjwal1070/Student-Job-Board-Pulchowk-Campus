# Generated by Django 2.2 on 2019-05-11 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0002_auto_20190511_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='month',
        ),
        migrations.RemoveField(
            model_name='training',
            name='year',
        ),
    ]