import statistics
from datetime import timedelta, datetime, timezone
# from time import
from typing import List

from django.db import models

from django.contrib.auth.models import User


# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=50)
    interval = models.FloatField(default=7.0)
    targetInterval = models.FloatField(default=7.0, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.__str__()

    def mean_interval(self, to_date=datetime.now()):
        ordered_task_done = self.taskdone_set.filter(done_date__lte=to_date).order_by('done_date')

        last_date = None

        intervals: List[timedelta] = []

        for taskDone in ordered_task_done.all():
            date = taskDone.done_date
            if last_date:
                intervals.append(date - last_date)

            last_date = date

        if intervals:

            mean_in_seconds = statistics.mean([interval.total_seconds() for interval in intervals])

            # return sum(intervals)/len(intervals)
            # [interval.days for interval in intervals]
            print(mean_in_seconds)
            return timedelta(seconds=mean_in_seconds)

        else:
            return None

    def compute_new_interval(self):

        if self.taskfeedback_set.latest("date").feedback == TaskFeedback.Behavior.DONE:
            self.interval = self.mean_interval()
        elif self.taskfeedback_set.latest("date").feedback == TaskFeedback.Behavior.LATER:
            self.interval *= 2


    def predict_next_date(self):
        try:
            next_date = self.taskdone_set.latest("done_date").predict_next_date()

        except:
            return datetime.now(timezone.utc)

        return next_date

        # if next_date:
        #    return next_date
        # else:
        #    datetime.now()

    def last_done_task_before(self, to_date=datetime.now()):
        return self.taskdone_set.filter(done_date__lt=to_date).latest('done_date')

    # def usual_delay(self):
    #     ordered_task_done = self.taskdone_set.order_by('done_date')
    #
    #     last_predicted_next_date = None
    #
    #     intervals: List[timedelta] = []
    #
    #     for taskDone in ordered_task_done.all():
    #         predicted_next_date = taskDone.predicted_next_date()
    #         if last_predicted_next_date:
    #             intervals.append(taskDone.done_date - last_predicted_next_date)
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
