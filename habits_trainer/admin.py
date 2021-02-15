from django.contrib import admin

# Register your models here.
from habits_trainer.models import Task, TaskFeedback, TaskDone

# admin.site.register(Task)
admin.site.register(TaskFeedback)


# admin.site.register(TaskDone)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "mean", "interval","next")

    def mean(self, obj: Task):
        return obj.mean_interval()

    def next(self, obj: Task):
        return obj.predict_next_date()


@admin.register(TaskDone)
class TaskDoneAdmin(admin.ModelAdmin):
    list_display = ("task", "doneDate", "predict")

    def predict(self, obj: TaskDone):
        return obj.predict_next_date()
