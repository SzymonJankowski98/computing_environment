from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django_fsm import FSMField, transition

from computing_environment.models import Job
from computing_environment.managers import SubJobManager
from computing_environment.models.worker import Worker
from ..constants import SubJobStates

def result_save_directory(instance, filename):
    return 'results/{0}/{1}_{2}'.format(instance.job.id, timezone.now(), filename)

class SubJob(models.Model):
    class Meta:
        app_label = "computing_environment"

    result = models.FileField(upload_to=result_save_directory, validators=[FileExtensionValidator(allowed_extensions=['zip', 'rar'])])
    job = models.ForeignKey(Job, on_delete=CASCADE, related_name='sub_jobs')
    worker = models.ForeignKey(Worker, on_delete=SET_NULL, related_name='sub_job', null=True)
    settings = models.JSONField(default=dict, blank=True)
    state = FSMField(default=SubJobStates.AVAILABLE, protected=True)
    last_worker_call = models.DateTimeField(null=True, blank=True)
    processor_usage = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    memory_usage = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    avg_processor_usage = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    avg_memory_usage = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SubJobManager()

    def execution_time(self):
        return self.updated_at - self.created_at

    def download_link(self):
        return mark_safe('<a href="{0}{1}">{1}</a>'.format(settings.MEDIA_URL, self.result))
    
    @transition(field=state, source=SubJobStates.AVAILABLE, target=SubJobStates.IN_PROGRESS)
    def mark_as_in_progress(self):
        self.last_worker_call = timezone.now()

    @transition(field=state, source=[SubJobStates.AVAILABLE,  SubJobStates.IN_PROGRESS, SubJobStates.COMPLETE, SubJobStates.FAILED], target=SubJobStates.AVAILABLE)
    def job_changed(self):
        self.processor_usage = None
        self.memory_usage = None
        self.avg_processor_usage = None
        self.memory_usage = None
        pass

    @transition(field=state, source=[SubJobStates.IN_PROGRESS], target=SubJobStates.AVAILABLE)
    def reactivate(self):
        self.processor_usage = None
        self.memory_usage = None
        self.avg_processor_usage = None
        self.memory_usage = None
        pass

    @transition(field=state, source=SubJobStates.IN_PROGRESS, target=SubJobStates.COMPLETE)
    def complete(self):
        pass

    @transition(field=state, source=SubJobStates.IN_PROGRESS, target=SubJobStates.FAILED)
    def fail(self):
        pass
