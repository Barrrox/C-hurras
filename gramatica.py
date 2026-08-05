producoes : list[list[str, list[str]]] = (
    # 0: <chs> → <churras>
    ('<chs>', ('<churras>')),

    # 1: <churras> → <if> <churras>
    ('<churras>', ('<if>', '<churras>')),
    # 2: <churras> → <churras>
    ('<churras>', ('<churras>')),
    # 3: <churras> → <for> <churras>
    ('<churras>', ('<for>', '<churras>')),
    # 4: <churras> → <declaracao> <churras>
    ('<churras>', ('<declaracao>', '<churras>')),
    # 5: <churras> → <entrada> <churras>
    ('<churras>', ('<entrada>', '<churras>')),
    # 6: <churras> → <saida> <churras>
    ('<churras>', ('<saida>', '<churras>')),
    # 7: <churras> → <atribuicao> <churras>
    ('<churras>', ('<atribuicao>', '<churras>')),
    # 8: <churras> → ε
    ('<churras>', ()),

    # 9: <declaracao> → vaca id ;
    ('<declaracao>', ('vaca', 'id', ';')),
    # 10: <declaracao> → frango id ;
    ('<declaracao>', ('frango', 'id', ';')),
    # 11: <declaracao> → porco id ;
    ('<declaracao>', ('porco', 'id', ';')),

    # 12: <while> → rodizio <exp> { <churras> }
    ('<while>', ('rodizio', '<exp>', '{', '<churras>', '}')),

    # 13: <for> → grelhar id <exp> { <churras> }
    ('<for>', ('grelhar', 'id', '<exp>', '{', '<churras>', '}')),

    # 14: <if> → ta_no_ponto? <exp> { <churras> } <if_comp>
    ('<if>', ('ta_no_ponto?', '<exp>', '{', '<churras>', '}', '<if_comp>')),

    # 15: <if_comp> → queimou { <churras> }
    ('<if_comp>', ('queimou', '{', '<churras>', '}')),
    # 16: <if_comp> → ε
    ('<if_comp>', ()),

    # 17: <entrada> → espetar id ;
    ('<entrada>', ('espetar', 'id', ';')),

    # 18: <saida> → servir <out> <saida_comp>
    ('<saida>', ('servir', '<out>', '<saida_comp>')),

    # 19: <saida_comp> → , <out> <saida_comp>
    ('<saida_comp>', (',', '<out>', '<saida_comp>')),
    # 20: <saida_comp> → ;
    ('<saida_comp>', (';')),

    # 21: <out> → char
    ('<out>', ('char')),
    # 22: <out> → string
    ('<out>', ('string')),
    # 23: <out> → id
    ('<out>', ('id')),
    # 24: <out> → servido
    ('<out>', ('servido')),
    # 25: <out> → <exp>
    ('<out>', ('<exp>')),

    # 26: <atribuicao> → id = <exp> ;
    ('<atribuicao>', ('id', '=', '<exp>', ';')),

    # Expressões
    # 27: <exp> → <logical-or>
    ('<exp>', ('<logical-or>')),

    # 28: <logical-or> → <logical-and> <or-tail>
    ('<logical-or>', ('<logical-and>', '<or-tail>')),

    # 29: <or-tail> → || <logical-and> <or-tail>
    ('<or-tail>', ('||', '<logical-and>', '<or-tail>')),
    # 30: <or-tail> → ε
    ('<or-tail>', ()),

    # 31: <logical-and> → <comparison> <and-tail>
    ('<logical-and>', ('<comparison>', '<and-tail>')),

    # 32: <and-tail> → && <comparison> <and-tail>
    ('<and-tail>', ('&&', '<comparison>', '<and-tail>')),
    # 33: <and-tail> → ε
    ('<and-tail>', ()),

    # 34: <comparison> → <additive> <comp-tail>
    ('<comparison>', ('<additive>', '<comp-tail>')),

    # 35: <comp-tail> → == <additive>
    ('<comp-tail>', ('==', '<additive>')),
    # 36: <comp-tail> → != <additive>
    ('<comp-tail>', ('!=', '<additive>')),
    # 37: <comp-tail> → < <additive>
    ('<comp-tail>', ('<', '<additive>')),
    # 38: <comp-tail> → > <additive>
    ('<comp-tail>', ('>', '<additive>')),
    # 39: <comp-tail> → <= <additive>
    ('<comp-tail>', ('<=', '<additive>')),
    # 40: <comp-tail> → >= <additive>
    ('<comp-tail>', ('>=', '<additive>')),
    # 41: <comp-tail> → ε
    ('<comp-tail>', ()),

    # 42: <additive> → <term> <add-tail>
    ('<additive>', ('<term>', '<add-tail>')),

    # 43: <add-tail> → + <term> <add-tail>
    ('<add-tail>', ('+', '<term>', '<add-tail>')),
    # 44: <add-tail> → - <term> <add-tail>
    ('<add-tail>', ('-', '<term>', '<add-tail>')),
    # 45: <add-tail> → ε
    ('<add-tail>', ()),

    # 46: <term> → <factor> <term-tail>
    ('<term>', ('<factor>', '<term-tail>')),

    # 47: <term-tail> → * <factor> <term-tail>
    ('<term-tail>', ('*', '<factor>', '<term-tail>')),
    # 48: <term-tail> → / <factor> <term-tail>
    ('<term-tail>', ('/', '<factor>', '<term-tail>')),
    # 49: <term-tail> → % <factor> <term-tail>
    ('<term-tail>', ('%', '<factor>', '<term-tail>')),
    # 50: <term-tail> → ε
    ('<term-tail>', ()),

    # 51: <factor> → <unary> <factor-tail>
    ('<factor>', ('<unary>', '<factor-tail>')),

    # 52: <factor-tail> → ** <unary> <factor-tail>
    ('<factor-tail>', ('**', '<unary>', '<factor-tail>')),
    # 53: <factor-tail> → ε
    ('<factor-tail>', ()),

    # 54: <unary> → - <unary>
    ('<unary>', ('-', '<unary>')),
    # 55: <unary> → ! <unary>
    ('<unary>', ('!', '<unary>')),
    # 56: <unary> → <primary>
    ('<unary>', ('<primary>')),

    # 57: <primary> → id
    ('<primary>', ('id')),
    # 58: <primary> → int
    ('<primary>', ('int')),
    # 59: <primary> → ( <exp> )
    ('<primary>', ('(', '<exp>', ')')),
)

class Gramatica:
        def __init__(self, producoes: list[list[str, list[str]]] = producoes):
            """Classe que:
                1. Lê o arquivo bruto da gramática (ATENÇÃO: Produções A -> a | b já estão separadas em A -> a e A -> b)
                2. Contém as regras de produção
                3. Pega terminais e não terminais
                4. Calcula First e Follow (guarda em atributos publicos para serem usados no construtor de tabelas)

            Args:
                caminho_arquivo (str): Caminho relativo para o arquivo da gramática
            """
            self.producoes = producoes
            self.regras = {}
            self.terminais = set()
            self.nao_terminais = set()
            self.first = {}
            self.follow = {}

        def calcular_first_follow(self) -> tuple[dict, dict]:
            """Roda algoritmo para criar e retornar conjuntos First e Follow.
            

            Returns:
                tuple[list[str], list[str]]: Conjuntos First e Follow
            """

            first = {producoes[i] : list[str]}
            follow = {producoes[i] : [a,b,c]}

            return first, follow