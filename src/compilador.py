import sys

from analisador_lexico import Lexer
from analisador_sintatico import ParserSLR

class Compilador(): # Classe compilador

    def __init__(self) -> None:
        """Classe que instancia as outras classes e orquestra a compilação
        """
        self.lexer = Lexer()
        self.parser = ParserSLR()
        pass

    def compilar(self, codigo : str) -> None:
        """Executa o pipeline completo de compilação: análise léxica seguida de análise sintática

        Args:
            codigo (str): Código-fonte da linguagem C-Hurras a ser compilado
        """

        lista_tokens = self.lexer.analisar_lexico(codigo)

        aceitou = self.parser.analisar_sintaxe(lista_tokens)

        if aceitou:
            print("Compilação foi um sucesso!")
            print("Churras no ponto")



    

