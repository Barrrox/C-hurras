import pytest
from analisador_lexico import analisar_lexico

@pytest.mark.parametrize("entrada", ["'a'", "' '", "'1'"])
def test_tipo_char(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    assert tokens[0].tipo == "char"
    assert tokens[0].texto == entrada

@pytest.mark.parametrize("entrada", ['"churrasco"', '"a b c"'])
def test_tipo_string(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    assert tokens[0].tipo == "string" 
    assert tokens[0].texto == entrada
