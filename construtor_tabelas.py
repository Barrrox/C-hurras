

class ConstrutorTabelaSLR:

    def __init__(self):
        """Classe responsável pela construção da tabela SLR a partir da gramática e do automato LR(0)

        Args:
                gramatica (_type_): Instância da classe Gramatica. Fornece conjuntos FOLLOW e terminais.
                automato (_type_): Instância da classe AutomatoLR0. Fornece estados e transições.

        Returns:
                Nada. Salva as tabelas em arquivos estáticos.
        """

        # Estruturas alvo (vão pro JSON e pro Parser)
        self.tabelaSLR = {}
        self.regras = {} # Regras de produção da gramática

    def aumentar_gramatica(self, gramatica):

        gramatica_aumentada = None
        return gramatica_aumentada
        pass

    def construir_tabelaSLR(self, gramatica, automato) -> None:
        """Constrói a tabela SLR
        """

        """
        O que faz:
        1. Varre estados do self.automato.
        2. Aplica lógica SLR(1) usando self.gramatica.follow_sets.
        3. Preenche self.tabelaSLR (com Shift, Reduce, Accept, Erro).
        4. Formata self.regras (ID -> {lhs, tamanho}).

        O que retorna: Nada. Altera atributos de instância.
        """

        """
Entrada: Gramática aumentada G’
Saída: Funções sintáticas SLR ação e desvio para G’
Proc tabela(G’) {

1. Construir C={I0..In} //coleção de itens para G’

2. O estado i é construído a partir de Ii. As ações sintáticas para o estado i são determinadas como segue:
    a) Se [A → α•aβ] estiver em Ii e desvio(Ii, a)=Ij, então estabelecer ação[i,a] em “empilha j”. Aqui a é terminal. //R1
    b)Se [A → α•] estiver em Ii, então estabelecer ação[i,a] em “reduzir através de A→ α” para todo a em Follow(A). Aqui A é diferente de S’. //R2
    c)Se[S’ → S•] estiver em Ii, então estabelecer ação[i,$] igual a “aceitar”. //R3

3. As transições de desvio para o estado i são construídos pra todos os não-terminais A usando a regra: se desvio(Ii, A) = Ij, então desvio[i,A] = j //R4

4. Entradas não definidas: erro

}
        """

        # Passo 1
        gramatica = self.aumentar_gramatica(gramatica) 

        # Inicializar tabela SLR com N linhas (N estados do automato) e com T + A colunas (T terminais + A não terminais -> Seguindo regra 4 dos slides na construção da tabela)
        tabelaSLR = {}
        
        pass

    def exportar_json(self, caminho="tabela_slr.json") -> None:
        """
        O que faz:
        - Salva self.tabelaSLR e self.regras em formato JSON.

        O que retorna: Nada. Gera artefato físico em disco.
        """
        pass
