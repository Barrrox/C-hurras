import pytest
import itertools
import analisador_lexico
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
    (("+", "op"), ("123", "int")),     # +123
    ((";", ";"), ("vaca", "vaca")),    # ;vaca
    (("{", "{"), ("id", "id")),        # {id
    (("123", "int"), (";", ";")),      # 123;
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

def test_id_colado_com_numero():
    """vaca123 deve ser um único ID, não 'vaca' + '123'"""
    tokens = executar_lexico("vaca123")
    assert len(tokens) == 1
    validar_token(tokens[0], "vaca123", "id")
