# Fornece o funcao minmax e avaliacao dos tabuleiros
from copy import deepcopy

def jogo_ganho(tabuleiro):
    """
        Retorna true se o jogo foi ganho
    """
    return tabuleiro.jogoGanho <> tabuleiro.ND
        

def minMax2(tabuleiro):
    """
        Funcao principal do minmax, recebe um tabuleiro como input e retorna o melhor movimento possivel
        como um tabuleiro e o valor daquele tabuleiro
    """
    melhor_tabuleiro = None
    profundidade_atual = tabuleiro.pronfundidade_maxima + 1
    while not melhor_tabuleiro and profundidade_atual > 0:
        profundidade_atual -= 1
        # Pega melhor jogada e o valor de maxMinTabuleiro (minmax handler)
        (melhor_tabuleiro, melhor_valor) = max_jogada2(tabuleiro, profundidade_atual)

        # Se receber um tabuleiro null lanca excecao
    if not melhor_tabuleiro:
        raise Exception("Apenas tabuleiros nulos foram retornados.")

    # Senao retorna o tabuleiro e o seu valor
    else:
        return (melhor_tabuleiro, melhor_valor)

def max_jogada2(tabuleiro_max, profundidade_atual):
    """
        Calcula o melhor movimento para as pecas pretas (computador)
        (procura um tabuleiro com valor infinito)
    """
    return max_min_tabuleiro(tabuleiro_max, profundidade_atual - 1, float('-inf'))
    

def min_jogada2(tabuleiro_min, profundidade_atual):
    """
        Calcula o melhor movimento para as pecas brancas (jogador)
        (procura um tabuleiro com valor -infinito)
    """
    return max_min_tabuleiro(tabuleiro_min, profundidade_atual - 1, float('inf'))

def max_min_tabuleiro(tabuleiro, profundidade_atual, melhor_jogada):
    """
        Faz o calculo do melhor movimento
    """
    # Verifica se atingiu o tabuleiro final
    if jogo_ganho(tabuleiro) or profundidade_atual <= 0:
        return (tabuleiro, avaliacao2(tabuleiro))

    # Se nao estamos no final, faca o minmax
    # Defina os valores pro minmax
    melhorJogada = melhor_jogada
    melhorTabuleiro = None

    # tabuleiro max
    if melhor_jogada == float('-inf'):
        # Cria o iterator para os movimentos
        jogadas = tabuleiro.iter_jogadas_pretas()
        for jogada in jogadas:
            tabuleiro_max = deepcopy(tabuleiro)
            tabuleiro_max.joga_preta_sem_printar(*jogada)
            valor = min_jogada2(tabuleiro_max, profundidade_atual - 1)[1]
            if valor > melhorJogada:
                melhorJogada = valor
                melhorTabuleiro = tabuleiro_max
  
    # tabuleiro min
    elif melhor_jogada == float('inf'):
        jogadas = tabuleiro.iter_jogadas_brancas()
        for jogada in jogadas:
            tabuleiro_min = deepcopy(tabuleiro)
            tabuleiro_min.joga_branca_sem_printar(*jogada)
            valor = max_jogada2(tabuleiro_min, profundidade_atual - 1)[1]

            # Pega o menor valor possivel
            if valor < melhorJogada:
                melhorJogada = valor
                melhorTabuleiro = tabuleiro_min

    # Se algo de errado acontece com a melhor jogada lanca uma excecao
    else:
        raise Exception("Melhor jogada e diferente de inf ou -inf")
  
    # Se tudo der certo, e possivel ter um tabuleiro com uma jogada boa
    return (melhorTabuleiro, melhorJogada)

def avaliacao2(avalia_tabuleiro):
    """
        Avalia quao bom o tabuleiro e
        -INF se BRANCO ganhou
        INF se PRETO ganhou
        Senao usa uma estrategia para avaliar a jogada
        Olhar comentario acima do avaliador para ver qual e a estrategia
    """

    # Alguem ganhou o jogo? Se sim retorna o valor INFINITO
    if avalia_tabuleiro.jogoGanho == avalia_tabuleiro.PRETA:
        return float('inf')  
    elif avalia_tabuleiro.jogoGanho == avalia_tabuleiro.BRANCA:
        return float('-inf')

    
    # Configuracao
    pontuacao = 0
    pecas = None
    if avalia_tabuleiro.vez == avalia_tabuleiro.BRANCA:
        pecas = avalia_tabuleiro.lista_das_brancas
        fator_pontuacao = -1
    elif avalia_tabuleiro.vez == avalia_tabuleiro.PRETAS:
        pecas = avalia_tabuleiro.lista_das_brancas
        fator_pontuacao = 1


    # Estrategia de defesa, manter as pecas juntas
    # ate ter a oportunidade de comer uma peca
    distancia = 0
    for peca1 in pecas:
        for peca2 in pecas:
            if peca1 == peca2:
                continue
            dx = abs(peca1[0] - peca2[0])
            dy = abs(peca1[1] - peca2[1])
            distancia += dx**2 + dy**2
    distancia /= len(pecas)
    pontuacao = 1.0/distancia * fator_pontuacao
    
    return pontuacao
