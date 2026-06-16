import os
import sys
import pygame

def resource_path(relative_path):
    """ Obtém o caminho absoluto para os recursos, funcionando em desenvolvimento e no PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Audio:
    
    def __init__(self):
        self.collect = None
        self.music_volume = 0.5
        self.effects_volume = 0.8

        try:
            pygame.mixer.music.load(resource_path("assets/music.mp3"))
            self.collect = pygame.mixer.Sound(resource_path("assets/collect.wav"))
            self.collect.set_volume(self.effects_volume)
        except Exception as e:
            print(f"Erro ao carregar arquivos de áudio: {e}")

    def play_music(self):
        try:
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Não foi possível tocar a música: {e}")

    def play_collect(self):
        if self.collect:
            self.collect.play()

    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except pygame.error:
            pass

    def set_effects_volume(self, volume):
        self.effects_volume = max(0, min(1, volume))
        if self.collect:
            self.collect.set_volume(self.effects_volume)
