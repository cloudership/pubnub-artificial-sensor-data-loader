import cloudership
from cloudership.pubnub_sensors import Loader


def test_answer():
    assert cloudership.pubnub_sensors.Loader == cloudership.pubnub_sensors.loader.Loader
    assert type(Loader()) == Loader
    assert 2*4 == 8
