import logging
import sys
from uuid import uuid4

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


class Loader:
    def __init__(self, subscribe_key, publish_key, channel, client_uuid=None):
        self.uuid = client_uuid or uuid4()
        self.publish_key = publish_key
        self.subscribe_key = subscribe_key
        self.channel = channel

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = self.subscribe_key
        pnconfig.publish_key = self.publish_key
        pnconfig.uuid = str(self.uuid)

        self._pubnub = PubNub(pnconfig)
        self._pubnub.add_listener(_PubNubSubscribeCallback())
        self._pubnub_subscribe_builder = self._pubnub.subscribe().channels(self.channel)

    def start(self):
        self._pubnub_subscribe_builder.execute()


class _PubNubSubscribeCallback(SubscribeCallback):
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
        print(message.message)
