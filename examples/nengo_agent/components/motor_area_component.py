
import math
from tf import transformations
import util
import numpy as np

class MotorAreaOperator():
    def __init__(self):
        self.last_angle = None
        self.target_pos = None
        self.output = (0, 0)

    def __get_force_straight(self, ori, pos, vel, target_pos):
        body_euler_yaw = transformations.euler_from_quaternion(ori)[2]
        vel_forward = - util.rotate2D(vel, -body_euler_yaw)[0]
        direction = target_pos - pos
        distance = util.rotate2D(direction, -body_euler_yaw)[0]
        power = 0.15*distance - 20*vel_forward
        return (power, power)

    def __get_force_reach(self, input_dat):
        ori = input_dat[0]
        pos = input_dat[1]
        vel = input_dat[2]
        self.target_pos = input_dat[3]

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
            return self.__get_force_straight(ori, pos, vel, self.target_pos)
        else:
            power = 1.5*angle - 200.0*anguler_vel_yaw
            return (power, -power)

    def fire(self, t, input_dat):
        pos = np.array(input_dat[0:2]) 
        vel = np.array(input_dat[2:4]) 
        ori = np.array(input_dat[4:8])
        target_pos = np.array(input_dat[8:10]) 
        input_dat = (ori, pos, vel, target_pos)
        self.output = self.__get_force_reach(input_dat)
        return self.output
        
    def callback(self):
        return self.output

