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

from ..serializers import SubJobSerializer
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
def send_result(request):
    job_result_serializer = SubJobSerializer(data=request.data)
    if job_result_serializer.is_valid():
        job_result_data = job_result_serializer.validated_data
        job_result = SubJob(**job_result_data)
        if job_result.job.state == JobStates.IN_PROGRESS:
            job_result.job.complete()
            job_result.job.save()
            job_result_serializer.save()
            return Response(job_result_serializer.data, status=status.HTTP_201_CREATED)
        content = { "error": "Job is not in progress or program changed" }
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    return Response(job_result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
