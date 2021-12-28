from allauth.account.forms import LoginForm

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        del self.fields['password'].widget.attrs['placeholder']
        del self.fields['login'].widget.attrs['placeholder']