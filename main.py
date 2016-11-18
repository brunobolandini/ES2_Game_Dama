# Main conduz o jogo
from minmax import *
from tabuleiro import *

# Configura os tamanhos do tabuleiro
largura = 8
altura = 8
primeiroJogador = 0

# Recebe o input do usuario

def get_jogada_usuario(t):

    aviso1 = "Escolha uma peca sua para mover... " + chr(t.lista_das_brancas[0][0] + 97) + str(t.lista_das_brancas[0][1])
    print(aviso1)
    while True: # Enquanto nao receber input valido
        jogada = []
        jogada = raw_input().lower().split()
        if not(len(jogada) == 2):
            print "Essa jogada nao e valida, tente novamente.", aviso1
            continue
        move_de_tup = (int(jogada[0][1]), ord(jogada[0][0]) - 97)
        move_para_tup = (int(jogada[1][1]), ord(jogada[1][0]) - 97)
        # A peca movida pertence ao jogador?
        if not (move_de_tup in t.lista_das_brancas):
            print "Voce nao pertence a peca ", move_de_tup, ". Por favor, selecione uma das suas pecas.", t.whitelist
            continue
        break
    jogada = (move_de_tup, move_para_tup, t.ND)
    return jogada

### MAIN  ###

t = tabuleiro(largura, altura, primeiroJogador)
t.printa_tabuleiro()
print("DamEX")

# loop
while t.jogoGanho == -1:
    # Usuario comeca jogando
    jogada_usuario = get_jogada_usuario(t)
    try:
        t.move_branca(*jogada_usuario)
    except Exception:
        print "Jogada invalida"
        continue

    # Vez da maquina
    print "Vez do computador: computador pensando..."
    temp = minMax2(t)
    t = temp[0]
    print "~~~~~~~~~~~~~JOGADA DO COMPUTADOR~~~~~~~~~~~~~"
    t.printa_tabuleiro()
    if t.jogoGanho == t.BRANCA:
        print "Usuario ganhou o jogo"
        print "Game Over"
        break
    elif t.jogoGanho == t.PRETA:
        print "Computador ganhou o jogo"
        print "Game Over"
        break
