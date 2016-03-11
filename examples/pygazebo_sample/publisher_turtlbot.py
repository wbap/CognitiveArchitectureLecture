
import trollius
from trollius import From

import pygazebo.msg.joint_cmd_pb2

@trollius.coroutine
def publish_loop():
    manager = yield From(pygazebo.connect())

    publisher = yield From(
        manager.advertise('/gazebo/default/turtlebot/joint_cmd',
                          'gazebo.msgs.JointCmd'))

    msg_left_wheel = pygazebo.msg.joint_cmd_pb2.JointCmd()
    msg_left_wheel.name = 'turtlebot::create::left_wheel'
    msg_left_wheel.force = -0.3

    msg_right_wheel = pygazebo.msg.joint_cmd_pb2.JointCmd()
    msg_right_wheel.name = 'turtlebot::create::right_wheel'
    msg_right_wheel.force = 0.3

    while True:
        yield From(publisher.publish(msg_left_wheel))
        yield From(publisher.publish(msg_right_wheel))
        msg_right_wheel.force *= -1
        msg_left_wheel.force *= -1
        yield From(trollius.sleep(3.01))

loop = trollius.get_event_loop()
loop.run_until_complete(publish_loop())



