# Generated by Django 3.1.6 on 2021-02-08 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('interval', models.FloatField(default=7.0)),
            ],
        ),
        migrations.CreateModel(
            name='TaskCompleted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('behavior', models.CharField(choices=[('DONE', 'Done'), ('LATER', 'Later')], default='DONE', max_length=10)),
                ('doneDate', models.DateTimeField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits_trainer.task')),
            ],
        ),
    ]
