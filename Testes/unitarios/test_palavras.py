import pytest
from analisador_lexico import analisar_lexico

@pytest.mark.parametrize("entrada", ["minha_var", "_var2", "variavel_123"])
def test_tipo_identificador(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    assert tokens[0].tipo == "id"
    assert tokens[0].texto == entrada

@pytest.mark.parametrize("entrada", [
    "vaca", "frango", "porco", "rodizio", "grelhar", 
    "ta_no_ponto?", "queimou", "ponto_certo", "queimado", 
    "espetar", "servir", "servido"
])
def test_tipo_palavra_reservada(entrada):
    tokens = analisar_lexico(entrada)
    assert len(tokens) == 1
    # O tipo da palavra reservada é o próprio texto dela
    assert tokens[0].tipo == entrada 
    assert tokens[0].texto == entrada
