from django.db import models
from django.db.models import Q

class JobManager(models.Manager):
    class Meta:
        app_label = "computing_environment"
    
    def visible_for_user(self, user):
        return self.filter(Q(is_private=False) | Q(creator=user.id))