# Generated by Django 3.0.12 on 2021-06-10 10:55

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('targetInterval', models.DurationField(blank=True, default=datetime.timedelta(days=7))),
                ('nextDoDate', models.DateTimeField(blank=True, null=True)),
                ('meanInterval', models.DurationField(blank=True, default=datetime.timedelta(days=7), null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback',
                 models.CharField(choices=[('DONE', 'Done'), ('LATER', 'Later')], default='DONE', max_length=10)),
                ('date', models.DateTimeField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits_trainer.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskDone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done_date', models.DateTimeField(null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits_trainer.Task')),
            ],
        ),
    ]
