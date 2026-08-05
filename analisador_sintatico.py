# classe para representar token
class Token:
    def __init__(self, texto, categoria, linha):
        self.texto = texto  # string do token
        self.categoria = categoria    # categoria/tipo do token (se eh operação, delimitador, etc)
        self.linha = linha  # numero da linha (para escrever as mensagens de erro)

    def tkprint(self):
        print("token:", self.texto, "| categoria:", self.categoria, "| linha:", self.linha)

class ACTIONcell:
    def __init__(self, tipo, valor):
        self.tipo = tipo   # empilha, reduz, aceita, errovazio, erroreduz -> 0, 1, 2, 3, 4
        self.valor = valor # valor numerico referente a acao


# Símbolos (terminais seguidos de não terminais, ordem da tabela SLR)
simbolos = {
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
    'EOF': 22
}
def simbolo(term):
    return simbolos.get(term, 'ERRO')

                
class ParserSLR():


    def __init__(self):
        """O ParserSLR tem os métodos para realizar a analise sintática do código.
        """

        self.pilha = []
        self.tokens = []
        self.tpointer = 0

    def get_tabelaSLR():
        """Função para pegar a tabela SLR. Carrega do disco se a tabela já foi salva e a gramática não sofreu alteração, caso contrário, cria a tabela SLR. 

        Returns:
            _type_: _description_
        """

        # Se a tabela SLR já existe (salva no disco) a gramática não foi alterada, da load.

        # Se a tabela SLR não existe ou a gramática foi alterada, chama a função para gerar uma nova tabelaSLR.

        return tabelaSLR

    def analisar_sintaxe(self, lista_tokens : list[Token]) -> bool:
        """Interface para realizar a analise sintática Bottom-up a partir da lista de tokens. Aceita (True) se o código estiver sintaticamente correto, caso contrário rejeita (False). Quando célula vazia na tabela ACTION, ativa o modo pânico.

        Args:
            lista_tokens (list[Token]): Lista de tokens vinda do analisador léxico.

        Returns:
            bool: True se aceitou, False se encontrou erros sintáticos, mesmo que recupere no modo pânico.
        """

        # Verificar se tabelaSLR existe e gramática não foi alterada
        tabelaSLR = self.get_tabelaSLR()

        return self.analisar_sintaxeAUX(lista_tokens, tabelaSLR, productions)

        pass

    def analisar_sintaxeAUX(self, tokens, tabelaSLR, productions) -> bool:
        # tokens: list of terminals, last element is "$"
        # productions: list of rules A → β (used for output and length lookup)

        stack = ["$", 0]

        ip = 0 # points to current input symbol

        while true:
            s = stack[-1] # current state
            a = tokens[ip] # current input symbol
            act = tabelaSLR[s, simbolo(a.categoria)]
            
            if act.tipo == 0: # empilha
                stack.append(a.categoria) # push the terminal
                stack.append(act.valor) # push the new state
                ip += 1
            
            else if act.tipo == 1: # reduz
                # redução: ['T', ['T', '*', 'F']]
                for i in productions[act.valor][1]:
                    stack.pop()
                    stack.pop()

                s_prime = stack[-1] # exposed state after popping
                stack.append(productions[act.valor][0]) # push the nonterminal
                stack.append(tabelaSLR[s_prime, simbolo(productions[act.valor][0])].valor) # push the new state
            
            else if act.tipo == 2: # aceita
                print("churras ta no ponto certo")
                break
            
            else:
                print("ERRO: token não esperado \"", a.texto, "\" na linha", a.linha)
                
                # attempt recovery
                if act.tipo == 3: # erro de estado vazio
                    ip += 1
                else: # erro de redução
                    # redução: ['T', ['T', '*', 'F']]
                    for i in productions[act.valor][1]:
                        stack.pop()
                        stack.pop()

                    s_prime = stack[-1] # exposed state after popping
                    stack.append(productions[act.valor][0]) # push the nonterminal
                    stack.append(tabelaSLR[s_prime, simbolo(productions[act.valor][0])].valor) # push the new state

        return True

    def modo_panico(self) -> None:
        """ Ativa o modo pânico, alterando o estado interno da analise. Segue o processo:
            1. Identifica falha: Lê token atual via self.tokens[self.tpointer].
            2. Alerta: Imprime mensagem de erro usando linha e texto do token atual.
            3. Descarta fita: Avança self.tpointer iterativamente até achar token de sincronização.
            4. Limpa pilha: Executa self.pilha.pop() até topo da pilha possuir transição válida na tabela ACTION para o token de sincronização.
        """

        pass
