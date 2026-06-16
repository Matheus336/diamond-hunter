from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Camera:
    def __init__(self, player):
        self.player = player
        self.yaw = 0
        self.height = 7
        self.distance = 10

    def update(self, keys):
        if keys[ord("d")]:
            self.yaw -= 1.8
        if keys[ord("a")]:
            self.yaw += 1.8
        if keys[ord("r")]:
            self.height = min(14, self.height + 0.12)
        if keys[ord("f")]:
            self.height = max(3, self.height - 0.12)
        if keys[ord("z")]:
            self.distance = max(5, self.distance - 0.12)
        if keys[ord("x")]:
            self.distance = min(18, self.distance + 0.12)

    def reset(self):
        self.yaw = 0
        self.height = 7
        self.distance = 10

    def apply(self):
        angle = math.radians(self.yaw)
        camera_x = self.player.x + math.sin(angle) * self.distance
        camera_z = self.player.z + math.cos(angle) * self.distance

        gluLookAt(
            camera_x, self.height, camera_z,
            self.player.x, 0, self.player.z,
            0, 1, 0
        )
