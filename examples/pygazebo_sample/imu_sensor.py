
import trollius
from trollius import From

import pygazebo.msg.imu_pb2

@trollius.coroutine
def publish_loop():
    manager = yield From(pygazebo.connect())

    def callback_imu(data):
        imu = pygazebo.msg.imu_pb2.IMU()
        message = imu.FromString(data)
        angular_velocity = message.angular_velocity
        print angular_velocity

    subscriber_imu = manager.subscribe(
        '/gazebo/default/turtlebot/rack/imu_sensor/imu',
        'gazebo.msgs.IMU',
        callback_imu)
    yield From(subscriber_imu.wait_for_connection())

    while True:
        yield From(trollius.sleep(1.00))

if __name__ == "__main__":
    loop = trollius.get_event_loop()
    loop.run_until_complete(publish_loop())
