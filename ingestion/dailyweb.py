from aiohttp import web
from aioinflux import *
from typing import NamedTuple
from datetime import datetime
import logging


logger = logging.getLogger('TS.webintake')

@lineprotocol
class Weight(NamedTuple):
    weight: FLOAT

async def hello(request):
    return web.Response(text="Hello, world")

async def load_wt(request):
    with open('htmls/wt.html') as f:
        content = f.read()
    logger.info('Initial wt page load')
    return web.Response(text=content, content_type='text/html')

async def wt(request):
    client = InfluxDBClient(db='Lifestyle')
    data = await request.post()
    wght = float(data['weight'])
    await client.write(Weight(wght))
    logger.info(f'pushed {wght} kgs')
    return web.Response(text=f'{datetime.utcnow()}: {wght}')