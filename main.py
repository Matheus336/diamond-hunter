import pygame
from game import Game

pygame.init()

screen = pygame.display.set_mode(
    (1000, 700),
    pygame.DOUBLEBUF | pygame.OPENGL
)

Game(screen).run()