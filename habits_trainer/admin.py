from django.contrib import admin

# Register your models here.
from habits_trainer.models import Task, TaskFeedback, TaskDone


# from habits_trainer.models.taskdone import TaskDone

# admin.site.register(Task)
# admin.site.register(TaskFeedback)


# admin.site.register(TaskDone)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name", "user", "targetInterval", "meanInterval", "nextDoDate", "last_done_date", "last_snooze_date")

    actions = ['reset']

    def mean(self, obj: Task):
        return obj.mean_interval()

    def next(self, obj: Task):
        return obj.predict_next_date

    def last_done_date(self, obj: Task):
        return obj.last_done_task().done_date

    def reset(self, request, queryset):
        [task.start() for task in queryset]

    reset.short_description = "Reset Interval and Prediction Date"

    # def meanInterval(self, obj: Task):
    #     return obj.predict_next_date
    #
    # def nextDoDate(self, obj: Task):
    #     return obj.predict_next_date


@admin.register(TaskDone)
class TaskDoneAdmin(admin.ModelAdmin):
    list_display = ("task", "done_date", "user")

    def predict(self, obj: TaskDone):
        return obj.predict_next_date()

    def user(self, obj: TaskDone):
        return obj.task.user

    def mean_interval(self, obj: TaskDone):
        return obj.mean_interval()


@admin.register(TaskFeedback)
class TaskFeedbackAdmin(admin.ModelAdmin):
    list_display = ("task", "date", "user")

    def predict(self, obj: TaskDone):
        return obj.predict_next_date()

    def user(self, obj: TaskDone):
        return obj.task.user

    def mean_interval(self, obj: TaskDone):
        return obj.mean_interval()
