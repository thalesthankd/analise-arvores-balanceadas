import random
from avl import ArvoreAVL
from rubro_negra import ArvoreRubroNegra

def menu():
    arvore_atual = None
    tipo_arvore = ""

    while True:
        print("\n" + "="*40)
        print("      SISTEMA DE ARVORES BALANCEADAS")
        print("="*40)
        print(f" Estrutura Ativa: {tipo_arvore if tipo_arvore else 'Nenhuma'}")
        print("-"*40)
        print("1. Selecionar Arvore AVL")
        print("2. Selecionar Arvore Rubro-Negra")
        print("3. Inserir um elemento manualmente")
        print("4. Inserir multiplos valores aleatorios")
        print("5. Remover um elemento por chave")
        print("6. Buscar um elemento por chave")
        print("7. Visualizar estrutura da arvore")
        print("0. Sair")
        print("="*40)
        
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            arvore_atual = ArvoreAVL()
            tipo_arvore = "AVL"
            print("\nArvore AVL inicializada.")
        
        elif opcao == "2":
            arvore_atual = ArvoreRubroNegra()
            tipo_arvore = "Rubro-Negra"
            print("\nArvore Rubro-Negra inicializada.")
            
        elif opcao == "3":
            if not arvore_atual:
                print("\n[Erro] Selecione uma arvore primeiro.")
                continue
            try:
                chave = int(input("Digite a chave (Inteiro): "))
                valor = input("Digite o valor/dado associado: ")
                arvore_atual.inserir(chave, valor)
                print(f"Chave {chave} inserida.")
            except ValueError:
                print("[Erro] A chave precisa ser um numero inteiro.")

        elif opcao == "4":
            if not arvore_atual:
                print("\n[Erro] Selecione uma arvore primeiro.")
                continue
            try:
                qtd = int(input("Quantos valores aleatorios deseja inserir? "))
                if qtd <= 0:
                    print("[Erro] A quantidade deve ser maior que zero.")
                    continue
                
                valores_gerados = [random.randint(1, qtd * 3) for _ in range(qtd)]
                for val in valores_gerados:
                    arvore_atual.inserir(val, f"Dado_{val}")
                print(f"\n[Sucesso] {qtd} elementos aleatorios foram inseridos.")
            except ValueError:
                print("[Erro] Digite um numero inteiro valido.")

        elif opcao == "5":
            if not arvore_atual:
                print("\n[Erro] Selecione uma arvore primeiro.")
                continue
            try:
                chave = int(input("Digite a chave para remocao: "))
                arvore_atual.remover(chave)
                print(f"Operacao de remocao executada para a chave {chave}.")
            except ValueError:
                print("[Erro] A chave precisa ser um numero inteiro.")

        elif opcao == "6":
            if not arvore_atual:
                print("\n[Erro] Selecione uma arvore primeiro.")
                continue
            try:
                chave = int(input("Digite a chave para busca: "))
                resultado = arvore_atual.buscar(chave)
                if resultado:
                    print(f"\nElemento Encontrado! Dado: {resultado.valor}")
                else:
                    print("\nChave nao encontrada na arvore.")
            except ValueError:
                print("[Erro] A chave precisa ser um número inteiro.")

        elif opcao == "7":
            if not arvore_atual:
                print("\n[Erro] Nenhuma arvore ativa para visualizar.")
                continue
            
            texto_dot = ""
            if tipo_arvore == "AVL":
                texto_dot = arvore_atual.gerar_dot_text()
            elif tipo_arvore == "Rubro-Negra":
                texto_dot = arvore_atual.gerar_dot_text()

            if not texto_dot:
                print("\nA arvore atual esta vazia.")
                continue

            print("\n--- COPIE O TEXTO ABAIXO ---")
            print(texto_dot)
            print("----------------------------")
            print("Copie todo o conteudo demarcado acima e cole no site 'edotor.net' ou 'dreampuf.github.io/graphviz-online/'")

        elif opcao == "0":
            print("\nEncerrando o programa.")
            break
        else:
            print("\Opção invalida.")

if __name__ == "__main__":
    menu()