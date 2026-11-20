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

        # ------ Colinha para a AST ---------
        # Análise Sintática -> retorna a raiz da AST (ou None se erro sintático)
        # Estrutura de cada nó (noAST):
        # =============================================================
        # noAST.tipo   : categoria do nó:
        #                  - Blocos/Comandos: "churras", "declaracao", "if", "else", "while", "for", "entrada", "saida"
        #                  - Operações: "operacao" ("=", "+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!")
        #                  - Folhas: "tipo", "id", "int", "char", "string", "ponto_certo", "queimado", "servido"
        # noAST.valor  : 
        #                  - se tipo é folha, valor é o lexema (ex: "vaca", "x", "10")
        #                  - se tipo é operador, valor é o operador (ex: "+", "<=")
        #                  - se tipo é comando, valor = None
        # noAST.filhos : lista de noAST filhos na ordem lógica: (Aqui foi bem fé se vai dar certo na análise semântica, há de se ver)
        #                  - "declaracao" : [tipo, id]
        #                  - "operacao"   : [esq, dir] (binária/atribuição) ou [operando] (unária "-" e "!")
        #                  - "if"         : [condicao, churras] ou [condicao, churras, else]
        #                  - "while"      : [condicao, churras]
        #                  - "for"        : [id, limite_exp, churras]
        #                  - "entrada"    : [id]
        #                  - "saida"      : [item1, item2, ...]
        # noAST.linha  : número da linha no código-fonte
        noAST = self.parser.analisar_sintaxe(lista_tokens)

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



    

