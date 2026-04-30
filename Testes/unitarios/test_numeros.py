import pytest
import analisador_lexico
from testes.utils import executar_lexico, validar_token


@pytest.mark.parametrize("entrada", ["123", "0", "9999"])
def test_tipo_inteiro(entrada):
    tokens = executar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, "int")
