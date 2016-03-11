import nengo
from nengo.utils.progress import ProgressTracker

import trollius
from trollius import From
import pygazebo.msg.joint_cmd_pb2
import numpy as np



class SampleAgent(nengo.Simulator):

    def set_modules(self, visual_comp, action_comp):
        self.sensor_comp = visual_comp
        self.action_comp = action_comp
        
    def run_steps(self, steps, progress_bar=True):
        loop = trollius.get_event_loop()
        loop.run_until_complete(self.publish_loop(steps, progress_bar))
                
    @trollius.coroutine
    def publish_loop(self, steps, progress_bar=True):
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

        with ProgressTracker(steps, progress_bar) as progress:
            for i in range(steps):
                self.step()
                force = self.action_comp.callback()

                max_force_strength = 0.7
                force = np.clip(force, -max_force_strength, max_force_strength)

                msg_right_wheel.force, msg_left_wheel.force = force
                From(publisher.publish(msg_left_wheel))
                From(publisher.publish(msg_right_wheel))
                yield From(trollius.sleep(0.01))    


