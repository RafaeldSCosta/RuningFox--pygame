"""
screens.py

Módulo que contém classes e funções para as telas visuais do jogo:
- BaseScreen: base para telas com fundo e utilitários
- Start: tela inicial com logo, nuvens e botão start
- Level: tela de transição/placeholder de nível
- End: tela final (game over)
- GameStateManager: gerencia o estado atual do fluxo do jogo

Também fornece funções utilitárias de exibição bloqueante:
- mostrar_instrucao: mostra imagem de instrução até ESPAÇO ou timeout
- mostrar_tela_level: wrapper para mostrar_instrucao (transição de level)
- mostrar_end_screen: mostra imagem final por um tempo fixo
"""
import pygame
import sys
import random
import math

SCREENWIDTH, SCREENHEIGHT = 950, 880
FPS = 60

class BaseScreen:
    """Classe base para telas do jogo.

    Responsabilidades:
    - carregar e escalar a imagem de fundo
    - manter referências ao display e ao GameStateManager (gsm)
    - fornecer fontes reutilizáveis e utilitário para desenhar texto centralizado
    """
    def __init__(self, display, gsm, bg_path):
        """Inicializa a tela base.

        display: superfície pygame onde desenhar
        gsm: instância de GameStateManager para controlar transições
        bg_path: caminho para a imagem de fundo
        """
        self.display = display
        self.gsm = gsm
        self.bg = pygame.image.load(bg_path).convert()
        self.bg = pygame.transform.scale(self.bg, (SCREENWIDTH, SCREENHEIGHT))
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_text = pygame.font.SysFont(None, 36)

    def draw_centered(self, text, font, y):
        """Desenha texto centralizado horizontalmente na posição y.

        Retorna o rect do texto desenhado (útil para posicionamento ou interatividade).
        """
        surface = font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(center=(SCREENWIDTH // 2, y))
        self.display.blit(surface, rect)
        return rect

class Start(BaseScreen):
    """Tela inicial com logo, nuvens animadas e botão START.

    Comportamento:
    - renderiza fundo, nuvens e logo
    - detecta clique no botão ou espaço para iniciar o level
    """
    def __init__(self, display, gsm):
        """Cria a tela inicial carregando imagens e preparando animações."""
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
        # Lista de dicionários com propriedades de cada nuvem para animação
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
        """Processa eventos de entrada na tela inicial.

        - Clique esquerdo sobre o botão -> muda o estado para 'level'
        - Tecla ESPAÇO -> muda o estado para 'level'
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                self.gsm.set_state('level')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.gsm.set_state('level')

    def mover_nuvens(self):
        """Anima as nuvens: movimento horizontal e leve oscilação vertical senoidal."""
        t = pygame.time.get_ticks() / 1000.0
        for nuvem in self.nuvens:
            nuvem["x"] += nuvem["vel"]
            if nuvem["x"] > SCREENWIDTH + 200:
                nuvem["x"] = -200
            bob = math.sin(t * 1.5 + nuvem["phase"]) * 6
            y = nuvem["base_y"] + bob
            self.display.blit(nuvem["img"], (nuvem["x"], y))

    def desenhar_logo(self):
        """Desenha o logo centralizado no topo da tela."""
        self.display.blit(self.logo_img, self.logo_rect)

    def run(self):
        """Renderiza a tela inicial inteira (fundo, nuvens, logo e botão)."""
        self.display.blit(self.bg, (0, 0))
        self.mover_nuvens()
        self.desenhar_logo()

        button_y_pos = (SCREENHEIGHT // 2) + 285
        mouse_pos = pygame.mouse.get_pos()
        current_button_image = self.start_button_image
        self.start_button_rect = current_button_image.get_rect(center=(SCREENWIDTH // 2, button_y_pos))

        # Troca para imagem de hover se o mouse estiver sobre o botão
        if self.start_button_rect.collidepoint(mouse_pos):
            current_button_image = self.start_button_hover_image

        self.display.blit(current_button_image, self.start_button_rect)

class Level(BaseScreen):
    """Tela simples usada como placeholder/preview do level.

    Mostra uma imagem de fundo e instrução de debug para encerrar (tecla E).
    """
    def __init__(self, display, gsm):
        """Inicializa a tela de level com a imagem de fundo apropriada."""
        super().__init__(display, gsm, "imagens_pygame/level_1.png")

    def handle_event(self, event):
        """Permite encerrar a tela de level pressionando a tecla E (usa para debug)."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.gsm.set_state('end')

    def run(self):
        """Desenha o fundo do level e mensagem informativa."""
        self.display.blit(self.bg, (0, 0))
        self.draw_centered("LEVEL - Pressione [E] para encerrar", self.font_text, SCREENHEIGHT - 100)

class End(BaseScreen):
    """Tela final (game over) com opções de reiniciar ou sair."""
    def __init__(self, display, gsm):
        """Inicializa a tela final usando a imagem de game over como fundo."""
        super().__init__(display, gsm, "imagens_pygame/game_over.png")

    def handle_event(self, event):
        """Processa teclas na tela final:
        - R: volta ao estado 'start' para reiniciar
        - Q: fecha o jogo completamente
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.gsm.set_state('start')
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    def run(self):
        """Desenha a tela final com instrução centralizada."""
        self.display.blit(self.bg, (0, 0))
        self.draw_centered("Pressione [R] para reiniciar ou [Q] para sair", self.font_text, SCREENHEIGHT // 2)

class GameStateManager:
    """Gerenciador simples do estado atual do jogo.

    Mantém uma string representando o estado atual (ex.: 'start', 'level', 'end').
    Usado pelas telas e pelo loop principal para coordenar transições.
    """
    def __init__(self, currentState):
        """Recebe o estado inicial como string."""
        self.currentState = currentState

    def get_state(self):
        """Retorna o estado atual."""
        return self.currentState

    def set_state(self, state):
        """Define um novo estado."""
        self.currentState = state

def mostrar_instrucao(screen, clock, imagem_path, duracao=20000):
    """Exibe uma tela de instrução até o jogador pressionar ESPAÇO ou até o timeout.

    Parâmetros:
    - screen: superfície onde desenhar
    - clock: pygame.time.Clock usada para limitar FPS no loop
    - imagem_path: caminho para a imagem de instrução
    - duracao: tempo máximo em milissegundos antes de continuar automaticamente
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

    # Loop bloqueante até o jogador prosseguir ou até o tempo expirar
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
    """Wrapper que mostra a imagem de transição de level reusando mostrar_instrucao."""
    mostrar_instrucao(screen, clock, imagem_path, duracao)

def mostrar_end_screen(screen, imagem_path, duracao=2500):
    """Mostra a imagem final (vitória/derrota) por um tempo fixo (bloqueante).

    Retorna após o delay definido.
    """
    SCREENW, SCREENH = screen.get_size()
    img = pygame.image.load(imagem_path).convert()
    img = pygame.transform.scale(img, (SCREENW, SCREENH))
    screen.blit(img, (0, 0))
    pygame.display.update()
    pygame.time.delay(duracao)
# filepath: c:\Users\lpr71\OneDrive\Desktop\CODE\RuningFox--pygame\RuningFox--pygame\screens.py
"""
screens.py

Módulo que contém classes e funções para as telas visuais do jogo:
- BaseScreen: base para telas com fundo e utilitários
- Start: tela inicial com logo, nuvens e botão start
- Level: tela de transição/placeholder de nível
- End: tela final (game over)
- GameStateManager: gerencia o estado atual do fluxo do jogo

Também fornece funções utilitárias de exibição bloqueante:
- mostrar_instrucao: mostra imagem de instrução até ESPAÇO ou timeout
- mostrar_tela_level: wrapper para mostrar_instrucao (transição de level)
- mostrar_end_screen: mostra imagem final por um tempo fixo
"""
import pygame
import sys
import random
import math

SCREENWIDTH, SCREENHEIGHT = 950, 880
FPS = 60

class BaseScreen:
    """Classe base para telas do jogo.

    Responsabilidades:
    - carregar e escalar a imagem de fundo
    - manter referências ao display e ao GameStateManager (gsm)
    - fornecer fontes reutilizáveis e utilitário para desenhar texto centralizado
    """
    def __init__(self, display, gsm, bg_path):
        """Inicializa a tela base.

        display: superfície pygame onde desenhar
        gsm: instância de GameStateManager para controlar transições
        bg_path: caminho para a imagem de fundo
        """
        self.display = display
        self.gsm = gsm
        self.bg = pygame.image.load(bg_path).convert()
        self.bg = pygame.transform.scale(self.bg, (SCREENWIDTH, SCREENHEIGHT))
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_text = pygame.font.SysFont(None, 36)

    def draw_centered(self, text, font, y):
        """Desenha texto centralizado horizontalmente na posição y.

        Retorna o rect do texto desenhado (útil para posicionamento ou interatividade).
        """
        surface = font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(center=(SCREENWIDTH // 2, y))
        self.display.blit(surface, rect)
        return rect

class Start(BaseScreen):
    """Tela inicial com logo, nuvens animadas e botão START.

    Comportamento:
    - renderiza fundo, nuvens e logo
    - detecta clique no botão ou espaço para iniciar o level
    """
    def __init__(self, display, gsm):
        """Cria a tela inicial carregando imagens e preparando animações."""
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
        # Lista de dicionários com propriedades de cada nuvem para animação
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
        """Processa eventos de entrada na tela inicial.

        - Clique esquerdo sobre o botão -> muda o estado para 'level'
        - Tecla ESPAÇO -> muda o estado para 'level'
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                self.gsm.set_state('level')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.gsm.set_state('level')

    def mover_nuvens(self):
        """Anima as nuvens: movimento horizontal e leve oscilação vertical senoidal."""
        t = pygame.time.get_ticks() / 1000.0
        for nuvem in self.nuvens:
            nuvem["x"] += nuvem["vel"]
            if nuvem["x"] > SCREENWIDTH + 200:
                nuvem["x"] = -200
            bob = math.sin(t * 1.5 + nuvem["phase"]) * 6
            y = nuvem["base_y"] + bob
            self.display.blit(nuvem["img"], (nuvem["x"], y))

    def desenhar_logo(self):
        """Desenha o logo centralizado no topo da tela."""
        self.display.blit(self.logo_img, self.logo_rect)

    def run(self):
        """Renderiza a tela inicial inteira (fundo, nuvens, logo e botão)."""
        self.display.blit(self.bg, (0, 0))
        self.mover_nuvens()
        self.desenhar_logo()

        button_y_pos = (SCREENHEIGHT // 2) + 285
        mouse_pos = pygame.mouse.get_pos()
        current_button_image = self.start_button_image
        self.start_button_rect = current_button_image.get_rect(center=(SCREENWIDTH // 2, button_y_pos))

        # Troca para imagem de hover se o mouse estiver sobre o botão
        if self.start_button_rect.collidepoint(mouse_pos):
            current_button_image = self.start_button_hover_image

        self.display.blit(current_button_image, self.start_button_rect)

class Level(BaseScreen):
    """Tela simples usada como placeholder/preview do level.

    Mostra uma imagem de fundo e instrução de debug para encerrar (tecla E).
    """
    def __init__(self, display, gsm):
        """Inicializa a tela de level com a imagem de fundo apropriada."""
        super().__init__(display, gsm, "imagens_pygame/level_1.png")

    def handle_event(self, event):
        """Permite encerrar a tela de level pressionando a tecla E (usa para debug)."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.gsm.set_state('end')

    def run(self):
        """Desenha o fundo do level e mensagem informativa."""
        self.display.blit(self.bg, (0, 0))
        self.draw_centered("LEVEL - Pressione [E] para encerrar", self.font_text, SCREENHEIGHT - 100)

class End(BaseScreen):
    """Tela final (game over) com opções de reiniciar ou sair."""
    def __init__(self, display, gsm):
        """Inicializa a tela final usando a imagem de game over como fundo."""
        super().__init__(display, gsm, "imagens_pygame/game_over.png")

    def handle_event(self, event):
        """Processa teclas na tela final:
        - R: volta ao estado 'start' para reiniciar
        - Q: fecha o jogo completamente
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.gsm.set_state('start')
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    def run(self):
        """Desenha a tela final com instrução centralizada."""
        self.display.blit(self.bg, (0, 0))
        self.draw_centered("Pressione [R] para reiniciar ou [Q] para sair", self.font_text, SCREENHEIGHT // 2)

class GameStateManager:
    """Gerenciador simples do estado atual do jogo.

    Mantém uma string representando o estado atual (ex.: 'start', 'level', 'end').
    Usado pelas telas e pelo loop principal para coordenar transições.
    """
    def __init__(self, currentState):
        """Recebe o estado inicial como string."""
        self.currentState = currentState

    def get_state(self):
        """Retorna o estado atual."""
        return self.currentState

    def set_state(self, state):
        """Define um novo estado."""
        self.currentState = state

def mostrar_instrucao(screen, clock, imagem_path, duracao=20000):
    """Exibe uma tela de instrução até o jogador pressionar ESPAÇO ou até o timeout.

    Parâmetros:
    - screen: superfície onde desenhar
    - clock: pygame.time.Clock usada para limitar FPS no loop
    - imagem_path: caminho para a imagem de instrução
    - duracao: tempo máximo em milissegundos antes de continuar automaticamente
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

    # Loop bloqueante até o jogador prosseguir ou até o tempo expirar
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
    """Wrapper que mostra a imagem de transição de level reusando mostrar_instrucao."""
    mostrar_instrucao(screen, clock, imagem_path, duracao)

def mostrar_end_screen(screen, imagem_path, duracao=2500):
    """Mostra a imagem final (vitória/derrota) por um tempo fixo (bloqueante).

    Retorna após o delay definido.
    """
    SCREENW, SCREENH = screen.get_size()
    img = pygame.image.load(imagem_path).convert()
    img = pygame.transform.scale(img, (SCREENW, SCREENH))
    screen.blit(img, (0, 0))
    pygame.display.update()
    pygame.time.delay(duracao)