from ..models import Job

class Reactivate_failed_jobs:
    def call(self):
        failed_jobs = Job.objects.failed_jobs()
        for job in failed_jobs:
            try:
                job.reactivate()
                job.save()
            except Exception as error:
                print(error)
