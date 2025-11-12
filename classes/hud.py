import pygame as pg


"""
Heads-up display (HUD) do jogo.

Define a classe `HUD` responsável por desenhar informações na tela, como
vidas (corações), mensagem de game over, instrução para reiniciar e um
timer. Os métodos aqui não gerenciam o estado do jogo, apenas o exibem
com base nos atributos do objeto `jogo` passado na inicialização.
"""


class HUD:
    """Gerencia elementos de interface (vidas, textos, timer).

    Parâmetros:
    - janela: surface do Pygame onde os elementos serão desenhados.
    - jogo: referência ao objeto do jogo (utilizada para ler `vidas`, etc.).
    """

    def __init__(self, janela, jogo):
        self.janela = janela
        self.jogo = jogo

        # Carrega ícones de coração (cheio/vazio). Em caso de falha, definimos
        # como None para evitar exceções posteriormente — os métodos checam isso.
        try:
            self.coracao_cheio = pg.image.load("imagens_pygame/cora.png").convert_alpha()
            self.coracao_vazio = pg.image.load("imagens_pygame/vazio.png").convert_alpha()

            TAMANHO = (45, 45)  # redimensiona para caber no HUD da janela 950x880
            self.coracao_cheio = pg.transform.scale(self.coracao_cheio, TAMANHO)
            self.coracao_vazio = pg.transform.scale(self.coracao_vazio, TAMANHO)
        except Exception as e:
            # Log simples e fallback para None; evita travar se arquivos de asset faltarem
            print("❌ Erro ao carregar ícones de coração:", e)
            self.coracao_cheio = None
            self.coracao_vazio = None

        # Fontes e cores usadas pelo HUD
        self.fonte_gameover = pg.font.Font(None, 84)
        self.fonte_instrucao = pg.font.Font(None, 36)
        self.cor_gameover = (255, 50, 50)
        self.cor_instrucao = (255, 255, 255)
        self.sombra = (0, 0, 0)

    def desenhar_vidas(self):
        """Desenha os ícones de vida no topo da tela.

        Usa `self.jogo.vidas` para decidir quantos corações cheios desenhar.
        Se os ícones não estiverem disponíveis (None), o método retorna
        imediatamente sem desenhar nada.
        """
        if not self.coracao_cheio or not self.coracao_vazio:
            return

        # posição fixa no topo
        x_inicial = 25   # distância da borda esquerda
        y = 20           # distância do topo da tela

        # Desenha até 3 corações (o jogo usa 3 vidas por padrão)
        for i in range(3):
            x = x_inicial + i * 55  # espaçamento horizontal entre corações
            if i < self.jogo.vidas:
                # Coração cheio para vidas restantes
                self.janela.blit(self.coracao_cheio, (x, y))
            else:
                # Coração vazio para vidas perdidas
                self.janela.blit(self.coracao_vazio, (x, y))

    def desenhar_gameover(self):
        """Desenha o texto centralizado 'GAME OVER' com sombra.

        Usamos duas renderizações (sombra + texto) para melhorar visibilidade.
        """
        texto = "GAME OVER"
        surf = self.fonte_gameover.render(texto, True, self.cor_gameover)
        rect = surf.get_rect(center=(self.janela.get_width() // 2, self.janela.get_height() // 2 - 40))
        sombra_surf = self.fonte_gameover.render(texto, True, self.sombra)
        sombra_rect = sombra_surf.get_rect(center=(rect.centerx + 3, rect.centery + 3))
        self.janela.blit(sombra_surf, sombra_rect)
        self.janela.blit(surf, rect)

    def desenhar_reiniciar_instrucao(self):
        """Desenha instrução para reiniciar abaixo do texto de game over.

        Também desenha a sombra do texto para contraste sobre o fundo.
        """
        texto = "Pressione R para reiniciar"
        surf = self.fonte_instrucao.render(texto, True, self.cor_instrucao)
        rect = surf.get_rect(center=(self.janela.get_width() // 2, self.janela.get_height() // 2 + 40))
        sombra_surf = self.fonte_instrucao.render(texto, True, self.sombra)
        sombra_rect = sombra_surf.get_rect(center=(rect.centerx + 2, rect.centery + 2))
        self.janela.blit(sombra_surf, sombra_rect)
        self.janela.blit(surf, rect)

    def desenhar_timer(self, segundos):
        """Desenha o cronômetro no canto superior direito.

        Recebe os segundos totais e formata em MM:SS para exibição.
        """
        minutos = segundos // 60
        segundos = segundos % 60
        tempo_str = f" {minutos:02}:{segundos:02}"

        fonte_timer = pg.font.Font(None, 40)
        surf = fonte_timer.render(tempo_str, True, (255, 255, 255))
        rect = surf.get_rect(topright=(self.janela.get_width() - 30, 20))
        self.janela.blit(surf, rect)
