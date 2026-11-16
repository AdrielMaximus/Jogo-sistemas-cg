import pygame
import sys

pygame.init()

LARGURA, ALTURA = 900, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Missão: Controle de Acesso")

fonte = pygame.font.SysFont(None, 32)
fonte_grande = pygame.font.SysFont(None, 48)
relogio = pygame.time.Clock()

SENHA = "1234"
MAX_ERROS = 3
erros = 0
entrada = ""
estado = "aguardando"

FUNDO = (23, 28, 43)
BRANCO = (245, 245, 245)
VERDE = (50, 200, 100)
VERMELHO = (230, 75, 75)
AMARELO = (240, 190, 50)
AZUL = (60, 110, 180)
PORTA = (110, 75, 48)
PORTA_CLARA = (145, 103, 65)
PRETO = (15, 18, 28)

# Porta: x muda gradualmente para criar a animação de abertura.
porta_x = 560
PORTA_ABERTA_X = 825

def texto(conteudo, x, y, cor=BRANCO, fonte_usada=fonte):
    imagem = fonte_usada.render(conteudo, True, cor)
    tela.blit(imagem, (x, y))

def carregar_personagem():
    try:
        imagem = pygame.image.load("personagem.png").convert_alpha()
        return pygame.transform.smoothscale(imagem, (130, 220))
    except (pygame.error, FileNotFoundError):
        return None

personagem = carregar_personagem()

def desenhar_personagem(x, y):
    if personagem:
        tela.blit(personagem, (x, y))
        return

    # Personagem provisório desenhado com formas geométricas.
    pygame.draw.circle(tela, (190, 35, 55), (x + 45, y + 35), 30)
    pygame.draw.rect(tela, (190, 35, 55), (x + 15, y + 65, 60, 95), border_radius=16)
    pygame.draw.line(tela, BRANCO, (x + 17, y + 85), (x + 72, y + 85), 3)
    pygame.draw.line(tela, BRANCO, (x + 45, y + 67), (x + 45, y + 155), 3)
    pygame.draw.line(tela, (30, 30, 35), (x + 27, y + 158), (x + 20, y + 210), 10)
    pygame.draw.line(tela, (30, 30, 35), (x + 62, y + 158), (x + 72, y + 210), 10)

executando = True

while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                executando = False

            elif evento.key == pygame.K_RETURN:
                if estado not in ("bloqueado", "autorizado") and entrada:
                    if entrada == SENHA:
                        estado = "autorizado"
                    else:
                        erros += 1
                        estado = "bloqueado" if erros >= MAX_ERROS else "negado"
                    entrada = ""

            elif evento.key == pygame.K_BACKSPACE:
                entrada = entrada[:-1]

            elif evento.unicode.isdigit() and estado not in ("bloqueado", "autorizado"):
                if len(entrada) < 4:
                    entrada += evento.unicode

            elif evento.key == pygame.K_r and estado in ("autorizado", "bloqueado"):
                erros = 0
                entrada = ""
                estado = "aguardando"
                porta_x = 560

    # Animação da porta abrindo.
    if estado == "autorizado" and porta_x < PORTA_ABERTA_X:
        porta_x += 5

    tela.fill(FUNDO)

    # Piso e parede ao fundo.
    pygame.draw.rect(tela, (35, 40, 55), (0, 500, LARGURA, 100))
    pygame.draw.line(tela, (80, 88, 105), (0, 500), (LARGURA, 500), 3)

    # Batente e interior visível atrás da porta.
    pygame.draw.rect(tela, (15, 18, 25), (550, 80, 270, 430))
    pygame.draw.rect(tela, (38, 55, 65), (570, 100, 220, 390))
    pygame.draw.circle(tela, (220, 190, 90), (680, 210), 35)

    # Porta deslizante.
    pygame.draw.rect(tela, PORTA, (porta_x, 90, 250, 410), border_radius=8)
    pygame.draw.rect(tela, PORTA_CLARA, (porta_x + 18, 108, 214, 374), 4, border_radius=5)
    pygame.draw.circle(tela, (220, 190, 80), (min(porta_x + 215, 875), 300), 9)

    # Painel de acesso.
    pygame.draw.rect(tela, AZUL, (465, 210, 75, 125), border_radius=8)
    pygame.draw.rect(tela, PRETO, (474, 220, 57, 35), border_radius=5)
    pygame.draw.circle(tela, VERDE if estado == "autorizado" else AMARELO,
                       (502, 280), 9)
    pygame.draw.circle(tela, VERMELHO if estado in ("negado", "bloqueado") else (70, 75, 85),
                       (502, 308), 9)

    # O personagem caminha em direção à porta após a autorização.
    personagem_x = 100
    if estado == "autorizado":
        personagem_x = min(100 + (porta_x - 560) // 2, 330)
    desenhar_personagem(personagem_x, 280)

    texto("CONTROLE DE ACESSO", 35, 25, BRANCO, fonte_grande)
    texto("Digite o codigo de 4 digitos e pressione ENTER.", 35, 75)

    # Mostra o estado do sistema.
    if estado == "aguardando":
        texto("Aguardando codigo", 35, 145, AMARELO)
    elif estado == "autorizado":
        texto("ACESSO AUTORIZADO! Porta abrindo...", 35, 145, VERDE)
    elif estado == "negado":
        texto("ACESSO NEGADO. Tente novamente.", 35, 145, VERMELHO)
    else:
        texto("BLOQUEADO! Pressione R para reiniciar.", 35, 145, AMARELO)

    texto(f"Codigo: {'*' * len(entrada)}", 35, 195)
    texto(f"Tentativas erradas: {erros}/{MAX_ERROS}", 35, 240)
    texto("R reinicia | Backspace apaga | ESC sai", 35, 540)

    pygame.display.flip()
    relogio.tick(30)

pygame.quit()
sys.exit()