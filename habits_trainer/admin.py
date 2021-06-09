from django.contrib import admin

# Register your models here.
from habits_trainer.models import Task, TaskFeedback, TaskDone

# from habits_trainer.models.taskdone import TaskDone

# admin.site.register(Task)
admin.site.register(TaskFeedback)


# admin.site.register(TaskDone)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "meanInterval", "nextDoDate")

    def mean(self, obj: Task):
        return obj.mean_interval()

    def next(self, obj: Task):
        return obj.predict_next_date

    # def meanInterval(self, obj: Task):
    #     return obj.predict_next_date
    #
    # def nextDoDate(self, obj: Task):
    #     return obj.predict_next_date


@admin.register(TaskDone)
class TaskDoneAdmin(admin.ModelAdmin):
    list_display = ("task", "done_date", "predict","delay","mean_interval")

    def predict(self, obj: TaskDone):
        return obj.predict_next_date()

    def delay(self, obj: TaskDone):
        return 0

    def mean_interval(self, obj: TaskDone):
        return obj.mean_interval()
