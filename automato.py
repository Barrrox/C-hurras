from gramatica import Gramatica

class Estado:
    id
    transições [
        ['<exp>', 3],
        ['<tail>', 8]
        ]
    fechamento [
        ['T', ['T', '', '~', 'F']], 
        ['T', ['T', '', '~', 'F']]
        ]




class AutomatoLR0:
    def __init__(self, gramatica: Gramatica):
        """ Recebe a gramatica já lida e processada """
        self.gramatica = gramatica
        self.estados = []    # Lista contendo os conjuntos de Itens LR(0)
        self.transicoes = {} # Mapeia: (estado_origem, simbolo) -> estado_destino

    def gerar_automato(self) -> None:
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