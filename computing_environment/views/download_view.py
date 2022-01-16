import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from computing_environment.models.job import Job
from zipfile import ZipFile

from computing_environment.models import SubJob
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from computing_environment.models.sub_job import SubJob

@login_required
def download(request, id):
    result = get_object_or_404(SubJob,pk=id)
    job = result.job
    if job.is_private and job.creator != request.user:
        raise PermissionDenied()
    file_buffer = open(result.result.path, "rb").read()
    response = HttpResponse(file_buffer, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(result.result.path)
    return response

@login_required
def download_all(request, id):
    job = get_object_or_404(Job,pk=id)
    if job.is_private and job.creator != request.user:
        raise PermissionDenied()

    with ZipFile('all_download.zip', 'w') as zipObj:
        for sub in job.get_completed_subtasks():
            zipObj.write(sub.result.path, os.path.basename(sub.result.path))

    response = HttpResponse(open('all_download.zip', "rb").read(), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(f"all_download.zip")
    os.remove('all_download.zip')
    return response