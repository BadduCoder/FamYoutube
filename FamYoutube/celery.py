import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamYoutube.settings')

app = Celery('FamYoutube')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-youtube-data-every-10-secs':{
        'task':'YoutubeSearch.tasks.fetch_data',
        'schedule':30.0
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')