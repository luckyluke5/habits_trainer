from django.db import models


# from . import Task


class TaskFeedback(models.Model):
    class Behavior(models.TextChoices):
        DONE = 'DONE'
        # SOON = 'SOON', _('Soon (Just a few days)')
        LATER = 'LATER'

    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    feedback = models.CharField(max_length=10, choices=Behavior.choices, default=Behavior.DONE)
    date = models.DateTimeField()

    def is_feedback_typ_later(self) -> bool:
        return self.feedback == TaskFeedback.Behavior.LATER
