from django.core.management.base import BaseCommand, CommandError
from computing_environment.services import reactivate_failed_jobs

class Command(BaseCommand):
    help = 'Changes state of jobs assigned to not responding workers to available'

    def handle(self, *args, **options):
        try:
            reactivate_failed_jobs()
        except Exception as error:
            raise CommandError('reactivate_failed_jobs failed: %s' % error)
        self.stdout.write(self.style.SUCCESS('Failed jobs reactivated'))
