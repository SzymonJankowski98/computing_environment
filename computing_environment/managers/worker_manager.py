from datetime import timedelta

from django.db import models
from django.utils import timezone
from ..constants import WORKER_UNRESPONSIVE_INTERVAL

class WorkerManager(models.Manager):
    class Meta:
        app_label = "computing_environment"

    def total_execution_time(self):
        workers = self.all()
        et=timedelta(0)

        for worker in workers:
            et += worker.worked_time

        return et.seconds

    def latest_reports(self):
        return self.all().order_by('-updated_at')

    def active(self):
        return self.filter(updated_at__gte=timezone.now() - timedelta(minutes=WORKER_UNRESPONSIVE_INTERVAL))