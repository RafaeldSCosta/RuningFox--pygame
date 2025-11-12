import pygame
import sys
from screens import GameStateManager, Start, End, Level, mostrar_instrucao, mostrar_tela_level, mostrar_end_screen
from classes.game import CruzamentoFazenda
from classes.hud import HUD
import ranking
from audio import init_audio

pygame.init()
SCREENWIDTH, SCREENHEIGHT = 950, 880
FPS = 60

# --- Inicializa áudio ---
audio = init_audio(".")

# --- Estados e inicialização ---
STATE = "menu"
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Running Fox Game")

gsm = GameStateManager("start")
menu_start = Start(screen, gsm)
menu_end = End(screen, gsm)
menu_level = Level(screen, gsm)

jogo = CruzamentoFazenda()
hud = HUD(jogo.janela, jogo)

# --- Timer ---
tempo_inicio = None
end_sequence_handled = False

# --- Loop principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if STATE == "menu":
            menu_start.handle_event(event)
            if gsm.get_state() == "level":
                if audio["som_start"]:
                    audio["som_start"].play()

                tempo_inicio = pygame.time.get_ticks()
                mostrar_instrucao(screen, clock, "imagens_pygame/instru.png", 20000)
                mostrar_tela_level(screen, clock, "imagens_pygame/level_1.png", 2000)
                tempo_inicio = pygame.time.get_ticks()
                STATE = "jogo"
                end_sequence_handled = False

        elif STATE == "end":
            menu_end.handle_event(event)
            if gsm.get_state() == "start":
                jogo = CruzamentoFazenda()
                hud = HUD(jogo.janela, jogo)
                tempo_inicio = None
                STATE = "menu"
                if audio["musica_loaded"]:
                    pygame.mixer.music.play(-1)
                end_sequence_handled = False

        elif STATE == "jogo":
            if event.type == pygame.KEYDOWN:
                tecla = pygame.key.name(event.key)
                jogo.raposa.mover_raposa(tecla)

                if tecla == "up" and audio["som_movimento"]:
                    audio["som_movimento"].play()

                if tecla == "escape":
                    STATE = "end"
                if tecla == "r":
                    jogo = CruzamentoFazenda()
                    hud = HUD(jogo.janela, jogo)
                    tempo_inicio = pygame.time.get_ticks()

    # --- Telas ---
    if STATE == "menu":
        menu_start.run()

    elif STATE == "jogo":
        jogo.relogio.tick(FPS)
        jogo.atualizar_plataformas()
        jogo.checar_colisoes_e_reagir()
        jogo.limpar_janela()
        jogo.desenhar_plataformas()
        jogo.raposa.desenhar_raposa(jogo.janela)
        hud.desenhar_vidas()

        if tempo_inicio is not None:
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
            hud.desenhar_timer(tempo_decorrido)

        if jogo.vidas <= 0 or jogo.game_over:
            pygame.mixer.music.stop()
            if audio["som_game_over"]:
                canal = pygame.mixer.find_channel()
                if canal:
                    canal.play(audio["som_game_over"])
                else:
                    audio["som_game_over"].play()
            STATE = "end"

        if jogo.fases.fase == 2 and not hasattr(jogo, "level2_shown"):
            if audio["som_troca_fase"]:
                audio["som_troca_fase"].play()
            mostrar_tela_level(screen, clock, "imagens_pygame/level_2.png", 2000)
            jogo.level2_shown = True

    elif STATE == "end":
        if not end_sequence_handled:
            is_win = getattr(jogo, "reached_ovos", False)
            end_img_path = "imagens_pygame/win.png" if is_win else "imagens_pygame/game_over.png"
            mostrar_end_screen(screen, end_img_path)

            if tempo_inicio is not None:
                elapsed_seconds = (pygame.time.get_ticks() - tempo_inicio) / 1000.0
            else:
                elapsed_seconds = 0.0

            if is_win:
                player_name = ranking.text_input_screen(
                    screen,
                    prompt="Parabéns! Digite seu nome:",
                    bg_path="imagens_pygame/ranking.png"
                )
                if not player_name:
                    player_name = "Player"

                ranking.add_score(player_name, elapsed_seconds)
                result = ranking.show_ranking_screen(
                    screen,
                    player_name=player_name,
                    player_time=elapsed_seconds,
                    bg_path="imagens_pygame/ranking.png"
                )
                if result == 'restart':
                    jogo = CruzamentoFazenda()
                    hud = HUD(jogo.janela, jogo)
                    tempo_inicio = None
                    STATE = "menu"
                    if audio["musica_loaded"]:
                        pygame.mixer.music.play(-1)
                    end_sequence_handled = False
                    continue
            else:
                result = ranking.show_ranking_screen(
                    screen,
                    player_name=None,
                    player_time=None,
                    bg_path="imagens_pygame/ranking.png"
                )
                if result == 'restart':
                    jogo = CruzamentoFazenda()
                    hud = HUD(jogo.janela, jogo)
                    tempo_inicio = None
                    STATE = "menu"
                    if audio["musica_loaded"]:
                        pygame.mixer.music.play(-1)
                    end_sequence_handled = False
                    continue

            end_sequence_handled = True

        menu_end.run()

    pygame.display.update()
    clock.tick(FPS)