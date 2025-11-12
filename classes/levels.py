import pygame as pg

class Fases:
    def __init__(self):
        # --- parâmetros gerais ---
        self.fase = 1
        self.v_dif = 0

        # --- Áreas e posições ---
        self.area_fazenda = pg.Rect(120, 50, 100, 100)
        self.area_ovos = pg.Rect(0, 0, 1, 1)
        self.y_posicoes_fase1 = [195, 295, 395, 495, 595, 695]
        self.y_posicoes_fase2 = [330, 470, 610]

        # --- Plataformas iniciais (Fase 1) ---
        self.linhas_das_plataformas = [
            [60, 420, 660],        # fenos (cima)
            [50, 650],             # cobras (cima)
            [50, 250, 450, 800],   # jacarés (meio)
            [120, 360, 720],       # fenos (baixo)
            [0, 700],              # cobras (baixo)
            [100, 250, 700, 800],  # jacarés (fundo)
        ]

    # -------------------------------------------------------------
    def proxima_fase(self):
        self.fase += 1
        print(f"🌾 Indo para a fase {self.fase}!")

        if self.fase == 2:
            self.area_ovos = pg.Rect(475, 100, 100, 150)
            self.v_dif = 1.8
            try:
                self.area_fazenda = pg.Rect(0, 0, 1, 1)
                self.fundo_imagem = pg.image.load("imagens_pygame/fundo_fazenda_2.png").convert()
                self.fundo_imagem = pg.transform.scale(self.fundo_imagem, (950, 880))
                print("🐔 Entrou na fazenda — Fase 2 iniciada!")
            except:
                print("⚠️ Fundo da Fase 2 não encontrado!")

            self.linhas_das_plataformas = [
                [50, 250, 450, 800],   # Ratazanas
                [120, 360, 720],       # Escorpiões
                [120, 360, 720],       # Cobras
            ]
            print("⚙️ Fase 2: Ratazanas, Escorpiões e Cobras.")
            self.vel_animacao = 0.15

        elif self.fase == 3:
            print("🚜 Fase 3 iniciada! (ainda sem cenário)")
            self.vel_animacao = 0.3
        else:
            print("🎉 Você zerou o jogo!")
            self.game_over = True
