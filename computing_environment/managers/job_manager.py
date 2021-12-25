from django.db import models
from django.db.models import Q
from ..constants import JobStates

class JobManager(models.Manager):
    class Meta:
        app_label = "computing_environment"
    
    def visible_for_user(self, user):
        return self.filter(Q(is_private=False) | Q(creator=user.id))

    def job_to_do(self):
        return self.filter(Q(state=JobStates.NEW) | Q(state=JobStates.UPDATED)).order_by('updated_at').first()

    def job_program(self, id):
        return self.filter(pk=id, state=JobStates.IN_PROGRESS).first()
