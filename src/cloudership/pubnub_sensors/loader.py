import json
import logging
import sys
from uuid import uuid4

import boto3
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


class Loader:
    def __init__(self, subscribe_key, channel, client_uuid,
                 write_bucket, write_path):
        self.subscribe_key = subscribe_key
        self.channel = channel
        self.uuid = client_uuid

        self._write_path = write_path
        self._write_bucket = write_bucket

        self._s3 = boto3.client('s3')
        assert self._s3.list_objects_v2(Bucket=self._write_bucket, MaxKeys=1)

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = self.subscribe_key
        pnconfig.uuid = str(self.uuid)

        self._pubnub = PubNub(pnconfig)
        subscribe_callback = _PubNubSubscribeCallback(s3_client=self._s3,
                                                      write_bucket=self._write_bucket,
                                                      write_path=self._write_path)
        self._pubnub.add_listener(subscribe_callback)
        self._pubnub_subscribe_builder = self._pubnub.subscribe().channels(self.channel)

    def start(self):
        self._pubnub_subscribe_builder.execute()


class _PubNubSubscribeCallback(SubscribeCallback):
    def __init__(self, s3_client, write_bucket, write_path):
        self._write_bucket = write_bucket
        self._write_path = write_path
        self._s3 = s3_client
        super().__init__()

    def presence(self, _pubnub, presence):
        pass

    def status(self, _pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            logging.info('{"event": "Unexpected Disconnect"}')

        elif status.category == PNStatusCategory.PNConnectedCategory:
            logging.info('{"event": "CONNECTED"}')

        elif status.category == PNStatusCategory.PNReconnectedCategory:
            logging.info('{"event": "RECONNECTED"}')

        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            logging.error('{"event": "Decryption Error"}')
            sys.exit("FATAL")

    def message(self, _pubnub, message):
        object_key = f"{self._write_path}/{message.timetoken}.json"
        logging.info({'event': 'MESSAGE',
                       'message': message.message,
                       'time': message.timetoken})
        self._s3.put_object(
            Bucket=self._write_bucket,
            Key=object_key,
            Body=json.dumps(message.message))
