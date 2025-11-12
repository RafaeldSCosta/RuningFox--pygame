from pathlib import Path
import json
import pygame

# Arquivo para salvar scores (Path)
SCORES_FILE = Path("scores.json")

def ensure_scores_file():
    """Garante que o arquivo exista (cria vazio se não existir)."""
    if not SCORES_FILE.exists():
        SCORES_FILE.write_text("[]", encoding="utf-8")  # inicializa com lista vazia

def load_scores():
    """Carrega scores do arquivo JSON. Se arquivo vazio/inválido, retorna []"""
    ensure_scores_file()
    try:
        text = SCORES_FILE.read_text(encoding="utf-8").strip()
        if not text:
            return []
        return json.loads(text)
    except json.JSONDecodeError:
        # Se estiver corrompido, reescreve como lista vazia e retorna []
        SCORES_FILE.write_text("[]", encoding="utf-8")
        return []

def save_scores(scores):
    """Salva scores no arquivo JSON, limitado a 10 entradas."""
    # Garantir que seja lista e ordenar
    if not isinstance(scores, list):
        scores = list(scores)
    scores.sort(key=lambda x: x.get("time", float("inf")))  # Ordena por tempo (menor primeiro)
    scores = scores[:10]  # Limite a top 10
    SCORES_FILE.write_text(json.dumps(scores, ensure_ascii=False, indent=4), encoding="utf-8")

def add_score(name, time):
    """Adiciona um score (name: str, time: float)."""
    scores = load_scores()
    try:
        time_val = float(time)
    except (ValueError, TypeError):
        time_val = 0.0
    scores.append({"name": str(name), "time": time_val})
    save_scores(scores)

# --- As funções de interface visual (mantive seu código, só troquei a leitura de imagem se quiser) ---

def text_input_screen(screen, prompt="Digite seu nome:", bg_path="imagens_pygame/ranking.png"):
    SCREENWIDTH, SCREENHEIGHT = screen.get_width(), screen.get_height()
    font = pygame.font.SysFont(None, 48)
    input_font = pygame.font.SysFont(None, 36)
    hint_font = pygame.font.SysFont(None, 28)
    text = ""
    clock = pygame.time.Clock()
    running = True

    # Carrega fundo — se o caminho for relativo, é recomendado usar Path(__file__).parent / 'imagens...' no main
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
                    if len(text) < 20:
                        text += event.unicode

        screen.blit(bg, (0, 0))
        prompt_surf = font.render(prompt, True, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(center=(SCREENWIDTH // 2, 200))
        screen.blit(prompt_surf, prompt_rect)

        text_surf = input_font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(SCREENWIDTH // 2, 300))
        screen.blit(text_surf, text_rect)

        hint_surf = hint_font.render("Aperte ENTER para ver ranking", True, (255, 255, 255))
        hint_rect = hint_surf.get_rect(center=(SCREENWIDTH // 2, 780))
        screen.blit(hint_surf, hint_rect)

        pygame.display.flip()
        clock.tick(30)

    return ""

def show_ranking_screen(screen, player_name=None, player_time=None, bg_path="imagens_pygame/ranking.png"):
    SCREENWIDTH, SCREENHEIGHT = screen.get_width(), screen.get_height()
    font_normal = pygame.font.SysFont(None, 36)
    font_player = pygame.font.SysFont(None, 50)
    font_title = pygame.font.SysFont(None, 75)
    clock = pygame.time.Clock()
    scores = load_scores()
    running = True

    bg = pygame.image.load(bg_path).convert()
    bg = pygame.transform.scale(bg, (SCREENWIDTH, SCREENHEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

        screen.blit(bg, (0, 0))

        title = font_title.render("RANKING", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREENWIDTH // 2, 70))
        screen.blit(title, title_rect)

        y = 200
        for i, score in enumerate(scores[:10], 1):
            minutos = int(score["time"] // 60)
            segundos = int(score["time"] % 60)
            text = f"{i}. {score['name']} - {minutos:02}:{segundos:02}"
            is_player = player_name and score["name"] == player_name and score["time"] == player_time
            surf = font_player.render(text, True, (255, 255, 255)) if is_player else font_normal.render(text, True, (255, 255, 255))
            rect = surf.get_rect(center=(SCREENWIDTH // 2, y))
            screen.blit(surf, rect)
            y += 50 if is_player else 40

        instructions = font_normal.render("Pressione R para reiniciar ou Q para sair", True, (255, 255, 255))
        instr_rect = instructions.get_rect(center=(SCREENWIDTH // 2, 780))
        screen.blit(instructions, instr_rect)

        pygame.display.flip()
        clock.tick(30)

    return None
