from ingestion.post_snaps import RedditSnap, RedditLogin, init_db
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from glob import glob
from logger import logger


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(init_db, 'interval', days=1)
    reddit = RedditLogin('configs/login_cred.yml')
    logger.debug('Loaded reddit credentials')
    for conf in glob('configs/PS_configs/*.yml'):
        x = RedditSnap(reddit, conf)
        scheduler.add_job(x.initiate, 'interval', minutes=x.init_delay)
        scheduler.add_job(x.update, 'interval', minutes=x.update_delay)
        logger.info(f'Added {x.subreddit} to scheduler')
    scheduler.start()
    logger.info('started the scheduler')
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_db())
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Closing program...')
