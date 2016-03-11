
import numpy as np
import pygazebo.msg.poses_stamped_pb2

class VisualAreaOperator():
    def __init__(self):
        self.last_position = np.array((0, 0))
        self.status = (0,) * 8
        
    def callback(self, data):
        pose = pygazebo.msg.poses_stamped_pb2.PosesStamped()
        message = pose.FromString(data)

        turtlebot_id = 0
        if message.pose[turtlebot_id].name != "turtlebot":
            raise Exception("message.pose[0].name is not turtlbot")

        position = np.array((
            message.pose[turtlebot_id].position.x,
            message.pose[turtlebot_id].position.y))
        orientation = np.array((
            message.pose[turtlebot_id].orientation.x,
            message.pose[turtlebot_id].orientation.y,
            message.pose[turtlebot_id].orientation.z,
            message.pose[turtlebot_id].orientation.w))

        vel = self.last_position - position
        self.last_position = position
        
        
        self.status = (position[0],position[1],
                       vel[0], vel[1], 
                       orientation[0],orientation[1],orientation[2],orientation[3])
        
    def fire(self, t, input_dat):
        return self.status
