from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from computing_environment.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = "computing_environment"

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    first_name = models.CharField(max_length=254, null=True)
    last_name = models.CharField(max_length=254, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)