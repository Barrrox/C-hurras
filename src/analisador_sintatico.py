from Token import Token
from gramatica import Gramatica
from construtor_tabelaSLR import ConstrutorTabelaSLR, SLRcell
from automato import AutomatoLR0
from arvore_ast import noAST, criar_no


class ParserSLR():

    def __init__(self) -> None:
        """O ParserSLR tem os métodos para realizar a analise sintática do código.
        """

        self.gramatica = Gramatica()
        self.AST: noAST | None = None

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
        automato.exportar_json()

        c_tabela = ConstrutorTabelaSLR()
        tabelaSLR = c_tabela.construir_tabelaSLR(self.gramatica, automato)


        return tabelaSLR

    def analisar_sintaxe(self, lista_tokens : list[Token]) -> noAST:
        """Interface para realizar a analise sintática Bottom-up a partir da lista de tokens. Aceita (Retorna a AST) se o código estiver sintaticamente correto, caso contrário rejeita (Retorna None). Quando célula vazia na tabela ACTION, ativa o modo pânico.

        Args:
            lista_tokens (list[Token]): Lista de tokens vinda do analisador léxico.

        Returns:
            noAST: Retorna a Árvore Sintática Abstrata se aceitou, senão retorna None pois algum token ativou o modo pânico.
        """

        tabelaSLR = self.criar_tabelaSLR()

        return self.analisar_sintaxeAUX(lista_tokens, tabelaSLR)

    def analisar_sintaxeAUX(self, tokens : list[Token], 
                            tabelaSLR : list[list[SLRcell]]) -> noAST:
        """Executa o algoritmo Shift-Reduce usando a pilha de estados e a tabela SLR. Chamado internamente por analisar_sintaxe.

        Args:
            tokens (list[Token]): Lista de tokens a ser analisada.
            tabelaSLR (list[list[SLRcell]]): Tabela SLR como matriz bidimensional de SLRcells.

        Returns:
            noAST: Retorna a Árvore Sintática Abstrata se aceitou, senão retorna None pois algum token ativou o modo pânico.
        """

        producoes = self.gramatica.producoes 
        regras_semanticas = self.gramatica.regras_semanticas

        stack: list[str | int] = ["$", 0]
        stack_ast: list[Token | noAST | None] = [] # Serve para guardar os nós da AST junto do stack normal. Assim, quando empiliar em um empilha no outro. Quando reduzir, forma-se um nó de nível mais alto na árvore.
        self.AST = None

        ip = 0 # points to current input symbol

        teve_erro = False

        while True:

            if ip >= len(tokens): 
                break

            s = stack[-1] # current state
            a = tokens[ip] # current input symbol

            act : SLRcell = tabelaSLR[s][self.simbolo(a.categoria)]

            if act.tipo == 0: # empilha

                stack.append(a.categoria) # push the terminal
                stack.append(act.valor) # push the new state
                stack_ast.append(a)
                ip += 1
            
            elif act.tipo == 1: # reduz

                # redução: ['T', ['T', '*', 'F']]
                simb_esq = producoes[act.valor][0]
                prod_dir = producoes[act.valor][1]
                elementos_desempilhados = []

                if prod_dir != ('~',):
                    for i in prod_dir:
                        stack.pop()
                        stack.pop()
                        elementos_desempilhados.append(stack_ast.pop())
                    elementos_desempilhados.reverse()

                regra_sem = regras_semanticas[act.valor] if act.valor < len(regras_semanticas) else None
                novo_no = criar_no(regra_sem, simb_esq, elementos_desempilhados)
                stack_ast.append(novo_no)

                s_prime = stack[-1] # exposed state after popping
                stack.append(simb_esq) # push the nonterminal
                stack.append(tabelaSLR[s_prime][self.simbolo(simb_esq)].valor) # push the new state
            elif act.tipo == 2: # aceita
                self.AST = stack_ast[-1] if stack_ast else None
                break
            
            else:
                teve_erro = True

                print("ERRO SINTÁTICO: token não esperado \"", a.texto, "\" na linha", a.linha)

                # attempt recovery
                if act.tipo == 3: # erro de estado vazio
                    ip += 1
                else: # erro de redução
                    # redução: ['T', ['T', '*', 'F']]
                    for i in producoes[act.valor][1]:
                        stack.pop()
                        stack.pop()
                        if stack_ast:
                            stack_ast.pop()
                    stack_ast.append(None)

                    s_prime = stack[-1] # exposed state after popping
                    stack.append(producoes[act.valor][0]) # push the nonterminal
                    stack.append(tabelaSLR[s_prime][self.simbolo(producoes[act.valor][0])].valor) # push the new state

        if not teve_erro:
            return self.AST
        else:
            return None
        