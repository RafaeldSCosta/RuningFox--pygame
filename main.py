"""
Script principal do jogo Running Fox.

Gerencia o loop principal, estados do jogo (menu, jogo, tela de fim),
transições de estado, atualização de lógica, desenho de sprites e áudio.
"""

import pygame
import sys
from screens import GameStateManager, Start, End, Level, mostrar_instrucao, mostrar_tela_level, mostrar_end_screen
from classes.game import CruzamentoFazenda
from classes.hud import HUD
import ranking
from audio import init_audio

# Inicializa Pygame
pygame.init()

# Constantes de tela
SCREENWIDTH, SCREENHEIGHT = 950, 880
FPS = 60

# --- Inicializa áudio ---
# Carrega efeitos sonoros e música (fpath = ".")
audio = init_audio(".")

# --- Estados e inicialização ---
# STATE controla qual tela/lógica está ativa (menu, jogo, end)
STATE = "menu"
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Running Fox Game")

# Gerenciador de estado e menus
gsm = GameStateManager("start")
menu_start = Start(screen, gsm)
menu_end = End(screen, gsm)
menu_level = Level(screen, gsm)

# Instâncias principais do jogo
jogo = CruzamentoFazenda()
hud = HUD(jogo.janela, jogo)

# --- Timer ---
# tempo_inicio: marca quando o jogo começou (para o cronômetro do HUD)
# end_sequence_handled: flag para evitar executar a sequência de fim múltiplas vezes
tempo_inicio = None
end_sequence_handled = False

# --- Loop principal ---
# Processa eventos e atualiza o estado do jogo continuamente
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # --- Estado: MENU ---
        # Tela inicial; permite transição para "jogo" quando jogador pressiona start
        if STATE == "menu":
            menu_start.handle_event(event)
            if gsm.get_state() == "level":
                # Toca som de início
                if audio["som_start"]:
                    audio["som_start"].play()

                # Mostra telas de instrução e nível antes de iniciar
                tempo_inicio = pygame.time.get_ticks()
                mostrar_instrucao(screen, clock, "imagens_pygame/instru.png", 20000)
                mostrar_tela_level(screen, clock, "imagens_pygame/level_1.png", 2000)
                tempo_inicio = pygame.time.get_ticks()
                STATE = "jogo"
                end_sequence_handled = False

        # --- Estado: END (Tela de Fim) ---
        # Mostra resultado (vitória/derrota) e ranking; permite voltar ao menu
        elif STATE == "end":
            menu_end.handle_event(event)
            if gsm.get_state() == "start":
                # Reinicia o jogo quando volta ao menu
                jogo = CruzamentoFazenda()
                hud = HUD(jogo.janela, jogo)
                tempo_inicio = None
                STATE = "menu"
                if audio["musica_loaded"]:
                    pygame.mixer.music.play(-1)
                end_sequence_handled = False

        # --- Estado: JOGO ---
        # Loop de gameplay; processa input do jogador
        elif STATE == "jogo":
            if event.type == pygame.KEYDOWN:
                tecla = pygame.key.name(event.key)
                jogo.raposa.mover_raposa(tecla)

                # Toca som ao mover
                if tecla == "up" and audio["som_movimento"]:
                    audio["som_movimento"].play()

                # ESC: vai para tela de fim
                if tecla == "escape":
                    STATE = "end"
                # R: reinicia a fase
                if tecla == "r":
                    jogo = CruzamentoFazenda()
                    hud = HUD(jogo.janela, jogo)
                    tempo_inicio = pygame.time.get_ticks()

    # --- Atualização de telas ---
    # Renderiza a tela apropriada baseada no estado atual
    
    if STATE == "menu":
        # Desenha menu inicial
        menu_start.run()

    elif STATE == "jogo":
        # Atualiza lógica de jogo
        jogo.relogio.tick(FPS)
        jogo.atualizar_plataformas()
        jogo.checar_colisoes_e_reagir()
        
        # Renderiza jogo
        jogo.limpar_janela()
        jogo.desenhar_plataformas()
        jogo.raposa.desenhar_raposa(jogo.janela)
        hud.desenhar_vidas()

        # Desenha cronômetro
        if tempo_inicio is not None:
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
            hud.desenhar_timer(tempo_decorrido)

        # Checa se perdeu ou venceu e vai para tela de fim
        if jogo.vidas <= 0 or jogo.game_over:
            pygame.mixer.music.stop()
            if audio["som_game_over"]:
                canal = pygame.mixer.find_channel()
                if canal:
                    canal.play(audio["som_game_over"])
                else:
                    audio["som_game_over"].play()
            STATE = "end"

        # Transição para fase 2 se completou fase 1
        if jogo.fases.fase == 2 and not hasattr(jogo, "level2_shown"):
            if audio["som_troca_fase"]:
                audio["som_troca_fase"].play()
            mostrar_tela_level(screen, clock, "imagens_pygame/level_2.png", 2000)
            jogo.level2_shown = True

    elif STATE == "end":
        # Tela de fim: mostra vitória/derrota e ranking
        if not end_sequence_handled:
            # Define qual imagem de fim exibir (vitória ou derrota)
            is_win = getattr(jogo, "reached_ovos", False)
            end_img_path = "imagens_pygame/win.png" if is_win else "imagens_pygame/game_over.png"
            mostrar_end_screen(screen, end_img_path)

            # Calcula tempo decorrido
            if tempo_inicio is not None:
                elapsed_seconds = (pygame.time.get_ticks() - tempo_inicio) / 1000.0
            else:
                elapsed_seconds = 0.0

            # Se venceu: pede nome e salva score
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
                # Se escolher restart, volta ao menu
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
                # Se perdeu: apenas mostra ranking sem salvar
                result = ranking.show_ranking_screen(
                    screen,
                    player_name=None,
                    player_time=None,
                    bg_path="imagens_pygame/ranking.png"
                )
                # Se escolher restart, volta ao menu
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

        # Desenha menu de fim
        menu_end.run()

    # Atualiza display e tick do relógio
    pygame.display.update()
    clock.tick(FPS)