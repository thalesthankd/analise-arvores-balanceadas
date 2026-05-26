class NodoAVL:
    def __init__(self, chave, valor):
        self.chave = chave        
        self.valor = valor        
        self.esquerda = None
        self.direita = None
        self.altura = 1          

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def obter_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obter_fator_balanceamento(self, nodo):
        if not nodo:
            return 0
        return self.obter_altura(nodo.esquerda) - self.obter_altura(nodo.direita)

    def rotacionar_direita(self, y):
        x = y.esquerda
        T2 = x.direita

        # Executa a rotação
        x.direita = y
        y.esquerda = T2

        # Atualiza as alturas
        y.altura = 1 + max(self.obter_altura(y.esquerda), self.obter_altura(y.direita))
        x.altura = 1 + max(self.obter_altura(x.esquerda), self.obter_altura(x.direita))

        return x

    def rotacionar_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda

        # Executa a rotação
        y.esquerda = x
        x.direita = T2

        # Atualiza as alturas
        x.altura = 1 + max(self.obter_altura(x.esquerda), self.obter_altura(x.direita))
        y.altura = 1 + max(self.obter_altura(y.esquerda), self.obter_altura(y.direita))

        return y

    def inserir(self, chave, valor):
        self.raiz = self._inserir_recursivo(self.raiz, chave, valor)

    def _inserir_recursivo(self, nodo, chave, valor):
        if not nodo:
            return NodoAVL(chave, valor)

        if chave < nodo.chave:
            nodo.esquerda = self._inserir_recursivo(nodo.esquerda, chave, valor)
        elif chave > nodo.chave:
            nodo.direita = self._inserir_recursivo(nodo.direita, chave, valor)
        else:
            nodo.valor = valor  
            return nodo

        # 2. Atualiza a altura do nó pai
        nodo.altura = 1 + max(self.obter_altura(nodo.esquerda), self.obter_altura(nodo.direita))

        # 3. Calcula o Fator de Balanceamento
        fb = self.obter_fator_balanceamento(nodo)

        # 4. Casos de Desbalanceamento
        # Caso Esquerda-Esquerda
        if fb > 1 and chave < nodo.esquerda.chave:
            return self.rotacionar_direita(nodo)

        # Caso Direita-Direita
        if fb < -1 and chave > nodo.direita.chave:
            return self.rotacionar_esquerda(nodo)

        # Caso Esquerda-Direita
        if fb > 1 and chave > nodo.esquerda.chave:
            nodo.esquerda = self.rotacionar_esquerda(nodo.esquerda)
            return self.rotacionar_direita(nodo)

        # Caso Direita-Esquerda
        if fb < -1 and chave < nodo.direita.chave:
            nodo.direita = self.rotacionar_direita(nodo.direita)
            return self.rotacionar_esquerda(nodo)

        return nodo

    def buscar(self, chave):
        return self._buscar_recursivo(self.raiz, chave)

    def _buscar_recursivo(self, nodo, chave):
        if not nodo or nodo.chave == chave:
            return nodo
        if chave < nodo.chave:
            return self._buscar_recursivo(nodo.esquerda, chave)
        return self._buscar_recursivo(nodo.direita, chave)

    def obter_minimo(self, nodo):
        atual = nodo
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def remover(self, chave):
        self.raiz = self._remover_recursivo(self.raiz, chave)

    def _remover_recursivo(self, nodo, chave):
        if not nodo:
            return nodo

        if chave < nodo.chave:
            nodo.esquerda = self._remover_recursivo(nodo.esquerda, chave)
        elif chave > nodo.chave:
            nodo.direita = self._remover_recursivo(nodo.direita, chave)
        else:
            # Nó com apenas um filho ou nenhum
            if not nodo.esquerda:
                return nodo.direita
            elif not nodo.direita:
                return nodo.esquerda

            # Nó com dois filhos: pega o sucessor
            temp = self.obter_minimo(nodo.direita)
            nodo.chave = temp.chave
            nodo.valor = temp.valor
            nodo.direita = self._remover_recursivo(nodo.direita, temp.chave)

        if not nodo:
            return nodo

        # Atualiza a altura
        nodo.altura = 1 + max(self.obter_altura(nodo.esquerda), self.obter_altura(nodo.direita))
        fb = self.obter_fator_balanceamento(nodo)

        # Rebalanceamento após remoção
        if fb > 1 and self.obter_fator_balanceamento(nodo.esquerda) >= 0:
            return self.rotacionar_direita(nodo)
        if fb > 1 and self.obter_fator_balanceamento(nodo.esquerda) < 0:
            nodo.esquerda = self.rotacionar_esquerda(nodo.esquerda)
            return self.rotacionar_direita(nodo)
        if fb < -1 and self.obter_fator_balanceamento(nodo.direita) <= 0:
            return self.rotacionar_esquerda(nodo)
        if fb < -1 and self.obter_fator_balanceamento(nodo.direita) > 0:
            nodo.direita = self.rotacionar_direita(nodo.direita)
            return self.rotacionar_esquerda(nodo)

        return nodo
    
    def gerar_dot_text(self):
        if not self.raiz:
            return ""
        linhas = ["digraph G {", "  node [shape=circle, style=filled, color=lightblue, fontname=Helvetica];"]
        
        def percorrer(nodo):
            if nodo:
                linhas.append(f'  {nodo.chave} [label="Chave: {nodo.chave}\\n[Alt: {nodo.altura}]"];')
                if nodo.esquerda:
                    linhas.append(f'  {nodo.chave} -> {nodo.esquerda.chave};')
                    percorrer(nodo.esquerda)
                if nodo.direita:
                    linhas.append(f'  {nodo.chave} -> {nodo.direita.chave};')
                    percorrer(nodo.direita)

        percorrer(self.raiz)
        linhas.append("}")
        return "\n".join(linhas)