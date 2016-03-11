
import trollius
from trollius import From
import pygazebo.msg.joint_cmd_pb2
import numpy as np


class SampleAgent():
    def __init__(self, brica_agent, visual_comp, action_comp):
        self.brica_agent = brica_agent
        self.sensor_comp = visual_comp
        self.action_comp = action_comp

    def run(self):
        loop = trollius.get_event_loop()
        loop.run_until_complete(self.publish_loop())

    @trollius.coroutine
    def publish_loop(self):
        manager = yield From(pygazebo.connect())

        def callback_pose(data):
            self.sensor_comp.callback(data)

        publisher = yield From(
            manager.advertise('/gazebo/default/turtlebot/joint_cmd',
                              'gazebo.msgs.JointCmd'))

        subscriber_pose = manager.subscribe(
            '/gazebo/default/pose/info',
            'gazebo.msgs.PosesStamped',
            callback_pose)
        yield From(subscriber_pose.wait_for_connection())

        msg_left_wheel = pygazebo.msg.joint_cmd_pb2.JointCmd()
        msg_left_wheel.name = 'turtlebot::create::left_wheel'
        msg_right_wheel = pygazebo.msg.joint_cmd_pb2.JointCmd()
        msg_right_wheel.name = 'turtlebot::create::right_wheel'

        print "wait for connection.."
        yield From(trollius.sleep(1.0))

        while True:
            self.brica_agent.step()
            force = self.action_comp.get_result("out_force")

            max_force_strength = 0.7
            force = np.clip(force, -max_force_strength, max_force_strength)

            msg_right_wheel.force, msg_left_wheel.force = force
            From(publisher.publish(msg_left_wheel))
            From(publisher.publish(msg_right_wheel))
            yield From(trollius.sleep(0.00))
