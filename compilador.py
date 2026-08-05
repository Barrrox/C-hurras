import sys

from analisador_lexico import Lexer
from analisador_sintatico import ParserSLR

class compilador(): # Classe compilador

    def __init__(self):
        """Classe que instância as outras classes e orquestra a compilação
        """
        self.lexer = Lexer()
        self.parser = ParserSLR()
        pass

    def compilar(self, codigo):

        lista_tokens = self.lexer.analisar_lexico(codigo)

        self.parser.analisar_sintaxe(lista_tokens)

    

