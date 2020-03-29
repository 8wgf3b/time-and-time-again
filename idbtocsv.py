from ingestion.post_snaps import idb_to_csv
import argh
import asyncio


def main(sub, loc):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(idb_to_csv(sub, loc))

argh.dispatch_command(main)
