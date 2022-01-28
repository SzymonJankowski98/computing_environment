from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone

from computing_environment.models import SubJob, Worker
from computing_environment.views.job_view import edit_job

from ..serializers import SubJobResultSerializer, JobReportSerializer, SubJobSerializer
from ..constants import JobStates

@login_required
@require_http_methods(["POST"])
def delete_sub_job(request, id):
    sub_job = get_object_or_404(SubJob, pk=id)
    if sub_job.job.creator != request.user:
        raise PermissionDenied()
    
    sub_job.delete()
    completion = sub_job.job.complete_percent()
    if completion == 100:
        sub_job.job.complete()
        sub_job.job.save()
    elif completion == 0:
        sub_job.job.job_changed()
        sub_job.job.save()
    messages.success(request, 'Sub task deleted successfully.')
    return redirect(edit_job, sub_job.job.id)

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

@api_view(['POST'])
def worker_report(request, id):
    sub_job = SubJob.objects.job_in_progress(id)
    if sub_job:
        job_report_serializer = JobReportSerializer(data=request.data)
        if job_report_serializer.is_valid():
            data = job_report_serializer.data
            sub_job.processor_usage = data['processor_usage']
            sub_job.memory_usage = data['memory_usage']
            sub_job.worker.ip_address = data['ip_address']
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

@api_view(['POST'])
def send_result(request, id):
    sub_job = SubJob.objects.job_in_progress(id)
    if sub_job:
        job_result_serializer = SubJobResultSerializer(data=request.data)
        if job_result_serializer.is_valid():
            if sub_job.state == JobStates.IN_PROGRESS:
                data = job_result_serializer.data
                sub_job.result = request.FILES.get('result')
                sub_job.avg_processor_usage = data['avg_processor_usage']
                sub_job.avg_memory_usage = data['avg_memory_usage']
                if 'failed' in data and data['failed']:
                    sub_job.fail()
                else:
                    sub_job.complete()
                sub_job.save()
                sub_job.worker.worked_time += sub_job.execution_time()
                sub_job.worker.save()
                if sub_job.job.complete_percent() == 100:
                    sub_job.job.complete()
                    sub_job.job.save()
                return Response(job_result_serializer.data, status=status.HTTP_201_CREATED)
            content = { "error": "Job is not in progress" }
            return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response(job_result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    content = { "error" : "Resource not found" }
    return Response(content, status=status.HTTP_404_NOT_FOUND)
