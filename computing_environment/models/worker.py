from django.db import models

from computing_environment.managers.worker_manager import WorkerManager

class Worker(models.Model):
    class Meta:
        app_label = "computing_environment"

    processor = models.CharField(max_length=254, null=True)
    ram = models.CharField(max_length=10, null=True)
    # ram = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WorkerManager()
