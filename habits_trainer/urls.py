from django.urls import path, include
from . import views

app_name = 'health_tracker'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('allTask/', views.AllTaskView.as_view(), name='allTask'),
    path('actuallTask/', views.ActuallTaskView.as_view(), name='actuallTask'),



]
