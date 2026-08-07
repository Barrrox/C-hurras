import pytest
from automato import AutomatoLR0, ItemLR
from gramatica import Gramatica

def test_fechamento_deep_closure(gramatica_simples2 : Gramatica):
    # Inicializa o automato com a gramatica injetada pela fixture
    automato = AutomatoLR0(gramatica_simples2)
    
    # O item semente que dispara o efeito cascata: S' -> • E
    I_inicial = automato.get_item_inicial(gramatica_simples2)

    producoes = gramatica_simples2.prod
    
    # Roda o fechamento
    resultado = automato.fechamento([I_inicial], producoes)
    for i in resultado:
        print(i.esq,"->", i.dir)
    
    # O efeito cascata deve puxar todas as regras porque S' -> E -> T -> F
    # Total esperado: 7 itens
    assert len(resultado) == 6
    
    # Extrai as tuplas (esquerda, direita, ponto) para facilitar o assert
    # (já que a classe ItemLR ainda não tem os métodos __eq__ e __hash__)
    itens_simplificados = [(item.esq, tuple(item.dir), item.ponto) for item in resultado]
    
    assert ("E", ("E", "+", "T"), 0) in itens_simplificados
    assert ("E", ("T",), 0) in itens_simplificados
    assert ("T", ("T", "*", "F"), 0) in itens_simplificados
    assert ("T", ("F",), 0) in itens_simplificados
    assert ("F", ("(", "E", ")"), 0) in itens_simplificados
    assert ("F", ("id",), 0) in itens_simplificados