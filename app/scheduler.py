
# TODO async APS

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


class Scheduler:

    def __init__(self):
        self.scheduler = BlockingScheduler()

    def add_daily_job(self, job, hours, minutes):
        trigger = CronTrigger(hour=hours, minute=minutes)
        self.scheduler.add_job(job, trigger)

    def start(self):
        self.scheduler.start()
