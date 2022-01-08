from computing_environment.models import Job

def dashboard_stats():
    stats = {
        'available': Job.objects.jobs_available().count(),
        'in_progress': Job.objects.jobs_in_progress().count(),
        'completed': Job.objects.jobs_completed().count(),
        'failed': Job.objects.jobs_failed().count()
    }
    
    return stats
