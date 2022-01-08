from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from computing_environment.models.job_result import JobResult
from ..serializers import JobSerializer, JobReportSerializer
from computing_environment.forms import JobForm
from computing_environment.models.job import Job
from computing_environment.models import JobResult
from computing_environment.services import dashboard_stats
from .dashboard_view import dashboard
from ..constants import JobStates


@login_required
def new_job(request):

    stats = dashboard_stats()
    recent_results = JobResult.objects.recent_results(request.user, 5)

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
    
    context = { 'job_form': job_form, 'current_user': request.user,
                'stats': stats, 'recent_results': recent_results }
    return render(request, 'job/new.html', context)

@login_required
def show_job(request, id):
    
    stats = dashboard_stats()
    recent_results = JobResult.objects.recent_results(request.user, 5)

    job = get_object_or_404(Job, pk=id)
    if job.is_private and job.creator != request.user:
        raise PermissionDenied()

    job_results = JobResult.objects.filter(job=job)
    context = { 'job': job, 'job_results': job_results, 'current_user': request.user,
                'stats': stats, 'recent_results': recent_results }
    print(job_results)
    return render(request, 'job/show.html', context)

@login_required
def edit_job(request, id):
    
    stats = dashboard_stats()
    recent_results = JobResult.objects.recent_results(request.user, 5)


    job = get_object_or_404(Job, pk=id)
    if job.creator != request.user:
        raise PermissionDenied()

    if request.POST:
        job_form = JobForm(request.POST, request.FILES, instance=job)
        if job_form.is_valid():
            job_form.save()
            if job.state == JobStates.IN_PROGRESS:
                job.job_changed_in_progress()
            else:
                job.job_changed()
            job.save()

            return redirect(dashboard)
    else:
        job_form = JobForm(instance=job)

    context = { 'job': job, 'job_form': job_form, 'current_user': request.user,
                'stats': stats, 'recent_results': recent_results }
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

@api_view(['GET'])
def get_program(request, id):
    job = Job.objects.job_program(id)
    content = { "error" : "Resource not found" }
    if job:
        if default_storage.exists(job.program.name):
            response = HttpResponse(job.program.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="%s"' % job.program
            return HttpResponse(response, status=status.HTTP_200_OK)
        content = { "error": "Program file doesn't exist" }

    return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def worker_report(request, id):
    job = Job.objects.job_in_progress(id)
    if job:
        job_report_serializer = JobReportSerializer(data=request.data)
        if job_report_serializer.is_valid():
            context = { 'updated': False}

            data = job_report_serializer.data
            job.processor_usage = data['processor_usage']
            job.memory_usage = data['memory_usage']
            if job.state == JobStates.CHANGED_IN_PROGRESS:
                serializer = JobSerializer(job)
                context['job'] = serializer.validated_data
                context['updated'] = True
                
                job.continue_execution()
            job.last_worker_call = timezone.now()
            job.save()

            return Response(context, status=status.HTTP_200_OK)

        return Response(job_report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    content = { "error" : "Resource not found" }
    return Response(content, status=status.HTTP_404_NOT_FOUND)
