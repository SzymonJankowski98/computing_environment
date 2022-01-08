from django.db import models
from django.db.models import Q

class JobResultManager(models.Manager):
    class Meta:
        app_label = "computing_environment"
    
    def recent_results(self, user=None, limit=10):
        q = Q(job__is_private=False)
        if user:
            q.add(Q(job__creator=user), Q.OR)

        return self.select_related('job').filter(q).order_by('-created_at')[:limit]
