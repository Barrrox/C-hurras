from Token import Token
from automato import AutomatoLR0
from gramatica import Gramatica

class ParserSLR():

    def __init__(self) -> None:
        """O ParserSLR tem os métodos para realizar a analise sintática do código.
        """

        gramatica = Gramatica()
        self.producoes = gramatica.producoes
        self.simbolos = gramatica.simbolos

    def simbolo(self, term : str) -> int:
        """Pega o símbolo 

        Args:
            term (str): _description_

        Returns:
            int: _description_
        """
        return self.simbolos.get(term, 'ERRO')

    def criar_tabelaSLR(self) -> dict:

        pass

    def analisar_sintaxe(self, lista_tokens : list[Token]) -> bool:
        """Interface para realizar a analise sintática Bottom-up a partir da lista de tokens. Aceita (True) se o código estiver sintaticamente correto, caso contrário rejeita (False). Quando célula vazia na tabela ACTION, ativa o modo pânico.

        Args:
            lista_tokens (list[Token]): Lista de tokens vinda do analisador léxico.

        Returns:
            bool: True se aceitou, False se encontrou erros sintáticos, mesmo que recupere no modo pânico.
        """

        # FAZER: Verificar se tabelaSLR existe no disco e gramática não foi alterada, se não criar tabelaSLR do zero
        tabelaSLR = self.criar_tabelaSLR()

        return self.analisar_sintaxeAUX(lista_tokens, tabelaSLR)

    def analisar_sintaxeAUX(self, tokens : list[Token], 
                            tabelaSLR : dict[tuple[int | str, int | str], 'Acao']) -> bool:

        producoes = self.producoes 

        stack: list[str | int] = ["$", 0]

        ip = 0 # points to current input symbol

        teve_erro = False

        while True:
            s = stack[-1] # current state
            a = tokens[ip] # current input symbol
            act = tabelaSLR[s][self.simbolo(a.categoria)]
            
            if act.tipo == 0: # empilha
                stack.append(a.categoria) # push the terminal
                stack.append(act.valor) # push the new state
                ip += 1
            
            elif act.tipo == 1: # reduz
                # redução: ['T', ['T', '*', 'F']]
                for i in producoes[act.valor][1]:
                    stack.pop()
                    stack.pop()

                s_prime = stack[-1] # exposed state after popping
                stack.append(producoes[act.valor][0]) # push the nonterminal
                stack.append(tabelaSLR[s_prime][self.simbolo(producoes[act.valor][0])].valor) # push the new state
            
            elif act.tipo == 2: # aceita
                print("churras ta no ponto certo")
                break
            
            else:
                print("ERRO: token não esperado \"", a.texto, "\" na linha", a.linha)
                teve_erro = True
                
                # attempt recovery
                if act.tipo == 3: # erro de estado vazio
                    ip += 1
                else: # erro de redução
                    # redução: ['T', ['T', '*', 'F']]
                    for i in producoes[act.valor][1]:
                        stack.pop()
                        stack.pop()

                    s_prime = stack[-1] # exposed state after popping
                    stack.append(producoes[act.valor][0]) # push the nonterminal
                    stack.append(tabelaSLR[s_prime][self.simbolo(producoes[act.valor][0])].valor) # push the new state

        return not teve_erro