import logging
import os

from dotenv import load_dotenv

from cloudership.pubnub_sensors.loader import Loader

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    loader = Loader(subscribe_key=os.environ['PUBNUB_SUBSCRIBE_KEY'],
                    channel=os.environ['PUBNUB_CHANNEL'],
                    client_uuid=os.environ['PUBNUB_CLIENT_UUID'],
                    write_bucket=os.environ['BUCKET'],
                    write_path=os.environ['BUCKET_PATH'])
    loader.start()
