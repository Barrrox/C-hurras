from Token import Token

TOKENS_IGNORADOS = {";", ",", "{", "}", "(", ")"}
PALAVRAS_COMANDO = {"rodizio", "grelhar", "ta_no_ponto?", "queimou", "espetar", "servir"}

CAUDAS = {"<or-tail>", "<and-tail>", "<comp-tail>", "<add-tail>", "<term-tail>"}
TIPOS_EXPRESSAO = {"<exp>", "<logical-or>", "<logical-and>", "<comparison>", "<additive>", "<term>", "<unary>", "<primary>", "<out>"}


class noAST:

    def __init__(self, 
                 tipo: str, 
                 valor: str | None = None,
                 filhos: list['noAST'] = None,
                 linha: int = -1):
        """Classe que guarda um nó da árvore

        Args:
            tipo (str): tipo do nó armazenado, Ex: Atribuição, Operação, Condicional, While, For...
            valor (str | None, optional): Se. Defaults to None.
            filhos (list[&#39;noAST&#39;], optional): Lista dos filhos do no atual, se vazio é uma folha. Defaults to None.
        """

        self.tipo = tipo
        self.valor = valor
        self.filhos = filhos if filhos is not None else []
        self.linha: int | None = linha

    def __repr__(self) -> str:
        if self.valor is not None and not self.filhos:
            return f"noAST({self.tipo}, {self.valor!r})"
        return f"noAST({self.tipo}, filhos={self.filhos})"
    
    def imprimir(self, nivel: int = 0) -> None:
        indent = "  " * nivel
        info_valor = f" ({self.valor})" if self.valor is not None else ""
        print(f"{indent}{self.tipo}{info_valor}")
        for filho in self.filhos:
            filho.imprimir(nivel + 1)

def token_para_no(token: Token | noAST) -> noAST:
    if isinstance(token, noAST):
        return token
    return noAST(tipo=token.categoria, valor=token.texto, linha=token.linha)

def criar_no(regra_semantica: list | None, simbolo_esq: str, elementos: list[Token | noAST | None]) -> noAST | None:
    # 1. Produção vazia (~)
    if not elementos:
        return None

    nome_no = regra_semantica[1] if (regra_semantica and len(regra_semantica) > 1) else simbolo_esq

    # 2. Filtrar None, pontuação e palavras-chave redundantes do comando
    # uteis guardará apenas tokens uteis para a AST/An Semantica,
    uteis: list[Token | noAST] = []
    linha_no = None
    for elemento in elementos:
        if elemento is None:
            continue
        if isinstance(elemento, Token):
            if linha_no is None:
                linha_no = elemento.linha
            if elemento.categoria in TOKENS_IGNORADOS or elemento.texto in PALAVRAS_COMANDO:
                continue
        elif isinstance(elemento, noAST) and linha_no is None:
            linha_no = elemento.linha
        uteis.append(elemento)

    if not uteis:
        return None

    # 3. Caudas binárias: ex. <add-tail> -> "+" <term> <add-tail>
    if simbolo_esq in CAUDAS:
        op_token = uteis[0]
        termo_dir = token_para_no(uteis[1])
        no_op = noAST(tipo="operacao", valor=op_token.texto, filhos=[termo_dir], linha=op_token.linha)
        if len(uteis) == 3 and isinstance(uteis[2], noAST):
            no_op.filhos.append(uteis[2])
        return no_op

    # 4. Níveis de expressão (ex: <additive> -> <term> <add-tail>)
    if simbolo_esq in TIPOS_EXPRESSAO:
        # Unário: "-" <unary> ou "!" <unary>
        if simbolo_esq == "<unary>" and len(uteis) == 2 and isinstance(uteis[0], Token):
            op_token = uteis[0]
            operando = token_para_no(uteis[1])
            return noAST(tipo="operacao", valor=op_token.texto, filhos=[operando], linha=op_token.linha)

        # Só 1 filho (sem cauda): sobe o filho direto sem criar nó intermediário
        if len(uteis) == 1:
            return token_para_no(uteis[0])

        # Operando esquerdo + cauda(s): encaixa operando esquerdo no operador da cauda
        esq = token_para_no(uteis[0])
        cauda = uteis[1]
        while isinstance(cauda, noAST) and cauda.tipo == "operacao":
            proxima_cauda = cauda.filhos.pop(1) if len(cauda.filhos) > 1 else None
            cauda.filhos.insert(0, esq)
            esq = cauda
            cauda = proxima_cauda
        return esq  

    # 4.1 Atribuição: id = <exp> ;
    if simbolo_esq == "<atribuicao>":
        return noAST(tipo=nome_no, valor="=", filhos=[token_para_no(uteis[0]), token_para_no(uteis[2])], linha=linha_no)

    # 5. Listas recursivas (<churras> e <saida_comp>): achatar comandos/itens no mesmo nível
    if simbolo_esq in {"<churras>", "<saida_comp>"}:
        filhos_lista: list[noAST] = []
        for item in uteis:
            no_item = token_para_no(item)
            if no_item.tipo == nome_no:
                filhos_lista.extend(no_item.filhos)
            else:
                filhos_lista.append(no_item)
        return noAST(tipo=nome_no, filhos=filhos_lista, linha=linha_no)

    # 6. Caso padrão (e achata <saida_comp> dentro de <saida>)
    filhos_finais: list[noAST] = []
    for item in uteis:
        no_item = token_para_no(item)
        if simbolo_esq == "<saida>" and no_item.tipo in {"<saida_comp>", "saida_comp"}:
            filhos_finais.extend(no_item.filhos)
        else:
            filhos_finais.append(no_item)

    return noAST(tipo=nome_no, filhos=filhos_finais, linha=linha_no)

