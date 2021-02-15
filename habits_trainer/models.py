import statistics
from datetime import timedelta, datetime
from typing import List

from django.db import models


# Create your models here.

# Test here


class Task(models.Model):
    name = models.CharField(max_length=50)
    interval = models.FloatField(default=7.0)
    targetInterval = models.FloatField(default=7.0, editable=True)

    def __str__(self):
        return self.name.__str__()

    def mean_interval(self, to_date=datetime.now()):
        ordered_task_done = self.taskdone_set.filter(doneDate__lte=to_date).order_by('doneDate')

        last_date = None

        intervals: List[timedelta] = []

        for taskDone in ordered_task_done.all():
            date = taskDone.doneDate
            if last_date:
                intervals.append(date - last_date)

            last_date = date

        if intervals:

            mean_in_days = statistics.mean([interval.days for interval in intervals])
            # [interval.days for interval in intervals]
            print(mean_in_days)
            return timedelta(days=mean_in_days)

        else:
            return None

    def compute_new_interval(self):

        if self.taskfeedback_set.latest("date").feedback == TaskFeedback.Behavior.DONE:
            self.interval = self.mean_interval()
        elif self.taskfeedback_set.latest("date").feedback == TaskFeedback.Behavior.LATER:
            self.interval *= 2

    def predict_next_date(self):
        return self.taskdone_set.latest("doneDate").predict_next_date()

    # def usual_delay(self):
    #     ordered_task_done = self.taskdone_set.order_by('doneDate')
    #
    #     last_predicted_next_date = None
    #
    #     intervals: List[timedelta] = []
    #
    #     for taskDone in ordered_task_done.all():
    #         predicted_next_date = taskDone.predicted_next_date()
    #         if last_predicted_next_date:
    #             intervals.append(taskDone.doneDate - last_predicted_next_date)
    #
    #         last_predicted_next_date = predicted_next_date
    #
    #     if intervals:
    #
    #         mean_in_days = statistics.mean([interval.days for interval in intervals])
    #         # [interval.days for interval in intervals]
    #         print(mean_in_days)
    #         return timedelta(days=mean_in_days)
    #
    #     else:
    #         return None

    # def number_of_delays_since_last_done(self) -> int:
    #     feedbacks = self.taskfeedback_set.order_by("-date")
    #
    #     result = 0
    #
    #     for feedback in feedbacks:
    #         if feedback.feedback == TaskFeedback.Behavior.DONE:
    #             break
    #         else:
    #             result += 1
    #
    #     return result


class TaskFeedback(models.Model):
    class Behavior(models.TextChoices):
        DONE = 'DONE'
        # SOON = 'SOON', _('Soon (Just a few days)')
        LATER = 'LATER'

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=10, choices=Behavior.choices, default=Behavior.DONE)
    date = models.DateTimeField()


class TaskDone(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    doneDate = models.DateTimeField(null=True)

    # predicted_next_date = models.DateTimeField(null=True)

    # actual_interval = models.FloatField()

    def __str__(self):
        return " ".join([self.task.name.__str__(), self.doneDate.__str__()])

    def predict_next_date(self):
        if self.task.mean_interval(self.doneDate):
            return self.doneDate + self.task.mean_interval(self.doneDate)
