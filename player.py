import math

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

class Player:
    def __init__(self):
        self.x = 0
        self.z = 0
        self.speed = 0.15
        self.facing_yaw = 0

    def reset(self):
        self.x = 0
        self.z = 0
        self.facing_yaw = 0

    def update(self, keys, world, camera_yaw):
        self.facing_yaw = camera_yaw
        angle = math.radians(camera_yaw)
        forward_x = -math.sin(angle)
        forward_z = -math.cos(angle)
        right_x = math.cos(angle)
        right_z = -math.sin(angle)

        move_x = 0
        move_z = 0

        if keys[pygame.K_w]:
            move_x += forward_x
            move_z += forward_z
        if keys[pygame.K_s]:
            move_x -= forward_x
            move_z -= forward_z
        

        length = math.hypot(move_x, move_z)
        if length:
            move_x = move_x / length * self.speed
            move_z = move_z / length * self.speed

        nx = self.x + move_x
        nz = self.z + move_z

        if not world.collides(nx, nz):
            self.x, self.z = nx, nz

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, 0, self.z)
        glRotatef(self.facing_yaw, 0, 1, 0)

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

        glColor3f(0.02, 0.03, 0.04)
        glPushMatrix()
        glTranslatef(0, 1.68, -0.32)
        glScalef(0.38, 0.12, 0.08)
        gluSphere(quad, 0.7, 12, 12)
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
