import pytest
from analisador_lexico import analisar_lexico


@pytest.mark.parametrize("entrada", ["123", "0", "9999"])
def test_tipo_inteiro(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    assert tokens[0].tipo == "int"
    assert tokens[0].texto == entrada
