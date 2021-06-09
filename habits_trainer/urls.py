from django.urls import path
from django.views import generic

from . import models
from . import views

app_name = 'habits_trainer'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('allTask/', views.AllTaskView.as_view(), name='allTask'),
    path('actuallTask/', views.ActuallTaskView.as_view(), name='actuallTask'),
    path('task/<slug:pk>/',
         generic.DetailView.as_view(model=models.Task),
         name="task_details"),
    path('task/<slug:task_id>/done/',
         views.taskDone,
         name="task_done"),
    path('task/<slug:task_id>/snoze/',
         views.taskSnoze,
         name="task_snoze"),
    path('task/<slug:pk>/update/',
         generic.UpdateView.as_view(model=models.Task, fields=['name', 'targetInterval']),
         name="task_edit"),

]
