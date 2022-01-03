import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from computing_environment.models import JobResult
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

@login_required
def download(request, id):
    result = get_object_or_404(JobResult,pk=id)
    job = result.job
    if job.is_private and job.creator != request.user:
        raise PermissionDenied()
    file_buffer = open(result.result.path, "rb").read()
    response = HttpResponse(file_buffer, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(result.result.path)
    return response
