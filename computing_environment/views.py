from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse
from computing_environment.models import invitation

from .models import Invitation

from allauth.account.views import SignupView
from allauth import app_settings
from allauth.utils import get_request_param
from allauth.account.utils import passthrough_next_redirect_url

def landing(request):
    return render(request, 'landing/index.html')

def sign_in(request):
    return render(request, 'landing/sign_in.html')

def error_404(request):
    response = render(request, 'landing/error404.html')
    response.status_code = 404
    return response


class CustomSignupView(SignupView):
    def dispatch(self, request, *args, **kwargs):
        if 'token' in kwargs:
            invitation = Invitation.objects.filter(token=kwargs['token']).first()
            if invitation:
                return super(SignupView, self).dispatch(request, *args, **kwargs)
        return redirect('landing')

custom_signup_view = CustomSignupView.as_view()