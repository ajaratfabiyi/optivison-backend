import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optivus_backend.settings')

# Create Celery instance
app = Celery('optivus_backend')

# Load config from Django settings, using CELERY_* namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all registered Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'[CELERY DEBUG] Request: {self.request!r}')
