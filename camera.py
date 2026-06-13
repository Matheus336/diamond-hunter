from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self, player):
        self.player = player

    def apply(self):
        gluLookAt(
            self.player.x, 6, self.player.z + 8,
            self.player.x, 0, self.player.z,
            0, 1, 0
        )