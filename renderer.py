from OpenGL.GL import *
from OpenGL.GLU import *

import camera

class Renderer:
    def __init__(self):
        self.width = 1000
        self.height = 700

        self.init_gl()

    def init_gl(self):
        
        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, self.width / self.height, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glClearColor(0.1, 0.1, 0.2, 1)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glDisable(GL_LIGHTING)

    # =========================
    # ESSENCIAL (o que estava faltando)
    # =========================
    def begin_frame(self, camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        camera.apply()

    def end_frame(self):
        pass