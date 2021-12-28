from allauth.account.forms import SetPasswordForm

class CustomLSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomLSetPasswordForm, self).__init__(*args, **kwargs)
        del self.fields['password1'].widget.attrs['placeholder']
        del self.fields['password2'].widget.attrs['placeholder']