import pytest
from analisador_lexico import analisar_lexico
from testes.utils import validar_token


@pytest.mark.parametrize("entrada", ["vaca123", "picanha", "_carne", "espeto_"])
def test_identificadores(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, "id")


@pytest.mark.parametrize("entrada", ["vaca", "frango", "porco", "rodizio", "grelhar", "ta_no_ponto?", "queimou", "ponto_certo", "queimado", "espetar", "servir", "servido"])
def test_reservadas(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, entrada)
