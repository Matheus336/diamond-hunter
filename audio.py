import pygame

class Audio:
    def __init__(self):
        self.collect = None

        try:
            pygame.mixer.music.load("assets/music.mp3")
            self.collect = pygame.mixer.Sound("assets/collect.wav")
        except:
            pass

    def play_music(self):
        pygame.mixer.music.play(-1)

    def play_collect(self):
        if self.collect:
            self.collect.play()