import pytest
import analisador_lexico
from testes.utils import validar_token


@pytest.mark.parametrize("entrada", ["'a'", "'1'", "' '", "'@'"])
def test_char(entrada):
    tokens = analisador_lexico.analisar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, "char")


@pytest.mark.parametrize("entrada", ['"123"', '" "', '"chu_rras"'])
def test_string(entrada):
    tokens = analisador_lexico.analisar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, "string")


def test_string_vazia():
    with pytest.raises(SystemExit):
        analisador_lexico.analisar_lexico('""')
