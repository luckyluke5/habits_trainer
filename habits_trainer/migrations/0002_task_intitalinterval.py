# Generated by Django 3.1.6 on 2021-02-08 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits_trainer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='intitalInterval',
            field=models.FloatField(default=7.0, editable=False),
        ),
    ]
