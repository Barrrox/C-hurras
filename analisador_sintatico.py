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


    def __init__(self, tabela_action, tabela_goto, gramatica):
        """O ParserSLR tem os métodos para realizar a analise sintática do código.

        Deve receber na sua inicialização as tabelas ACTION e GOTO e a gramática (regras de produção)

        Args:
            tabela_action (_type_): _description_
            tabela_goto (_type_): _description_
            gramatica (_type_): _description_
        """

        self.tabela_action = tabela_action
        self.tabela_goto = tabela_goto
        self.regras = gramatica
        self.pilha = []
        self.tokens = []
        self.tpointer = 0

    def analisar_sintaxe(self, lista_tokens : list[Token]) -> bool:
        """Realiaza a analise sintática a partir da lista de tokens. Aceita (True) se o código estiver sintaticamente correto, caso contrário rejeita (False). Quando célula vazia na tabela ACTION, ativa o modo pânico.

        Args:
            lista_tokens (list[Token]): Lista de tokens vinda do analisador léxico.

        Returns:
            bool: True se aceitou, False se encontrou erros sintáticos, mesmo que recupere no modo pânico.
        """

        pass

    def modo_panico(self) -> None:
        """ Ativa o modo pânico, alterando o estado interno da analise. Segue o processo:
            1. Identifica falha: Lê token atual via self.tokens[self.tpointer].
            2. Alerta: Imprime mensagem de erro usando linha e texto do token atual.
            3. Descarta fita: Avança self.tpointer iterativamente até achar token de sincronização.
            4. Limpa pilha: Executa self.pilha.pop() até topo da pilha possuir transição válida na tabela ACTION para o token de sincronização.
        """

        pass





