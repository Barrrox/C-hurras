from Token import Token
from gramatica import Gramatica
from construtor_tabelaSLR import ConstrutorTabelaSLR, SLRcell
from automato import AutomatoLR0


class ParserSLR():

    def __init__(self) -> None:
        """O ParserSLR tem os métodos para realizar a analise sintática do código.
        """

        self.gramatica = Gramatica()

    def simbolo(self, term : str) -> int:
        """Retorna o índice numérico de um símbolo da gramática

        Args:
            term (str): String do símbolo a ser consultado

        Returns:
            int: Índice do símbolo no dicionário, ou 'ERRO' se não encontrado
        """
        return self.gramatica.simbolos.get(term, 'ERRO')

    def criar_tabelaSLR(self) -> list[list['SLRcell']]:
        """Carrega ou constrói a tabela SLR para a gramática atual

        Returns:
            list[list[SLRcell]]: Tabela SLR como matriz bidimensional de SLRcells
        """

        automato = AutomatoLR0()
        automato.gerar_automato(self.gramatica)

        c_tabela = ConstrutorTabelaSLR()
        tabelaSLR = c_tabela.construir_tabelaSLR(self.gramatica, automato)


        return tabelaSLR

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
                            tabelaSLR : list[list[SLRcell]]) -> bool:
        """Executa o algoritmo Shift-Reduce usando a pilha de estados e a tabela SLR. Chamado internamente por analisar_sintaxe.

        Args:
            tokens (list[Token]): Lista de tokens a ser analisada.
            tabelaSLR (list[list[SLRcell]]): Tabela SLR como matriz bidimensional de SLRcells.

        Returns:
            bool: True se não houve erros, False se algum token ativou o modo pânico.
        """

        producoes = self.gramatica.producoes 

        stack: list[str | int] = ["$", 0]

        ip = 0 # points to current input symbol

        teve_erro = False

        while True:

            if ip >= len(tokens): 
                break

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