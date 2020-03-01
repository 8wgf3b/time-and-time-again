from ingestion.post_snaps import RedditSnap
import asyncio

async def save_snaps():
    x = RedditSnap('configs/login_cred.yml', 'configs/test0.yml')
    await x.initiate()
    await x.update()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_snaps())
    loop.close()
