from Token import Token
from automato import AutomatoLR0


# Símbolos (terminais seguidos de não terminais, ordem da tabela SLR)
simbolos = {
    # Terminais (0 – 22)
    ',': 0,
    ';': 1,
    '{': 2,
    '}': 3,
    '(': 4,
    ')': 5,
    'char': 6,
    'id': 7,
    'int': 8,
    'op': 9,
    'string': 10,
    'tipo': 11,
    '=': 12,
    'rodizio': 13,
    'grelhar': 14,
    'ta_no_ponto?': 15,
    'queimou': 16,
    'ponto_certo': 17,
    'queimado': 18,
    'espetar': 19,
    'servir': 20,
    'servido': 21,
    'EOF': 22,

    # Não‑terminais (23 – 49)
    '<chs>': 23,
    '<churras>': 24,
    '<declaracao>': 25,
    '<while>': 26,
    '<for>': 27,
    '<if>': 28,
    '<if_comp>': 29,
    '<entrada>': 30,
    '<saida>': 31,
    '<saida_comp>': 32,
    '<out>': 33,
    '<atribuicao>': 34,
    '<exp>': 35,
    '<logical-or>': 36,
    '<or-tail>': 37,
    '<logical-and>': 38,
    '<and-tail>': 39,
    '<comparison>': 40,
    '<comp-tail>': 41,
    '<additive>': 42,
    '<add-tail>': 43,
    '<term>': 44,
    '<term-tail>': 45,
    '<factor>': 46,
    '<factor-tail>': 47,
    '<unary>': 48,
    '<primary>': 49
}

def simbolo(term : str) -> int:
    return simbolos.get(term, 'ERRO')

                
class ParserSLR():

    def __init__(self):
        """O ParserSLR tem os métodos para realizar a analise sintática do código.
        """

        self.pilha = []
        self.tokens = []
        self.tpointer = 0

    def criar_tabelaSLR(self):

        return tabelaSLR

    def analisar_sintaxe(self, lista_tokens : list[Token]) -> bool:
        """Interface para realizar a analise sintática Bottom-up a partir da lista de tokens. Aceita (True) se o código estiver sintaticamente correto, caso contrário rejeita (False). Quando célula vazia na tabela ACTION, ativa o modo pânico.

        Args:
            lista_tokens (list[Token]): Lista de tokens vinda do analisador léxico.

        Returns:
            bool: True se aceitou, False se encontrou erros sintáticos, mesmo que recupere no modo pânico.
        """

        # Verificar se tabelaSLR existe e gramática não foi alterada
        tabelaSLR = self.criar_tabelaSLR()

        return self.analisar_sintaxeAUX(lista_tokens, tabelaSLR, producoes)

        pass

    def analisar_sintaxeAUX(self, tokens : list[Token], 
                            tabelaSLR : dict[str | int, int], 
                            producoes) -> bool:
        # tokens: list of terminals, last element is "$"
        # producoes: list of rules A → β (used for output and length lookup)

        stack: list[str | int] = ["$", 0]

        ip = 0 # points to current input symbol

        while True:
            s = stack[-1] # current state
            a = tokens[ip] # current input symbol
            act = tabelaSLR[s, simbolo(a.categoria)]


            
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
                stack.append(tabelaSLR[s_prime, simbolo(producoes[act.valor][0])].valor) # push the new state
            
            elif act.tipo == 2: # aceita
                print("churras ta no ponto certo")
                break
            
            else:
                print("ERRO: token não esperado \"", a.texto, "\" na linha", a.linha)
                
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
                    stack.append(tabelaSLR[s_prime, simbolo(producoes[act.valor][0])].valor) # push the new state

        return True

    def modo_panico(self) -> None:
        """ Ativa o modo pânico, alterando o estado interno da analise. Segue o processo:
            1. Identifica falha: Lê token atual via self.tokens[self.tpointer].
            2. Alerta: Imprime mensagem de erro usando linha e texto do token atual.
            3. Descarta fita: Avança self.tpointer iterativamente até achar token de sincronização.
            4. Limpa pilha: Executa self.pilha.pop() até topo da pilha possuir transição válida na tabela ACTION para o token de sincronização.
        """

        pass
