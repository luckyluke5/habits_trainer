import statistics
from datetime import datetime, timedelta
from typing import List, Optional

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from ..models import taskdone
from ..models import taskfeedback


# from models import TaskFeedback


class Task(models.Model):
    name = models.CharField(max_length=50)
    # interval = models.DurationField(blank=True,default=timedelta(days=7))
    targetInterval = models.DurationField(blank=True, default=timedelta(days=7))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nextDoDate = models.DateTimeField(blank=True, null=True)
    meanInterval = models.DurationField(blank=True, null=True, default=timedelta(days=7))

    def __str__(self):
        return self.name.__str__()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super().save(force_insert, force_update, using, update_fields)

        if self.taskdone_set.count() == 0:
            self.task_done_at_date()

    def start(self):

        if self.taskdone_set.count() == 0:
            self.task_done_at_date()
        else:
            self.mean_interval()
            self.predict_next_date()

        self.save()

    def get_absolute_url(self):
        return reverse('habits_trainer:task_details', args=[self.pk])

    def mean_interval(self) -> None:
        ordered_task_done = self.taskdone_set.filter(done_date__lte=timezone.now()).order_by('done_date')

        last_date = None

        intervals: List[timedelta] = []

        for taskDone in ordered_task_done.reverse()[:5]:
            date = taskDone.done_date
            if last_date:
                intervals.append(last_date - date)

            last_date = date

        if intervals:

            mean_in_seconds = statistics.mean([interval.total_seconds() for interval in intervals])

            # return sum(intervals)/len(intervals)
            # [interval.days for interval in intervals]
            # print(mean_in_seconds)
            self.meanInterval = timedelta(seconds=mean_in_seconds)

        else:
            self.meanInterval = None

    def predict_next_date(self) -> None:

        last_done_date = self.last_done_task().done_date
        last_snooze_date = self.last_snooze_date()

        if not last_done_date:
            raise ValueError('last_done_date should never be null')

        if not last_snooze_date:
            last_snooze_date = last_done_date

        if last_snooze_date > last_done_date:
            next_date = self.targetInterval * 0.25 + last_snooze_date

            self.nextDoDate = max(self.nextDoDate, next_date)

        else:

            if self.meanInterval:

                if self.meanInterval > self.targetInterval:
                    reduced_mean_interval = (self.meanInterval - self.targetInterval) * 0.8 + self.targetInterval

                else:
                    reduced_mean_interval = self.targetInterval
            else:
                reduced_mean_interval = self.targetInterval

            self.nextDoDate = last_done_date + reduced_mean_interval
        # additional_delay_interval = reduced_mean_interval * (1.25 ** self.number_of_delays_since_last_done())
        # print(additional_delay_interval)

        # if last_done_date:
        #
        # else:
        #    self.nextDoDate = datetime.now(timezone.utc)

    def last_done_task(self) -> taskdone.TaskDone:
        return self.taskdone_set.filter(done_date__lt=timezone.now()).latest('done_date')

    def last_snooze_date(self) -> Optional[datetime]:
        # self.taskdone_set.filter(done_date__lt=timezone.now()).latest('done_date')

        last_task_feedback = self.taskfeedback_set.filter(
            feedback__exact=taskfeedback.TaskFeedback.Behavior.LATER)

        if last_task_feedback:

            return last_task_feedback.latest('date').date
        else:
            return None

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

    def number_of_delays_since_last_done(self) -> int:
        feedbacks: List[taskfeedback.TaskFeedback] = self.taskfeedback_set \
            .filter(date__gt=self.last_done_task().done_date) \
            .order_by("-date")

        result = 0

        # feedback: TaskFeedback
        for feedback in feedbacks:
            # from habits_trainer.models import TaskFeedback
            if feedback.is_feedback_typ_later():
                result += 1
            else:
                break

        return result

    def task_done_at_date(self):
        task_done = taskdone.TaskDone(task=self, done_date=timezone.now())
        task_done.save()

        self.mean_interval()
        self.predict_next_date()
        self.save()

    def task_snooze(self):
        task_done = taskfeedback.TaskFeedback(task=self, feedback=taskfeedback.TaskFeedback.Behavior.LATER,
                                              date=timezone.now())
        task_done.save()

        # self.mean_interval()
        self.predict_next_date()
        self.save()
