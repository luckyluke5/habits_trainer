from habits_trainer.models import TaskFeedback


def compute_new_interval(self):
    if self.taskfeedback_set.latest("date").feedback == TaskFeedback.Behavior.DONE:
        self.interval = self.mean_interval()
    elif self.taskfeedback_set.latest("date").feedback == TaskFeedback.Behavior.LATER:
        self.interval *= 2
