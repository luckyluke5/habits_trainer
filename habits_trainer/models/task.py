import json
import statistics
from datetime import datetime, timedelta
from typing import List, Optional

import requests
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone

from .. import api_call
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
    acceptance = models.FloatField(blank=False, null=True, default=1)
    tenthLastDoneDate = models.DateTimeField(blank=True, null=True)

    notified = models.BooleanField(default=False)

    def __str__(self):
        return self.name.__str__()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super().save(force_insert, force_update, using, update_fields)

        if self.taskdone_set.count() == 0:
            self.task_done_at_date()

    def update(self):

        self.calculate_tenth_last_done_date()
        self.mean_interval()
        self.predict_next_date()
        self.calculate_acceptance()
        # self.createNotificationForNextDoDate()

        self.save()

    def get_absolute_url(self):
        return reverse('habits_trainer:task_details', args=[self.pk])

    def mean_interval(self) -> None:
        intervals = self.done_intervals()

        if intervals:

            # [interval.total_seconds() for interval in intervals[:5]]

            intervals_in_secounds = []

            for interval in intervals:

                if interval < self.targetInterval * 4:
                    intervals_in_secounds.append(interval.total_seconds())

            valid_intervals = min(5, len(intervals_in_secounds))

            if valid_intervals > 0:
                mean_in_seconds = statistics.mean(intervals_in_secounds)
                mean_in_timedelta = timedelta(seconds=mean_in_seconds)

                solution = (mean_in_timedelta * valid_intervals + self.targetInterval * (5 - valid_intervals)) / 5

            else:
                solution = self.targetInterval

            # return sum(intervals)/len(intervals)
            # [interval.days for interval in intervals]
            # print(mean_in_seconds)
            self.meanInterval = solution

        else:
            self.meanInterval = self.targetInterval

    def done_intervals(self):
        ordered_task_done = self.taskdone_set \
            .filter(done_date__lte=timezone.now()) \
            .filter(done_date__gte=self.tenthLastDoneDate).order_by('done_date')
        last_date = None
        intervals: List[timedelta] = []
        for taskDone in ordered_task_done.reverse():
            date = taskDone.done_date
            if last_date:
                intervals.append(last_date - date)

            last_date = date
        return intervals

    def predict_next_date(self) -> None:

        last_done_date = self.last_done_task().done_date
        last_snooze_date = self.last_snooze_date()

        if not last_done_date:
            raise ValueError('last_done_date should never be null')

        if not last_snooze_date:
            last_snooze_date = last_done_date

        if last_snooze_date > last_done_date:
            next_date = self.targetInterval * (
                        0.25 * (1.25 ** self.number_of_delays_since_last_done())) + last_snooze_date

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

    def last_done_date(self) -> Optional[datetime]:
        return self.last_done_task().done_date

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

    def task_done_at_date(self, via_notification=False):
        task_done = taskdone.TaskDone(task=self, done_date=timezone.now())
        task_done.save()

        self.notified = False

        self.update()

        api_call.callMeasurementProtocolAPI("task_done", self.user_id, via_notification)

        self.user.profile.notified = False
        self.user.profile.save()

        if via_notification:
            self.user.profile.send_notifications()

        # self.calculate_tenth_last_done_date()
        # self.mean_interval()
        # self.predict_next_date()
        # self.calculate_acceptance()
        # self.save()

    def task_snooze(self, via_notification=False):
        task_done = taskfeedback.TaskFeedback(task=self, feedback=taskfeedback.TaskFeedback.Behavior.LATER,
                                              date=timezone.now())
        task_done.save()

        self.notified = False

        # self.mean_interval()
        self.update()

        api_call.callMeasurementProtocolAPI("task_snooze", self.user_id, via_notification)

        self.user.profile.notified = False
        self.user.profile.save()

        if via_notification:
            self.user.profile.send_notifications()

    def calculate_acceptance(self):
        task_done_set = self.taskdone_set \
            .filter(done_date__lte=timezone.now()) \
            .filter(done_date__gte=self.tenthLastDoneDate)

        task_snooze_set = self.taskfeedback_set \
            .filter(feedback__exact=taskfeedback.TaskFeedback.Behavior.LATER) \
            .filter(date__lte=timezone.now()) \
            .filter(date__gte=self.tenthLastDoneDate)

        snoozes = task_snooze_set.count()
        dones = task_done_set.count()
        if snoozes + dones > 0:
            self.acceptance = dones / (snoozes + dones)
        else:
            self.acceptance = 0.5

    def calculate_tenth_last_done_date(self):
        task_done_set: QuerySet = self.taskdone_set \
            .filter(done_date__lte=timezone.now()) \
            .order_by("-done_date")

        lastDate = None
        counter = 0

        for taskdone in task_done_set.all():
            nextDate = taskdone.done_date

            if lastDate:
                if lastDate - nextDate < self.targetInterval * 4:
                    counter += 1

                    if counter == 10:
                        self.tenthLastDoneDate = nextDate
                        return

            lastDate = nextDate

        if task_done_set.count() > 0:

            self.tenthLastDoneDate = task_done_set.earliest("done_date").done_date
        else:
            self.tenthLastDoneDate = timezone.now() - timedelta(days=1)

        # self.save()

    def createNotificationForNextDoDate(self):

        # HttpRequest(url)

        auth = 'key=AAAA7-DDDtc:APA91bHbGdJ_ZEmrXB_39DYvr-6tZ9Yg25aYWqlGYnadoGXRBx60Tqwl5JRO6I2HntZ3NJWaZsyTti8XMJtMau8U6M5-in1dkaFohuPCxEM3sBpXNM4tJJqcDQOVr7PShvMSGpdXFzP-'

        headers = {'Content-Type': 'application/json', 'Authorization': auth}

        actions = [{'title': 'Anzeigen', 'action': reverse("habits_trainer:task_details",
                                                           kwargs={'task_id': self.pk})},
                   {'title': 'Erledigt',
                    'action': reverse("habits_trainer:task_done_via_notification", kwargs={'task_id': self.pk})},

                   {'title': 'Verschieben', 'action': reverse("habits_trainer:task_snooze_via_notification",
                                                              kwargs={'task_id': self.pk})}]

        # actions = [{'title': 'Done', 'action': '/tas/145/done/'},
        #
        #           {'title': 'Snoze', 'action': '/tas/145/snoze/'}]

        dict = {"to": self.user.profile.vapid,
                "notification": {"title": self.name,
                                 "body": "Deine nächste Aufgabe '" + self.name + "' steht für dich bereit"},
                "data": {"actions": json.dumps(actions)}}
        # print(json.dumps(dict))
        response = requests.post("https://fcm.googleapis.com/fcm/send", data=json.dumps(dict), headers=headers)
        print(response)

        # print(response)
