import pytest
from analisador_lexico import analisar_lexico


@pytest.mark.parametrize("entrada", [
    "-", "+", "*", "/", "%",  # Aritméticos
    "&&", "||",               # Lógicos
    "==", "!=", "<=", ">=", "=", "<", ">" # Relacionais e Atribuição
])
def test_tipo_operador(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    assert tokens[0].tipo == "op"
    assert tokens[0].texto == entrada

@pytest.mark.parametrize("entrada", [",", ";", "{", "}"])
def test_tipo_delimitador(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    # O tipo do delimitador é o próprio caractere
    assert tokens[0].tipo == entrada 
    assert tokens[0].texto == entrada
