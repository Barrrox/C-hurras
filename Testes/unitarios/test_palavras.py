import pytest
import analisador_lexico
from testes.utils import executar_lexico, validar_token


@pytest.mark.parametrize("entrada", ["vaca123", "picanha", "_carne", "espeto_"])
def test_identificadores(entrada):
    tokens = executar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, "id")

@pytest.mark.parametrize("entrada", ["rodizio", "grelhar", "ta_no_ponto?", "queimou", "ponto_certo", "queimado", "espetar", "servir", "servido"])
def test_reservadas(entrada):
    tokens = executar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, entrada)

@pytest.mark.parametrize("entrada", ["vaca", "frango", "porco"])
def test_tipos(entrada):
    tokens = executar_lexico(entrada)
    assert len(tokens) == 1
    validar_token(tokens[0], entrada, "tipo")