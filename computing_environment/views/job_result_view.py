from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from computing_environment.models import JobResult

from ..serializers import JobResultSerializer
from ..constants import JobStates

@api_view(['POST'])
def send_result(request):
    job_result_serializer = JobResultSerializer(data=request.data)
    if job_result_serializer.is_valid():
        job_result_data = job_result_serializer.validated_data
        job_result = JobResult(**job_result_data)
        if job_result.job.state == JobStates.IN_PROGRESS:
            job_result.job.complete()
            job_result.job.save()
            job_result_serializer.save()
            return Response(job_result_serializer.data, status=status.HTTP_201_CREATED)
        content = { "error": "Job is not in progress or program changed" }
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    return Response(job_result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)