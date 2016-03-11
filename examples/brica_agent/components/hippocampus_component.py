
import brica1
import numpy as np
import random


class HippocampusComponent(brica1.Component):
    def __init__(self):
        super(HippocampusComponent, self).__init__()
        self.target_pos = np.array((1.4, 1.4))

    def __next_place_id(self, current_place_id):
        if current_place_id == (0, 0):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
        else:
            x = 0
            y = 0

        return (x, y)

    def __to_place_position(self, area_id):
        k = 1.4
        return np.array((area_id[0] * k, area_id[1] * k))

    def __to_place_id(self, pos2d):
        x = pos2d[0]
        y = pos2d[1]
        radius = 1
        maze_width = 1

        if x*x + y*y < radius*radius:
            return (0, 0)

        areaIdX = 0
        if x < -maze_width*0.5:
            areaIdX = -1
        if x > maze_width*0.5:
            areaIdX = 1

        areaIdY = 0
        if y < -maze_width*0.5:
            areaIdY = -1
        if y > maze_width*0.5:
            areaIdY = 1

        return (areaIdX, areaIdY)

    def fire(self):
        pos = self.inputs["in_body_position"].astype(np.float32)
        dis = np.linalg.norm(self.target_pos - pos)

        if dis < 0.15:
            current_place_id = self.__to_place_id(pos)
            next_place_id = self.__next_place_id(current_place_id)
            self.target_pos = self.__to_place_position(next_place_id)
            print "change target position", self.target_pos

        self.results["out_target_position"] = self.target_pos
