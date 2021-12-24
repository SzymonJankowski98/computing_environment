
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse

from computing_environment.forms import CustomSignupForm

from ..models import Invitation

from allauth.account.views import LoginView, SignupView
from allauth.utils import get_request_param
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.utils import passthrough_next_redirect_url, complete_signup


def sign_in(request):
    return render(request, 'landing/sign_in.html')

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