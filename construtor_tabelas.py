

class ConstrutorTabelas:

    def __init__(self, gramatica, automato):
        """Classe responsável pela construção das tabelas ACTION e GOTO a partir da gramática e do automato LR(0)

        Args:
                gramatica (_type_): Instância da classe Gramatica. Fornece conjuntos FOLLOW e terminais.
                automato (_type_): Instância da classe AutomatoLR0. Fornece estados e transições.

        Returns:
                Nada. Salva as tabelas em arquivos estáticos.
        """
        
        self.gramatica = gramatica
        self.automato = automato

        # Estruturas alvo (vão pro JSON e pro Parser)
        self.tabela_action = {}
        self.tabela_goto = {}
        self.regras = {} # Regras de produção da gramática

    def construir_tabelas(self) -> None:
        """Constrói as tabelas ACTION e GOTO
        """

        """
        O que faz:
        1. Varre estados do self.automato.
        2. Aplica lógica SLR(1) usando self.gramatica.follow_sets.
        3. Preenche self.action_table (Shift, Reduce, Accept).
        4. Preenche self.goto_table.
        5. Formata self.regras_parser (ID -> {lhs, tamanho}).

        O que retorna: Nada. Altera atributos de instância.
        """

        
        pass

    def exportar_json(self, caminho="tabelas_slr.json") -> None:
        """
        O que faz:
        - Salva self.action_table, self.goto_table e self.regras_parser em formato JSON.

        O que retorna: Nada. Gera artefato físico em disco.
        """
        pass
