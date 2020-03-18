import aiohttp
import asyncio
import yaml
import praw, prawcore
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
                logger.warning(f'{e} - {post}')
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
        logger.info(f'fetched {len(data)} entries from pushshift')
        for i in range(0, len(data), 100):
            yield [f"t3_{i['id']}" for i in data[i: i + 100]]

    async def write(self, post):
        try:
            row = PostSnaps(self.subreddit, post.id, post.num_comments,
                            post.score, post.upvote_ratio)
        except prawcore.exceptions.ServerError as e:
            logger.warning(f'{e} - {post}')
            await asyncio.sleep(30)
            await self.write(post)
        await self.client.write(row)


    async def initiate(self):
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
            async for ids in self.get_latest_posts(after=after):
                logger.info(f'initiating {len(ids)} entries: {self.subreddit}')
                await self.save_posts_by_id(ids)
                logger.info(f'initiated {len(ids)} entries: {self.subreddit}')
        except Exception:
            logger.exception('Failed fetching from pushshift :(')

    async def update(self):
        qs = f"""
SELECT uv_r, id
FROM PostSnaps
WHERE sub='{self.subreddit}' and time > now() - 1d and time < now() - {self.update_delay - 5}m"""
        results = await self.client.query(qs, chunked=True, chunk_size=100)
        async for result in results:
            try:
                values = result['results'][0]['series'][0]['values']
                ids = set(i[2] for i in values)
                ids = [f't3_{i}' for i in ids]
                logger.info(f'updating {len(ids)} entries: {self.subreddit}')
                await self.save_posts_by_id(ids)
                logger.info(f'updated {len(ids)} entries: {self.subreddit}')
            except KeyError:
                logger.warning(f'No older entries?!: {self.subreddit}')

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
