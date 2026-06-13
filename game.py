import pygame
from renderer import Renderer
from player import Player
from world import World
from camera import Camera
from audio import Audio
from OpenGL.GL import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        pygame.mixer.init()

        self.renderer = None
        self.player = Player()
        self.world = World()
        self.camera = Camera(self.player)
        self.audio = Audio()

        self.running = True
        self.clock = pygame.time.Clock()

        self.audio.play_music()

    def run(self):
        self.init_renderer()

        while self.running:
            self.clock.tick(60)

            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()

        self.player.update(keys, self.world)

        self.world.update(self.player, self.audio)


    def render(self):
        self.renderer.begin_frame(self.camera)

        # TESTE TRIÂNGULO
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 1, 0)
        glVertex3f(-1, -1, 0)
        glVertex3f(1, -1, 0)
        glEnd()

        self.world.draw()
        self.player.draw()

        self.renderer.end_frame()
        pygame.display.flip()

    def __del__(self):
        pygame.quit()

    def init_renderer(self):
        self.renderer = Renderer()
        self.renderer.init_gl()