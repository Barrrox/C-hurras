import pytest
from automato import AutomatoLR0, ItemLR
from gramatica import Gramatica
from testes.unitarios.sintatico.conftest import GramaticaMock


# Auxiliar: monta o fechamento do estado 0 de uma gramatica
def _estado_0(automato: AutomatoLR0, gramatica: Gramatica) -> list:
    item_inicial = automato.get_item_inicial(gramatica)
    return automato.fechamento([item_inicial], gramatica.producoes)


def _simplificar(itens: list) -> list:
    # Extrai (esq, dir, ponto) de cada ItemLR para facilitar asserts
    return [(i.esq, tuple(i.dir), i.ponto) for i in itens]


def test_desvio_por_terminal_avanca_ponto(gramatica2: Gramatica):
    # Gramatica:
    # <E> -> <E> + <T> | <T>
    # <T> -> <T> * <F> | <F>
    # <F> -> ( <E> ) | id
    #
    # Estado 0 contem <F> -> . id
    # Desvio por 'id' deve gerar {<F> -> id .}

    automato = AutomatoLR0(gramatica2)
    estado_0 = _estado_0(automato, gramatica2)

    resultado = automato.desvio_estado(estado_0, "id", gramatica2.producoes)
    itens = _simplificar(resultado)

    # Unico item esperado apos desvio: <F> -> id . (item de reducao, ponto no fim)
    assert ("<F>", ("id",), 1) in itens


def test_desvio_por_terminal_nao_gera_fechamento_adicional(gramatica2: Gramatica):
    # Desvio por 'id' gera so <F> -> id .
    # Como ponto_dir de <F> -> id . eh None (fim), fechamento nao adiciona nada

    automato = AutomatoLR0(gramatica2)
    estado_0 = _estado_0(automato, gramatica2)

    resultado = automato.desvio_estado(estado_0, "id", gramatica2.producoes)
    itens = _simplificar(resultado)

    assert len(itens) == 1
    assert ("<F>", ("id",), 1) in itens


def test_desvio_por_nao_terminal_avanca_ponto(gramatica2: Gramatica):
    # Desvio por <E> do estado 0:
    # Estado 0 contem <E> -> . <E> + <T>
    # Apos desvio: <E> -> <E> . + <T>  (ponto na posicao 1)

    automato = AutomatoLR0(gramatica2)
    estado_0 = _estado_0(automato, gramatica2)

    resultado = automato.desvio_estado(estado_0, "<E>", gramatica2.producoes)
    itens = _simplificar(resultado)

    assert ("<E>", ("<E>", "+", "<T>"), 1) in itens


def test_desvio_por_nao_terminal_expande_com_fechamento(gramatica2: Gramatica):
    # Desvio por <T> do estado 0:
    # Estado 0 contem:
    #   <E> -> . <T>       => apos desvio: <E> -> <T> .    (reducao)
    #   <T> -> . <T> * <F> => apos desvio: <T> -> <T> . * <F>
    # Fechamento nao adiciona nada (ponto_dir e terminal ou None)

    automato = AutomatoLR0(gramatica2)
    estado_0 = _estado_0(automato, gramatica2)

    resultado = automato.desvio_estado(estado_0, "<T>", gramatica2.producoes)
    itens = _simplificar(resultado)

    assert ("<E>", ("<T>",), 1) in itens
    assert ("<T>", ("<T>", "*", "<F>"), 1) in itens


def test_desvio_por_parentese_expande_fechamento(gramatica2: Gramatica):
    # Desvio por '(' do estado 0:
    # Estado 0 contem <F> -> . ( <E> )
    # Apos desvio: <F> -> ( . <E> )
    # ponto_dir = <E> => fechamento adiciona todas as producoes de <E>, <T>, <F>

    automato = AutomatoLR0(gramatica2)
    estado_0 = _estado_0(automato, gramatica2)

    resultado = automato.desvio_estado(estado_0, "(", gramatica2.producoes)
    itens = _simplificar(resultado)

    # Item desviado direto
    assert ("<F>", ("(", "<E>", ")"), 1) in itens

    # Fechamento expande <E>
    assert ("<E>", ("<E>", "+", "<T>"), 0) in itens
    assert ("<E>", ("<T>",), 0) in itens

    # Fechamento expande <T>
    assert ("<T>", ("<T>", "*", "<F>"), 0) in itens
    assert ("<T>", ("<F>",), 0) in itens

    # Fechamento expande <F>
    assert ("<F>", ("(", "<E>", ")"), 0) in itens
    assert ("<F>", ("id",), 0) in itens


def test_desvio_por_simbolo_ausente_retorna_vazio(gramatica2: Gramatica):
    # Se nenhum item do conjunto I tem o simbolo X apos o ponto,
    # o desvio deve retornar lista vazia

    automato = AutomatoLR0(gramatica2)
    estado_0 = _estado_0(automato, gramatica2)

    # '$' nao aparece em nenhum item do estado 0
    resultado = automato.desvio_estado(estado_0, "$", gramatica2.producoes)

    assert resultado == []


def test_desvio_ignora_itens_sem_simbolo(gramatica1: Gramatica):
    # Gramatica:
    # <E> -> <E> + <T> | <T>
    # <T> -> id
    #
    # Estado 0 contem: <E>->.<E>+<T>, <E>->.<T>, <T>->.id
    # Desvio por 'id' so deve avancar <T> -> . id
    # <E>->.<E>+<T> e <E>->.<T> nao tem 'id' apos o ponto => ignorados

    automato = AutomatoLR0(gramatica1)
    estado_0 = _estado_0(automato, gramatica1)

    resultado = automato.desvio_estado(estado_0, "id", gramatica1.producoes)
    itens = _simplificar(resultado)

    assert ("<T>", ("id",), 1) in itens

    # Confirma que os outros itens nao escaparam
    assert ("<E>", ("<E>", "+", "<T>"), 0) not in itens
    assert ("<E>", ("<T>",), 0) not in itens


def test_desvio_sobre_item_de_reducao_retorna_vazio(gramatica1: Gramatica):
    # Um item de reducao (ponto no fim) nao pode ser desviado por nenhum simbolo.
    # Conjunto I com apenas um item de reducao deve sempre gerar desvio vazio.
    # <T> -> id . (ponto = 1 = len(dir))

    automato = AutomatoLR0(gramatica1)
    item_reducao = ItemLR("<T>", ("id",), 1)  # ponto no fim

    resultado = automato.desvio_estado([item_reducao], "id", gramatica1.producoes)

    assert resultado == []
