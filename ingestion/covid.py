import aiohttp
import asyncio
import csv
from aioinflux import *
from tqdm import tqdm
from typing import NamedTuple
from pprint import pprint
import logging


logger = logging.getLogger('TS.covid')

@lineprotocol
class DistrictWise(NamedTuple):
    state: TAG
    district: TAGENUM
    active: INT
    confirmed: INT
    dead: INT
    recovered: INT

@lineprotocol
class StateWise(NamedTuple):
    state: TAG
    active: INT
    confirmed: INT
    dead: INT
    recovered: INT


class Covid:
    def __init__(self):
        self.client = InfluxDBClient(db='Covid')
        self.base_url = 'https://api.covid19india.org/'

    async def get_states_data(self):
        url = f'{self.base_url}data.json'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = (await r.json())['statewise']
                    logger.info('Downloaded states data')
                    for state in data:
                        row = StateWise(state['state'].lower(), state['active'], state['confirmed'],
                                            state['deaths'], state['recovered'])
                        await self.client.write(row)
                    logger.info('Pushed the states data')
        except Exception:
            logger.exception('Current states data failed to br fetched :(')

    async def get_states_hist(self):
        pass

    async def get_dist_data(self):
        url = f'{self.base_url}v2/state_district_wise.json'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = (await r.json())
                    logger.info('Downloaded dist. data')
                    for state in data:
                        st_name = state['state'].lower()
                        for dist in state['districtData']:
                            row = DistrictWise(st_name, dist['district'].lower().replace(' ', '_'),
                                               dist['active'], dist['confirmed'],
                                               dist['deceased'], dist['recovered'])
                            await self.client.write(row)
                    logger.info('Pushed the dist. data')
        except Exception:
            logger.exception('Current states data failed to br fetched :(')

    async def write(self, type, dic_row):
        if type == 'S':
            row = StateWise(**dic_row)
        elif type == 'D':
            row = DistrictWise(**dic_row)
        await self.client.write(row)



if __name__ == '__main__':
    from post_snaps import init_db

    z = Covid()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db('Covid'))
    loop.run_until_complete(z.get_dist_data())
