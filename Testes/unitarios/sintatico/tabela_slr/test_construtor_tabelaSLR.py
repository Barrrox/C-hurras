import pytest
from automato import AutomatoLR0
from construtor_tabelaSLR import ConstrutorTabelaSLR
from gramatica import Gramatica

def test_construir_tabelaSLR_gramatica5(gramatica5: Gramatica):
    automato = AutomatoLR0()
    automato.gerar_automato(gramatica5)

    tabelador = ConstrutorTabelaSLR()
    tabelador.construir_tabelaSLR(gramatica5, automato)

    tabela = tabelador.tabelaSLR

    def get_acao(estado, simbolo_texto):
        simbolo_id = gramatica5.simbolos[simbolo_texto]
        return tabela[estado][simbolo_id]

    assert get_acao(0, "(").tipo == 0 and get_acao(0, "(").valor == 4
    assert get_acao(0, "id").tipo == 0 and get_acao(0, "id").valor == 3
    assert get_acao(0, "<T>").tipo == 5 and get_acao(0, "<T>").valor == 1
    assert get_acao(0, "<F>").tipo == 5 and get_acao(0, "<F>").valor == 2
    assert get_acao(0, "*").tipo == 3
    
    assert get_acao(1, "*").tipo == 0 and get_acao(1, "*").valor == 5
    assert get_acao(1, "$").tipo == 2
    
    for term in ["*", "$", ")"]:
        assert get_acao(2, term).tipo == 1 and get_acao(2, term).valor == 1
        
    for term in ["*", "$", ")"]:
        assert get_acao(3, term).tipo == 1 and get_acao(3, term).valor == 3
        
    assert get_acao(4, "(").tipo == 0 and get_acao(4, "(").valor == 4
    assert get_acao(4, "id").tipo == 0 and get_acao(4, "id").valor == 3
    assert get_acao(4, "<T>").tipo == 5 and get_acao(4, "<T>").valor == 6
    assert get_acao(4, "<F>").tipo == 5 and get_acao(4, "<F>").valor == 2
    
    assert get_acao(5, "(").tipo == 0 and get_acao(5, "(").valor == 4
    assert get_acao(5, "id").tipo == 0 and get_acao(5, "id").valor == 3
    assert get_acao(5, "<F>").tipo == 5 and get_acao(5, "<F>").valor == 7
    
    assert get_acao(6, "*").tipo == 0 and get_acao(6, "*").valor == 5
    assert get_acao(6, ")").tipo == 0 and get_acao(6, ")").valor == 8
    
    for term in ["*", "$", ")"]:
        assert get_acao(7, term).tipo == 1 and get_acao(7, term).valor == 2
        
    for term in ["*", "$", ")"]:
        assert get_acao(8, term).tipo == 1 and get_acao(8, term).valor == 4

def test_construir_tabelaSLR_gramatica6(gramatica6: Gramatica):
    automato = AutomatoLR0()
    automato.gerar_automato(gramatica6)

    tabelador = ConstrutorTabelaSLR()
    tabelador.construir_tabelaSLR(gramatica6, automato)

    tabela = tabelador.tabelaSLR

    def get_acao(estado, simbolo_texto):
        simbolo_id = gramatica6.simbolos[simbolo_texto]
        return tabela[estado][simbolo_id]

    # Estado 0
    assert get_acao(0, "a").tipo == 0 and get_acao(0, "a").valor == 2
    assert get_acao(0, "[").tipo == 0 and get_acao(0, "[").valor == 3
    assert get_acao(0, "<S>").tipo == 5 and get_acao(0, "<S>").valor == 1
    
    # Estado 1
    assert get_acao(1, "$").tipo == 2
    
    # Estado 2 (R1: <S> -> a)
    # Follow(S) = {$, ], ;}
    for term in ["$", "]", ";"]:
        assert get_acao(2, term).tipo == 1 and get_acao(2, term).valor == 1
        
    # Estado 3
    assert get_acao(3, "a").tipo == 0 and get_acao(3, "a").valor == 2
    assert get_acao(3, "[").tipo == 0 and get_acao(3, "[").valor == 3
    assert get_acao(3, "<S>").tipo == 5 and get_acao(3, "<S>").valor == 5
    assert get_acao(3, "<L>").tipo == 5 and get_acao(3, "<L>").valor == 4
    
    # Estado 4
    assert get_acao(4, "]").tipo == 0 and get_acao(4, "]").valor == 6
    assert get_acao(4, ";").tipo == 0 and get_acao(4, ";").valor == 7
    
    # Estado 5 (R4: <L> -> <S>)
    # Follow(L) = {], ;}
    for term in ["]", ";"]:
        assert get_acao(5, term).tipo == 1 and get_acao(5, term).valor == 4
        
    # Estado 6 (R2: <S> -> [<L>])
    # Follow(S) = {$, ], ;}
    for term in ["$", "]", ";"]:
        assert get_acao(6, term).tipo == 1 and get_acao(6, term).valor == 2
        
    # Estado 7
    assert get_acao(7, "a").tipo == 0 and get_acao(7, "a").valor == 2
    assert get_acao(7, "[").tipo == 0 and get_acao(7, "[").valor == 3
    assert get_acao(7, "<S>").tipo == 5 and get_acao(7, "<S>").valor == 8
    
    # Estado 8 (R3: <L> -> <L>;<S>)
    # Follow(L) = {], ;}
    for term in ["]", ";"]:
        assert get_acao(8, term).tipo == 1 and get_acao(8, term).valor == 3
