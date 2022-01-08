from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.conf import settings
from computing_environment.models import Job
from computing_environment.managers import JobResultManager

def result_save_directory(instance, filename):
    return 'results/{0}/{1}_{2}'.format(instance.job.id, timezone.now(), filename)

class JobResult(models.Model):
    class Meta:
        app_label = "computing_environment"

    result = models.FileField(upload_to=result_save_directory)
    job = models.ForeignKey(Job, on_delete=CASCADE, related_name='results')
    avg_processor_usage = models.DecimalField(max_digits=5, decimal_places=2)
    avg_memory_usage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JobResultManager()

    def execution_time(self):
        return self.job.updated_at - self.updated_at

    def download_link(self):
        return mark_safe('<a href="{0}{1}">{1}</a>'.format(settings.MEDIA_URL, self.result))
