import pytest
from gramatica import Gramatica


def test_calcular_follow(gramatica_simples2 : Gramatica):
    # Gramática:
    # E → E + T | T
    # T → T * F | F
    # F → ( E ) | id

    follow = gramatica_simples2.calcular_follow()

    # FOLLOW(E) = { +, ), $ }  — E é símbolo inicial e aparece em F → ( E )
    assert set(follow["E"]) == {"+", ")", "$"}

    # FOLLOW(T) = { +, *, ), $ }  — T aparece em E → E + T e em T → T * F
    assert set(follow["T"]) == {"+", "*", ")", "$"}

    # FOLLOW(F) = { +, *, ), $ }  — F aparece em T → T * F, herda FOLLOW(T)
    assert set(follow["F"]) == {"+", "*", ")", "$"}