import os
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from computing_environment.models.job import Job
from zipfile import ZipFile
from django.utils import timezone
from config.base import MEDIA_ROOT

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

def save_all_results_directory(id,name):
    zip_directory ='{0}/combined_results/{1}/'.format(MEDIA_ROOT,id)
    Path(zip_directory).mkdir(parents=True, exist_ok=True)
    filename = "{}_{}_{}".format(timezone.now().strftime("%Y-%m-%d_%H%M%S.%f"),name,'all_results.zip')
    return  os.path.join(zip_directory,filename)

@login_required
def download_all(request, id):
    job = get_object_or_404(Job,pk=id)
    if job.is_private and job.creator != request.user:
        raise PermissionDenied()

    zip_path = save_all_results_directory(job.id,job.name)
    
    with ZipFile(zip_path, 'w') as zipObj:
        for sub in job.get_completed_subtasks():
            zipObj.write(sub.result.path, os.path.basename(sub.result.path))

    response = HttpResponse(open(zip_path, "rb").read(), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(zip_path)
    return response