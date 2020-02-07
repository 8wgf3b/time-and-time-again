import praw
import time
import asyncio
import os

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     username=os.environ['USERNAME'],
                     password=os.environ['PASSWORD'],
                     user_agent=os.environ['USER_AGENT'])

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
