from gramatica import Gramatica


class ItemLR:
    def __init__(self, esquerda_producao: str, direita_producao: list[str], ponto: int = 0):
        self.esq = esquerda_producao
        self.dir = direita_producao
        self.ponto = ponto # Começa em 0

        # Deixar alocado o simbolo apos o ponto. Talvez nem precise guardar dir e ponto separados dai:
        self.ponto_dir = self.dir[self.ponto]

        # Como aloca:
            #  T → • T * F: ItemLR(esquerda, direita, 0)
            #  T → T * • F: ItemLR(T, [T,*,F], 2)

        # Operações:
            # Símbolo após o ponto: dir[ponto] -> da pra deixar alocado já que os itens são estáticos
            # É item de redução? ponto == len(direita)
            # Desvio (avançar o ponto): ItemLR(esquerda, direita, ponto + 1)

class Estado:

    def __init__(self, id : int,
                 fechamento : list['ItemLR']):
        self.id = id
        self.fechamento = fechamento


class AutomatoLR0:
    def __init__(self, gramatica: Gramatica):
        """ Recebe a gramatica já lida e processada """
        self.estados = []    # Lista contendo os conjuntos de Itens LR(0)
        self.transicoes = {} # Mapeia: (estado_origem, simbolo) -> estado_destino

        self.gerar_automato(gramatica) # Gera o automato

    def gerar_automato(self, gramatica) -> None:
        """
        O que faz:
        1. Inicia estado 0 com regra aumentada (ex: S' -> . S)
        2. Roda algoritmos 'Closure' (Fechamento) e 'Goto' em loop.
        3. Descobre matematicamente todos os estados e rotas possíveis.

        O que retorna: Nada. Preenche self.estados e self.transicoes.
        """
        pass

    def exportar_json(self, caminho="automato.json") -> None:
        """Lê os estados e transições e salva o automato em um JSON
        """