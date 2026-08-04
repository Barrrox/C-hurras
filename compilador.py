import sys

from analisador_lexico import Lexer
from analisador_sintatico import ParserSLR

class compilador(): # Classe compilador

    def __init__(self):
        """Classe que instância as outras classes e orquestra a compilação
        """
        self.Lexer = Lexer(sys.argv[1])
        pass

    def compilar(self):

        if len(sys.argv) != 2:
            print("ERRO: arquivo não informado, use o analisador como:\n\tpython analisador_lexico.py codigo.churras")
            return
            
        self.Lexer.ler_arquivo()
        self.Lexer.analisar_lexico()
        self.Lexer.print_tokens()
        self.Lexer.salvar_tokens()

if __name__ == "__main__":

    churras = compilador()
    churras.compilar()
    

