from django.db import models
from django.db.models import Q
from django.db import transaction
from ..constants import JobStates

class JobManager(models.Manager):
    class Meta:
        app_label = "computing_environment"
    
    def visible_for_user(self, user):
        return self.filter(Q(is_private=False) | Q(creator=user.id))

    @transaction.atomic
    def job_to_do(self):
        job = self.filter(Q(state=JobStates.AVAILABLE)).order_by('updated_at').select_for_update().first()
        if not job:
            return None
        job.mark_as_in_progress()
        job.save()
        return job
    
    def job_in_progress(self, id):
        q = Q(state=JobStates.IN_PROGRESS)
        q.add(Q(state=JobStates.CHANGED_IN_PROGRESS), Q.OR)
        q.add(Q(pk=id), Q.AND)
        return self.filter(q).order_by('updated_at').first()

    def job_program(self, id):
        return self.filter(pk=id, state=JobStates.IN_PROGRESS).first()
