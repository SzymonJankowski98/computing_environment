from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import get_object_or_404

from computing_environment import forms
from computing_environment.models import invitation
from computing_environment.forms import CustomSignupForm
from computing_environment.forms import JobForm
from computing_environment.models.job import Job

from .models import Invitation

from allauth.account.views import LoginView, SignupView
from allauth import app_settings
from allauth.utils import get_request_param
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.utils import passthrough_next_redirect_url, complete_signup

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing/index.html')

def sign_in(request):
    return render(request, 'landing/sign_in.html')

@login_required
def dashboard(request):
    jobs = Job.objects.visible_for_user(request.user)

    context = { 'jobs': jobs, 'current_user': request.user }
    return render(request, 'dashboard/index.html', context)

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


class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def dispatch(self, request, *args, **kwargs):
        if 'token' in kwargs:
            invitation = Invitation.objects.filter(token=kwargs['token'], accepted=False).first()
            if invitation:
                return super(CustomSignupView, self).dispatch(request, *args, **kwargs)
        return redirect('landing')

    def form_valid(self, form):
        self.user = form.save(self.request)
        invitation = Invitation.objects.filter(email=self.user.email).first()
        if invitation:
            Invitation.objects.filter(id=invitation.id).update(accepted=True)
        try:
            return complete_signup(
                self.request,
                self.user,
                None,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response

    def get_context_data(self, **kwargs):
        ret = super(CustomSignupView, self).get_context_data(**kwargs)
        form = ret["form"]
        invitation = Invitation.objects.filter(token=self.kwargs['token']).first()
        if invitation:
            form.fields['email'].initial = invitation.email
            form.fields['token'].initial = invitation.token
        
        login_url = passthrough_next_redirect_url(
            self.request, reverse("account_login"), self.redirect_field_name
        )
        redirect_field_name = self.redirect_field_name
        site = get_current_site(self.request)
        redirect_field_value = get_request_param(self.request, redirect_field_name)
        ret.update(
            {
                "login_url": login_url,
                "redirect_field_name": redirect_field_name,
                "redirect_field_value": redirect_field_value,
                "site": site,
            }
        )
        return ret

custom_signup_view = CustomSignupView.as_view()

class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        redirect_field_value = get_request_param(self.request, self.redirect_field_name)
        site = get_current_site(self.request)

        ret.update(
            {
                "site": site,
                "redirect_field_name": self.redirect_field_name,
                "redirect_field_value": redirect_field_value,
            }
        )
        return ret

custom_login_view = CustomLoginView.as_view()