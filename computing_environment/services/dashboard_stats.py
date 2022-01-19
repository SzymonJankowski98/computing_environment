from computing_environment.models.worker import Worker
from computing_environment.models import SubJob
from datetime import timedelta

def dashboard_stats():
    subjobs = SubJob.objects.all()
    et=timedelta(0)
    for sub in subjobs:
        et+=sub.execution_time()

    stats = {
        'workers': Worker.objects.active().count(),
        'available': SubJob.objects.jobs_available().count(),
        'in_progress': SubJob.objects.jobs_in_progress().count(),
        'completed': SubJob.objects.jobs_completed().count(),
        'failed': SubJob.objects.jobs_failed().count(),
        'et': et.seconds
    }
    
    return stats
