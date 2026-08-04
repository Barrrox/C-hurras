# classe para representar token
class Token:
    def __init__(self, texto, categoria, linha):
        self.texto = texto  # string do token
        self.categoria = categoria    # categoria/tipo do token (se eh operação, delimitador, etc)
        self.linha = linha  # numero da linha (para escrever as mensagens de erro)

    def tkprint(self):
        print("token:", self.texto, "| categoria:", self.categoria, "| linha:", self.linha)

"""
Uma produção pode ser definida como um vetor, tipo

    opcoes = ['A', 'A-', '%']
    
Depois essa opção pode ser convertida em um inteiro pra referencia na tabela com um dicionario, tipo:

    nao_terminais = {
        'A': 0,
        'A-': 1,
        '%': 2
    }

E para acessar, da pra usar uma função, tipo

    def nao_terminal(nterm):
        return nao_terminais.get(nterm, 'ERRO')
        
    def terminal(term):
        return terminais.get(term, 'ERRO')

Para representar a gramática em código, um dicionario também seria interessante:

    gramática = {
        'A': ['%', ['%', 'A-']],
        'A-': ['%']
    }

"""

# Símbolos terminais
terminais = {
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
def terminal(term):
    return terminais.get(term, 'ERRO')

# Realiza analise sintatica topdown
def analisador_sintatico(tokens, tabela):
    # Criar pilha
    pilha = []
    pilha.append('$')
    
    # Ponteiro de token
    tpointer = 0
    
    # Topo da pilha
    ptop = ' '
    
    # Algoritmo principal (derivação de árvore a esquerda com pilha)
    while ptop != '$':
        ptop = pilha[-1]
        simbolo = tokens[tpointer].categoria
        
        if eh_terminal(simbolo):
            if ptop == simbolo:
                pilha.pop()
                tpointer += 1
            else:
                pass #ERRO
        else:
            if tabela[nao_terminal(ptop)][terminal(simbolo)] != []:
                pilha.pop()
                for prod in reversed(tabela[nao_terminal(ptop)][terminal(simbolo)]):
                    pilha.append(prod)
                # print(tabela[nao_terminal(ptop)][terminal(simbolo)])
            else:
                pass #ERRO
                
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

        return self.analisar_sintaxeAUX(lista_tokens, tabelaSLR)

        pass

    def analisar_sintaxeAUX(self, lista_tokens : list[Token], tabelaSLR) -> bool:


        return True

    def modo_panico(self) -> None:
        """ Ativa o modo pânico, alterando o estado interno da analise. Segue o processo:
            1. Identifica falha: Lê token atual via self.tokens[self.tpointer].
            2. Alerta: Imprime mensagem de erro usando linha e texto do token atual.
            3. Descarta fita: Avança self.tpointer iterativamente até achar token de sincronização.
            4. Limpa pilha: Executa self.pilha.pop() até topo da pilha possuir transição válida na tabela ACTION para o token de sincronização.
        """

        pass

def bottomUpParse(tokens, ACTION, GOTO, productions):
    # tokens: list of terminals, last element is "$"
    # productions: list of rules A → β (used for output and length lookup)

    stack = empty stack
    push state 0 onto stack

    ip = 0                     // points to current input symbol

    while true:
        s = top of stack       // current state
        a = tokens[ip]         // current input symbol
        
        if ACTION[s, a] == "shift t":
            push a             // push the terminal (optional)
            push t             // push the new state
            ip = ip + 1
        
        else if ACTION[s, a] == "reduce A → β":
            // pop 2 * |β| items: for each symbol in β, pop state and symbol
            for i = 1 to length(β):
                pop()          // pop state
                pop()          // pop grammar symbol
            s_prime = top of stack   // exposed state after popping
            push A                     // push the nonterminal (optional)
            push GOTO[s_prime, A]      // push the new state
            output "reduce by A → β"   // build parse tree / AST node here
        
        else if ACTION[s, a] == "accept":
            output "parsing successful"
            break
        
        else:
            // error entry in table
            report syntax error and attempt recovery (or halt)
