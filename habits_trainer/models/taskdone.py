from datetime import datetime

from django.db import models

from habits_trainer.models.task import Task


class TaskDone(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    done_date = models.DateTimeField(null=True)

    # predicted_next_date = models.DateTimeField(null=True)

    # actual_interval = models.FloatField()

    def __str__(self):
        return " ".join([self.task.name.__str__(), self.done_date.__str__()])

    def predict_next_date(self) -> datetime:
        if self.task.mean_interval(self.done_date):
            return self.done_date + self.task.mean_interval(self.done_date)

    def delay(self):
        prediction_at_last_done_date = self.task.last_done_task_before(self.done_date).predict_next_date()
        if prediction_at_last_done_date:

            return self.done_date - prediction_at_last_done_date
        else:
            return None

    def mean_interval(self):

        return self.task.mean_interval(self.done_date)
