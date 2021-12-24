from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from computing_environment.models.job import Job

@login_required
def dashboard(request):
    jobs = Job.objects.visible_for_user(request.user)

    context = { 'jobs': jobs, 'current_user': request.user }
    return render(request, 'dashboard/index.html', context)