
import trollius
from trollius import From

import pygazebo.msg.joint_cmd_pb2

@trollius.coroutine
def publish_loop():
    manager = yield From(pygazebo.connect())

    publisher_model = yield From(
       manager.advertise('/gazebo/default/model/modify',
                         'gazebo.msgs.Model'))

    msg_model = pygazebo.msg.model_pb2.Model()
    msg_model.name = "turtlebot"
    msg_model.id = 129
    msg_model.pose = pygazebo.msg.pose_pb2.Pose()
    msg_model.pose.position.x = 0
    msg_model.pose.position.y = 0
    msg_model.pose.position.z = 0
    msg_model.pose.quaternion = pygazebo.msg.quaternion_pb2.Quaternion()

    while True:
        From(publisher_model.publish(msg_model))
        yield From(trollius.sleep(1.0))

loop = trollius.get_event_loop()
loop.run_until_complete(publish_loop())
