class NodoRB:
    def __init__(self, chave, valor):
        self.chave = chave        
        self.valor = valor       
        self.esquerda = None
        self.direita = None
        self.pai = None           
        self.cor = "VERMELHO"     

class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = NodoRB(0, "NIL")
        self.NIL.cor = "PRETO"
        self.NIL.esquerda = None
        self.NIL.direita = None
        self.raiz = self.NIL

    def rotacionar_esquerda(self, x):
        y = x.direita
        x.direita = y.esquerda
        
        if y.esquerda != self.NIL:
            y.esquerda.pai = x
            
        y.pai = x.pai
        
        if x.pai is None:
            self.raiz = y
        elif x == x.pai.esquerda:
            x.pai.esquerda = y
        else:
            x.pai.direita = y
            
        y.esquerda = x
        x.pai = y

    def rotacionar_direita(self, x):
        y = x.esquerda
        x.esquerda = y.direita
        
        if y.direita != self.NIL:
            y.direita.pai = x
            
        y.pai = x.pai
        
        if x.pai is None:
            self.raiz = y
        elif x == x.pai.direita:
            x.pai.direita = y
        else:
            x.pai.esquerda = y
            
        y.direita = x
        x.pai = y

    def inserir(self, chave, valor):
        novo_nodo = NodoRB(chave, valor)
        novo_nodo.esquerda = self.NIL
        novo_nodo.direita = self.NIL
        novo_nodo.cor = "VERMELHO"

        y = None
        x = self.raiz

        # Caminha pela árvore até achar a folha correta
        while x != self.NIL:
            y = x
            if novo_nodo.chave < x.chave:
                x = x.esquerda
            elif novo_nodo.chave > x.chave:
                x = x.direita
            else:
                x.valor = valor # Atualiza se duplicado
                return

        novo_nodo.pai = y
        
        if y is None:
            self.raiz = novo_nodo
        elif novo_nodo.chave < y.chave:
            y.esquerda = novo_nodo
        else:
            y.direita = novo_nodo

        # Se for a raiz, corrige e finaliza
        if novo_nodo.pai is None:
            novo_nodo.cor = "PRETO"
            return

        if novo_nodo.pai.pai is None:
            return

        self._corrigir_insercao(novo_nodo)

    def _corrigir_insercao(self, k):
        while k.pai.cor == "VERMELHO":
            if k.pai == k.pai.pai.direita:
                tio = k.pai.pai.esquerda
                if tio.cor == "VERMELHO":
                    # Apenas recolore
                    tio.cor = "PRETO"
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    k = k.pai.pai
                else:
                    # Rotação à direita
                    if k == k.pai.esquerda:
                        k = k.pai
                        self.rotacionar_direita(k)
                    # Rotação à esquerda
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    self.rotacionar_esquerda(k.pai.pai)
            else:
                tio = k.pai.pai.direita
                if tio.cor == "VERMELHO":
                    # Apenas recolore
                    tio.cor = "PRETO"
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    k = k.pai.pai
                else:
                    # Rotação à direita
                    if k == k.pai.direita:
                        k = k.pai
                        self.rotacionar_esquerda(k)
                    # Rotação à esquerda
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    self.rotacionar_direita(k.pai.pai)
            if k == self.raiz:
                break
        self.raiz.cor = "PRETO"

    def buscar(self, chave):
        return self._buscar_recursivo(self.raiz, chave)

    def _buscar_recursivo(self, nodo, chave):
        if nodo == self.NIL or chave == nodo.chave:
            return None if nodo == self.NIL else nodo
        if chave < nodo.chave:
            return self._buscar_recursivo(nodo.esquerda, chave)
        return self._buscar_recursivo(nodo.direita, chave)

    def obter_minimo(self, nodo):
        while nodo.esquerda != self.NIL:
            nodo = nodo.esquerda
        return nodo

    def substituir_nodos(self, u, v):
        if u.pai is None:
            self.raiz = v
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        v.pai = u.pai

    def remover(self, chave):
        nodo = self._buscar_recursivo(self.raiz, chave)
        if nodo == self.NIL or nodo is None:
            return # Chave não encontrada

        y = nodo
        y_cor_original = y.cor
        if nodo.esquerda == self.NIL:
            x = nodo.direita
            self.substituir_nodos(nodo, nodo.direita)
        elif nodo.direita == self.NIL:
            x = nodo.esquerda
            self.substituir_nodos(nodo, nodo.esquerda)
        else:
            y = self.obter_minimo(nodo.direita)
            y_cor_original = y.cor
            x = y.direita
            if y.pai == nodo:
                x.pai = y
            else:
                self.substituir_nodos(y, y.direita)
                y.direita = nodo.direita
                y.direita.pai = y

            self.substituir_nodos(nodo, y)
            y.esquerda = nodo.esquerda
            y.esquerda.pai = y
            y.cor = nodo.cor

        if y_cor_original == "PRETO":
            self._corrigir_remocao(x)

    def _corrigir_remocao(self, x):
        while x != self.raiz and x.cor == "PRETO":
            if x == x.pai.esquerda:
                irmao = x.pai.direita
                if irmao.cor == "VERMELHO":
                    irmao.cor = "PRETO"
                    x.pai.cor = "VERMELHO"
                    self.rotacionar_esquerda(x.pai)
                    irmao = x.pai.direita

                if irmao.esquerda.cor == "PRETO" and irmao.direita.cor == "PRETO":
                    irmao.cor = "VERMELHO"
                    x = x.pai
                else:
                    if irmao.direita.cor == "PRETO":
                        irmao.esquerda.cor = "PRETO"
                        irmao.cor = "VERMELHO"
                        self.rotacionar_direita(irmao)
                        irmao = x.pai.direita

                    irmao.cor = x.pai.cor
                    x.pai.cor = "PRETO"
                    irmao.direita.cor = "PRETO"
                    self.rotacionar_

    def gerar_dot_text(self):
            if self.raiz == self.NIL:
                return ""
            
            linhas = ["digraph G {", "  node [shape=circle, style=filled, fontname=Helvetica, fontcolor=white];"]
            
            def percorrer(nodo):
                if nodo != self.NIL:
                    cor = "red" if nodo.cor == "VERMELHO" else "black"
                    linhas.append(f'  {nodo.chave} [fillcolor={cor}, color={cor}];')
                    if nodo.esquerda != self.NIL:
                        linhas.append(f'  {nodo.chave} -> {nodo.esquerda.chave};')
                        percorrer(nodo.esquerda)
                    if nodo.direita != self.NIL:
                        linhas.append(f'  {nodo.chave} -> {nodo.direita.chave};')
                        percorrer(nodo.direita)
                        
            percorrer(self.raiz)
            linhas.append("}")
            return "\n".join(linhas)