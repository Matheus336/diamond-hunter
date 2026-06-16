from OpenGL.GL import *
from OpenGL.GLU import *

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
        glClearColor(0.04, 0.05, 0.08, 1)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 12, 8, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.25, 0.25, 0.28, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.85, 0.82, 0.72, 1))
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

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
