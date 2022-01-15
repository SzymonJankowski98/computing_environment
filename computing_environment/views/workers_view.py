from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from computing_environment.constants import JOB_PAGINATION

from computing_environment.models.job import Job
from computing_environment.models import SubJob
from computing_environment.models.sub_job import SubJob
from computing_environment.models.worker import Worker
from computing_environment.services import dashboard_stats
from computing_environment.search_filters import JobFilter


@login_required
def show_workers(request):
    workers = Worker.objects.latest_reports()

    stats = dashboard_stats()
    recent_results = SubJob.objects.recent_results(request.user, 5)

    context = {
        'workers': workers, 'current_user': request.user,
        'stats': stats, 'recent_results': recent_results
    }
    return render(request, 'workers/index.html', context)
