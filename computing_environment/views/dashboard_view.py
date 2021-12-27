from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from computing_environment.models.job import Job
from computing_environment.models import JobResult
from computing_environment.services import dashboard_stats

@login_required
def dashboard(request):
    jobs = Job.objects.visible_for_user(request.user)
    stats = dashboard_stats()
    recent_results = JobResult.objects.recent_results(request.user, 5)

    context = {
        'jobs': jobs, 'current_user': request.user,
        'stats': stats, 'recent_results': recent_results
    }
    return render(request, 'dashboard/index.html', context)
