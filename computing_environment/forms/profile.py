from django import forms
from ..models import User

class ProfileForm(forms.ModelForm):
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

    class Meta:
        model = User
        fields = ['first_name', 'last_name']