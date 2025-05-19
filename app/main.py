import os
from dotenv import load_dotenv
from feeder import Feeder
from networker import Networker
from db import Database
import logging
from scheduler import Scheduler


load_dotenv()

loglevel = os.getenv('loglevel').upper()
log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}
logging.basicConfig(level=log_levels[loglevel],
                    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.info(f'loglevel is {loglevel}')

USER_AGENT = os.getenv('User-Agent')
UI = os.getenv('ui')
SESSID_LONG = os.getenv('sessid_long')
SESSID_SHORT = os.getenv('sessid_short')
networker = Networker(user_agent=USER_AGENT, ui=UI, sessid_long=SESSID_LONG, sessid_short=SESSID_SHORT)

DB = os.getenv('db')
HOST = os.getenv('db_host')
PORT = os.getenv('db_port')
USER = os.getenv('db_user')
PASS = os.getenv('db_password')
db_url = f'postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}'
db_url = os.getenv('DATABASE_URL', db_url)
logging.debug(db_url)
database = Database(db_url)

SP = int(os.getenv('start_page_number'))
EP = int(os.getenv('end_page_number'))
batch_size = int(os.getenv('async_batch_size'))
feeder = Feeder(networker, start_page=SP, end_page=EP, database=database, async_batch_size=batch_size)

scheduler = Scheduler()

START_HOURS = int(os.getenv('start_hours'))
START_MINUTES = int(os.getenv('start_minutes'))
scheduler.add_daily_job(feeder.run, hours=START_HOURS, minutes=START_MINUTES)

DUMP_HOURS = int(os.getenv('dump_hours'))
DUMP_MINUTES = int(os.getenv('dump_minutes'))
scheduler.add_daily_job(database.dump, hours=DUMP_HOURS, minutes=DUMP_MINUTES)

scheduler.start()
