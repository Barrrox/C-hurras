import os
import json

class Gramatica:
        def __init__(self, arquivo_producoes = "regras_producao.json") -> None:
            """Classe que:
                1. Lê o arquivo bruto da gramática (ATENÇÃO: Produções A -> a | b já estão separadas em A -> a e A -> b)
                2. Contém as regras de produção
                3. Pega terminais e não terminais
                4. Calcula First e Follow (guarda em atributos publicos para serem usados no construtor de tabelas)

            Args:
                arquivo_producoes (str): Caminho relativo para o arquivo da gramática
            """

            # Pega o caminho absoluto da pasta atual (src/) e junta com o nome do arquivo
            caminho_base = os.path.dirname(os.path.abspath(__file__))
            caminho_completo = os.path.join(caminho_base, arquivo_producoes)

            with open(caminho_completo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                # JSON lê como listas. Transforma em tuplas:
                producoes = tuple(tuple([regra[0], (tuple(dir for dir in regra[1]))]) for regra in dados)

            self.producoes: tuple[tuple[str, tuple[str, ...]], ...] = producoes
            self.terminais: set[str] = set()
            self.nao_terminais: set[str] = set()

        def calcular_follow(self) -> dict[str, list[str]]:
            """Roda algoritmo para criar e retornar Follow. Vai precisar calcular o First antes.
            
            Returns:
                dict: Conjuntos Follow
            """

            # Calcular First

            # Calcular Follow

            # Ideia para a estrutura do Follow: Dicionario em que cada chave é uma produção de producoes e cada valor é uma lista com os não terminais, que são o Follow
            # 
            # follow = {producoes[i] : [a,b,c]}

            return follow