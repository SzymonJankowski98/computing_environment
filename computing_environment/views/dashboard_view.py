from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from computing_environment.constants import JOB_PAGINATION


from computing_environment.models.job import Job
from computing_environment.models import JobResult
from computing_environment.services import dashboard_stats

@login_required
def dashboard(request):
    jobs = Job.objects.visible_for_user(request.user)
    paginator = Paginator(jobs, JOB_PAGINATION)
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger: # If page is not an integer deliver the first page
        jobs = paginator.page(1)
    except EmptyPage: # If page is out of range deliver last page of results
        jobs = paginator.page(paginator.num_pages)

    stats = dashboard_stats()
    recent_results = JobResult.objects.recent_results(request.user, 5)

    context = {
        'jobs': jobs, 'current_user': request.user,
        'stats': stats, 'recent_results': recent_results
    }
    return render(request, 'dashboard/index.html', context)
