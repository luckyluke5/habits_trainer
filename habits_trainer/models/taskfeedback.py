from django.db import models

from habits_trainer.models.task import Task


class TaskFeedback(models.Model):
    class Behavior(models.TextChoices):
        DONE = 'DONE'
        # SOON = 'SOON', _('Soon (Just a few days)')
        LATER = 'LATER'

    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    feedback = models.CharField(max_length=10, choices=Behavior.choices, default=Behavior.DONE)
    date = models.DateTimeField()
