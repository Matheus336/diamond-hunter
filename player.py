from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

class Player:
    def __init__(self):
        self.x = 0
        self.z = 0
        self.speed = 0.15

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
        glTranslatef(self.x, 0.6, self.z)

        glColor3f(0.2, 0.4, 1)

        quad = gluNewQuadric()
        gluSphere(quad, 0.5, 20, 20)

        glPopMatrix()