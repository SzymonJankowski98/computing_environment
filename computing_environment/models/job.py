from .user import *
from django.db.models.deletion import SET_NULL
from django_fsm import FSMField, transition
from django.utils import timezone
from ..constants import JobStates, LANGUAGES
from ..exceptions import WrongLanguage
from ..managers import JobManager

def program_save_directory(instance, filename):
    creator_id = instance.creator.id or 'no_author'
    return 'programs/{0}/{1}_{2}'.format(creator_id, timezone.now(), filename)

class Job(models.Model):
    class Meta:
        app_label = "computing_environment"
        ordering = ['updated_at']
    objects = JobManager()

    name = models.CharField(max_length=254)
    creator = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    language = models.CharField(max_length=63, choices=LANGUAGES)
    program = models.FileField(upload_to=program_save_directory)
    settings = models.JSONField()
    is_private = models.BooleanField(default=False)
    state = FSMField(default=JobStates.AVAILABLE, protected=True)
    last_worker_call = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.language in map(lambda l: l[0], LANGUAGES):
            super(Job, self).save(*args, **kwargs)
        else:
            raise WrongLanguage

    @transition(field=state, source=JobStates.AVAILABLE, target=JobStates.IN_PROGRESS)
    def mark_as_in_progress(self):
        self.last_worker_call = timezone.now()

    @transition(field=state, source=[JobStates.IN_PROGRESS, JobStates.COMPLETE], target=JobStates.CHANGED_IN_PROGRESS)
    def job_changed(self):
        pass

    @transition(field=state, source=JobStates.CHANGED_IN_PROGRESS, target=JobStates.IN_PROGRESS)
    def continue_execution(self):
        self.last_worker_call = timezone.now()

    @transition(field=state, source=[JobStates.IN_PROGRESS, JobStates.CHANGED_IN_PROGRESS], target=JobStates.AVAILABLE)
    def reactivate(self):
        pass

    @transition(field=state, source=JobStates.IN_PROGRESS, target=JobStates.COMPLETE)
    def complete(self):
        pass
