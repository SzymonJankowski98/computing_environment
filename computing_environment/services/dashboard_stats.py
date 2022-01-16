from computing_environment.models.worker import Worker
from computing_environment.models import SubJob

def dashboard_stats():

    stats = {
        'workers': Worker.objects.active().count(),
        'available': SubJob.objects.jobs_available().count(),
        'in_progress': SubJob.objects.jobs_in_progress().count(),
        'completed': SubJob.objects.jobs_completed().count(),
        'failed': SubJob.objects.jobs_failed().count()
    }
    
    return stats
