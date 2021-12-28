from allauth.account.forms import ChangePasswordForm

class CustomLChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomLChangePasswordForm, self).__init__(*args, **kwargs)
        del self.fields['password1'].widget.attrs['placeholder']
        del self.fields['password2'].widget.attrs['placeholder']