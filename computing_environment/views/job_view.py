import json

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
from computing_environment.managers import sub_job_manager

from computing_environment.models.sub_job import SubJob
from computing_environment.models.worker import Worker
from ..serializers import JobSerializer, JobReportSerializer, SubJobSerializer, WorkerSerializer
from computing_environment.forms import JobForm, EditJobForm
from computing_environment.models.job import Job
from computing_environment.models import SubJob
from computing_environment.services import dashboard_stats
from .dashboard_view import dashboard
from ..constants import JobStates


@login_required
def new_job(request):

    stats = dashboard_stats()
    recent_results = SubJob.objects.recent_results(request.user, 5)

    if request.POST:
        job_form = JobForm(request.POST, request.FILES)

        if job_form.is_valid() and job_form.cleaned_data['settings']:
            new_job = job_form.save(commit=False)
            new_job.creator = request.user
            new_job.save()
            for s in json.loads(job_form.cleaned_data['settings']):
                SubJob.objects.create(job=new_job, settings=s)

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
    recent_results = SubJob.objects.recent_results(request.user, 5)
    
    job = get_object_or_404(Job, pk=id)
    if job.is_private and job.creator != request.user:
        raise PermissionDenied()

    job_results = SubJob.objects.filter(job=job)
    context = { 'job': job, 'job_results': job_results, 'current_user': request.user,
                'stats': stats, 'recent_results': recent_results }

    return render(request, 'job/show.html', context)

@login_required
def edit_job(request, id):
    
    stats = dashboard_stats()
    recent_results = SubJob.objects.recent_results(request.user, 5)


    job = get_object_or_404(Job, pk=id)
    if job.creator != request.user:
        raise PermissionDenied()

    if request.POST:
        job_form = EditJobForm(request.POST, request.FILES, instance=job)
        if job_form.is_valid():
            if 'program' in job_form.changed_data or 'language' in job_form.changed_data:
                for sub_job in job.sub_jobs.all():
                    sub_job.job_changed()
                    sub_job.save()
                job.job_changed()
            job_form.save()
            if job_form.cleaned_data['settings'] != '':
                for s in json.loads(job_form.cleaned_data['settings']):
                    SubJob.objects.create(job=job, settings=s)
                if job.state == JobStates.COMPLETE:
                    job.more_sub_jobs()
            job.save()

            return redirect(dashboard)
    else:
        job_form = EditJobForm(instance=job)

    context = { 'job': job, 'sub_jobs': job.sub_jobs.all(), 'job_form': job_form, 'current_user': request.user,
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
    sub_job = SubJob.objects.sub_job_to_do()
    if sub_job:
        worker = Worker.objects.create()
        sub_job.worker = worker
        sub_job.save()
        serializer = SubJobSerializer(sub_job)
        sub_job.job.mark_as_in_progress()
        sub_job.job.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    content = { "error" : "Resource not found" }
    return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def job_to_do_registered(request, id):
    worker = Worker.objects.filter(pk=id).first()
    if worker:
        sub_job = SubJob.objects.sub_job_to_do()
        if sub_job:
            sub_job.worker = worker
            sub_job.save()
            sub_job_serializer = SubJobSerializer(sub_job)
            sub_job.job.mark_as_in_progress()
            sub_job.job.save()
            return Response(sub_job_serializer.data, status=status.HTTP_200_OK)

        content = { "error" : "Resource not found" }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    content = { "error" : "Worker not found" }
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
    sub_job = SubJob.objects.job_in_progress(id)
    if sub_job:
        job_report_serializer = JobReportSerializer(data=request.data)
        if job_report_serializer.is_valid():
            data = job_report_serializer.data
            sub_job.processor_usage = data['processor_usage']
            sub_job.memory_usage = data['memory_usage']
            sub_job.worker.processor = data['processor']
            sub_job.worker.ram = data['ram']
            sub_job.last_worker_call = timezone.now()
            sub_job.worker.save()
            sub_job.save()

            sub_job_serializer = SubJobSerializer(sub_job)

            return Response(sub_job_serializer.data, status=status.HTTP_200_OK)

        return Response(job_report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    content = { "error" : "Resource not found" }
    return Response(content, status=status.HTTP_404_NOT_FOUND)
