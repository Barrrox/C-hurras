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
            else
                pass #ERRO
        else:
            if tabela[nao_terminal(ptop)][terminal(simbolo)] != []:
                pilha.pop()
                for prod in reversed(tabela[nao_terminal(ptop)][terminal(simbolo)]):
                    pilha.append(prod)
                # print(tabela[nao_terminal(ptop)][terminal(simbolo)])
            else:
                pass #ERRO
                
