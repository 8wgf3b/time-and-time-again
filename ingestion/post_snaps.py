import aiohttp
from datetime import datetime
from datetime import timedelta
import time
import asyncio
import os
import yaml
from tqdm import tqdm
import pandas as pd
import praw
import pystore


class RedditSnap:
    def __init__(self, login_conf, store_conf):
        with open(login_conf, 'r') as stream:
            self.reddit = praw.Reddit(**yaml.safe_load(stream))
        with open(store_conf, 'r') as stream:
            config = yaml.safe_load(stream)
        self.subreddit = config['subreddit']
        pystore.set_path(config['savefolder'])
        self.store = pystore.store(config['store'])
        self.collection = self.store.collection('psnaps.EOD')
        self.limit = config['initial_limit']


    async def subreddit_post_snaps(self):
        subreddit = self.reddit.subreddit(self.subreddit)
        pbar = tqdm(total=self.limit)
        for post in subreddit.new(limit=self.limit):
            await asyncio.sleep(0)
            pbar.update(1)
            yield post
        pbar.close()

    @staticmethod
    def row_conv(post):
        time_format = "%Y-%m-%dT%H:%M:%S"
        row = [post.id,
               post.subreddit.display_name,
               datetime.utcnow().strftime(time_format),
               post.num_comments,
               post.score,
               post.upvote_ratio]
        return row

    async def store_write(self, subs, df):
        pbar = tqdm(total=len(subs))
        for sub in subs:
            await asyncio.sleep(0)
            temp = df[df['sub'] == sub]
            try:
                item = self.collection.item(sub)
                olddata = item.data
                new_df = olddata.append(temp)
                new_df = new_df.repartition(npartitions=1)
                self.collection.write(item=sub, data=new_df, reload_items=False, overwrite=True)
            except ValueError:
                self.collection.write(sub, temp, reload_items=False)
            pbar.update(1)
        pbar.close()

    async def initiate(self):
        post_gen = self.subreddit_post_snaps()
        columns = ['id', 'sub', 'time', 'num_com', 'score', 'uv_r']
        rows = [self.row_conv(post) async for post in post_gen]
        init = pd.DataFrame(rows, columns=columns)
        init['time'] = pd.to_datetime(init['time'])
        subs = self.subreddit.split('+')
        await self.store_write(subs, init)

    async def update(self):
        subs = self.subreddit.split('+')
        post_ids = []
        pbar = tqdm(total=len(subs))
        for sub in subs:
            df = self.collection.item(sub).to_pandas()
            x = df.groupby('id').agg({'time': ['max', 'min']}).reset_index()
            x.columns = ['id', 'max', 'min']
            first = datetime.utcnow() - x['min'] < pd.Timedelta(days=1)
            last = datetime.utcnow() - x['max'] > pd.Timedelta(minutes=30)
            post_ids += [f't3_{i}' for i in x[first & last]['id']]
            pbar.update(1)
            await asyncio.sleep(0)
        pbar.close()
        columns = ['id', 'sub', 'time', 'num_com', 'score', 'uv_r']
        rows = [self.row_conv(post) for post in self.reddit.info(post_ids)]
        upd = pd.DataFrame(rows, columns=columns)
        upd['time'] = pd.to_datetime(upd['time'])
        await self.store_write(subs, upd)


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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(add(1, 2)))
    loop.close()
