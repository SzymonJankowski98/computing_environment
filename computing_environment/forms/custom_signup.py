from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    token = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "hidden"
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