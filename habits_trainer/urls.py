from django.urls import path, include
from . import views



app_name = 'health_tracker'
urlpatterns = [
    path('test', views.index, name='index'),
]