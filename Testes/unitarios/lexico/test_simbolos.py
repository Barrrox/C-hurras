import pytest
import analisador_lexico
from testes.utils import executar_lexico, validar_token


@pytest.mark.parametrize("entrada", ["+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "="])
def test_operadores(entrada):
    tokens = executar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, entrada)


@pytest.mark.parametrize("entrada", [",", ";", "{", "}", "(", ")"])
def test_delimitadores(entrada):
    tokens = executar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, entrada)
