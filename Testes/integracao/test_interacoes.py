import pytest
import itertools
from analisador_lexico import analisar_lexico


# Amostras de tokens para as combinações
# Cada tupla eh (texto, tipo_esperado)
TOKENS_TESTE = [
    ("vaca", "vaca"),
    ("minha_var", "id"),
    ("123", "int"),
    ("+", "op"),
    ("==", "op"),
    (";", ";"),
]

@pytest.mark.parametrize("tk1, tk2", itertools.product(TOKENS_TESTE, TOKENS_TESTE))
def test_interacao_com_espaco(tk1, tk2):
    """Garante que T1 + Espaco + T2 sempre gera 2 tokens."""
    texto1, tipo1 = tk1
    texto2, tipo2 = tk2
    
    codigo = f"{texto1} {texto2}"
    tokens = analisar_lexico(codigo)
    
    assert len(tokens) == 2
    assert tokens[0].tipo == tipo1
    assert tokens[1].tipo == tipo2

@pytest.mark.parametrize("tk1, tk2", [
    ( ("vaca", "vaca"), ("+", "op") ),       # Palavra + Op
    ( ("vaca", "vaca"), ("<=", "op") ),       # Palavra + Op2
    
    ( ("123", "int"),   ("+", "op") ),       # Num + Op

    ( ("+", "op"),      ("vaca", "vaca") ),  # Op + Palavra
    ( (">=", "op"),      ("vaca", "vaca") ),  # Op2 + Palavra
    ( (";", ";"),       ("vaca", "vaca") ),   # Delim + Palavra
    ( ("{", "{"),       ("vaca", "vaca") ),   # Delim2 + Palavra

    ( ("+", "op"),      ("123", "int") ),    # Op + Num

    ( ("-", "op"),     (";", ";") ),        # Op + Delim
    ( ("==", "op"),     (";", ";") ),        # Op2 + Delim
    ( ("<=", "op"),     (";", ";") ),        # Op2 + Delim
])
def test_interacao_sem_espaco_separaveis(tk1, tk2):
    """Casos onde o lexer DEVE conseguir separar mesmo sem espaço."""
    texto1, tipo1 = tk1
    texto2, tipo2 = tk2
    
    codigo = f"{texto1}{texto2}"
    tokens = analisar_lexico(codigo)
    
    assert len(tokens) == 2
    assert tokens[0].tipo == tipo1
    assert tokens[1].tipo == tipo2

def test_interacao_maximal_munch_id_num():
    """Teste de 'Gulodice': vaca + 123 deve virar um único ID 'vaca123'."""
    tokens = analisar_lexico("vaca123")
    assert len(tokens) == 1
    assert tokens[0].tipo == "id"
    assert tokens[0].texto == "vaca123"
