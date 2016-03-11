
import trollius
from trollius import From
from pprint import pprint

import pygazebo.msg.raysensor_pb2

@trollius.coroutine
def publish_loop():
    manager = yield From(pygazebo.connect())

    def callback(data):
        ray = pygazebo.msg.raysensor_pb2.RaySensor()
        msg = ray.FromString(data)

    subscriber = manager.subscribe(
        '/gazebo/default/turtlebot/rack/laser/scan',
        'gazebo.msgs.RaySensor',
        callback)
    yield From(subscriber.wait_for_connection())

    while True:
        yield From(trollius.sleep(1.00))

if __name__ == "__main__":
    loop = trollius.get_event_loop()
    loop.run_until_complete(publish_loop())
