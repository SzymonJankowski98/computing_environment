from django import forms
from django.contrib.auth import get_user_model
from ..models import Invitation

from ..exceptions import AlreadyAccepted, AlreadyInvited, UserRegisteredEmail

class CleanEmailMixin(object):
    def validate_invitation(self, email):
        if Invitation.objects.filter(
                email__iexact=email, accepted=False):
            raise AlreadyInvited
        elif Invitation.objects.filter(
                email__iexact=email, accepted=True):
            raise AlreadyAccepted
        elif get_user_model().objects.filter(email__iexact=email):
            raise UserRegisteredEmail
        else:
            return True

    def clean_email(self):
        email = self.cleaned_data["email"]

        errors = {
            "already_invited": "This e-mail address has already been"
                                 " invited.",
            "already_accepted": "This e-mail address has already"
                                  " accepted an invite.",
            "email_in_use": "An active user is using this e-mail address",
        }
        try:
            self.validate_invitation(email)
        except(AlreadyInvited):
            raise forms.ValidationError(errors["already_invited"])
        except(AlreadyAccepted):
            raise forms.ValidationError(errors["already_accepted"])
        except(UserRegisteredEmail):
            raise forms.ValidationError(errors["email_in_use"])
        return email


class InvitationAdminAddForm(forms.ModelForm, CleanEmailMixin):
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.TextInput(attrs={"type": "email", "size": "50"}))

    def save(self, *args, **kwargs):
        cleaned_data = super(InvitationAdminAddForm, self).clean()
        email = cleaned_data.get("email")
        params = {'email': email}
        if cleaned_data.get("inviter"):
            params['inviter'] = cleaned_data.get("inviter")
        instance = Invitation.create(**params)
        instance.send_invitation(self.request)
        super(InvitationAdminAddForm, self).save(*args, **kwargs)
        return instance

    class Meta:
        model = Invitation
        fields = ("email", "inviter")