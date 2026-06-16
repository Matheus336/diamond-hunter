from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

class Player:
    def __init__(self):
        self.x = 0
        self.z = 0
        self.speed = 0.15

    def reset(self):
        self.x = 0
        self.z = 0

    def update(self, keys, world):

        nx, nz = self.x, self.z

        if keys[pygame.K_w]:
            nz -= self.speed
        if keys[pygame.K_s]:
            nz += self.speed
        if keys[pygame.K_a]:
            nx -= self.speed
        if keys[pygame.K_d]:
            nx += self.speed

        if not world.collides(nx, nz):
            self.x, self.z = nx, nz

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, 0, self.z)

        glColor3f(0.18, 0.36, 0.95)

        quad = gluNewQuadric()
        glPushMatrix()
        glTranslatef(0, 0.75, 0)
        glScalef(0.55, 0.85, 0.55)
        gluSphere(quad, 0.7, 24, 24)
        glPopMatrix()

        glColor3f(0.95, 0.78, 0.55)
        glPushMatrix()
        glTranslatef(0, 1.65, 0)
        gluSphere(quad, 0.35, 20, 20)
        glPopMatrix()

        glColor3f(0.08, 0.12, 0.18)
        glPushMatrix()
        glTranslatef(-0.2, 0.25, 0.1)
        glScalef(0.18, 0.5, 0.18)
        gluSphere(quad, 0.7, 12, 12)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.2, 0.25, 0.1)
        glScalef(0.18, 0.5, 0.18)
        gluSphere(quad, 0.7, 12, 12)
        glPopMatrix()

        glPopMatrix()
