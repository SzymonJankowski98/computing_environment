from allauth.account.forms import ResetPasswordForm

class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        del self.fields['email'].widget.attrs['placeholder']