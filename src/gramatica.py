import os
import json

class Gramatica:
        def __init__(self, arquivo_producoes = "regras_producao.json") -> None:
            """Classe que:
                1. Lê o arquivo JSON da gramática (ATENÇÃO: Produções A -> a | b já estão separadas em A -> a e A -> b)
                2. Contém as regras de produção
                3. Pega terminais e não terminais
                4. Calcula First e Follow (guarda em atributos publicos para serem usados no construtor de tabelas)

            Args:
                arquivo_producoes (str): Caminho relativo para o arquivo da gramática
            """

            # Pega o caminho absoluto da pasta atual (src/) e junta com o nome do arquivo
            caminho_base = os.path.dirname(os.path.abspath(__file__))
            caminho_completo = os.path.join(caminho_base, arquivo_producoes)

            with open(caminho_completo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                # JSON lê como listas. Transforma em tuplas:
                producoes = tuple(tuple([regra[0], (tuple(dir for dir in regra[1]))]) for regra in dados)

            self.producoes: tuple[tuple[str, tuple[str, ...]], ...] = producoes

            self.terminais: list[str] = []
            self.nao_terminais: list[str] = []
            
            self.simbolos = self.get_simbolos()

            # Dicionário onde a chave é o não terminal X e o valor é uma lista onde cada elemento está em follow(X)
            self.follow = self.calcular_conjunto_follow()

        def get_simbolos(self) -> dict[str, int]:
            """Lê as regras de produção e retorna um dict com os símbolos indexados da gramática para e evitar trabalhar com strings. Também salva separadamente os terminais e não terminais em self.terminais e self.nao_terminais.

            Returns:
                dict[str, int]: Dicionário em que a chave é uma string e o valor é um int.
            """
            terminais = []
            nao_terminais = []

            # Loop para iterar sobre todas as produções e capturar os terminais e n-terminais
            # producao = (prod_esq, [prod_dir1, prod_dir2, ...])
            for simb_esq, prod_dir in self.producoes:

                if simb_esq not in nao_terminais:
                    nao_terminais.append(simb_esq) # Pega simbolo da esquerda da produção

                for simbolo in prod_dir: # Pega simbolos da direita da produção

                    if simbolo[0] == "<" and simbolo[-1]  == ">": # Se é n terminal
                        if simbolo not in nao_terminais:
                            nao_terminais.append(simbolo)

                    else: # é terminal
                        if simbolo not in terminais:
                            terminais.append(simbolo)

            # Montar o dicionário { 'simbolo': indice }
            simbolos = {}
            idx = 0
            
            # Adiciona Não-Terminais primeiro (Tentar garantir <chs> como 0)
            for nt in nao_terminais:
                simbolos[nt] = idx
                idx += 1

            # Adiciona Terminais depois
            for t in terminais:
                simbolos[t] = idx
                idx += 1

            self.terminais = terminais
            self.nao_terminais = nao_terminais

            return simbolos

        def calcular_conjunto_first(self) -> dict[str, list[str | tuple]]:
            """Calcula o conjunto First para toda a gramática. Retorna em foma de dicionário onde a chave é o não terminal X e o valor é o first(X) em forma de lista. O vazio é representado por uma tupla vazia ().

            Returns:
                dict[str, list[str]]: _description_
            """

            # Dicionário onde a chave é o não terminal X e o valor é uma lista onde cada elemento está em first(X)
            # Está global aqui para que first possa alterar em todas as chamadas recursivas
            conjunto_first = {nao_t : set() for nao_t in self.nao_terminais}

            def first(X : str) -> set[str]:
                """Calcula o First do símbolo X e retorna o conjunto First(X)
                
                Args:
                    X (str): Símbolo (terminal ou não terminal)

                Returns:
                    list[str] : Conjunto First(X) 

                """

                # Caso base
                # 1. Se X é um símbolo terminal, então FIRST(X) = {X}.
                if X in self.terminais:
                    return set([X])

                # Inicializa conjunto first de X vazio
                firstX = set()

                # Buscar todas as produções que começam com o símbolo
                for producao in self.producoes:

                    esq_prod = producao[0]
                    dir_prod = producao[1]

                    # Se não é o símbolo que estamos procurando, vai para a próxima produção
                    if esq_prod != X:
                        continue

                    # 2. Se X for uma produção do tipo X -> ε, adicione ε a FIRST(X) e vai para a próxima produção
                    if len(dir_prod) == 1 and dir_prod[0] == (): # produção só tem 1 elemento e é uma Tupla vazia = ε
                        firstX.add(()) # sim, isso realmente adiciona a tupla vazia no conjunto, eu testei
                        continue

                    # 3. Se X for uma produção do tipo X -> Y1Y2...Yk, coloque em FIRST(X) todos os terminais de FIRST(Y1), exceto ε. Adicione também os de FIRST(Y2), exceto ε, se Y1 derivar ε, e assim sucessivamente até Yk ou até que algum Yi não derive ε.
                    
                    # Ler os símbolos
                    for i in range(len(dir_prod)):

                        Y = dir_prod[i]

                        if Y == X: # E -> E, pula
                            break

                        firstY = first(Y) # Pode dar loop infinito se first(Y) contém first(X) (Y -> X)
                        firstYsemVazio = firstY - {()}

                        # Adiciona em first(Y) - {ε} em first(X)
                        firstX |= firstYsemVazio # a |= b -> a = a | b (insira caveira emoji). 

                        # Adicionar firstX no dicionario conjunto_first
                        conjunto_first[X] |= firstX 

                        # Se não há vazio em first(Y), não pode prosseguir para o próximo simbolo da produção
                        if () not in firstY: 
                            break
                        else: # Se há vazio, prossegue.
                            # Situação X -> YZW: Se estamos na última produção e há vazio em W, adiciona o vazio a first(X)
                            if i == len(dir_prod) - 1: 
                                conjunto_first[X].add(())

                return firstX

            for nao_t in self.nao_terminais:
                conjunto_first[nao_t] = first(nao_t)

            return conjunto_first

            

        def calcular_conjunto_follow(self) -> dict[str, list[str]]:
            """Roda algoritmo para criar e retornar o conjunto Follow para toda a gramática. Vai precisar calcular o First antes.
            
            Returns:
                dict: Conjunto Follow. Chave = Não terminal X. Valor = lista dos não terminais -> follow(X)
            """


            """
            Sendo X um não-terminal, Follow(X) é o conjunto de terminais que podem aparecer imediatamente à direita de X em alguma forma sentencial

            Regras para o conjunto FOLLOW:
            1. Se S é o símbolo inicial da gramática, adicione $ a FOLLOW(S).
            2. Se houver uma produção A -> aBb, então tudo que está em FIRST(b), exceto ε, é adicionado a FOLLOW(B).
            3. Se houver uma produção A -> aB, ou uma produção A -> aBb onde FIRST(b) contém ε, então tudo que está em FOLLOW(A) é adicionado a FOLLOW(B)."""

            first = self.calcular_conjunto_first()

            def follow(X : str):
                """Calcula o conjunto follow para o símbolo não terminal X.

                Args:
                    X (str): Símbolo não terminal cujo conjunto follow(X) deseja-se encontrar

                Returns:
                    set[str]: Conjunto Follow
                """

            follow_x = set()
            for producao in self.producoes:
                


                # 1. Se S é o símbolo inicial da gramática, adicione $ a FOLLOW(S).





            return None