from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views import generic

from . import models
from . import views

app_name = 'habits_trainer'
urlpatterns = [
    # path('index/', views.index, name='index'),
    path('allTask/', login_required(views.AllTaskView.as_view()), name='allTask'),
    path('', login_required(views.BestTaskView.as_view()), name='bestTask'),
    # path('actuallTask/', login_required(views.ActuallTaskView.as_view()), name='actuallTask'),
    path('task/add/',
         views.UserSpecificCreate.as_view(model=models.Task, fields=['name', 'targetInterval']),
         name="task_add"),
    path('task/safe_vapid/',
         views.safe_vapid,
         name="safe_vapid"),
    path('task/get_vapid/',
         views.get_vapid,
         name="get_vapid"),

    path('task/send_notifications/',
         views.send_notifications,
         name="send_notifications"),

    path('task/<slug:pk>/',
         views.TaskView.as_view(),
         name="task_details"),

    path('task/<slug:task_id>/done/',
         views.taskDone,
         name="task_done"),

    path('task/<slug:task_id>/snoze/',
         views.taskSnooze,
         name="task_snoze"),

    path('task/<slug:task_id>/done/via_notification/',
         views.taskDone, {'via_notification': True},
         name="task_done_via_notification"),

    path('task/<slug:task_id>/snooze/via_notification/',
         views.taskSnooze, {'via_notification': True},
         name="task_snooze_via_notification"),

    path('task/<slug:pk>/update/',
         generic.UpdateView.as_view(model=models.Task, fields=['name', 'targetInterval']),
         name="task_edit"),
    path('firebase-messaging-sw.js', views.ServiceWorkerView.as_view(), name='service-worker')

]
