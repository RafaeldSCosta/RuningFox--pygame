import pygame as pg
from sys import exit
from classes.player import Raposa
from classes.enemies import Inimigos
from classes.levels import Fases


class CruzamentoFazenda:
    def __init__(self):
        pg.init()
        self.janela = pg.display.set_mode((950, 880))
        pg.display.set_caption("Cruzamento da Fazenda")
        self.relogio = pg.time.Clock()

        try:
            # --- Fundo inicial ---
            self.fundo_imagem = pg.image.load("imagens_pygame/fundo_fazenda.png").convert()
            self.fundo_imagem = pg.transform.scale(self.fundo_imagem, (950, 880))
        except Exception as e:
            print("❌ ERRO ao carregar imagens:", e)
            pg.quit()
            exit()

        # --- Componentes principais ---
        self.raposa = Raposa()
        self.inimigos = Inimigos()
        self.fases = Fases()

        # --- parâmetros gerais ---
        self.vidas = 3
        self.game_over = False
        self.indice_animacao = 0
        self.tempo_animacao = 0.0
        self.vel_animacao = 0.20
        self.reached_ovos = False

    # -------------------------------------------------------------
    def limpar_janela(self):
        self.janela.blit(self.fundo_imagem, (0, 0))

    # -------------------------------------------------------------
    def desenhar_plataformas(self):
        y_posicoes = self.fases.y_posicoes_fase1 if self.fases.fase == 1 else self.fases.y_posicoes_fase2
        self.tempo_animacao += self.vel_animacao
        if self.tempo_animacao >= 1:
            self.indice_animacao = (self.indice_animacao + 1) % max(1, len(self.inimigos.cobra_frames))
            self.tempo_animacao = 0

        for linha, xs in enumerate(self.fases.linhas_das_plataformas):
            if linha >= len(y_posicoes):
                break
            y = y_posicoes[linha]
            for x in xs:
                # 🐊 Jacarés (fase 1) / 🐀 Ratazanas (fase 2)
                if (self.fases.fase == 1 and linha in (2, 5)):
                    img = self.inimigos.jacare_frames[self.indice_animacao % len(self.inimigos.jacare_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_jacare[0] // 2, y))
                    self.janela.blit(img, rect)
                elif (self.fases.fase == 2 and linha == 0):
                    img = self.inimigos.ratazana_frames[self.indice_animacao % len(self.inimigos.ratazana_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_ratazana[0] // 2, y))
                    self.janela.blit(img, rect)

                # 🌾 Fenos (fase 1) / 🦂 Escorpiões (fase 2)
                elif (self.fases.fase == 1 and linha in (0, 3)):
                    img = self.inimigos.feno_frames[self.indice_animacao % len(self.inimigos.feno_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_feno[0] // 2, y))
                    self.janela.blit(img, rect)
                elif (self.fases.fase == 2 and linha == 1):
                    img = self.inimigos.esc_frames[self.indice_animacao % len(self.inimigos.esc_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_esc[0] // 2, y))
                    self.janela.blit(img, rect)

                # 🐍 Cobras (ambas fases)
                elif (self.fases.fase == 1 and linha in (1, 4)) or (self.fases.fase == 2 and linha == 2):
                    img = self.inimigos.cobra_frames[self.indice_animacao % len(self.inimigos.cobra_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_cobra[0] // 2, y))
                    self.janela.blit(img, rect)

    # -------------------------------------------------------------
    def atualizar_plataformas(self):
        for y in range(len(self.fases.linhas_das_plataformas)):
            for i in range(len(self.fases.linhas_das_plataformas[y])):
                if y in (2, 5):  # jacarés / ratazanas
                    self.fases.linhas_das_plataformas[y][i] += 1 + self.fases.v_dif
                    if self.fases.linhas_das_plataformas[y][i] > 880:
                        self.fases.linhas_das_plataformas[y][i] = -100
                elif y in (0, 3):  # fenos / escorpiões
                    self.fases.linhas_das_plataformas[y][i] -= 2 + self.fases.v_dif
                    if self.fases.linhas_das_plataformas[y][i] < -120:
                        self.fases.linhas_das_plataformas[y][i] = 880
                elif y in (1, 4):  # cobras
                    self.fases.linhas_das_plataformas[y][i] += 1.5 + self.fases.v_dif
                    if self.fases.linhas_das_plataformas[y][i] > 950:
                        self.fases.linhas_das_plataformas[y][i] = -300

    # -------------------------------------------------------------
    def raposa_colidiu_com_objeto(self):
        raposa_rect = pg.Rect(int(self.raposa.pos_raposa[0]), int(self.raposa.pos_raposa[1] + self.raposa.ajuste_y_raposa),
                              int(self.raposa.tamanho_raposa[0]), int(self.raposa.tamanho_raposa[1]))
        y_posicoes = self.fases.y_posicoes_fase1 if self.fases.fase == 1 else self.fases.y_posicoes_fase2
        for linha, xs in enumerate(self.fases.linhas_das_plataformas):
            if linha >= len(y_posicoes):
                break
            y_plat = y_posicoes[linha]
            for x in xs:
                if (self.fases.fase == 1 and linha in (2, 5)):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.inimigos.tamanho_jacare[1] // 2), *self.inimigos.tamanho_jacare)
                elif (self.fases.fase == 2 and linha == 0):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.inimigos.tamanho_ratazana[1] // 2), *self.inimigos.tamanho_ratazana)
                elif (self.fases.fase == 1 and linha in (0, 3)) or (self.fases.fase == 2 and linha == 1):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.inimigos.tamanho_feno[1] // 2), *self.inimigos.tamanho_feno)
                elif (self.fases.fase == 1 and linha in (1, 4)) or (self.fases.fase == 2 and linha == 2):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.inimigos.tamanho_cobra[1] // 2), *self.inimigos.tamanho_cobra)
                else:
                    continue
                if raposa_rect.colliderect(plat_rect):
                    return True
        return False

    # -------------------------------------------------------------
    def resetar_posicao_raposa(self, colisao=False):
        if colisao:
            self.vidas -= 1
            if self.vidas < 0:
                self.vidas = 0
            print(f"💥 Colidiu! Vidas restantes: {self.vidas}")
            if self.vidas == 0:
                self.game_over = True
        self.raposa.pos_raposa = [370, 760]
        self.raposa.sprite_raposa_atual = self.raposa.sprite_frente

    # -------------------------------------------------------------
    def checar_colisoes_e_reagir(self):
        if self.game_over:
            return

        if self.raposa_colidiu_com_objeto():
            self.resetar_posicao_raposa(colisao=True)

        raposa_rect = pg.Rect(
            int(self.raposa.pos_raposa[0]),
            int(self.raposa.pos_raposa[1] + self.raposa.ajuste_y_raposa),
            int(self.raposa.tamanho_raposa[0]),
            int(self.raposa.tamanho_raposa[1]),
        )

        if raposa_rect.colliderect(self.fases.area_fazenda):
            print("🐾 A raposa chegou na fazenda!")
            self.fases.proxima_fase()
            self.fundo_imagem = pg.image.load("imagens_pygame/fundo_fazenda_2.png").convert()
            self.fundo_imagem = pg.transform.scale(self.fundo_imagem, (950, 880))
            self.resetar_posicao_raposa()

        if self.fases.area_ovos and self.fases.area_ovos.width > 1 and raposa_rect.colliderect(self.fases.area_ovos):
            if not self.reached_ovos:
                print("🐾 A raposa chegou nos ovos!")
                self.reached_ovos = True
                self.game_over = True
