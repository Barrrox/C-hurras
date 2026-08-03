
class Gramatica:
        def __init__(self, caminho_arquivo: str):
            """Classe que:
                1. Lê o arquivo bruto da gramática
                2. Contém as regras de produção
                3. Pega terminais e não terminais
                4. Calcula First e Follow (guarda em atributos publicos para serem usados no construtor de tabelas)

            Args:
                caminho_arquivo (str): Caminho relativo para o arquivo da gramática
            """
            self.caminho = caminho_arquivo
            self.regras = {}       # Ex: { 1: ["lado esquerdo", ["lado direito", ...]] }
            self.terminais = set()
            self.nao_terminais = set()
            self.first = {}
            self.follow = {}

        def ler_arquivo(self) -> None:
            """
            O que faz: Abre txt bruto. Extrai regras. Popula terminais e não-terminais.
            """
            pass

        def calcular_first_follow(self) -> None:
            """
            O que faz: Roda algoritmo para conjuntos FIRST e FOLLOW e salva em self.first e self.follow
            """
            pass