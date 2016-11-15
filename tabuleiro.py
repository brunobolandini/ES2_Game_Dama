# Tabuleiro do jogo. Precisa de uma altura e uma largura para ser instanciado

class tabuleiro(object):
    PRETA = 1
    BRANCA = 0
    ND = -1
    def __init__(self, altura, largura, primeiroJogador):
        """
            Monta o tauleiro, profundidade eh estaticamente atribuida
        """
        # Define altura e largura do tabuleiro
        self.largura = largura
        self.altura = altura

        # Cria duas listas, cada uma contendo as pecas que cada jogador tem
        self.lista_das_pretas = []
        self.lista_das_brancas = []

        # Colocando as pecas nas posicoes iniciais
        for i in range(largura):
            self.lista_das_pretas.append((i, i % 2))
            self.lista_das_brancas.append((i, altura - (i % 2) - 1))
            if(largura==8)and(i==0):
                self.lista_das_brancas.append((i, 5))
                self.lista_das_brancas.append((2, 5))
                self.lista_das_brancas.append((4, 5))
                self.lista_das_brancas.append((6, 5))
                self.lista_das_pretas.append((i, 2))
                self.lista_das_pretas.append((2, 2))
                self.lista_das_pretas.append((4, 2))
                self.lista_das_pretas.append((6, 2))

        # estado_tabuleiro guarda o estado atual do tabuleiro para printar e para avaliar
        self.estado_tabuleiro = [[' '] * self.largura for x in range(self.altura)]
        self.jogo_vencido = self.ND
        self.vez = primeiroJogador
        self.pronfundidade_maxima = 10

    # Gera um iterator com todos os movimentos
    def iter_jogadas_brancas(self):
        """
            Generator das jogadas para pecas brancas
        """
        for peca in self.lista_das_brancas:
            for jogada in self.iter_pecas_brancas(peca):
                yield jogada
                
    def iter_jogadas_pretas(self):
        """
            Generator das jogadas para pecas brancas
        """
        for peca in self.lista_das_pretas:
            for jogadas in self.iter_pecas_pretas(peca):
                yield jogadas
                
    def iter_pecas_brancas(self, peca):
        """
            Gera as jogadas possiveis para as pecas brancas
        """            
        return self.iter_jogadas(peca, ((-1, -1), (1, -1)))
    
    def iter_pecas_pretas(self, peca):
        """
            Gera as jogadas possiveis para as pecas pretas
        """
        return self.iter_jogadas(peca, ((-1, 1), (1, 1)))

    def iter_jogadas(self, peca, jogadas):
        """
            Faz a execucao das jogadas para pecas brancas e pretas
        """
        for jogada in jogadas:
            # Jogada normal
            alvox = peca[0] + jogada[0]
            alvoy = peca[1] + jogada[1]

            # Checa se jogada esta dentro dos limites do tabuleiro
            if alvox < 0 or alvox >= self.largura or alvoy < 0 or alvoy >= self.altura:
                continue
            alvo = (alvox, alvoy)

            # Checa se tem algo no caminho pro alvo da jogada
            preta = alvo in self.lista_das_pretas
            branca = alvo in self.lista_das_brancas
            if not preta and not branca:
                yield (peca, alvo, self.ND)

            # Tem algo no caminho, da pra pular?
            else:

                # Tem que ser da outra cor pra poder pular
                if self.vez == self.PRETA and preta:
                    continue
                elif self.vez == self.BRANCA and branca:
                    continue

                # Pulo procede adicionando o mesmo movimento para pular pela peca do oponente
                pulax = alvo[0] + jogada[0]
                pulay = alvo[1] + jogada[1]

                # Se o pulo for pra fora do tabuleiro nao pule
                if pulax < 0 or pulax >= self.largura or pulay < 0 or pulay >= self.altura:
                    continue
                pulo = (pulax, pulay)

                # Verifica se nao tem nada pra onde vai pular
                preta = pulo in self.lista_das_pretas
                branca = pulo in self.lista_das_brancas
                if not preta and not branca:
                    yield (peca, pulo, self.vez)
    
    def atualiza_tabuleiro(self):
        """
            Atualiza o array que tem o tabuleiro para representar o estado das pecas no tabuleiro
        """
        for i in range(self.largura):
            for j in range(self.altura):
                self.estado_tabuleiro[i][j] = " "
        for peca in self.lista_das_pretas:
            self.estado_tabuleiro[peca[1]][peca[0]] = u'◆'
        for peca in self.lista_das_brancas:
            self.estado_tabuleiro[peca[1]][peca[0]] = u'◇'

    # Movimento das pecas
    def joga_preta_sem_printar(self, move_de, move_para, ganha_perde):
        """
            Mova peca preta sem printar
        """
        if move_para[0] < 0 or move_para[0] >= self.largura or move_para[1] < 0 or move_para[1] >= self.altura:
            raise Exception("Move peca preta ", move_de, " para fora do tabuleiro")
        preta = move_para in self.lista_das_pretas
        branca = move_para in self.lista_das_brancas
        if not (preta or branca):
            self.lista_das_pretas[self.lista_das_pretas.index(move_de)] = move_para
            self.atualiza_tabuleiro()
            self.vez = self.BRANCA
            self.jogo_vencido = ganha_perde
        else:
            raise Exception
        
    def joga_branca_sem_printar(self, move_de, move_para, ganha_perde):
        """
            Mova peca branca sem printar
        """
        if move_para[0] < 0 or move_para[0] >= self.largura or move_para[1] < 0 or move_para[1] >= self.altura:
            raise Exception("Move peca branca ", move_de, " para fora do tabuleiro")
        preta = move_para in self.lista_das_pretas
        branca = move_para in self.lista_das_brancas
        if not (preta or branca):
            self.lista_das_brancas[self.lista_das_brancas.index(move_de)] = move_para
            self.atualiza_tabuleiro()
            self.vez = self.PRETA
            self.jogo_vencido = ganha_perde
        else:
            raise Exception
    
    def move_preta(self, move_de, move_para, ganha_perde):
        """
            Move a peca preta de uma casa pra outra
            ganha_perde e passado como 0 (se branca) ou 1 (se preta) se o movimento e um pulo
        """
        self.joga_sem_printar(move_de, move_para, ganha_perde)
        self.printa_tabuleiro()
        
    def move_branca(self, move_de, move_para, ganha_perde):
        """

            Move a peca branca de uma casa pra outra
            ganha_perde e passado como 0 (se branca) ou 1 (se preta) se o movimento e um pulo
        """
        self.joga_branca_sem_printar(move_de, move_para, ganha_perde)
        self.printa_tabuleiro()

    def printa_tabuleiro(self):
        """
            Printa o tabuleiro no console
        """
        print unicode(self)
        
    def __unicode__(self):
        """
            Guarda o unicode e outro estado do tabuleiro para printar o tabuleiro
        """
        # Atauliza o estado do tabuleiro
        self.atualiza_tabuleiro()
        linhas = []
        # Printa o numero no topo do tabuleiro
        linhas.append('    ' + '   '.join(map(str, range(self.largura))))

        # Printa a borda de cima do tabuleiro em unicode
        linhas.append(u'  ╭' + (u'───┬' * (self.largura - 1)) + u'───╮')

        # Printa as linhas do tabuleiro
        for num, linha in enumerate(self.estado_tabuleiro[:-1]):
            linhas.append(chr(num+65) + u' │ ' + u' │ '.join(linha) + u' │')
            linhas.append(u'  ├' + (u'───┼' * (self.largura - 1)) + u'───┤')

        # Printa a ultima linha
        linhas.append(chr(self.altura + 64) + u' │ ' + u' │ '.join(self.estado_tabuleiro[-1]) + u' │')

        # Printa a ultima linha do tabuleiro
        linhas.append(u'  ╰' + (u'───┴' * (self.largura - 1)) + u'───╯')
        return '\n'.join(linhas)
