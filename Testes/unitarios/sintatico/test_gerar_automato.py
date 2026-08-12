import pytest
from automato import AutomatoLR0, ItemLR
from gramatica import Gramatica
from testes.unitarios.sintatico.conftest import GramaticaMock


def test_gerar_automato_gramatica1_numero_de_estados(gramatica1: Gramatica):
    # Gramatica:
    # <E> -> <E> + <T> | <T>
    # <T> -> id
    #
    # Automato LR(0) esperado para essa gramatica:
    # Estado 0: fechamento({<E> -> . <E> + <T>}) -> expande tudo
    # Derivacao gera 6 estados no total

    automato = AutomatoLR0(gramatica1)
    automato.gerar_automato(gramatica1)

    assert len(automato.estados) > 0


def test_gerar_automato_estado_inicial_existe(gramatica2: Gramatica):
    # O automato deve ter pelo menos 1 estado (o estado inicial)
    # e o estado 0 deve ser criado a partir do item inicial da gramatica

    automato = AutomatoLR0(gramatica2)
    automato.gerar_automato(gramatica2)

    # Estado 0 deve existir
    ids = [estado.id for estado in automato.estados]
    assert 0 in ids


def test_gerar_automato_gramatica2_numero_de_estados(gramatica2: Gramatica):
    # Gramatica classica de expressoes aritmeticas:
    # <E> -> <E> + <T> | <T>
    # <T> -> <T> * <F> | <F>
    # <F> -> ( <E> ) | id
    #
    # O automato LR(0) classico para essa gramatica gera 12 estados

    automato = AutomatoLR0(gramatica2)
    automato.gerar_automato(gramatica2)

    assert len(automato.estados) == 12


def test_gerar_automato_gramatica2_numero_de_transicoes(gramatica2: Gramatica):
    # Gramatica classica: 12 estados geram um numero fixo de transicoes.
    # O automato correto para essa gramatica tem 20 transicoes (leitura dos simbolos).

    automato = AutomatoLR0(gramatica2)
    automato.gerar_automato(gramatica2)

    assert len(automato.transicoes) > 0


def test_gerar_automato_transicoes_sao_dict(gramatica1: Gramatica):
    # self.transicoes deve ser um dict mapeando (estado_origem, simbolo) -> estado_destino

    automato = AutomatoLR0(gramatica1)
    automato.gerar_automato(gramatica1)

    assert isinstance(automato.transicoes, dict)

    for chave in automato.transicoes:
        # Chave deve ser uma tupla (int, str)
        assert isinstance(chave, tuple)
        assert len(chave) == 2
        origem, simbolo = chave
        assert isinstance(origem, int)
        assert isinstance(simbolo, str)


def test_gerar_automato_estado_inicial_tem_item_inicial(gramatica2: Gramatica):
    # O estado 0 deve conter o item inicial da gramatica em seu fechamento:
    # <E> -> . <E> + <T>  (ponto na posicao 0)

    automato = AutomatoLR0(gramatica2)
    automato.gerar_automato(gramatica2)

    estado_0 = next((e for e in automato.estados if e.id == 0), None)
    assert estado_0 is not None

    itens = [(i.esq, i.dir, i.ponto) for i in estado_0.fechamento]
    assert ("<E>", ("<E>", "+", "<T>"), 0) in itens


def test_gerar_automato_ids_sao_unicos(gramatica2: Gramatica):
    # Cada estado deve ter um id unico

    automato = AutomatoLR0(gramatica2)
    automato.gerar_automato(gramatica2)

    ids = [estado.id for estado in automato.estados]
    assert len(ids) == len(set(ids)), "IDs de estados nao sao unicos"


def test_gerar_automato_nenhum_estado_com_fechamento_vazio(gramatica2: Gramatica):
    # Nenhum estado do automato pode ter fechamento vazio

    automato = AutomatoLR0(gramatica2)
    automato.gerar_automato(gramatica2)

    for estado in automato.estados:
        assert len(estado.fechamento) > 0, f"Estado {estado.id} tem fechamento vazio"


def test_gerar_automato_gramatica5(gramatica5: Gramatica):
    automato = AutomatoLR0(gramatica5)
    automato.gerar_automato(gramatica5)

    def itens_estado(id):
            for e in automato.estados:
                if e.id == id:
                    estado = set((i.esq, i.dir, i.ponto) for i in e.fechamento)
                    return estado 
            return set()
    # print("\n--- DEBUG AUTOMATO ---")
    # for estado in automato.estados:
    #     print(f"\nEstado I{estado.id}")
    #     for item in estado.fechamento:
    #         item.imprimir()
    
    assert len(automato.estados) == 9
    
    assert itens_estado(0) == {
        ("<S'>", ("<T>",), 0), ("<T>", ("<F>",), 0),
        ("<T>", ("<T>", "*", "<F>"), 0), ("<F>", ("id",), 0),
        ("<F>", ("(", "<T>", ")"), 0)
    }
    
    assert itens_estado(1) == {
        ("<S'>", ("<T>",), 1), ("<T>", ("<T>", "*", "<F>"), 1)
    }
    
    assert itens_estado(2) == {
        ("<T>", ("<F>",), 1)
    }
    
    assert itens_estado(3) == {
        ("<F>", ("id",), 1)
    }
    
    assert itens_estado(4) == {
        ("<F>", ("(", "<T>", ")"), 1), ("<T>", ("<F>",), 0),
        ("<T>", ("<T>", "*", "<F>"), 0), ("<F>", ("id",), 0),
        ("<F>", ("(", "<T>", ")"), 0)
    }
    
    assert itens_estado(5) == {
        ("<T>", ("<T>", "*", "<F>"), 2), ("<F>", ("id",), 0),
        ("<F>", ("(", "<T>", ")"), 0)
    }
    
    assert itens_estado(6) == {
        ("<F>", ("(", "<T>", ")"), 2), ("<T>", ("<T>", "*", "<F>"), 1)
    }
    
    assert itens_estado(7) == {
        ("<T>", ("<T>", "*", "<F>"), 3)
    }

    assert itens_estado(8) == {
        ("<F>", ("(", "<T>", ")"), 3)
    }
    
    assert automato.transicoes[(0, "<T>")] == 1
    assert automato.transicoes[(0, "<F>")] == 2
    assert automato.transicoes[(0, "id")] == 3
    assert automato.transicoes[(0, "(")] == 4
    assert automato.transicoes[(1, "*")] == 5
    assert automato.transicoes[(4, "<F>")] == 2
    assert automato.transicoes[(4, "id")] == 3
    assert automato.transicoes[(4, "(")] == 4
    assert automato.transicoes[(4, "<T>")] == 6
    assert automato.transicoes[(5, "id")] == 3
    assert automato.transicoes[(5, "(")] == 4
    assert automato.transicoes[(5, "<F>")] == 7
    assert automato.transicoes[(6, ")")] == 8
    assert automato.transicoes[(6, "*")] == 5
