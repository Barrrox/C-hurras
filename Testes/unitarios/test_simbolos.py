import pytest
from analisador_lexico import analisar_lexico
from testes.utils import validar_token


@pytest.mark.parametrize("entrada", ["+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "="])
def test_operadores(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, "op")


@pytest.mark.parametrize("entrada", [",", ";", "{", "}", "(", ")"])
def test_delimitadores(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, entrada)
