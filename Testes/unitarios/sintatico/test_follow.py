import pytest
from gramatica import Gramatica
from testes.unitarios.sintatico.conftest import GramaticaMock


def test_follow_simbolo_inicial_tem_dolar(gramatica1: Gramatica):
    # Gramatica:
    # <E> -> <E> + <T> | <T>
    # <T> -> id

    follow = gramatica1.calcular_conjunto_follow()

    # Regra 1: simbolo inicial sempre tem $ em seu FOLLOW
    assert "$" in follow["<E>"]


def test_follow_gramatica1(gramatica1: Gramatica):
    # Gramatica:
    # <E> -> <E> + <T> | <T>
    # <T> -> id

    follow = gramatica1.calcular_conjunto_follow()

    # FOLLOW(<E>) = { $, + }
    #   <E> eh simbolo inicial -> $
    #   <E> -> <E> + <T> -> + vem logo apos <E>
    assert set(follow["<E>"]) == {"+", "$"}

    # FOLLOW(<T>) = { $, + }
    #   <E> -> <E> + <T> -> T eh o ultimo simbolo -> herda FOLLOW(<E>) = {+, $}
    #   <E> -> <T>       -> T eh o ultimo simbolo -> herda FOLLOW(<E>) = {+, $}
    assert set(follow["<T>"]) == {"+", "$"}


def test_follow_gramatica2(gramatica2: Gramatica):
    # Gramatica:
    # <E> -> <E> + <T> | <T>
    # <T> -> <T> * <F> | <F>
    # <F> -> ( <E> ) | id

    follow = gramatica2.calcular_conjunto_follow()

    # FOLLOW(<E>) = { $, +, ) }
    #   Simbolo inicial -> $
    #   <F> -> ( <E> ) -> ) vem apos <E>
    #   <E> -> <E> + <T> -> + vem apos <E>
    assert set(follow["<E>"]) == {"+", ")", "$"}

    # FOLLOW(<T>) = { $, +, *, ) }
    #   <E> -> <E> + <T> -> ultimo simbolo -> herda FOLLOW(<E>) = {+, ), $}
    #   <E> -> <T>       -> ultimo simbolo -> herda FOLLOW(<E>) = {+, ), $}
    #   <T> -> <T> * <F> -> * vem apos <T>
    assert set(follow["<T>"]) == {"+", "*", ")", "$"}

    # FOLLOW(<F>) = { $, +, *, ) }
    #   <T> -> <T> * <F> -> ultimo simbolo -> herda FOLLOW(<T>) = {+, *, ), $}
    #   <T> -> <F>       -> ultimo simbolo -> herda FOLLOW(<T>) = {+, *, ), $}
    assert set(follow["<F>"]) == {"+", "*", ")", "$"}


def test_follow_gramatica4(gramatica4: Gramatica):
    # Gramatica:
    # <E>  -> <T> <E2>
    # <E2> -> v <T> <E2> | epsilon
    # <T>  -> <F> <T2>
    # <T2> -> a <F> <T2>
    # <F>  -> n <F> | id

    follow = gramatica4.calcular_conjunto_follow()

    # FOLLOW(<E>) = { $ }
    assert "$" in follow["<E>"]

    # FOLLOW(<E2>) = { $ }
    #   <E>  -> <T> <E2>   -> ultimo simbolo -> herda FOLLOW(<E>) = {$}
    #   <E2> -> v <T> <E2> -> ultimo simbolo -> herda FOLLOW(<E2>) (fixpoint)
    assert set(follow["<E2>"]) == {"$"}

    # FOLLOW(<T>) = { v, $ }
    #   <E>  -> <T> <E2>   -> FIRST(<E2>)-{eps} = {v} + (E2 deriva eps -> FOLLOW(<E>) = {$})
    #   <E2> -> v <T> <E2> -> FIRST(<E2>)-{eps} = {v} + (E2 deriva eps -> FOLLOW(<E2>) = {$})
    assert set(follow["<T>"]) == {"v", "$"}

    # FOLLOW(<F>) = { a, v, $ }
    #   <T> -> <F> <T2> -> FIRST(<T2>)-{eps} = {a}
    #   <F> -> n <F>    -> ultimo simbolo -> herda FOLLOW(<F>) (fixpoint)
    assert set(follow["<F>"]) == {"a", "v", "$"}


def test_follow_nao_terminal_intermediario_herda_contexto():
    # Gramatica minima para testar heranca de FOLLOW via cadeia:
    # <S> -> <A> b
    # <A> -> <B>
    # <B> -> id
    #
    # FOLLOW(<A>) = { b }   -- <S> -> <A> b
    # FOLLOW(<B>) = { b }   -- <A> -> <B> (ultimo), herda FOLLOW(<A>) = {b}

    producoes = (
        ("<S>", ("<A>", "b")),
        ("<A>", ("<B>",)),
        ("<B>", ("id",)),
    )
    g = GramaticaMock(producoes)
    g.simbolos = g.get_simbolos()

    follow = g.calcular_conjunto_follow()

    assert set(follow["<A>"]) == {"b"}
    assert set(follow["<B>"]) == {"b"}


def test_follow_nao_contem_vazio():
    # vazio nunca deve aparecer em nenhum conjunto FOLLOW
    producoes = (
        ("<E>", ("<T>", "<E2>")),
        ("<E2>", ("v", "<T>", "<E2>")),
        ("<E2>", ("~",)),
        ("<T>", ("id",)),
    )
    g = GramaticaMock(producoes)
    g.simbolos = g.get_simbolos()

    follow = g.calcular_conjunto_follow()

    for nao_terminal, conjunto in follow.items():
        assert "~" not in conjunto, f"vazio nao deve estar em FOLLOW({nao_terminal})"
