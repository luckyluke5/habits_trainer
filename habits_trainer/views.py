from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
from django.utils import timezone
from django.views import generic

from .models.task import Task


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserView(generic.ListView):
    model = Task

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

        # return super().get_queryset().filter(user__id=2)


class BestTaskView(UserView):
    model = Task
    template_name = "habits_trainer/best_task.html"

    # allow_empty = True

    def get_queryset(self):
        # timezone.activate("Europe/Paris")
        query = super().get_queryset().filter(nextDoDate__lte=timezone.now())

        if query:

            return query.earliest("nextDoDate")
        else:
            return None

    def get_context_data(self, *, object_list=None, **kwargs):

        nextDoDate = super().get_queryset().earliest('nextDoDate').nextDoDate

        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({"nextDoDate": nextDoDate})

        return context

class AllTaskView(UserView):
    model = Task
    template_name = "habits_trainer/task_list.html"

    # ordering = "predict_next_date"

    def get_queryset(self):
        # timezone.activate("Europe/Paris")
        return super().get_queryset().order_by('targetInterval')

        # return sorted(super().get_queryset(), key=lambda object: object.predict_next_date)


class ActuallTaskView(UserView):
    model = Task
    template_name = "habits_trainer/task_list.html"

    # ordering = "predict_next_date"

    def get_queryset(self):
        # timezone.activate("Europe/Paris")
        return super().get_queryset().order_by('nextDoDate').filter(nextDoDate__lte=timezone.now())

        # filtered = filter(lambda object: object.predict_next_date <= datetime.now(timezone.utc),
        #                  super().get_queryset())
        # return sorted(filtered, key=lambda object: object.predict_next_date)


def taskDone(request, task_id):
    # print(task_id)

    task = get_object_or_404(Task, pk=task_id)

    if not request.user == task.user:
        return HttpResponse('Unauthorized', status=401)

    task.task_done_at_date()
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect(task)


def taskSnooze(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if not request.user == task.user:
        return HttpResponse('Unauthorized', status=401)

    task.task_snooze()

    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect(task)


class UserSpecificCreate(generic.CreateView):

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserSpecificCreate, self).form_valid(form)


class TaskView(generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object: Task = self.get_object()

        context.update({"intervals": object.done_intervals()})

        return context
