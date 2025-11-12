import pygame
import json

# Arquivo para salvar scores
SCORES_FILE = "scores.json"

def load_scores():
    """Carrega scores do arquivo JSON."""
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

def save_scores(scores):
    """Salva scores no arquivo JSON, limitado a 10 entradas."""
    scores.sort(key=lambda x: x["time"])  # Ordena por tempo (menor primeiro)
    scores = scores[:10]  # Limite
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

def add_score(name, time):
    """Adiciona um score."""
    scores = load_scores()
    scores.append({"name": name, "time": time})
    save_scores(scores)

def text_input_screen(screen, prompt="Digite seu nome:", bg_path="imagens_pygame/ranking.png"):
    """Tela para entrada de texto com fundo personalizado. Centralizada. Texto branco. Frase adicional."""
    SCREENWIDTH, SCREENHEIGHT = screen.get_width(), screen.get_height()
    font = pygame.font.SysFont(None, 48)
    input_font = pygame.font.SysFont(None, 36)
    hint_font = pygame.font.SysFont(None, 28)  # Fonte menor para a dica
    text = ""
    clock = pygame.time.Clock()
    running = True

    # Carrega fundo
    bg = pygame.image.load(bg_path).convert()
    bg = pygame.transform.scale(bg, (SCREENWIDTH, SCREENHEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and text.strip():
                    return text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 20:  # Limite de caracteres
                        text += event.unicode

        # Desenha fundo
        screen.blit(bg, (0, 0))

        # Prompt centralizado
        prompt_surf = font.render(prompt, True, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(center=(SCREENWIDTH // 2, 200))
        screen.blit(prompt_surf, prompt_rect)

        # Texto digitado centralizado (branco)
        text_surf = input_font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(SCREENWIDTH // 2, 300))
        screen.blit(text_surf, text_rect)

        # Frase adicional embaixo (mais para cima)
        hint_surf = hint_font.render("Aperte ENTER para ver ranking", True, (255, 255, 255))
        hint_rect = hint_surf.get_rect(center=(SCREENWIDTH // 2, 780))  # Movido de 340 para 320 (mais para cima)
        screen.blit(hint_surf, hint_rect)

        pygame.display.flip()
        clock.tick(30)

    return ""

def show_ranking_screen(screen, player_name=None, player_time=None, bg_path="imagens_pygame/ranking.png"):
    """Exibe o ranking com fundo personalizado. Jogador em fonte maior, branca. Ranking centralizado entre título e instruções. Instruções na parte inferior, não muito perto do fim."""
    SCREENWIDTH, SCREENHEIGHT = screen.get_width(), screen.get_height()
    font_normal = pygame.font.SysFont(None, 36)
    font_player = pygame.font.SysFont(None, 50)  # Fonte maior para o jogador
    font_title = pygame.font.SysFont(None, 75)  # Título maior
    clock = pygame.time.Clock()
    scores = load_scores()
    running = True

    # Carrega fundo
    bg = pygame.image.load(bg_path).convert()
    bg = pygame.transform.scale(bg, (SCREENWIDTH, SCREENHEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reiniciar: retorna 'restart' para o main.py lidar
                    return 'restart'
                elif event.key == pygame.K_q:
                    # Sair
                    pygame.quit()
                    exit()

        # Desenha fundo
        screen.blit(bg, (0, 0))

        # Título centralizado (maior, mais para baixo)
        title = font_title.render("RANKING", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREENWIDTH // 2, 70))  # Movido de 55 para 70 (mais para baixo)
        screen.blit(title, title_rect)

        # Lista scores centralizada entre título e instruções (máximo 10)
        # Espaço disponível: de ~120 (abaixo do título) até ~780 (acima das instruções em 780)
        # Começar em y=200 para centralizar aproximadamente
        y = 200
        for i, score in enumerate(scores[:10], 1):  # Garante máximo 10
            minutos = int(score["time"] // 60)
            segundos = int(score["time"] % 60)
            text = f"{i}. {score['name']} - {minutos:02}:{segundos:02}"
            is_player = player_name and score["name"] == player_name and score["time"] == player_time
            surf = font_player.render(text, True, (255, 255, 255)) if is_player else font_normal.render(text, True, (255, 255, 255))
            rect = surf.get_rect(center=(SCREENWIDTH // 2, y))
            screen.blit(surf, rect)
            y += 50 if is_player else 40  # Espaçamento maior para jogador

        # Instruções na parte inferior da tela, não muito perto do fim (centralizadas)
        instructions = font_normal.render("Pressione R para reiniciar ou Q para sair", True, (255, 255, 255))
        instr_rect = instructions.get_rect(center=(SCREENWIDTH // 2, 780))  # Parte inferior, mas não no fim (ex.: 780 em tela de 880)
        screen.blit(instructions, instr_rect)

        pygame.display.flip()
        clock.tick(30)

    return None
