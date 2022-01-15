from computing_environment.models.sub_job import SubJob
from ..models import SubJob

def reactivate_unresponsive_jobs():
    failed_jobs = SubJob.objects.failed_jobs()
    
    for sub_job in failed_jobs:
        try:
            sub_job.reactivate()
            sub_job.save()
        except Exception as error:
            print('reactivate_unresponsive_jobs error: %s' % error)
