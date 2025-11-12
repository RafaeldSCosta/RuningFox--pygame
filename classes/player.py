"""
classes/player.py

Define a classe Raposa que representa o jogador (a raposa).
Responsabilidades:
- carregar sprites (frente, costas, esquerda, direita)
- manter posição, velocidade e ajustes visuais
- fornecer métodos para desenhar e mover a raposa

As imagens são carregadas da pasta imagens_pygame/ e escaladas para um
tamanho fixo definido por TAMANHO_RAPOSA.
"""
import pygame as pg

class Raposa:
    """Representa a raposa controlada pelo jogador.

    Atributos principais:
    - sprite_*: superfícies Pygame com as orientações da raposa
    - sprite_raposa_atual: sprite atualmente exibido
    - pos_raposa: posição [x, y] da raposa na tela
    - velocidade: deslocamento em pixels por movimento (tecla)
    - tamanho_raposa: tamanho do sprite (largura, altura)
    - ajuste_y_raposa: correção vertical ao desenhar (offset visual)
    """
    def __init__(self):
        """Carrega sprites, escala-os e inicializa parâmetros de movimento."""
        # --- Sprites da raposa ---
        TAMANHO_RAPOSA = (50, 50)
        img_frente = pg.image.load("imagens_pygame/frente.png").convert_alpha()
        self.sprite_frente = pg.transform.scale(img_frente, TAMANHO_RAPOSA)
        img_costas = pg.image.load("imagens_pygame/costas.png").convert_alpha()
        self.sprite_costas = pg.transform.scale(img_costas, TAMANHO_RAPOSA)
        img_esquerda = pg.image.load("imagens_pygame/LADO_E.png").convert_alpha()
        self.sprite_esquerda = pg.transform.scale(img_esquerda, TAMANHO_RAPOSA)
        img_direita = pg.image.load("imagens_pygame/LADO_D.png").convert_alpha()
        self.sprite_direita = pg.transform.scale(img_direita, TAMANHO_RAPOSA)
        self.sprite_raposa_atual = self.sprite_frente

        # --- Parâmetros ---
        # Posição inicial (x, y) e velocidade de movimento em pixels por tecla
        self.pos_raposa = [370, 760]
        self.velocidade = 30
        self.tamanho_raposa = self.sprite_frente.get_rect().size
        # Ajuste vertical para posicionar sprite corretamente na tela (offset)
        self.ajuste_y_raposa = -35

    # -------------------------------------------------------------
    def desenhar_raposa(self, janela):
        """Desenha o sprite atual da raposa na janela.

        Aplica ajuste vertical ao blit para alinhar visualmente o sprite.
        Parâmetros:
        - janela: superfície Pygame onde desenhar
        """
        janela.blit(self.sprite_raposa_atual,
                     (self.pos_raposa[0], self.pos_raposa[1] + self.ajuste_y_raposa))

    # -------------------------------------------------------------
    def mover_raposa(self, tecla):
        """Move a raposa e atualiza o sprite conforme a direção.

        Espera receber o nome da tecla como string ('up','down','left','right').
        Cada movimento altera a posição e troca o sprite atual para a direção.
        """
        if tecla == "up":
            self.sprite_raposa_atual = self.sprite_costas
            self.pos_raposa[1] -= self.velocidade
        elif tecla == "down":
            self.sprite_raposa_atual = self.sprite_frente
            self.pos_raposa[1] += self.velocidade
        elif tecla == "left":
            self.sprite_raposa_atual = self.sprite_esquerda
            self.pos_raposa[0] -= self.velocidade
        elif tecla == "right":
            self.sprite_raposa_atual = self.sprite_direita
            self.pos_raposa[0] += self.velocidade
