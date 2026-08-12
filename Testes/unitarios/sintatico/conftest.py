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
def gramatica1():
    producoes = (
        ('<E>', ('<E>', '+', '<T>')),
        ('<E>', ('<T>',)),
        ('<T>', ('id',))
    )
    g = GramaticaMock(producoes)
    g.simbolos = g.get_simbolos()
    return g

@pytest.fixture
def gramatica2():
    producoes = (
        ("<E>", ("<E>", "+", "<T>"),),
        ("<E>", ("<T>",)),
        ("<T>", ("<T>", "*", "<F>")),
        ("<T>", ("<F>",)),
        ("<F>", ("(", "<E>", ")")),
        ("<F>", ("id",))
    )
    g = GramaticaMock(producoes)
    g.simbolos = g.get_simbolos()
    return g

@pytest.fixture
def gramatica3():
    # E → T | T a | b | ε | F
    # F → ε

    producoes = (
        ('<E>', ('<T>',)),
        ('<E>', ('<T>', 'a')),
        ('<E>', ('b',)),
        ('<E>', ("~",)),
        ('<E>', ('<F>',)),
        ('<F>', ("~",)),
    )
    g = GramaticaMock(producoes)
    g.simbolos = {"<E>", "<T>", "<F>", "a", "b", "~"} 
    g.nao_terminais = ['<E>', '<F>']
    g.terminais     = ['<T>', 'a', 'b']
    return g

@pytest.fixture
def gramatica4():
    # E  → T E2
    # E2 → v T E2 | ε
    # T  → F T2
    # T2 → a F T2
    # F  → n F | id

    

    producoes = (
        ('<E>',  ('<T>', '<E2>')),
        ('<E2>', ('v', '<T>', '<E2>')),
        ('<E2>', ("~",)),
        ('<T>',  ('<F>', '<T2>')),
        ('<T2>', ('a', '<F>', '<T2>')),
        ('<T2>', ("~",)),
        ('<F>',  ('n', '<F>')),
        ('<F>',  ('id',)),
    )
    g = GramaticaMock(producoes)
    g.simbolos = {"<E>", "<T>", "<F>", 'v', 'a', 'n', 'id'}
    g.nao_terminais = ['<E>', '<E2>', '<T>', '<T2>', '<F>']
    g.terminais     = ['v', 'a', 'n', 'id']
    return g

@pytest.fixture
def gramatica5():
    producoes = (
        ("<S'>", ("<T>",)),
        ("<T>", ("<F>",)),
        ("<T>", ("<T>", "*", "<F>")),
        ("<F>", ("id",)),
        ("<F>", ("(", "<T>", ")"))
    )
    g = GramaticaMock(producoes)
    g.simbolos = g.get_simbolos()
    g.follow = g.calcular_conjunto_follow()
    return g

@pytest.fixture
def gramatica6():
    producoes = (
        ("<S'>", ("<S>",)),
        ("<S>", ("a",)),
        ("<S>", ("[", "<L>", "]")),
        ("<L>", ("<L>", ";", "<S>")),
        ("<L>", ("<S>",))
    )
    g = GramaticaMock(producoes)
    g.simbolos = g.get_simbolos()
    g.follow = g.calcular_conjunto_follow()
    return g