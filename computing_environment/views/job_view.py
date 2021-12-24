from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from computing_environment.forms import JobForm
from computing_environment.models.job import Job
from .dashboard_view import dashboard


def sign_in(request):
    return render(request, 'landing/sign_in.html')


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
        return HttpResponseForbidden()
    
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
        return HttpResponseForbidden()
    
    job.delete()
    return redirect(dashboard)


def error_404(request):
    response = render(request, 'error404.html')
    response.status_code = 404
    return response