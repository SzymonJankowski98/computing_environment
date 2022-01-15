import imp
from datetime import date
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
    workers = request.GET.get('workers', 'all')

    workersMock = []
    workersMock.append(Worker(processor='Intel® Core™ i7-12650H Processor (24M Cache, up to 4.70 GHz)', 
                            ram='32 GB', created_at=date(2022, 1, 10), updated_at=date(2022, 1, 14)))
    workersMock.append(Worker(processor='Ryzen 5 5600X', ram='8 GB', created_at=date(2022, 1, 10), updated_at=date(2022, 1, 11)))
    workersMock.append(Worker(processor='Intel® Core™ i7-12650H Processor (24M Cache, up to 4.70 GHz)',
                            ram='16 GB', created_at=date(2022, 1, 10), updated_at=date(2022, 1, 10)))
    workersMock.append(Worker(processor='Ryzen 9 9600X', ram='8 GB', created_at=date(2022, 1, 10), updated_at=date(2022, 1, 14)))
    workersMock.append(Worker(processor='Intel® Core™ i5', ram='4 GB', created_at=date(2022, 1, 10), updated_at=date(2022, 1, 15)))
    workersMock.append(Worker(processor='Ryzen 5 5600X', ram='8 GB', created_at=date(2022, 1, 1), updated_at=date(2022, 1, 9)))

    stats = dashboard_stats()
    recent_results = SubJob.objects.recent_results(request.user, 5)

    context = {
        'workers': workersMock, 'current_user': request.user,
        'stats': stats, 'recent_results': recent_results
    }
    return render(request, 'workers/index.html', context)
