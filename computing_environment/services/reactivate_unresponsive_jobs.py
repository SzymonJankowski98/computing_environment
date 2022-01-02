from ..models import Job

def reactivate_unresponsive_jobs():
    failed_jobs = Job.objects.failed_jobs()
    
    for job in failed_jobs:
        try:
            job.reactivate()
            job.save()
        except Exception as error:
            print('reactivate_unresponsive_jobs error: %s' % error)
