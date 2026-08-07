import pytest
from automato import ItemLR
from gramatica import Gramatica

# Classe exclusiva de teste que herda a lógica de Gramatica,
# mas pula a abertura de arquivos para poder injetar as producoes mock
class GramaticaMock(Gramatica):
    def __init__(self, producoes_tupla):
        self.producoes = producoes_tupla
        self.terminais = set()
        self.nao_terminais = set()

@pytest.fixture
def gramatica_simples():
    producoes = (
        ('E', ('E', '+', 'T')),
        ('E', ('T',)),
        ('T', ('id',))
    )
    return GramaticaMock(producoes)

@pytest.fixture
def gramatica_simples2():
    producoes = (
        ("E", ("E", "+", "T"),),
        ("E", ("T",)),
        ("T", ("T", "*", "F")),
        ("T", ("F",)),
        ("F", ("(", "E", ")")),
        ("F", ("id",))
    )
    return GramaticaMock(producoes)