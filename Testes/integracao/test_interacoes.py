import pytest
import itertools
from testes.utils import executar_lexico, validar_token

# Amostras de tokens para as combinações
TOKENS_TESTE = [
    ("123", "int"),
    ("vaca", "vaca"),
    ("id_teste", "id"),
    ("+", "op"),
    (";", ";")
]

@pytest.mark.parametrize("tk1, tk2", itertools.product(TOKENS_TESTE, TOKENS_TESTE))
def test_interacao_com_espaco(tk1, tk2):
    """Garante que T1 + Espaco + T2 sempre gera 2 tokens."""
    txt1, tipo1 = tk1
    txt2, tipo2 = tk2
    
    codigo = f"{txt1} {txt2}"
    tokens = executar_lexico(codigo)
    
    assert len(tokens) == 2
    validar_token(tokens[0], txt1, tipo1)
    validar_token(tokens[1], txt2, tipo2)

@pytest.mark.parametrize("tk1, tk2", [
    (("+", "op"), ("123", "int")),      # Operator + Number (+123)
    (("123", "int"), ("+", "op")),      # Number + Operator (123+)
    (("vaca", "vaca"), (";", ";")),     # ID + Semicolon (vaca;)
    ((";", ";"), ("vaca", "vaca")),     # Semicolon + ID (;vaca)
    (("+", "op"), ("vaca", "vaca")),    # Operator + ID (+vaca)
    (("vaca", "vaca"), ("+", "op")),    # ID + Operator (vaca+)
    (("{", "{"), ("123", "int")),       # Delimiter + Number ({123)
    (("123", "int"), ("}", "}")),       # Number + Delimiter (123})
    (("id_teste", "id"), (";", ";")),   # ID + Semicolon (id_teste;)
    ((";", ";"), ("id_teste", "id")),   # Semicolon + ID (;id_teste)
    (("(", "("), ("123", "int")),       # Delimiter + Number ((123)
    (("123", "int"), (")", ")")),       # Number + Delimiter (123))
])
def test_interacao_sem_espaco(tk1, tk2):
    """Testa tokens colados que devem ser distinguidos pelo lexer."""
    txt1, tipo1 = tk1
    txt2, tipo2 = tk2
    
    codigo = f"{txt1}{txt2}"
    tokens = executar_lexico(codigo)
    
    assert len(tokens) == 2
    validar_token(tokens[0], txt1, tipo1)
    validar_token(tokens[1], txt2, tipo2)

def test_tres_tokens_colados():
    """Garante que 123+vaca gera 3 tokens."""
    codigo = "123+vaca"
    tokens = executar_lexico(codigo)
    
    assert len(tokens) == 3
    validar_token(tokens[0], "123", "int")
    validar_token(tokens[1], "+", "op")
    validar_token(tokens[2], "vaca", "vaca")

def test_id_ponto_virgula_numero():
    """vaca;123 gera 3 tokens."""
    codigo = "vaca;123"
    tokens = executar_lexico(codigo)
    
    assert len(tokens) == 3
    validar_token(tokens[0], "vaca", "vaca")
    validar_token(tokens[1], ";", ";")
    validar_token(tokens[2], "123", "int")

def test_delimitadores_aninhados():
    """Garante que (()) gera 4 tokens de parênteses."""
    codigo = "(())"
    tokens = executar_lexico(codigo)
    
    assert len(tokens) == 4
    validar_token(tokens[0], "(", "(")
    validar_token(tokens[1], "(", "(")
    validar_token(tokens[2], ")", ")")
    validar_token(tokens[3], ")", ")")

def test_id_colado_com_numero():
    """vaca123 deve ser um único ID, não 'vaca' + '123'"""
    tokens = executar_lexico("vaca123")
    assert len(tokens) == 1
    validar_token(tokens[0], "vaca123", "id")
