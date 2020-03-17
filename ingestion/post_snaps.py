import aiohttp
import asyncio
import yaml
import praw
from aioinflux import *
from typing import NamedTuple
from pprint import pprint
import logging


logger = logging.getLogger('TS.postsnaps')


async def init_db():
    async with InfluxDBClient(db='PostSnaps') as client:
        await client.create_database(db='PostSnaps')
    logger.info("Creating database if it ain't")


@lineprotocol
class PostSnaps(NamedTuple):
    sub: TAG
    id: TAGENUM
    num_com: INT
    score: INT
    uv_r: FLOAT


class RedditLogin:
    def __init__(self, login_conf):
        with open(login_conf, 'r') as stream:
            self.reddit = praw.Reddit(**yaml.safe_load(stream))

class RedditSnap:
    def __init__(self, Reddit, store_conf):
        self.reddit = Reddit.reddit
        with open(store_conf, 'r') as stream:
            config = yaml.safe_load(stream)
        self.subreddit = config['subreddit']
        self.client = InfluxDBClient(db='PostSnaps')
        self.init_delay = config['init_delay']
        self.update_delay = config['update_delay']

    async def subreddit_post_snaps(self):
        subreddit = self.reddit.subreddit(self.subreddit)
        pbar = tqdm(total=self.limit)
        for post in subreddit.new(limit=self.limit):
            await asyncio.sleep(0)
            pbar.update(1)
            yield post
        pbar.close()

    async def save_posts_by_id(self, ids):
        posts = self.reddit.info(ids)
        for post in posts:
            try:
                await self.write(post)
            except TypeError:
                print(f'TE {post.subreddit.display_name}: {post.id}')
            except prawcore.exceptions.ServerError as e:
                print(e)
                await asyncio.sleep(30)
                await self.write(post)

    async def get_latest_posts(self, after=None, limit=1000):
        sub_url = 'https://api.pushshift.io/reddit/submission/search'
        params = {'limit': limit, 'fields': 'id'}
        sub = self.subreddit
        if sub != 'all':
            params['subreddit'] = sub
        if after:
            params['after'] = after
        else:
            params['limit'] = 100
        async with aiohttp.ClientSession() as session:
            async with session.get(sub_url, params=params) as r:
                data = (await r.json())['data']
        logger.info(f'{len(data)} entries')
        for i in range(0, len(data), 100):
            yield [f"t3_{i['id']}" for i in data[i: i + 100]]

    async def write(self, post):
        try:
            row = PostSnaps(post.subreddit.display_name, post.id, post.num_comments,
                            post.score, post.upvote_ratio)
        except prawcore.exceptions.ServerError as e:
            logger.exception(f'{post}')
            await asyncio.sleep(30)
            await self.write(post)
        await self.client.write(row)


    async def initiate(self):
        logger.info(f'initiating {self.subreddit}...')
        qs = f"""
SELECT last(uv_r), id
FROM PostSnaps
WHERE sub='{self.subreddit}'"""
        results = await self.client.query(qs, epoch='s')
        try:
            after = str(results['results'][0]['series'][0]['values'][0][0])
        except KeyError:
            after = None
        try:
            async for chonk in self.get_latest_posts(after=after):
                await self.save_posts_by_id(chonk)
            logger.info(f'initiated {self.subreddit}!')
        except Exception:
            logger.exception('Failed fetching from pushshift :(')

    async def update(self):
        logger.info(f'Updating {self.subreddit}...')
        qs = f"""
SELECT uv_r, id
FROM PostSnaps
WHERE sub='{self.subreddit}' and time > now() - 1d and time < now() - {self.update_delay - 5}m"""
        results = await self.client.query(qs, chunked=True, chunk_size=100)
        async for result in results:
            try:
                values = result['results'][0]['series'][0]['values']
                ids = [f't3_{i[2]}' for i in values]
                await self.save_posts_by_id(ids)
            except KeyError:
                logger.exception('No older entries?!')
        logger.info(f'Updated {self.subreddit}!')

'''
def gap_ensurer(gap):
    def wrap(func):
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            diff = gap - end + start
            diff = max(0, diff)
            print(diff)
            await asyncio.sleep(diff)
            return result
        return wrapper
    return wrap


@gap_ensurer(1)
def add(a, b):
    return a + b
'''
