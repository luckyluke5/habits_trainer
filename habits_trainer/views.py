from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.
from django.utils import timezone
from django.views import generic, View

from . import api_call
from .models import Profile
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
        query: QuerySet = super().get_queryset().filter(nextDoDate__lte=timezone.now())

        if query:

            return query.order_by("acceptance", "-nextDoDate").last()
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


def taskDone(request, task_id, via_notification=False):
    # print(task_id)

    task = get_object_or_404(Task, pk=task_id)

    if not request.user == task.user:
        return HttpResponse('Unauthorized', status=401)

    task.task_done_at_date(via_notification)
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect(task)


def taskSnooze(request, task_id, via_notification=False):
    task = get_object_or_404(Task, pk=task_id)

    if not request.user == task.user:
        return HttpResponse('Unauthorized', status=401)

    task.task_snooze(via_notification)

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


class ServiceWorkerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'habits_trainer/service-worker.js', content_type="application/x-javascript")


def safe_vapid(request):
    # if request.is_ajax():
    #    message = "Yes, AJAX!"
    # else:
    #    message = "Not Ajax"
    # return HttpResponse(message)

    vapid = request.POST.get('vapid')
    user_profile: Profile = request.user.profile
    user_profile.vapid = vapid

    user_profile.save()

    return HttpResponse()


def get_vapid(request):
    vapid = request.user.profile.vapid
    return JsonResponse({'vapid': vapid}, status=200)


def send_notifications(request):
    for profile in Profile.objects.all():
        profile.send_notifications()

    return HttpResponse("Ready" + str(Profile.objects.count()))


def log_event(request):
    event_name = request.POST.get('event_name')
    event_parameters = request.POST.get('event_parameter')

    response = api_call.logEvent(event_name, event_parameters, request.user)
    return HttpResponse("Good")
