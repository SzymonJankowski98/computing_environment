from .user import *
from django.db.models.deletion import SET_NULL

class Job(models.Model):
    class Meta:
        app_label = "computing_environment"

    name = models.CharField(max_length=254)
    creator = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    program = models.FileField()
    settings = models.JSONField()
    is_private = models.BooleanField(default=False)
