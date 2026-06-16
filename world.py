import math
import random

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class World:
    def __init__(self):
        self.level = 1
        self.max_level = 5
        self.cell_size = 2.0
        self.room_half_size = 14.0
        self.crystals = []
        self.obstacles = []
        self.collected = 0
        self.total_crystals = 0
        self.start_time = pygame.time.get_ticks()
        self.level_complete = False
        self.game_complete = False
        self.generate_level(self.level)

    def generate_level(self, level):
        random.seed(level * 37)
        self.level = level
        self.collected = 0
        self.level_complete = False
        self.game_complete = False
        self.start_time = pygame.time.get_ticks()

        grid_radius = 6 + (level // 3)
        self.room_half_size = (grid_radius + 1) * self.cell_size
        wall_count = 8 + level * 7
        blocked = set()
        boundary = set()

        for x in range(-grid_radius, grid_radius + 1):
            boundary.add((x, -grid_radius))
            boundary.add((x, grid_radius))
        for z in range(-grid_radius, grid_radius + 1):
            boundary.add((-grid_radius, z))
            boundary.add((grid_radius, z))

        blocked.update(boundary)

        safe_cells = {
            (0, 0), (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (-1, -1), (2, 0), (-2, 0),
        }

        candidates = [
            (x, z)
            for x in range(-grid_radius + 1, grid_radius)
            for z in range(-grid_radius + 1, grid_radius)
            if (x, z) not in safe_cells and (x + z + level) % 2 == 0
        ]
        random.shuffle(candidates)

        for cell in candidates[:wall_count]:
            blocked.add(cell)

        crystal_count = 4 + level
        reachable = self.find_reachable_cells(blocked, grid_radius)
        playable_cells = [
            cell for cell in reachable
            if cell not in safe_cells and cell not in boundary
        ]

        removable_walls = [cell for cell in candidates if cell in blocked and cell not in boundary]
        while len(playable_cells) < crystal_count and removable_walls:
            blocked.remove(removable_walls.pop())
            reachable = self.find_reachable_cells(blocked, grid_radius)
            playable_cells = [
                cell for cell in reachable
                if cell not in safe_cells and cell not in boundary
            ]

        self.obstacles = [
            (x * self.cell_size, 0, z * self.cell_size)
            for x, z in sorted(blocked)
        ]

        open_cells = sorted(playable_cells)
        random.shuffle(open_cells)
        self.crystals = [
            [x * self.cell_size, 0.9, z * self.cell_size]
            for x, z in open_cells[:crystal_count]
        ]
        self.total_crystals = len(self.crystals)

    def find_reachable_cells(self, blocked, grid_radius):
        start = (0, 0)
        if start in blocked:
            return set()

        visited = {start}
        queue = [start]

        while queue:
            x, z = queue.pop(0)
            neighbors = ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1))

            for neighbor in neighbors:
                nx, nz = neighbor
                if abs(nx) >= grid_radius or abs(nz) >= grid_radius:
                    continue
                if neighbor in blocked or neighbor in visited:
                    continue

                visited.add(neighbor)
                queue.append(neighbor)

        return visited

    def reset(self):
        self.generate_level(1)

    def next_level(self):
        if self.level >= self.max_level:
            self.game_complete = True
            self.level_complete = True
            return
        self.generate_level(self.level + 1)

    def collides(self, x, z):
        if abs(x) > self.room_half_size - 1.0 or abs(z) > self.room_half_size - 1.0:
            return True

        for ox, oy, oz in self.obstacles:
            if abs(x - ox) < 1.25 and abs(z - oz) < 1.25:
                return True
        return False

    def update(self, player, audio):
        remaining = []

        for cx, cy, cz in self.crystals:
            if abs(player.x - cx) < 1.0 and abs(player.z - cz) < 1.0:
                self.collected += 1

                if audio:
                    audio.play_collect()
            else:
                remaining.append([cx, cy, cz])

        self.crystals = remaining
        self.level_complete = len(self.crystals) == 0

    def draw_cube(self, x, y, z, sx, sy, sz, color):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(sx, sy, sz)
        glColor3f(*color)

        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glNormal3f(0, 0, -1)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)

        glNormal3f(1, 0, 0)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)

        glNormal3f(-1, 0, 0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)

        glNormal3f(0, 1, 0)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)

        glNormal3f(0, -1, 0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glEnd()

        glPopMatrix()

    def draw_room(self):
        size = self.room_half_size * 2 + 2
        wall = self.room_half_size + 1

        self.draw_cube(0, -0.06, 0, size, 0.12, size, (0.18, 0.2, 0.22))
        self.draw_cube(0, 2.0, -wall, size, 4, 0.4, (0.32, 0.32, 0.36))
        self.draw_cube(0, 2.0, wall, size, 4, 0.4, (0.28, 0.28, 0.33))
        self.draw_cube(-wall, 2.0, 0, 0.4, 4, size, (0.28, 0.29, 0.34))
        self.draw_cube(wall, 2.0, 0, 0.4, 4, size, (0.3, 0.31, 0.36))

        glDisable(GL_LIGHTING)
        glColor3f(0.1, 0.12, 0.14)
        glBegin(GL_LINES)
        grid_limit = int(self.room_half_size)
        for value in range(-grid_limit, grid_limit + 1, 2):
            glVertex3f(value, 0.01, -grid_limit)
            glVertex3f(value, 0.01, grid_limit)
            glVertex3f(-grid_limit, 0.01, value)
            glVertex3f(grid_limit, 0.01, value)
        glEnd()
        glEnable(GL_LIGHTING)

    def draw_obstacles(self):
        for ox, oy, oz in self.obstacles:
            self.draw_cube(ox, 1.1, oz, 1.8, 2.2, 1.8, (0.55, 0.16, 0.13))
            self.draw_cube(ox, 2.25, oz, 1.95, 0.18, 1.95, (0.72, 0.28, 0.2))

    def draw_crystal(self, cx, cy, cz):
        angle = pygame.time.get_ticks() / 5.0
        pulse = 1 + 0.08 * math.sin(pygame.time.get_ticks() / 220.0)

        glPushMatrix()
        glTranslatef(cx, cy, cz)
        glRotatef(angle, 0, 1, 0)
        glScalef(pulse, pulse, pulse)
        glColor3f(0.1, 0.9, 1.0)

        glBegin(GL_TRIANGLES)
        top = (0, 0.75, 0)
        bottom = (0, -0.75, 0)
        ring = [(-0.45, 0, -0.45), (0.45, 0, -0.45), (0.45, 0, 0.45), (-0.45, 0, 0.45)]

        for index in range(4):
            a = ring[index]
            b = ring[(index + 1) % 4]
            glNormal3f(0, 0.7, 0.4)
            glVertex3f(*top)
            glVertex3f(*a)
            glVertex3f(*b)

            glNormal3f(0, -0.7, 0.4)
            glVertex3f(*bottom)
            glVertex3f(*b)
            glVertex3f(*a)
        glEnd()

        glPopMatrix()

    def draw(self):
        self.draw_room()
        self.draw_obstacles()

        for cx, cy, cz in self.crystals:
            self.draw_crystal(cx, cy, cz)
