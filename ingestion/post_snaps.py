import aiohttp
import asyncio
import os
import yaml
from tqdm import tqdm
import pandas as pd
import praw
from aioinflux import *
from typing import NamedTuple
from pprint import pprint


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
        self.limit = config['initial_limit']
        self.client = InfluxDBClient(db='PostSnaps')

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

    async def get_latest_posts(self, after=None, limit=1000):
        sub_url = 'https://api.pushshift.io/reddit/submission/search'
        params = {'limit': limit, 'fields': 'id'}
        sub = self.subreddit
        if sub != 'all':
            params['sub'] = sub
        if after:
            params['after'] = after
        else:
            params['limit'] = 100
        async with aiohttp.ClientSession() as session:
            async with session.get(sub_url, params=params) as r:
                data = (await r.json())['data']
        for i in range(0, len(data), 100):
            yield [f"t3_{i['id']}" for i in data[i: i + 100]]

    async def write(self, post):
        row = PostSnaps(post.subreddit.display_name, post.id, post.num_comments,
                      post.score, post.upvote_ratio)
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
        async for chonk in self.get_latest_posts(after=after):
            await self.save_posts_by_id(chonk)

    async def update(self):
        qs = f"""
SELECT uv_r, id
FROM PostSnaps
WHERE sub='{self.subreddit}' and time > now() - 1d and time < now() - 30m"""
        results = await self.client.query(qs, chunked=True, chunk_size=100)
        async for result in results:
            try:
                values = result['results'][0]['series'][0]['values']
                ids = [f't3_{i[2]}' for i in values]
                await self.save_posts_by_id(ids)
            except KeyError:
                pprint(result)

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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(add(1, 2)))
    loop.close()
