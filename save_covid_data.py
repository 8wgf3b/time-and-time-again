from ingestion.covid import Covid
from ingestion.post_snaps import init_db
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logger import logger
from datetime import datetime


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(init_db, 'interval', days=1, args=['Covid'])
    cov = Covid()
    scheduler.add_job(cov.get_states_data, 'interval', hours=6, misfire_grace_time=600)
    scheduler.add_job(cov.get_dist_data, 'interval', hours=6, misfire_grace_time=600)
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_db('Covid'))
        loop.run_until_complete(cov.get_dist_data())
        loop.run_until_complete(cov.get_states_data())
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Closing program...')
