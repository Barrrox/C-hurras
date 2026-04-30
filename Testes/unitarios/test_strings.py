import pytest
import analisador_lexico
from testes.utils import executar_lexico, validar_token, verificar_erro_lexico


@pytest.mark.parametrize("entrada", ["'a'", "'1'", "' '", "'@'"])
def test_char(entrada):
    tokens = executar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, "char")


@pytest.mark.parametrize("entrada", ['"123"', '" "', '"chu_rras"'])
def test_string(entrada):
    tokens = executar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, "string")


def test_string_vazia():
    verificar_erro_lexico('""')
