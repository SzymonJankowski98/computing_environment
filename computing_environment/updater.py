from apscheduler.schedulers.background import BackgroundScheduler
from computing_environment.services import reactivate_unresponsive_jobs
from computing_environment.constants import REACTIVATE_JOB_WORKER_INTERVAL


def start():
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(reactivate_unresponsive_jobs, 'interval', seconds=REACTIVATE_JOB_WORKER_INTERVAL)
    scheduler.start()
