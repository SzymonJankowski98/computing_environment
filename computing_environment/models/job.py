from .user import *
from django.db.models.deletion import SET_NULL
from django_fsm import FSMField

class Job(models.Model):
    class Meta:
        app_label = "computing_environment"

    name = models.CharField(max_length=254)
    creator = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    program = models.FileField()
    settings = models.JSONField()
    is_private = models.BooleanField(default=False)
    state = FSMField(default='new', protected=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
