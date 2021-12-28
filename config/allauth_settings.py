SITE_ID = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_FORMS = {
    'login': 'computing_environment.forms.CustomLoginForm',
    'change_password': 'computing_environment.forms.CustomLoginForm',
    'set_password': 'computing_environment.forms.CustomSetPasswordForm',
    'reset_password_from_key': 'computing_environment.forms.CustomResetPasswordKeyForm',
    'reset_password': 'computing_environment.forms.CustomResetPasswordForm',
    }
