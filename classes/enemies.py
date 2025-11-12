import pygame as pg

class Inimigos:
    def __init__(self):
        # --- JACARÉS (usados apenas na fase 1) ---
        TAMANHO_JACARE = (70, 50)
        self.jacare_frames = [
            pg.transform.scale(pg.image.load(f"imagens_pygame/jac{i}.png").convert_alpha(), TAMANHO_JACARE)
            for i in range(1, 10)
        ]

        # --- RATAZANAS (substituem os jacarés na fase 2) ---
        TAMANHO_RATAZANA = (100, 50)
        self.ratazana_frames = []
        for i in range(1, 5):
            caminho = f"imagens_pygame/rat{i}.png"
            try:
                img = pg.image.load(caminho).convert_alpha()
                img = pg.transform.scale(img, TAMANHO_RATAZANA)
                self.ratazana_frames.append(img)
            except Exception as e:
                print(f"❌ Erro ao carregar {caminho}: {e}")

        # --- FENOS (fase 1) ---
        TAMANHO_FENO = (60, 60)
        self.feno_frames = [
            pg.transform.scale(pg.image.load(f"imagens_pygame/feno{i}.png").convert_alpha(), TAMANHO_FENO)
            for i in range(1, 10)
        ]

        # --- ESCORPIÕES (fase 2) ---
        TAMANHO_ESC = (70, 50)
        self.esc_frames = [
            pg.transform.scale(pg.image.load(f"imagens_pygame/esc{i}.png").convert_alpha(), TAMANHO_ESC)
            for i in range(1, 5)
        ]

        # --- COBRAS (iguais nas duas fases) ---
        TAMANHO_COBRA = (160, 50)
        self.cobra_frames = []
        for i in range(1, 9):
            if i == 4:
                continue
            caminho = f"imagens_pygame/cob{i}.png"
            try:
                img = pg.transform.scale(pg.image.load(caminho).convert_alpha(), TAMANHO_COBRA)
                self.cobra_frames.append(img)
            except:
                print(f"⚠️ Não encontrei {caminho}, pulando...")

        # --- Guardar tamanhos para referência ---
        self.tamanho_jacare = TAMANHO_JACARE
        self.tamanho_ratazana = TAMANHO_RATAZANA
        self.tamanho_feno = TAMANHO_FENO
        self.tamanho_cobra = TAMANHO_COBRA
        self.tamanho_esc = TAMANHO_ESC
