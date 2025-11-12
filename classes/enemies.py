import pygame as pg

import pygame as pg


"""
Módulo de inimigos

Este módulo define a classe `Inimigos` que carrega e armazena os frames
(superfícies Pygame) usados para renderizar inimigos e obstáculos no jogo.

Os sprites são carregados da pasta `imagens_pygame/` e redimensionados para
valores fixos por tipo. A classe apenas prepara as listas de frames e guarda
os tamanhos usados como referência — não realiza lógica de movimento/colisão.
"""


class Inimigos:
    """Carrega sprites (frames) para diferentes inimigos/obstáculos.

    A intenção é centralizar o carregamento das imagens em um único lugar.
    Cada atributo *_frames contém uma lista de superfícies (surfaces) que
    podem ser usadas para animação. Os atributos tamanho_* guardam as
    dimensões usadas ao redimensionar as imagens.
    """

    def __init__(self):
        # --- JACARÉS (usados apenas na fase 1) ---
        # Definimos uma tupla (largura, altura) que será usada para escalar
        # todas as imagens dos jacarés. Usamos list comprehension para
        # carregar e escalar os frames de forma compacta.
        TAMANHO_JACARE = (70, 50)
        self.jacare_frames = [
            pg.transform.scale(
                pg.image.load(f"imagens_pygame/jac{i}.png").convert_alpha(),
                TAMANHO_JACARE,
            )
            for i in range(1, 10)
        ]

        # --- RATAZANAS (substituem os jacarés na fase 2) ---
        # Aqui usamos um loop com try/except para capturar erros de I/O
        # (por exemplo, arquivo não encontrado). Em caso de erro, é
        # impresso um aviso e o frame é ignorado — isso evita quebrar o jogo
        # se faltar alguma imagem.
        TAMANHO_RATAZANA = (100, 50)
        self.ratazana_frames = []
        for i in range(1, 5):
            caminho = f"imagens_pygame/rat{i}.png"
            try:
                img = pg.image.load(caminho).convert_alpha()
                img = pg.transform.scale(img, TAMANHO_RATAZANA)
                self.ratazana_frames.append(img)
            except Exception as e:
                # Mensagem de erro específica ajuda na depuração de assets
                print(f"❌ Erro ao carregar {caminho}: {e}")

        # --- FENOS (fase 1) ---
        # Outro exemplo de uso de list comprehension para carregar frames.
        TAMANHO_FENO = (60, 60)
        self.feno_frames = [
            pg.transform.scale(
                pg.image.load(f"imagens_pygame/feno{i}.png").convert_alpha(),
                TAMANHO_FENO,
            )
            for i in range(1, 10)
        ]

        # --- ESCORPIÕES (fase 2) ---
        TAMANHO_ESC = (70, 50)
        self.esc_frames = [
            pg.transform.scale(
                pg.image.load(f"imagens_pygame/esc{i}.png").convert_alpha(),
                TAMANHO_ESC,
            )
            for i in range(1, 5)
        ]

        # --- COBRAS (iguais nas duas fases) ---
        # Observação: o loop pula quando i == 4 — isso provavelmente ocorre
        # porque a imagem de índice 4 não existe ou é indesejada.
        TAMANHO_COBRA = (160, 50)
        self.cobra_frames = []
        for i in range(1, 9):
            if i == 4:
                # Pula o índice 4 intencionalmente
                continue
            caminho = f"imagens_pygame/cob{i}.png"
            try:
                img = pg.transform.scale(
                    pg.image.load(caminho).convert_alpha(), TAMANHO_COBRA
                )
                self.cobra_frames.append(img)
            except Exception:
                # Mensagem menos verbosa quando a imagem não é essencial
                print(f"⚠️ Não encontrei {caminho}, pulando...")

        # --- Guardar tamanhos para referência ---
        # Esses atributos podem ser usados por outros módulos para criar
        # rects, colisões, ou posicionamento correto dos sprites.
        self.tamanho_jacare = TAMANHO_JACARE
        self.tamanho_ratazana = TAMANHO_RATAZANA
        self.tamanho_feno = TAMANHO_FENO
        self.tamanho_cobra = TAMANHO_COBRA
        self.tamanho_esc = TAMANHO_ESC
