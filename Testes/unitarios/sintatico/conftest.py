import pytest
from automato import ItemLR # Ajuste o import conforme onde a classe estiver
from gramatica import Gramatica

@pytest.fixture #  = fixed + feature
def gramatica_simples():
    """Retorna uma gramática mínima apenas com E -> E + T | T, etc."""
    producoes = (
        ('E', ('E', '+', 'T')),
        ('E', ('T',)),
        ('T', ('id',))
    )
    
    return Gramatica(prod=producoes)

@pytest.fixture
def gramatica_expressao():
    """
    Gramática robusta para testes sintáticos:
    E  -> E + T | T
    T  -> T * F | F
    F  -> ( E ) | id
    """
    producoes = (
        ("E", ("E", "+", "T"),),
        ("E", ("T",)),
        # ("E", ("{",)),
        ("T", ("T", "*", "F")),
        ("T", ("F",)),
        ("F", ("(", "E", ")")),
        ("F", ("id",))
    )
    return Gramatica(prod=producoes)
