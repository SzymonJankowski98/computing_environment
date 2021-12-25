from .user import *
from django.db.models.deletion import SET_NULL
from django_fsm import FSMField, transition
from datetime import datetime
from ..constants import JobStates
from ..managers import JobManager

def program_save_directory(instance, filename):
    return '{0}/programs/{1}_{2}'.format(instance.creator.id, datetime.now(), filename)

class Job(models.Model):
    class Meta:
        app_label = "computing_environment"

    objects = JobManager()

    name = models.CharField(max_length=254)
    creator = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    program = models.FileField(upload_to=program_save_directory)
    settings = models.JSONField()
    is_private = models.BooleanField(default=False)
    state = FSMField(default=JobStates.AVAILABLE, protected=True)
    last_worker_call = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @transition(field=state, source=JobStates.AVAILABLE, target=JobStates.IN_PROGRESS)
    def mark_as_in_progress(self):
        self.last_worker_call = datetime.now()

    @transition(field=state, source=JobStates.CHANGED_IN_PROGRESS, target=JobStates.IN_PROGRESS)
    def continue_execution(self):
        self.last_worker_call = datetime.now()
