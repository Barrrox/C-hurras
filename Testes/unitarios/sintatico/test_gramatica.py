import pytest
from gramatica import Gramatica
from testes.unitarios.sintatico.conftest import GramaticaMock

def test_get_simbolos():
    
    # Criamos uma gramática mockada seguindo a regra da linguagem (< > para não-terminais)
    producoes_mock = (
        ("<chs>", ("<churras>", "id")),
        ("<churras>", ("+", "<outro>")),
        ("<churras>", ("<", "id", ">", "<outro>")),
        ("<outro>", (())) # Simula uma produção vazia
    )
    
    gramatica = GramaticaMock(producoes_mock)
    
    # Executa a função
    dicionario_simbolos = gramatica.get_simbolos()
    
    # 1. Testa se os conjuntos foram preenchidos corretamente
    assert gramatica.nao_terminais == ["<chs>", "<churras>", "<outro>"]
    assert gramatica.terminais == ["id", "+", "<", ">"]
    
    # 2. Testa se o dicionário manteve a ordem certa (Não-terminais primeiro, e <chs> em index 0)
    assert dicionario_simbolos["<chs>"] == 0
    assert dicionario_simbolos["<churras>"] == 1
    assert dicionario_simbolos["<outro>"] == 2
    assert dicionario_simbolos["$"] == 3
    assert dicionario_simbolos["id"] == 4
    assert dicionario_simbolos["+"] == 5
    
    # 3. Testa se o vazio () não entrou em lugar nenhum, como esperado
    assert "" not in dicionario_simbolos
    assert () not in dicionario_simbolos


def test_calcular_first_gramatica1(gramatica1 : Gramatica):
    # Gramática:
    # <E> → <E> + <T> | <T>
    # <T> → id

    first = gramatica1.calcular_conjunto_first()

    # FIRST(<E>) = { (, id }  — <E> deriva <T> deriva <F> deriva ( <E> ) | id
    assert set(first['<E>']) == {'id'}

    # FIRST(<T>) = { (, id }  — <T> deriva <F> deriva ( <E> ) | id
    assert set(first['<T>']) == {'id'}

def test_calcular_first_gramatica2(gramatica2 : Gramatica):
    # Gramática:
    # <E> → <E> + <T> | <T>
    # <T> → <T> * <F> | <F>
    # <F> → ( <E> ) | id

    first = gramatica2.calcular_conjunto_first()

    # FIRST(<E>) = { (, id }  — <E> deriva <T> deriva <F> deriva ( <E> ) | id
    assert set(first['<E>']) == {'(', 'id'}

    # FIRST(<T>) = { (, id }  — <T> deriva <F> deriva ( <E> ) | id
    assert set(first['<T>']) == {'(', 'id'}

    # FIRST(<F>) = { (, id }  — produções diretas
    assert set(first['<F>']) == {'(', 'id'}

def test_calcular_first_gramatica3(gramatica3 : Gramatica):
    # Gramática:
    # E → T | T a | b | ε | F
    # F → ε
    # ε é representado como () (tupla vazia)

    first = gramatica3.calcular_conjunto_first()

    # FIRST(F) = { ε }  — única produção é F → ε
    assert set(first['<F>']) == {()}

    # FIRST(E) = { T, b, ε }
    #   E → T     → T é terminal → T entra
    #   E → T a   → T é terminal → T entra (já está)
    #   E → b     → b entra
    #   E → ε     → ε entra
    #   E → F     → FIRST(F)-{ε} = {} → nada entra; F deriva ε e é último símbolo → ε entra (já está)
    assert set(first['<E>']) == {'<T>', 'b', ()}

def test_calcular_first_gramatica4(gramatica4 : Gramatica):
    # Gramática:
    # E  → T E2
    # E2 → v T E2 | ε
    # T  → F T2
    # T2 → a F T2
    # F  → n F | id

    first = gramatica4.calcular_conjunto_first()

    # FIRST(F) = { n, id }
    assert set(first['<F>']) == {'n', 'id'}

    # FIRST(T2) = { a }  — única produção, a é terminal
    assert set(first['<T2>']) == {'a'}

    # FIRST(T) = { n, id }  — T → F T2; F não deriva ε, usa só FIRST(F)
    assert set(first['<T>']) == {'n', 'id'}

    # FIRST(E2) = { v, ε }
    #   E2 → v T E2 → v é terminal → v entra
    #   E2 → ε      → ε entra
    assert set(first['<E2>']) == {'v', ()}

    # FIRST(E) = { n, id }  — E → T E2; T não deriva ε, usa só FIRST(T)
    assert set(first['<E>']) == {'n', 'id'}

# def test_calcular_follow(gramatica2 : Gramatica):
#     # Gramática:
#     # <E> → <E> + <T> | <T>
#     # <T> → <T> * <F> | <F>
#     # <F> → ( <E> ) | id

#     follow = gramatica2.calcular_follow()

#     # FOLLOW(<E>) = { +, ), $ }  — <E> é símbolo inicial e aparece em <F> → ( <E> )
#     assert set(follow["<E>"]) == {"+", ")", "$"}

#     # FOLLOW(<T>) = { +, *, ), $ }  — <T> aparece em <E> → <E> + <T> e em <T> → <T> * <F>
#     assert set(follow["<T>"]) == {"+", "*", ")", "$"}

#     # FOLLOW(<F>) = { +, *, ), $ }  — <F> aparece em <T> → <T> * <F>, herda FOLLOW(<T>)
#     assert set(follow["<F>"]) == {"+", "*", ")", "$"}