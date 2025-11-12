NTEGRANTES DO GRUPO:

Julia Mendes, Livia Pinheiro e Rafael dos Santos

LINK PARA VÍDEO NO YOUTUBE:

O vídeo demonstra o funcionamento do jogo. Link: https://youtu.be/3nlJiPyZyPI 

SOBRE O JOGO:

Running Fox é um jogo do gênero "crossy road" onde você controla uma raposa que deve fugir de vários inimigos. O objetivo é pegar os ovos no celeiro no menor tempo possível.

COMO JOGAR: ↑ :mover-se para frente (único movimento que emite som). ← →:movimentação lateral. Pressione R para reiniciar a fase. Pressione Q para sair para o menu.

MECÂNICA PRINCIPAL: Evite colisões e tente terminar com todas as vidas para vencer a fase.

  A raposa deve atravessar a fase desviando de obstáculos e inimigos.
  
  O jogo é sincronizado com uma trilha sonora, criando ritmo e imersão.
  
  A cada fase, a dificuldade e a velocidade aumentam.
  
  Se perder todas as vidas → Game Over.
  
  Ao alcançar os ovos no final → Vitória e entrada no ranking.

ESTRUTURA DE CÓDIGO:
RunningFox--Pygame/
  main.py                     # Script principal: gerencia o loop do jogo e os estados (menu, jogo, end)
  audio.py                    # Carrega e inicializa sons e músicas do jog
  ranking.py                  # Sistema de ranking (salva e mostra pontuações em JSON)
  screens.py                  # Gerencia telas (Start, Level, End) e transições
  scores.json                 # Arquivo JSON para salvar o ranking de jogadores

  classes/                    # Contém as classes principais do jogo
    game.py                 # Classe principal do jogo (CruzamentoFazenda): lógica e fases
    hud.py                  # Classe HUD: interface gráfica (vidas, cronômetro, etc.)
    player.py               # Classe da raposa (personagem jogável)
    enemies.py              # Classes de inimigos e obstáculos
    levels.py               # Configuração e controle das fases do jogo
   __pycache__           # Cache interno do Python (gerado automaticamente)
  
  imagens_pygame/             # Recursos visuais do jogo (sprites, fundos, botões)
    imagem_start.png        # Tela inicial
    instru.png              # Tela de instruções
    level_1.png             # Tela de início da fase 1
    level_2.png             # Tela de início da fase 2
    titulo.png              # Logo do jogo (Running Fox)
    win.png                 # Tela de vitória
    game_over.png           # Tela de derrota
    ranking.png             # Tela de ranking
    nuvem1.png ... nuvem4.png # Sprites das nuvens do menu
    botao_start.png         # Imagem do botão de iniciar
    fundo_fazenda.png       # Fundo do cenário principal
    frente.png, costas.png  # Sprites da raposa
    feno1.png ... feno9.png # Sprites dos obstáculos
    rat1.png ... ra
  sons/                       # Recursos de áudio (efeitos e trilhas sonoras)
    start.mp3               # Som ao iniciar o jogo
    fases.mp3               # Som de transição entre fases
    trilha.mp3              # Trilha sonora principal
    raposa.mp3              # Som da raposa se movendo
    game_over.mp3           # Som de derrota

 .vscode/                    # Configurações do VS Code
 ── settings.json           # Configuração do ambiente de desenvolvimento

__pycache__/                # Arquivos compilados do Python (gerado automaticamente)
