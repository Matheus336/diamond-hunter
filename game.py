import pygame
from OpenGL.GL import *

from audio import Audio
from camera import Camera
from player import Player
from renderer import Renderer
from world import World


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
        self.state = "menu"
        self.menu_page = "main"
        self.menu_index = 0
        self.has_started = False
        self.session_best_level = 1
        self.session_best_collected = 0
        self.best_completion_time = None

        self.font = pygame.font.SysFont("arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("arial", 20)
        self.title_font = pygame.font.SysFont("arial", 58, bold=True)

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
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key):
        if self.state in ("menu", "paused"):
            self.handle_menu_key(key)
            return

        if key == pygame.K_ESCAPE:
            self.state = "paused"
            self.menu_page = "pause"
            self.menu_index = 0
        elif self.state == "level_complete" and key in (pygame.K_RETURN, pygame.K_SPACE):
            self.player.reset()
            self.world.next_level()
            self.state = "victory" if self.world.game_complete else "playing"
        elif self.state == "victory" and key == pygame.K_RETURN:
            self.open_main_menu()

    def handle_menu_key(self, key):
        items = self.current_menu_items()
        selectable = [index for index, item in enumerate(items) if item["enabled"]]

        if key in (pygame.K_w, pygame.K_UP):
            self.move_menu_selection(-1, selectable)
        elif key in (pygame.K_s, pygame.K_DOWN):
            self.move_menu_selection(1, selectable)
        elif key in (pygame.K_a, pygame.K_LEFT):
            self.adjust_option(-1)
        elif key in (pygame.K_d, pygame.K_RIGHT):
            self.adjust_option(1)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            items[self.menu_index]["action"]()
        elif key == pygame.K_ESCAPE:
            if self.menu_page in ("options", "controls"):
                self.open_main_menu()
            elif self.state == "paused":
                self.state = "playing"

    def move_menu_selection(self, direction, selectable):
        if not selectable:
            return

        if self.menu_index not in selectable:
            self.menu_index = selectable[0]
            return

        position = selectable.index(self.menu_index)
        self.menu_index = selectable[(position + direction) % len(selectable)]

    def adjust_option(self, direction):
        if self.menu_page != "options":
            return

        item = self.current_menu_items()[self.menu_index]
        if item["id"] == "music":
            self.audio.set_music_volume(self.audio.music_volume + direction * 0.1)
        elif item["id"] == "effects":
            self.audio.set_effects_volume(self.audio.effects_volume + direction * 0.1)

    def current_menu_items(self):
        if self.menu_page == "pause":
            return [
                {"label": "Continuar", "enabled": True, "action": self.resume_game},
                {"label": "Reiniciar fase", "enabled": True, "action": self.restart_level},
                {"label": "Opções", "enabled": True, "action": self.open_options},
                {"label": "Voltar ao menu", "enabled": True, "action": self.open_main_menu},
                {"label": "Sair", "enabled": True, "action": self.quit_game},
            ]

        if self.menu_page == "options":
            return [
                {"id": "music", "label": f"Música: {int(self.audio.music_volume * 100)}%", "enabled": True, "action": lambda: None},
                {"id": "effects", "label": f"Efeitos: {int(self.audio.effects_volume * 100)}%", "enabled": True, "action": lambda: None},
                {"id": "back", "label": "Voltar", "enabled": True, "action": self.open_main_menu},
            ]

        if self.menu_page == "controls":
            return [
                {"label": "W/S/A/D: Mover relativo a camera", "enabled": False, "action": lambda: None},
                {"label": "R/F: Subir ou baixar câmera", "enabled": False, "action": lambda: None},
                {"label": "Z/X: Aproximar ou afastar", "enabled": False, "action": lambda: None},
                {"label": "Enter / Espaco: Selecionar", "enabled": False, "action": lambda: None},
                {"label": "Esc: Pausar ou voltar", "enabled": False, "action": lambda: None},
                {"label": "Voltar", "enabled": True, "action": self.open_main_menu},
            ]

        return [
            {"label": "Iniciar jogo", "enabled": True, "action": self.start_new_game},
            {"label": "Continuar", "enabled": self.has_started, "action": self.resume_game},
            {"label": "Opções", "enabled": True, "action": self.open_options},
            {"label": "Controles", "enabled": True, "action": self.open_controls},
            {"label": "Sair", "enabled": True, "action": self.quit_game},
        ]

    def start_new_game(self):
        self.has_started = True
        self.player.reset()
        self.camera.reset()
        self.world.reset()
        self.state = "playing"

    def resume_game(self):
        if self.has_started:
            self.state = "playing"

    def restart_level(self):
        self.player.reset()
        self.world.generate_level(self.world.level)
        self.state = "playing"

    def open_main_menu(self):
        self.state = "menu"
        self.menu_page = "main"
        self.menu_index = 0

    def open_options(self):
        self.menu_page = "options"
        self.menu_index = 0

    def open_controls(self):
        self.menu_page = "controls"
        self.menu_index = 6

    def quit_game(self):
        self.running = False

    def update(self):
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        self.camera.update(keys)
        self.player.update(keys, self.world, self.camera.yaw)
        self.world.update(self.player, self.audio)

        self.session_best_level = max(self.session_best_level, self.world.level)
        self.session_best_collected = max(self.session_best_collected, self.world.collected)

        if self.world.level_complete:
            elapsed = (pygame.time.get_ticks() - self.world.start_time) / 1000
            if self.best_completion_time is None or elapsed < self.best_completion_time:
                self.best_completion_time = elapsed
            self.state = "level_complete"

    def render(self):
        if self.state in ("menu", "paused"):
            self.render_menu()
        else:
            self.render_world()

        pygame.display.flip()

    def render_world(self):
        self.renderer.begin_frame(self.camera)
        self.world.draw()
        self.player.draw()
        self.renderer.end_frame()
        self.draw_hud()

        if self.state == "level_complete":
            self.draw_center_message("Fase concluída!", "Pressione Enter para avançar")
        elif self.state == "victory":
            self.draw_center_message("Você venceu!", "Pressione Enter para voltar ao menu")

    def render_menu(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_menu_background()

        title = "DIAMOND HUNTER"
        subtitle = "Colete todos os cristais em uma sala com obstáculos para vencer"
        if self.menu_page == "pause":
            title = "PAUSADO"
            subtitle = "A fase continua exatamente daqui"
        elif self.menu_page == "options":
            title = "OPÇÕES"
            subtitle = "Use A/D ou setas laterais para ajustar"
        elif self.menu_page == "controls":
            title = "CONTROLES"
            subtitle = "Comandos principais do jogo"

        self.draw_text(title, 70, 70, self.title_font, (235, 242, 255))
        self.draw_text(subtitle, 74, 135, self.small_font, (165, 178, 195))

        self.draw_text(self.best_text(), 74, 178, self.small_font, (95, 225, 255))

        items = self.current_menu_items()
        y = 245
        for index, item in enumerate(items):
            selected = index == self.menu_index and item["enabled"]
            enabled = item["enabled"]
            color = (255, 236, 155) if selected else (222, 226, 232)
            if not enabled:
                color = (95, 100, 110)

            prefix = "> " if selected else "  "
            self.draw_text(prefix + item["label"], 120, y, self.font, color)
            y += 48

        self.draw_text("W/S/A/D Navega  |  Enter Seleciona  |  Esc Volta/Pausa", 74, 640, self.small_font, (150, 160, 174))

    def best_text(self):
        best_time = "--" if self.best_completion_time is None else f"{self.best_completion_time:.1f}s"
        return f"Melhor da Sessão: Fase {self.session_best_level} | Cristais {self.session_best_collected} | Melhor Fase {best_time}"

    def draw_menu_background(self):
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        self.begin_2d()

        glBegin(GL_QUADS)
        glColor3f(0.03, 0.04, 0.07)
        glVertex2f(0, 0)
        glVertex2f(self.renderer.width, 0)
        glColor3f(0.08, 0.1, 0.14)
        glVertex2f(self.renderer.width, self.renderer.height)
        glVertex2f(0, self.renderer.height)
        glEnd()

        glColor3f(0.12, 0.55, 0.68)
        glBegin(GL_LINES)
        for x in range(0, self.renderer.width, 50):
            glVertex2f(x, 520)
            glVertex2f(x + 280, 700)
        glEnd()

        self.end_2d()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    def draw_hud(self):
        elapsed = (pygame.time.get_ticks() - self.world.start_time) / 1000
        self.draw_text(f"Fase {self.world.level}/{self.world.max_level}", 24, 20, self.small_font, (245, 245, 245))
        self.draw_text(f"Cristais {self.world.collected}/{self.world.total_crystals}", 24, 46, self.small_font, (100, 235, 255))
        self.draw_text(f"Tempo {elapsed:.1f}s", 24, 72, self.small_font, (245, 220, 150))
        self.draw_text("Q/E giram camera/agente | R/F Altura | Z/X Zoom", 24, 98, self.small_font, (185, 195, 210))

    def draw_center_message(self, title, subtitle):
        self.draw_panel(285, 235, 500, 150)
        self.draw_text(title, 330, 260, self.title_font, (255, 224, 90))
        self.draw_text(subtitle, 345, 332, self.font, (255, 255, 255))

    def draw_panel(self, x, y, width, height):
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.begin_2d()

        glColor4f(0.02, 0.03, 0.05, 0.82)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

        glColor4f(0.1, 0.85, 1.0, 0.95)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()
        glLineWidth(1)

        self.end_2d()
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    def draw_text(self, text, x, y, font, color):
        surface = font.render(text, True, color)
        data = pygame.image.tostring(surface, "RGBA", False)
        width, height = surface.get_size()

        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            data,
        )

        self.begin_2d()
        glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(x, y)
        glTexCoord2f(1, 0)
        glVertex2f(x + width, y)
        glTexCoord2f(1, 1)
        glVertex2f(x + width, y + height)
        glTexCoord2f(0, 1)
        glVertex2f(x, y + height)
        glEnd()
        self.end_2d()

        glBindTexture(GL_TEXTURE_2D, 0)
        glDeleteTextures([texture])
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    def begin_2d(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.renderer.width, self.renderer.height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

    def end_2d(self):
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def __del__(self):
        pygame.quit()

    def init_renderer(self):
        self.renderer = Renderer()
        self.renderer.init_gl()
