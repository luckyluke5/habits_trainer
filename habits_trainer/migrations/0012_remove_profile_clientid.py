# Generated by Django 3.0.12 on 2021-08-10 22:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('habits_trainer', '0011_profile_clientid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='clientID',
        ),
    ]
