__author__ = 'Peter'
import math
from math import degrees

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

    def get_bearing(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        angle = math.atan2(dy, dx)
        return (math.pi/2 - angle)%(2*math.pi)

    def get_angle(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.atan2(dy, dx)

    def __add__(self, other):
        return Position((self.x + other.x),(self.y + other.y))

    def __sub__(self, other):
        return Position((self.x - other.x),(self.y - other.y))

    def __str__(self):
        return "({},{})".format(self.x,self.y)

class Vector:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        # self.accelerationX = 0
        # self.accelerationY = 0
        # self.torqueX = 0
        # self.torqueY = 0
        self.x = 300
        self.y = 400

    def update(self, timestep = 1):
        y = self.y
        dy = self.dy
        x = self.x
        dx = self.dx
        y += dy * timestep
        x += dx * timestep
        self.y = y
        self.x = x

    @property
    def position(self):
        return Position(self.x,self.y)

    @property
    def orientation(self):
        return math.atan2(self.dy, self.dx)

def get_bearing(toX, toY, fromX, fromY):
    dx = toX - fromX
    dy = toY - fromY
    angle = math.atan2(dy, dx)
    # print("To:({},{}) angle:{}, degrees:{}".format(toX, toY, angle, degrees(angle)))
    b = (math.pi/2 - angle)%(2*math.pi)
    print("Bearing: {}, degrees: {}".format(b, degrees(b)))

if __name__ == "__main__":
    testV3 = Vector()
    testV4 = Vector()
    testV3.x = 0
    testV3.y = 0
    testV4.x = 0
    testV4.y = -1
    distance = testV3.position.get_distance(testV4)
    angle = testV3.position.get_bearing(testV4)
    print("From:{} To:{} Distance: {}, Bearing: {}".format(testV3.position, testV4.position, distance, angle))