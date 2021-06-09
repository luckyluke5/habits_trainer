from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
from django.views import generic

from .models.task import Task


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class AllTaskView(generic.ListView):
    model = Task
    template_name = "habits_trainer/task_list.html"

    # ordering = "predict_next_date"

    def get_queryset(self):
        return super().get_queryset().order_by('nextDoDate')

        # return sorted(super().get_queryset(), key=lambda object: object.predict_next_date)


class ActuallTaskView(generic.ListView):
    model = Task
    template_name = "habits_trainer/task_list.html"

    # ordering = "predict_next_date"

    def get_queryset(self):
        return super().get_queryset().order_by('nextDoDate').filter(nextDoDate__lte=datetime.now())

        # filtered = filter(lambda object: object.predict_next_date <= datetime.now(timezone.utc),
        #                  super().get_queryset())
        # return sorted(filtered, key=lambda object: object.predict_next_date)


def taskDone(request, task_id):
    print(task_id)

    task = get_object_or_404(Task, pk=task_id)
    task.task_done_at_date()

    return redirect(task)


def taskSnoze(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.task_snoze()

    return redirect(task)
