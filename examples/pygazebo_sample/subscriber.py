
import trollius
from trollius import From

import pygazebo.msg.poses_stamped_pb2

import logging
logging.basicConfig()


@trollius.coroutine
def publish_loop():
    manager = yield From(pygazebo.connect())

    def callback(data):
        pose = pygazebo.msg.poses_stamped_pb2.PosesStamped()
        message = pose.FromString(data)
        print message.pose[0]

    subscriber = manager.subscribe('/gazebo/default/pose/info',
                                   'gazebo.msgs.PosesStamped',
                                   callback)

    yield From(subscriber.wait_for_connection())
    while(True):
        yield From(trollius.sleep(1.0))
        print('wait...')
    print(dir(manager))

loop = trollius.get_event_loop()
loop.run_until_complete(publish_loop())
