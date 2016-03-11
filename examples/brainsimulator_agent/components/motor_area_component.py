
import math
from tf import transformations
import brica1
import util
import numpy as np


class MotorAreaComponent(brica1.Component):
    def __init__(self):
        super(MotorAreaComponent, self).__init__()
        self.last_angle = None
        self.target_pos = None
        self.results["out_force"] = (0, 0)

    def __get_force_straight(self, target_pos):
        vel = self.inputs["in_body_velocity"].astype(np.float32)
        pos = self.inputs["in_body_position"].astype(np.float32)
        ori = self.inputs["in_body_orientation"].astype(np.float32)

        body_euler_yaw = transformations.euler_from_quaternion(ori)[2]
        vel_forward = - util.rotate2D(vel, -body_euler_yaw)[0]
        direction = target_pos - pos
        distance = util.rotate2D(direction, -body_euler_yaw)[0]
        power = 0.15*distance - 20*vel_forward
        return power, power

    def __get_force_reach(self):
        ori = self.inputs["in_body_orientation"].astype(np.float32)
        pos = self.inputs["in_body_position"].astype(np.float32)
        target_pos = self.inputs["in_target_position"].astype(np.float32)
        self.target_pos = target_pos

        body_euler_yaw = transformations.euler_from_quaternion(ori)[2]
        direction = self.target_pos - pos
        distance = np.linalg.norm(direction)
        dir_world_pos = (- math.cos(body_euler_yaw), -math.sin(body_euler_yaw))
        angle = util.angle2D_sign((direction[0], direction[1]), dir_world_pos)

        if self.last_angle is None:
            self.last_angle = angle
        if self.last_angle - angle > math.pi:
            anguler_vel_yaw = 0
        elif self.last_angle - angle < -math.pi:
            anguler_vel_yaw = 0
        else:
            anguler_vel_yaw = self.last_angle - angle
        self.last_angle = angle

        if math.fabs(angle) < math.pi / 18.0 or distance < 0.3:
            return self.__get_force_straight(self.target_pos)
        else:
            power = 1.5*angle - 200.0*anguler_vel_yaw
            return power, -power
        
    def set_client_request(self, force):
        self.results["out_force"] = force

    def fire(self):
        pass
        #self.results["out_force"] = self.__get_force_reach()
