import os
import django
from apscheduler.schedulers.blocking import BlockingScheduler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connector.settings")
django.setup()
scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=3)
def timed_job():
    from connector.engine import Engine
    engine = Engine()
    engine.reconcile_all()


scheduler.start()
