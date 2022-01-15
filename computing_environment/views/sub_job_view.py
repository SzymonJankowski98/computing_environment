from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages

from computing_environment.models import SubJob
from computing_environment.views.job_view import edit_job

from ..serializers import SubJobResultSerializer
from ..constants import JobStates

@login_required
@require_http_methods(["POST"])
def delete_sub_job(request, id):
    sub_job = get_object_or_404(SubJob, pk=id)
    if sub_job.job.creator != request.user:
        raise PermissionDenied()
    
    sub_job.delete()
    messages.success(request, 'Sub task deleted successfully.')
    return redirect(edit_job, sub_job.job.id)

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
                return Response(job_result_serializer.data, status=status.HTTP_201_CREATED)
            content = { "error": "Job is not in progress" }
            return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response(job_result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    content = { "error" : "Resource not found" }
    return Response(content, status=status.HTTP_404_NOT_FOUND)
