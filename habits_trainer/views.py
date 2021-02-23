from django.http import HttpResponse

from datetime import timedelta, datetime, timezone
from django.shortcuts import render

# Create your views here.
from django.views import generic

from habits_trainer.models import Task


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class AllTaskView(generic.ListView):
    model = Task
    template_name = "habits_trainer/task_list.html"

    # ordering = "predict_next_date"

    def get_queryset(self):
        return sorted(super().get_queryset(), key=lambda object: object.predict_next_date())


class ActuallTaskView(generic.ListView):
    model = Task
    template_name = "habits_trainer/task_list.html"

    # ordering = "predict_next_date"

    def get_queryset(self):
        filtered = filter(lambda object: object.predict_next_date() <= datetime.now(timezone.utc),
                          super().get_queryset())
        return sorted(filtered,key=lambda object: object.predict_next_date())

