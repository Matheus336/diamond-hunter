import pygame

class Audio:
    def __init__(self):
        self.collect = None
        self.music_volume = 0.5
        self.effects_volume = 0.8

        try:
            pygame.mixer.music.load("assets/music.mp3")
            self.collect = pygame.mixer.Sound("assets/collect.wav")
            self.collect.set_volume(self.effects_volume)
        except:
            pass

    def play_music(self):
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def play_collect(self):
        if self.collect:
            self.collect.play()

    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_effects_volume(self, volume):
        self.effects_volume = max(0, min(1, volume))
        if self.collect:
            self.collect.set_volume(self.effects_volume)
