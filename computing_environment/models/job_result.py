from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from computing_environment.models import Job

def result_save_directory(instance, filename):
    return 'results/{0}/{1}_{2}'.format(instance.job.id, timezone.now(), filename)

class JobResult(models.Model):
    class Meta:
        app_label = "computing_environment"

    result = models.FileField(upload_to=result_save_directory)
    job = models.ForeignKey(Job, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
