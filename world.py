import random
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math


class World:
    def __init__(self):
        # ----------------------------
        # CRISTAIS
        # ----------------------------
        self.crystals = [
            [random.randint(-8, 8), 0.5, random.randint(-8, 8)]
            for _ in range(6)
        ]

        # ----------------------------
        # OBSTÁCULOS
        # ----------------------------
        self.obstacles = [
            (-3, 0, -3),
            (3, 0, -3),
            (-3, 0, 3),
            (3, 0, 3)
        ]

        self.collected = 0
        self.start_time = pygame.time.get_ticks()

    # ----------------------------
    # COLISÃO COM OBSTÁCULOS
    # ----------------------------
    def collides(self, x, z):
        for ox, oy, oz in self.obstacles:
            if abs(x - ox) < 1 and abs(z - oz) < 1:
                return True
        return False

    # ----------------------------
    # UPDATE (COLETA)
    # ----------------------------
    def update(self, player, audio):

        remaining = []

        for cx, cy, cz in self.crystals:
            dx = abs(player.x - cx)
            dz = abs(player.z - cz)

            if dx < 1 and dz < 1:
                self.collected += 1

                if audio:
                    audio.play_collect()
            else:
                remaining.append([cx, cy, cz])

        self.crystals = remaining

    # ----------------------------
    # CHÃO
    # ----------------------------
    def draw_ground(self):
        glColor3f(0.2, 0.7, 0.2)

        glBegin(GL_QUADS)
        glVertex3f(-15, 0, -15)
        glVertex3f(15, 0, -15)
        glVertex3f(15, 0, 15)
        glVertex3f(-15, 0, 15)
        glEnd()

    # ----------------------------
    # DRAW
    # ----------------------------
    def draw(self):

        # chão
        self.draw_ground()

        # ----------------------------
        # OBSTÁCULOS
        # ----------------------------
        glColor3f(0.8, 0.2, 0.2)

        for ox, oy, oz in self.obstacles:
            glPushMatrix()
            glTranslatef(ox, oy, oz)

            quad = gluNewQuadric()
            gluSphere(quad, 0.5, 10, 10)

            glPopMatrix()

        # ----------------------------
        # CRISTAIS
        # ----------------------------
        angle = pygame.time.get_ticks() / 5.0
        pulse = 1 + 0.2 * math.sin(pygame.time.get_ticks() / 300.0)

        glColor3f(0, 1, 1)

        for cx, cy, cz in self.crystals:

            glPushMatrix()

            glTranslatef(cx, cy, cz)
            glRotatef(angle, 0, 1, 0)
            glScalef(pulse, pulse, pulse)

            glBegin(GL_TRIANGLES)

            # topo
            glVertex3f(0, 1, 0)
            glVertex3f(-0.5, 0, -0.5)
            glVertex3f(0.5, 0, -0.5)

            glVertex3f(0, 1, 0)
            glVertex3f(0.5, 0, 0.5)
            glVertex3f(-0.5, 0, 0.5)

            # laterais (mais volume visual)
            glVertex3f(0, 1, 0)
            glVertex3f(0.5, 0, -0.5)
            glVertex3f(0.5, 0, 0.5)

            glVertex3f(0, 1, 0)
            glVertex3f(-0.5, 0, 0.5)
            glVertex3f(-0.5, 0, -0.5)

            glEnd()

            glPopMatrix()