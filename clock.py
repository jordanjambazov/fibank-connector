import os
import django
from apscheduler.schedulers.blocking import BlockingScheduler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connector.settings")
django.setup()
scheduler = BlockingScheduler()


def reconcile_job():
    from connector.engine import Engine
    engine = Engine()
    engine.reconcile_all()


scheduler.add_job(reconcile_job, 'cron', hour='3', minute='0', args=[])
scheduler.add_job(reconcile_job, 'cron', hour='18', minute='0', args=[])
scheduler.start()
