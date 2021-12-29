from allauth.account.forms import SignupForm
from django import forms
from allauth.account.adapter import get_adapter
from allauth.account import app_settings

from computing_environment.models.invitation import Invitation


class CustomSignupForm(SignupForm):
    token = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "hidden"
            }
        )
    )

    first_name = forms.CharField(max_length=50, label='First Name', required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
            }
        )
    )

    last_name = forms.CharField(max_length=50, label='Last Name', required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
            }
        )
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "readonly": True,
                "placeholder": "E-mail address",
                "autocomplete": "email",
            }
        )
    )

    def clean_email(self):
        value = self.data["email"]
        value = get_adapter().clean_email(value)
        if value and app_settings.UNIQUE_EMAIL:
            value = self.validate_email(value)
        return value

    def validate_email(self, value):
        invitation = Invitation.objects.filter(token=self.data["token"], email=value).first()
        if not invitation:
            raise forms.ValidationError("No invitation for this email")
        return get_adapter().validate_unique_email(value)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
