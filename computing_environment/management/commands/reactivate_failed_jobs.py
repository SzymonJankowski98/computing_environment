from django.core.management.base import BaseCommand, CommandError
from computing_environment.services import reactivate_unresponsive_jobs

class Command(BaseCommand):
    help = 'Changes state of jobs assigned to not responding workers to available'

    def handle(self, *args, **options):
        try:
            reactivate_unresponsive_jobs()
        except Exception as error:
            raise CommandError('reactivate_unresponsive_jobs failed: %s' % error)
        self.stdout.write(self.style.SUCCESS('unresponsive jobs reactivated'))
