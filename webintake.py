from ingestion.dailyweb import hello, load_wt, wt
from ingestion.post_snaps import init_db
from aiohttp import web
from logger import logger
import asyncio

if __name__ == '__main__':
    app = web.Application()

    routes = [web.get('/', hello), web.get('/wt', load_wt),
              web.post('/wt', wt)]

    app.add_routes(routes)
    logger.info('Adding routes')
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_db('Lifestyle'))
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Closing program...')
    logger.info('Starting the web app')
    web.run_app(app)
