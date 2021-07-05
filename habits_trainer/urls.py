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
    path('task/<slug:pk>/',
         views.TaskView.as_view(),
         name="task_details"),
    path('task/<slug:task_id>/done/',
         views.taskDone,
         name="task_done"),
    path('task/<slug:task_id>/snoze/',
         views.taskSnooze,
         name="task_snoze"),
    path('task/<slug:pk>/update/',
         generic.UpdateView.as_view(model=models.Task, fields=['name', 'targetInterval']),
         name="task_edit"),

]
