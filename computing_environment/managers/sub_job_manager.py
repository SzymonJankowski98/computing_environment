from django.db import models
from django.db.models import Q
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from ..constants import SubJobStates, JOB_UNRESPONSIVE_INTERVAL

class SubJobManager(models.Manager):
    class Meta:
        app_label = "computing_environment"
    
    def recent_results(self, user=None, limit=10):
        q = Q(job__is_private=False)
        if user:
            q.add(Q(job__creator=user), Q.OR)

        return self.select_related('job').filter(q).order_by('-created_at')[:limit]
    
    @transaction.atomic
    def sub_job_to_do(self):
        job = self.filter(Q(state=SubJobStates.AVAILABLE)).order_by('updated_at').select_for_update().first()
        if not job:
            return None
        job.mark_as_in_progress()
        job.save()
        return job
    
    def job_in_progress(self, id):
        q = Q(state=SubJobStates.IN_PROGRESS)
        q.add(Q(pk=id), Q.AND)
        return self.filter(q).order_by('updated_at').first()

    def failed_jobs(self):
        fail_border = timezone.now() - timedelta(minutes=JOB_UNRESPONSIVE_INTERVAL)
        q = Q(state=SubJobStates.IN_PROGRESS)
        q.add(Q(last_worker_call__lte=fail_border), Q.AND)
        return self.filter(q)

    def jobs_in_states(self, state, start_date=None, end_date=None):
        if state and isinstance(state, list):
            q = Q(state=state[0])
            for s in state[1:]:
                q.add(Q(state=state[0]), Q.OR)
        else:
            q = Q(state=state)
        if start_date and end_date:
            q.add(Q(updated_at__gte=(start_date, end_date)), Q.AND)
        elif start_date:
            q.add(Q(updated_at__gte=(start_date, end_date)), Q.AND)
        elif end_date:
            q.add(Q(updated_at__range=(start_date, end_date)), Q.AND)

        return self.filter(q)

    def jobs_completed(self, start_date=None, end_date=None):
        return self.jobs_in_states(SubJobStates.COMPLETE)

    def jobs_available(self, start_date=None, end_date=None):
        return self.jobs_in_states(SubJobStates.AVAILABLE)

    def jobs_in_progress(self, start_date=None, end_date=None):
        return self.jobs_in_states(SubJobStates.IN_PROGRESS)

    def jobs_failed(self, start_date=None, end_date=None):
        return self.jobs_in_states(SubJobStates.FAILED)

