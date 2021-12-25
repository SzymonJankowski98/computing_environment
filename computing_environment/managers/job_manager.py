from django.db import models
from django.db.models import Q
from ..constants import JobStates

class JobManager(models.Manager):
    class Meta:
        app_label = "computing_environment"
    
    def visible_for_user(self, user):
        return self.filter(Q(is_private=False) | Q(creator=user.id))

    def job_to_do(self):
        return self.filter(Q(state=JobStates.NEW)).order_by('updated_at').first()
    
    def job_in_progress(self, id):
        q = Q(state=JobStates.IN_PROGRESS)
        q.add(Q(state=JobStates.CHANGED_IN_PROGRESS), Q.OR)
        q.add(Q(pk=id), Q.AND)
        return self.filter(q).order_by('updated_at').first()

    def job_program(self, id):
        return self.filter(pk=id, state=JobStates.IN_PROGRESS).first()
