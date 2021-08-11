from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# from . import Task
from ..models import task


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vapid = models.CharField(max_length=256, blank=True, null=True)
    notified = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        pass

    def send_notifications(self):
        if self.vapid and not self.notified:
            best_task: task.Task = task.Task.objects.filter(nextDoDate__lte=timezone.now()).filter(
                user=self.user).filter(notified=False).order_by("acceptance", "-nextDoDate").last()

            if best_task:
                best_task.createNotificationForNextDoDate()
                best_task.notified = True
                best_task.save()  #

                self.notified = True
                self.save()

        # toilette = get_object_or_404(Task, pk=145)
        # toilette.createNotificationForNextDoDate()

        return

    def allOpenTask(self):

        return task.Task.objects.filter(user=self.user).filter(nextDoDate__lte=timezone.now())
