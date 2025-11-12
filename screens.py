import pygame
import sys
import random
import math

SCREENWIDTH, SCREENHEIGHT = 950, 880
FPS = 60

class BaseScreen:
    def __init__(self, display, gsm, bg_path):
        self.display = display
        self.gsm = gsm
        self.bg = pygame.image.load(bg_path).convert()
        self.bg = pygame.transform.scale(self.bg, (SCREENWIDTH, SCREENHEIGHT))
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_text = pygame.font.SysFont(None, 36)

    def draw_centered(self, text, font, y):
        surface = font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(center=(SCREENWIDTH // 2, y))
        self.display.blit(surface, rect)
        return rect

# --- TELA DE INÍCIO ---
class Start(BaseScreen):
    def __init__(self, display, gsm):
        super().__init__(display, gsm, "imagens_pygame/imagem_start.png")

        # --- BOTÃO START ---
        button_image_path = "imagens_pygame/botao_start.png"
        self.start_button_image = pygame.image.load(button_image_path).convert_alpha()
        target_width = 200
        original_width, original_height = self.start_button_image.get_size()
        new_height = int(original_height * (target_width / original_width))
        self.start_button_image = pygame.transform.scale(self.start_button_image, (target_width, new_height))
        self.start_button_hover_image = self.start_button_image.copy()
        self.start_button_hover_image.fill((50, 50, 50, 0), special_flags=pygame.BLEND_RGB_SUB)
        self.start_button_rect = None

        # --- NUVENS EM MOVIMENTO ---
        self.nuvens = []
        for i in range(1, 5):
            img = pygame.image.load(f"imagens_pygame/nuvem{i}.png").convert_alpha()
            escala = pygame.transform.scale(img, (int(img.get_width() * 1.0), int(img.get_height() * 1.0)))
            x = i * 250
            base_y = random.randint(40, 180) + (i * 5)
            vel = 1.2 + (i * 0.3)
            phase = random.uniform(0, math.pi * 2)
            self.nuvens.append({"img": escala, "x": x, "base_y": base_y, "vel": vel, "phase": phase})

        # --- LOGO DO JOGO (RUNNING FOX) ---
        logo_path = "imagens_pygame/titulo.png"
        self.logo_img = pygame.image.load(logo_path).convert_alpha()
        self.logo_img = pygame.transform.smoothscale(self.logo_img, (int(SCREENWIDTH * 0.65), int(SCREENHEIGHT * 0.25)))
        self.logo_rect = self.logo_img.get_rect(center=(SCREENWIDTH // 2, 150))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                self.gsm.set_state('level')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.gsm.set_state('level')

    def mover_nuvens(self):
        t = pygame.time.get_ticks() / 1000.0
        for nuvem in self.nuvens:
            nuvem["x"] += nuvem["vel"]
            if nuvem["x"] > SCREENWIDTH + 200:
                nuvem["x"] = -200
            bob = math.sin(t * 1.5 + nuvem["phase"]) * 6
            y = nuvem["base_y"] + bob
            self.display.blit(nuvem["img"], (nuvem["x"], y))

    def desenhar_logo(self):
        self.display.blit(self.logo_img, self.logo_rect)

    def run(self):
        self.display.blit(self.bg, (0, 0))
        self.mover_nuvens()
        self.desenhar_logo()

        button_y_pos = (SCREENHEIGHT // 2) + 285
        mouse_pos = pygame.mouse.get_pos()
        current_button_image = self.start_button_image
        self.start_button_rect = current_button_image.get_rect(center=(SCREENWIDTH // 2, button_y_pos))

        if self.start_button_rect.collidepoint(mouse_pos):
            current_button_image = self.start_button_hover_image

        self.display.blit(current_button_image, self.start_button_rect)

# --- TELA DE LEVEL ---
class Level(BaseScreen):
    def __init__(self, display, gsm):
        super().__init__(display, gsm, "imagens_pygame/level_1.png")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.gsm.set_state('end')

    def run(self):
        self.display.blit(self.bg, (0, 0))
        self.draw_centered("LEVEL - Pressione [E] para encerrar", self.font_text, SCREENHEIGHT - 100)

# --- TELA FINAL ---
class End(BaseScreen):
    def __init__(self, display, gsm):
        super().__init__(display, gsm, "imagens_pygame/game_over.png")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.gsm.set_state('start')
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    def run(self):
        self.display.blit(self.bg, (0, 0))
        self.draw_centered("Pressione [R] para reiniciar ou [Q] para sair", self.font_text, SCREENHEIGHT // 2)

# --- GERENCIADOR DE ESTADOS ---
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state

# ------------------------- #
#     FUNÇÕES DE TELAS VISUAIS
# ------------------------- #
def mostrar_instrucao(screen, clock, imagem_path, duracao=20000):
    """
    Exibe uma tela de instrução até o jogador pressionar ESPAÇO ou o tempo acabar.
    """
    SCREENW, SCREENH = screen.get_size()

    imagem = pygame.image.load(imagem_path).convert()
    imagem = pygame.transform.scale(imagem, (SCREENW, SCREENH))
    screen.blit(imagem, (0, 0))
    pygame.display.update()

    start_time = pygame.time.get_ticks()
    esperando = True

    font = pygame.font.SysFont("arial", 30)
    texto = font.render("Pressione ESPAÇO para continuar", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(SCREENW // 2, SCREENH - 50))

    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                esperando = False
                break

        if pygame.time.get_ticks() - start_time >= duracao:
            esperando = False

        screen.blit(imagem, (0, 0))
        screen.blit(texto, texto_rect)
        pygame.display.flip()
        clock.tick(FPS)


def mostrar_tela_level(screen, clock, imagem_path, duracao=2000):
    """
    Exibe a tela de mudança de fase (level).
    """
    mostrar_instrucao(screen, clock, imagem_path, duracao)


def mostrar_end_screen(screen, imagem_path, duracao=2500):
    """
    Mostra a tela final (vitória ou game over).
    """
    SCREENW, SCREENH = screen.get_size()
    img = pygame.image.load(imagem_path).convert()
    img = pygame.transform.scale(img, (SCREENW, SCREENH))
    screen.blit(img, (0, 0))
    pygame.display.update()
    pygame.time.delay(duracao)
