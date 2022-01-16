from .user import *
from django.db.models.deletion import SET_NULL
from django.db.models import Q
from django_fsm import FSMField, transition
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from ..constants import JobStates, LANGUAGES, SubJobStates
from ..exceptions import WrongLanguage
from ..managers import JobManager

def program_save_directory(instance, filename):
    creator_id = instance.creator.id or 'no_author'
    return 'programs/{0}/{1}_{2}'.format(creator_id, timezone.now(), filename)

class Job(models.Model):
    class Meta:
        app_label = "computing_environment"

    objects = JobManager()

    name = models.CharField(max_length=254)
    creator = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    language = models.CharField(max_length=63, choices=LANGUAGES)
    program = models.FileField(upload_to=program_save_directory, validators=[FileExtensionValidator(allowed_extensions=['zip', 'rar'])])
    is_private = models.BooleanField(default=False)
    state = FSMField(default=JobStates.AVAILABLE, protected=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_all_subtasks(self):
        return self.sub_jobs.count()

    def get_completed_subtasks(self):
        q = Q(state=SubJobStates.COMPLETE)
        q.add(Q(state=SubJobStates.FAILED), Q.OR)
        return self.sub_jobs.filter(q).count()

    def get_in_progress_subtasks(self):
        return self.sub_jobs.filter(state=SubJobStates.IN_PROGRESS).count()

    def complete_percent(self):
        all = self.get_all_subtasks()
        if all == 0: 
            return 0
        else:
            completed = self.get_completed_subtasks()
            return round((completed / all) * 100, 2)

    def last_result(self):
        self.sub_jobs.order_by('-updated_at').first()

    def save(self, *args, **kwargs):
        if self.language in map(lambda l: l[0], LANGUAGES):
            super(Job, self).save(*args, **kwargs)
        else:
            raise WrongLanguage

    @transition(field=state, source=[JobStates.AVAILABLE, JobStates.IN_PROGRESS], target=JobStates.IN_PROGRESS)
    def mark_as_in_progress(self):
        pass
    
    @transition(field=state, source=[JobStates.AVAILABLE,  JobStates.IN_PROGRESS, JobStates.COMPLETE], target=JobStates.AVAILABLE)
    def job_changed(self):
        pass

    @transition(field=state, source=JobStates.IN_PROGRESS, target=JobStates.AVAILABLE)
    def reactivate(self):
        pass

    @transition(field=state, source=JobStates.COMPLETE, target=JobStates.IN_PROGRESS)
    def more_sub_jobs(self):
        pass

    @transition(field=state, source=JobStates.IN_PROGRESS, target=JobStates.COMPLETE)
    def complete(self):
        pass
