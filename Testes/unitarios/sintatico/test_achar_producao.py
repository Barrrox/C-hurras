import pytest
from automato import AutomatoLR0, ItemLR, Estado
from gramatica import Gramatica
from testes.unitarios.sintatico.conftest import GramaticaMock


# Auxiliar: popula self.estados do automato manualmente
def _montar_automato(gramatica: Gramatica) -> tuple:
    automato = AutomatoLR0(gramatica)

    item_inicial = automato.get_item_inicial(gramatica)
    fechamento_0 = automato.fechamento([item_inicial], gramatica.producoes)

    estado_0 = Estado(0, fechamento_0)
    automato.estados.append(estado_0)

    return automato, fechamento_0


def test_achar_producao_encontra_item_existente(gramatica2: Gramatica):
    # Item que realmente esta no fechamento do estado 0 deve retornar id 0

    automato, fechamento_0 = _montar_automato(gramatica2)

    # Pega um item que sabemos estar no fechamento
    item_presente = fechamento_0[0]

    resultado = automato.achar_producao_no_automato(item_presente)

    assert resultado == 0


def test_achar_producao_retorna_id_correto_com_multiplos_estados(gramatica2: Gramatica):
    # Com dois estados, o metodo deve retornar o id do estado correto

    automato = AutomatoLR0(gramatica2)

    item_a = ItemLR("<E>", ("<E>", "+", "<T>"), 0)
    item_b = ItemLR("<T>", ("<F>",), 0)

    estado_0 = Estado(0, [item_a])
    estado_1 = Estado(1, [item_b])

    automato.estados.append(estado_0)
    automato.estados.append(estado_1)

    # item_a esta no estado 0
    assert automato.achar_producao_no_automato(item_a) == 0

    # item_b esta no estado 1
    assert automato.achar_producao_no_automato(item_b) == 1


def test_achar_producao_retorna_menos1_quando_ausente(gramatica1: Gramatica):
    # Item que nao esta em nenhum estado deve retornar -1

    automato, _ = _montar_automato(gramatica1)

    # Cria um item novo (objeto diferente, nao registrado em nenhum estado)
    item_ausente = ItemLR("<E>", ("<E>", "+", "<T>"), 2)

    resultado = automato.achar_producao_no_automato(item_ausente)

    assert resultado == -1


def test_achar_producao_automato_vazio_retorna_menos1(gramatica1: Gramatica):
    # Com self.estados vazio, qualquer busca deve retornar -1

    automato = AutomatoLR0(gramatica1)
    # Nao adiciona nenhum estado

    item = ItemLR("<E>", ("<T>",), 0)

    assert automato.achar_producao_no_automato(item) == -1


def test_achar_producao_usa_identidade_de_objeto(gramatica1: Gramatica):
    # ItemLR nao implementa __eq__, entao a comparacao usa identidade (is).
    # Dois itens com os mesmos dados mas objetos diferentes nao sao encontrados.

    automato = AutomatoLR0(gramatica1)

    item_registrado = ItemLR("<T>", ("id",), 0)
    estado_0 = Estado(0, [item_registrado])
    automato.estados.append(estado_0)

    # Objeto diferente, mesmos dados
    item_copia = ItemLR("<T>", ("id",), 0)

    # item_copia nao e o mesmo objeto que item_registrado => retorna -1
    assert automato.achar_producao_no_automato(item_copia) == -1

    # O objeto original ainda e encontrado
    assert automato.achar_producao_no_automato(item_registrado) == 0


def test_achar_producao_retorna_primeiro_estado_encontrado(gramatica1: Gramatica):
    # Se o mesmo objeto estiver em dois estados (situacao anormal mas possivel),
    # o metodo retorna o id do primeiro estado encontrado na lista

    automato = AutomatoLR0(gramatica1)

    item_compartilhado = ItemLR("<E>", ("<T>",), 0)

    estado_0 = Estado(0, [item_compartilhado])
    estado_5 = Estado(5, [item_compartilhado])

    automato.estados.append(estado_0)
    automato.estados.append(estado_5)

    resultado = automato.achar_producao_no_automato(item_compartilhado)

    # Deve retornar o id do primeiro estado que contem o item
    assert resultado == 0


def test_achar_producao_varre_todos_os_items_do_fechamento(gramatica2: Gramatica):
    # O item buscado pode estar em qualquer posicao do fechamento, nao so na primeira

    automato = AutomatoLR0(gramatica2)

    item_meio = ItemLR("<T>", ("<T>", "*", "<F>"), 0)
    item_fim  = ItemLR("<F>", ("id",), 0)

    estado_0 = Estado(0, [
        ItemLR("<E>", ("<E>", "+", "<T>"), 0),
        item_meio,
        item_fim,
    ])

    automato.estados.append(estado_0)

    assert automato.achar_producao_no_automato(item_meio) == 0
    assert automato.achar_producao_no_automato(item_fim)  == 0
