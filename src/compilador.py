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

        # Analise léxica
        lista_tokens = self.lexer.analisar_lexico(codigo)

        # Análise Sintática
        noAST = self.parser.analisar_sintaxe(lista_tokens)

        # Análise semântica

        if noAST is not None:
            print("Compilação foi um sucesso!")
            print("Churras no ponto!\n")

            print("Árvore Sintática Abstrata gerada:")
            noAST.imprimir()

        # # Análise Semântica: recebe arvore_ast (noAST), valida escopos/tipos na TabelaDeSimbolos -> bool
        # aceitou_semantica = self.semantico.analisar(arvore_ast)
        # if not aceitou_semantica:
        #     return

        # # Geração de Código Intermediário (TAC): recebe arvore_ast validada -> list[str] (instruções 3 endereços)
        # codigo_tac = self.gerador_tac.gerar(arvore_ast)
        # self.gerador_tac.salvar(codigo_tac, "output/codigo_tac.txt")



    

