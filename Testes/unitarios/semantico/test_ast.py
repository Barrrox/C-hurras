import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from Token import Token
from arvore_ast import noAST, token_para_no, criar_no
from analisador_lexico import Lexer
from analisador_sintatico import ParserSLR

# Instância compartilhada do ParserSLR para não reconstruir o autômato LR(0) a cada teste
_PARSER = ParserSLR()
_TABELA_SLR = _PARSER.criar_tabelaSLR()


def gerar_ast(codigo: str) -> noAST:
    lexer = Lexer()
    tokens = lexer.analisar_lexico(codigo)
    aceitou = _PARSER.analisar_sintaxeAUX(tokens, _TABELA_SLR)
    assert aceitou is True, f"Falha sintática inesperada ao gerar AST para: {codigo}"
    assert _PARSER.AST is not None
    return _PARSER.AST


# =====================================================================
# GRUPO 1: Testes unitários isolados de noAST, token_para_no e criar_no
# =====================================================================

def test_token_para_no():
    tk = Token("10", "int", 3)
    no = token_para_no(tk)
    assert isinstance(no, noAST)
    assert no.tipo == "int"
    assert no.valor == "10"
    assert no.linha == 3
    assert no.filhos == []
    # Se já for noAST, deve retornar o próprio objeto
    assert token_para_no(no) is no


def test_criar_no_producao_vazia():
    assert criar_no(["criar_no", "vazio"], "<churras>", []) is None


def test_criar_no_ignora_pontuacao_e_palavras_comando():
    elementos = [
        Token("espetar", "espetar", 1),
        Token("x", "id", 1),
        Token(";", ";", 1),
    ]
    no = criar_no(["criar_no", "entrada"], "<entrada>", elementos)
    assert no is not None
    assert no.tipo == "entrada"
    assert len(no.filhos) == 1
    assert no.filhos[0].tipo == "id"
    assert no.filhos[0].valor == "x"


# =====================================================================
# GRUPO 2: Comandos simples via Parser (Declaração, I/O, Atribuição)
# =====================================================================

@pytest.mark.parametrize("tipo_churras, nome_var", [
    ("vaca", "a"),
    ("frango", "c"),
    ("porco", "flag"),
])
def test_ast_declaracao(tipo_churras, nome_var):
    ast = gerar_ast(f"{tipo_churras} {nome_var};")
    assert ast.tipo == "churras"
    assert len(ast.filhos) == 1

    decl = ast.filhos[0]
    assert decl.tipo == "declaracao"
    assert len(decl.filhos) == 2
    assert decl.filhos[0].tipo == "tipo"
    assert decl.filhos[0].valor == tipo_churras
    assert decl.filhos[1].tipo == "id"
    assert decl.filhos[1].valor == nome_var


def test_ast_entrada():
    ast = gerar_ast("espetar picanha;")
    cmd = ast.filhos[0]
    assert cmd.tipo == "entrada"
    assert len(cmd.filhos) == 1
    assert cmd.filhos[0].tipo == "id"
    assert cmd.filhos[0].valor == "picanha"


def test_ast_saida_multiplos_itens_achatados():
    ast = gerar_ast('servir x, "no ponto", servido;')
    cmd = ast.filhos[0]
    assert cmd.tipo == "saida"
    assert len(cmd.filhos) == 3
    assert (cmd.filhos[0].tipo, cmd.filhos[0].valor) == ("id", "x")
    assert (cmd.filhos[1].tipo, cmd.filhos[1].valor) == ("string", '"no ponto"')
    assert (cmd.filhos[2].tipo, cmd.filhos[2].valor) == ("servido", "servido")


@pytest.mark.parametrize("codigo, tipo_esperado, valor_esperado", [
    ("x = 42;", "int", "42"),
    ("c = 'z';", "char", "'z'"),
    ("p = ponto_certo;", "ponto_certo", "ponto_certo"),
    ("p = queimado;", "queimado", "queimado"),
])
def test_ast_atribuicao_simples(codigo, tipo_esperado, valor_esperado):
    ast = gerar_ast(codigo)
    atrib = ast.filhos[0]
    assert atrib.tipo == "operacao"
    assert atrib.valor == "="
    assert len(atrib.filhos) == 2
    assert atrib.filhos[0].tipo == "id"
    assert atrib.filhos[1].tipo == tipo_esperado
    assert atrib.filhos[1].valor == valor_esperado


# =====================================================================
# GRUPO 3: Expressões e Operações (Unárias, Binárias, Precedência)
# =====================================================================

@pytest.mark.parametrize("codigo, op_unario, tipo_alvo, valor_alvo", [
    ("x = -5;", "-", "int", "5"),
    ("p = !queimado;", "!", "queimado", "queimado"),
])
def test_ast_operacao_unaria(codigo, op_unario, tipo_alvo, valor_alvo):
    ast = gerar_ast(codigo)
    atrib = ast.filhos[0]
    unario = atrib.filhos[1]
    assert unario.tipo == "operacao"
    assert unario.valor == op_unario
    assert len(unario.filhos) == 1
    assert unario.filhos[0].tipo == tipo_alvo
    assert unario.filhos[0].valor == valor_alvo


@pytest.mark.parametrize("op", ["+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "&&", "||"])
def test_ast_operacoes_binarias(op):
    ast = gerar_ast(f"r = a {op} b;")
    atrib = ast.filhos[0]
    binaria = atrib.filhos[1]
    assert binaria.tipo == "operacao"
    assert binaria.valor == op
    assert len(binaria.filhos) == 2
    assert (binaria.filhos[0].tipo, binaria.filhos[0].valor) == ("id", "a")
    assert (binaria.filhos[1].tipo, binaria.filhos[1].valor) == ("id", "b")


def test_ast_precedencia_multiplicacao_sobre_soma():
    # a = 1 + 2 * 3 -> +(1, *(2, 3))
    ast = gerar_ast("a = 1 + 2 * 3;")
    soma = ast.filhos[0].filhos[1]
    assert (soma.tipo, soma.valor) == ("operacao", "+")
    assert (soma.filhos[0].tipo, soma.filhos[0].valor) == ("int", "1")

    mult = soma.filhos[1]
    assert (mult.tipo, mult.valor) == ("operacao", "*")
    assert (mult.filhos[0].valor, mult.filhos[1].valor) == ("2", "3")


def test_ast_parenteses_alteram_precedencia_e_somem():
    # a = (1 + 2) * 3 -> *(+(1, 2), 3)
    ast = gerar_ast("a = (1 + 2) * 3;")
    mult = ast.filhos[0].filhos[1]
    assert (mult.tipo, mult.valor) == ("operacao", "*")
    assert (mult.filhos[1].tipo, mult.filhos[1].valor) == ("int", "3")

    soma = mult.filhos[0]
    assert (soma.tipo, soma.valor) == ("operacao", "+")
    assert (soma.filhos[0].valor, soma.filhos[1].valor) == ("1", "2")


def test_ast_associatividade_esquerda_cauda():
    # a = 10 - 3 - 2 -> -(-(10, 3), 2)
    ast = gerar_ast("a = 10 - 3 - 2;")
    sub_externa = ast.filhos[0].filhos[1]
    assert (sub_externa.tipo, sub_externa.valor) == ("operacao", "-")
    assert sub_externa.filhos[1].valor == "2"

    sub_interna = sub_externa.filhos[0]
    assert (sub_interna.tipo, sub_interna.valor) == ("operacao", "-")
    assert (sub_interna.filhos[0].valor, sub_interna.filhos[1].valor) == ("10", "3")


# =====================================================================
# GRUPO 4: Estruturas de Controle e Achatamento de Blocos
# =====================================================================

def test_ast_achatamento_sequencia_comandos():
    ast = gerar_ast("vaca a; a = 1; servir a;")
    assert ast.tipo == "churras"
    assert len(ast.filhos) == 3
    assert [f.tipo for f in ast.filhos] == ["declaracao", "operacao", "saida"]


def test_ast_if_sem_else():
    ast = gerar_ast("ta_no_ponto? a > 0 { servir a; }")
    no_if = ast.filhos[0]
    assert no_if.tipo == "if"
    assert len(no_if.filhos) == 2
    assert (no_if.filhos[0].tipo, no_if.filhos[0].valor) == ("operacao", ">")
    assert no_if.filhos[1].tipo == "churras"


def test_ast_if_com_else():
    ast = gerar_ast("ta_no_ponto? a > 0 { servir a; } queimou { servir 0; }")
    no_if = ast.filhos[0]
    assert no_if.tipo == "if"
    assert len(no_if.filhos) == 3
    assert no_if.filhos[2].tipo == "else"
    assert no_if.filhos[2].filhos[0].tipo == "churras"


def test_ast_while():
    ast = gerar_ast("rodizio a < 10 { a = a + 1; }")
    no_while = ast.filhos[0]
    assert no_while.tipo == "while"
    assert len(no_while.filhos) == 2
    assert (no_while.filhos[0].tipo, no_while.filhos[0].valor) == ("operacao", "<")
    assert no_while.filhos[1].tipo == "churras"


def test_ast_for():
    ast = gerar_ast("grelhar i 10 { servir i; }")
    no_for = ast.filhos[0]
    assert no_for.tipo == "for"
    assert len(no_for.filhos) == 3
    assert (no_for.filhos[0].tipo, no_for.filhos[0].valor) == ("id", "i")
    assert (no_for.filhos[1].tipo, no_for.filhos[1].valor) == ("int", "10")
    assert no_for.filhos[2].tipo == "churras"
