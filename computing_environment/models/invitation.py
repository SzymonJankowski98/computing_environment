from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.crypto import get_random_string

from computing_environment.models.user import User

class Invitation(models.Model):
    class Meta:
        app_label = "computing_environment"

    email = models.EmailField(max_length=254, unique=True)
    token = models.CharField(max_length=64, unique=True)
    accepted = models.BooleanField(default=False)
    inviter = models.ForeignKey(User, null=True, blank=True, on_delete=SET_NULL) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)