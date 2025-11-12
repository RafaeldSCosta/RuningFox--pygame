import pygame as pg

class Raposa:
    def __init__(self):
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
        self.pos_raposa = [370, 760]
        self.velocidade = 30
        self.tamanho_raposa = self.sprite_frente.get_rect().size
        self.ajuste_y_raposa = -35

    # -------------------------------------------------------------
    def desenhar_raposa(self, janela):
        janela.blit(self.sprite_raposa_atual,
                     (self.pos_raposa[0], self.pos_raposa[1] + self.ajuste_y_raposa))

    # -------------------------------------------------------------
    def mover_raposa(self, tecla):
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
