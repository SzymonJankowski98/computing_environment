from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..serializers import JobSerializer
from computing_environment.forms import JobForm
from computing_environment.models.job import Job
from .dashboard_view import dashboard


@login_required
def new_job(request):
    job_form = None
    if request.POST:
        job_form = JobForm(request.POST, request.FILES)

        if job_form.is_valid():
            new_job = job_form.save(commit=False)
            new_job.creator = request.user
            new_job.save()

            return redirect('dashboard')
        print(job_form.errors)
    else:
        job_form = JobForm()
    
    context = { 'job_form': job_form }
    return render(request, 'job/new.html', context)

@login_required
def edit_job(request, id):
    job = get_object_or_404(Job, pk=id)
    if job.creator != request.user:
        raise PermissionDenied()
    
    job_form = JobForm(instance=job)

    if request.POST:
        job_form.save()
        return redirect(dashboard)
    else:
        context = { 'job': job, 'job_form': job_form }
        return render(request, 'job/edit.html', context)

@login_required
@require_http_methods(["POST"])
def delete_job(request, id):
    job = get_object_or_404(Job, pk=id)
    if job.creator != request.user:
        raise PermissionDenied()
    
    job.delete()
    return redirect(dashboard)

@api_view(['GET'])
def job_to_do(request):
    job = Job.objects.job_to_do()
    if job:
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
    content = { "error" : "Resource not found" }
    return Response(content, status=status.HTTP_404_NOT_FOUND)