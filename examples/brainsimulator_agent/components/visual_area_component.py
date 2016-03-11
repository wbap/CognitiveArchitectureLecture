
import brica1
import numpy as np
import pygazebo.msg.poses_stamped_pb2
import pickle

class VisualAreaComponent(brica1.Component):
    def __init__(self):
        super(VisualAreaComponent, self).__init__()
        self.last_position = np.array((0, 0))

    def __position_to_area_id(self, pos2d):
        x = pos2d[0]
        y = pos2d[1]
        radius = 1
        maze_width = 1

        if x*x + y*y < radius*radius:
            return (0, 0)

        areaIdX = 0
        if x < maze_width*0.5:
            areaIdX = -1
        if x > maze_width*0.5:
            areaIdX = 1

        areaIdY = 0
        if y < maze_width*0.5:
            areaIdY = -1
        if y > maze_width*0.5:
            areaIdY = 1
        return (areaIdX, areaIdY)
    
    def get_server_response(self):
        return self.server_response
    
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

        self.set_state("out_body_velocity",
                       np.array((vel[0], vel[1])).astype(np.float32))
        self.set_state("out_body_position",
                       position.astype(np.float32))
        self.set_state("out_body_orientation",
                       orientation.astype(np.float32))
        
        self.server_response = {"out_body_velocity":vel.tolist(),
                                "out_body_position":position.tolist(),
                                "out_body_orientation":orientation.tolist()}
        #print self.server_response

    def fire(self):
        for key in self.states.keys():
            self.results[key] = self.states[key]
