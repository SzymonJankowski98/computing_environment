class JobStates(object):
    AVAILABLE = 'available'
    IN_PROGRESS = 'in_progress'
    CHANGED_IN_PROGRESS = 'changed_in_progress'
    COMPLETE = 'complete'
    FAILED = 'failed'

JOB_UNRESPONSIVE_INTERVAL = 2 # minutes
REACTIVATE_JOB_WORKER_INTERVAL = 10 # seconds
JOB_PAGINATION = 16

LANGUAGES = (
    ('python', 'Python'),
    ('java', 'Java')
)