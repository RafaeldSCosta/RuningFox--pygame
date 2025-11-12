import pygame as pg


"""
Módulo de gerenciamento de fases/níveis.

Define a classe `Fases` que armazena configurações específicas de cada fase
(mapa de plataformas, posições Y, áreas de chegada, dificuldade) e fornece
um método para transicionar para a próxima fase.
"""


class Fases:
    """Gerencia dados de níveis e transição de fases.

    Cada instância armazena as plataformas (linhas_das_plataformas), posições
    verticais (y_posicoes_*), áreas de colisão (area_fazenda, area_ovos) e
    dificuldade (v_dif) para a fase atual. O método `proxima_fase()` atualiza
    esses valores de acordo com o nível.
    """

    def __init__(self):
        # --- parâmetros gerais ---
        # Fase começa em 1; v_dif é um multiplicador de velocidade
        self.fase = 1
        self.v_dif = 0

        # --- Áreas e posições ---
        # area_fazenda: zona de chegada (destino de vitória da fase 1)
        # area_ovos: zona dos ovos (meta final da fase 2, inicialmente "vazia")
        self.area_fazenda = pg.Rect(120, 50, 100, 40)
        self.area_ovos = pg.Rect(0, 0, 1, 1)
        # y_posicoes_fase1: posições Y (verticais) das 6 linhas de plataformas na fase 1
        # y_posicoes_fase2: posições Y das 3 linhas de plataformas na fase 2
        self.y_posicoes_fase1 = [195, 295, 395, 495, 595, 695]
        self.y_posicoes_fase2 = [330, 470, 610]

        # --- Plataformas iniciais (Fase 1) ---
        # lista de 6 linhas, cada uma contendo as posições X dos objetos naquela linha
        # Ordem das linhas: [fenos (cima), cobras (cima), jacarés (meio),
        #                    fenos (baixo), cobras (baixo), jacarés (fundo)]
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
        """Avança para a próxima fase e atualiza configurações.

        - Incrementa `self.fase` e imprime mensagem.
        - Se fase == 2: troca a área de chegada pela área de ovos, aumenta
          dificuldade (v_dif = 1.8), redefine plataformas e tenta carregar
          novo fundo (fundo_fazenda_2.png).
        - Se fase == 3: prepara para fase 3 (aumenta v_dif e aviso).
        - Casos posteriores: marca como "zerou o jogo".
        """
        self.fase += 1
        print(f"🌾 Indo para a fase {self.fase}!")

        if self.fase == 2:
            # Define nova meta (área dos ovos) na parte superior central
            self.area_ovos = pg.Rect(475, 100, 100, 50)
            # Aumenta dificuldade multiplicando velocidades das plataformas
            self.v_dif = 1.8
            try:
                # Desativa a área da fazenda (redimensiona para 1x1 invisível)
                self.area_fazenda = pg.Rect(0, 0, 1, 1)
                # Carrega novo fundo (fase 2 ocorre dentro da fazenda)
                self.fundo_imagem = pg.image.load("imagens_pygame/fundo_fazenda_2.png").convert()
                self.fundo_imagem = pg.transform.scale(self.fundo_imagem, (950, 880))
                print("🐔 Entrou na fazenda — Fase 2 iniciada!")
            except Exception:
                # Se fundo não existir, apenas avisa mas continua
                print("⚠️ Fundo da Fase 2 não encontrado!")

            # Redefine as plataformas para fase 2 (3 linhas: ratazanas, escorpiões, cobras)
            self.linhas_das_plataformas = [
                [50, 250, 450, 800],   # Ratazanas
                [120, 360, 720],       # Escorpiões
                [120, 360, 720],       # Cobras
            ]
            print("⚙️ Fase 2: Ratazanas, Escorpiões e Cobras.")
            # Diminui velocidade de animação (frames passam mais lento)
            self.vel_animacao = 0.15

        elif self.fase == 3:
            print("🚜 Fase 3 iniciada! (ainda sem cenário)")
            # Aumenta mais ainda a velocidade de animação
            self.vel_animacao = 0.3
        else:
            # Qualquer fase > 3 é considerada vitória
            print("🎉 Você zerou o jogo!")
            self.game_over = True
