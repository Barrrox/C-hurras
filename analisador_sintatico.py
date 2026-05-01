# classe para representar token (copiada)
class token:
    def __init__(self, texto, tipo, linha):
        self.texto = texto  # string do token
        self.tipo = tipo    # tipo do token (se eh operação, delimitador, etc)
        self.linha = linha  # numero da linha (para escrever as mensagens de erro)

    def tkprint(self):
        print("token:", self.texto, "| tipo:", self.tipo, "| linha:", self.linha)

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
        simbolo = tokens[tpointer].tipo
        
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
                
