import os
import pygame

def init_audio(base_dir):
    """
    Inicializa o áudio e carrega todos os sons e música.
    Retorna um dicionário com os objetos carregados.
    """

    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)

    audio = {
        "musica_loaded": False,
        "som_movimento": None,
        "som_start": None,
        "som_troca_fase": None,
        "som_game_over": None
    }

    def p(caminho):
        return os.path.join(base_dir, caminho)

    # Música de fundo
    trilha_path = p("sons/sons/trilha.mp3")
    pygame.mixer.music.load(trilha_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    audio["musica_loaded"] = True

    # Efeitos sonoros
    som_movimento = pygame.mixer.Sound(p("sons/sons/raposa.mp3"))
    som_start = pygame.mixer.Sound(p("sons/sons/start.mp3"))
    som_troca_fase = pygame.mixer.Sound(p("sons/sons/fases.mp3"))
    som_game_over = pygame.mixer.Sound(p("sons/sons/game_over.mp3"))

    som_movimento.set_volume(0.6)
    som_start.set_volume(0.8)
    som_troca_fase.set_volume(0.8)
    som_game_over.set_volume(1.0)

    audio["som_movimento"] = som_movimento
    audio["som_start"] = som_start
    audio["som_troca_fase"] = som_troca_fase
    audio["som_game_over"] = som_game_over

    print("Áudio carregado com sucesso!")
    return audio