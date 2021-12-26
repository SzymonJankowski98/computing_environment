class JobStates(object):
    AVAILABLE = 'available'
    IN_PROGRESS = 'in_progress'
    CHANGED_IN_PROGRESS = 'changed_in_progress'

JOB_FAIL_INTERVAL = 2 # minutes
REACTIVATE_JOB_WORKER_INTERVAL = 10 # seconds
