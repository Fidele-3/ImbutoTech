import os
import ssl
import sys
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ibabi.settings")

app = Celery("ibabi")

print("⏳ Initializing Celery app...", flush=True)

# Load from Django settings
try:
    app.config_from_object("django.conf:settings", namespace="CELERY")
    print("✅ Loaded Celery config from Django settings", flush=True)
except Exception as e:
    print(f"❌ Failed to load Celery config: {e}", file=sys.stderr, flush=True)

# Log broker and backend URLs
print(f"🔗 CELERY_BROKER_URL: {settings.CELERY_BROKER_URL}", flush=True)
print(f"🔗 CELERY_RESULT_BACKEND: {getattr(settings, 'CELERY_RESULT_BACKEND', 'Not Set')}", flush=True)

# Apply SSL override for secure Redis (Upstash, etc.)
try:
    app.conf.broker_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}
    print("🔐 Applied broker_use_ssl = CERT_NONE", flush=True)
except Exception as e:
    print(f"❌ Failed to apply broker_use_ssl: {e}", file=sys.stderr, flush=True)

try:
    app.conf.result_backend_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}
    print("🔐 Applied result_backend_use_ssl = CERT_NONE", flush=True)
except Exception as e:
    print(f"❌ Failed to apply result_backend_use_ssl: {e}", file=sys.stderr, flush=True)

# Autodiscover tasks from all installed apps
try:
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    print("✅ Autodiscovered tasks from installed apps", flush=True)
except Exception as e:
    print(f"❌ Failed to autodiscover tasks: {e}", file=sys.stderr, flush=True)

# Celery Beat Schedule (only ibabi-specific tasks)
try:
    app.conf.beat_schedule = {
        'fetch_24h_forecast_hourly': {
            'task': 'users.tasks.fetch_climate_data.fetch_24h_forecast',
            'schedule': crontab(minute=0, hour='1', day_of_week='mon'),  # every Monday 1AM
        },
        'fetch_past_3months_weekly': {
            'task': 'users.tasks.fetch_climate_data.fetch_past_3months_data',
            'schedule': crontab(minute=0, hour='1', day_of_week='mon'),  # every Monday 1AM
        },
    }

    print("📅 Celery Beat schedule configured", flush=True)
except Exception as e:
    print(f"❌ Failed to configure beat schedule: {e}", file=sys.stderr, flush=True)

# Final log to confirm full load
print("✅ Celery app setup complete!", flush=True)
