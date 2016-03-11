# temporary functions

import math
import numpy as np


def project(vec, direction):
    return np.dot(vec, direction) / (np.linalg.norm(direction)**2) * direction


def rotate2D(vec, angle):
    return (vec[0] * math.cos(angle) - vec[1] * math.sin(angle),
            vec[0] * math.sin(angle) + vec[1] * math.cos(angle))


def angle2D(x, y):
    if np.linalg.norm(x) * np.linalg.norm(y) == 0:
        return 0
    return math.acos(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y)))


def angle2D_sign(x, y):
    try:
        x_by_y = rotate2D(x, -np.angle(complex(y[0], y[1])))
        sign = np.sign(np.angle(complex(x_by_y[0], x_by_y[1])))
        return angle2D(x, y) * sign
    except:
        return 0
