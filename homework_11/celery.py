import os
import time

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_11.settings')

app = Celery('homework_11')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1.0, debug_task, name='add every 1')


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    # print(f'Request: {self.request!r}')
    print(f"Hello from celery.py at {time.time()}")
