import pytest
from gramatica import Gramatica
from testes.unitarios.sintatico.conftest import GramaticaMock

def test_get_simbolos():
    
    # Criamos uma gramática mockada seguindo a regra da linguagem (< > para não-terminais)
    producoes_mock = (
        ("<chs>", ("<churras>", "id")),
        ("<churras>", ("+", "<outro>")),
        ("<churras>", ("<", "id", ">", "<outro>")),
        ("<outro>", ()) # Simula uma produção vazia
    )
    
    gramatica = GramaticaMock(producoes_mock)
    
    # Executa a função
    dicionario_simbolos = gramatica.get_simbolos()
    
    # 1. Testa se os conjuntos foram preenchidos corretamente
    assert gramatica.nao_terminais == {"<chs>", "<churras>", "<outro>"}
    assert gramatica.terminais == {"id", "+", "<", ">"}
    
    # 2. Testa se o dicionário manteve a ordem certa (Não-terminais primeiro, e <chs> em index 0)
    assert dicionario_simbolos["<chs>"] == 0
    assert dicionario_simbolos["<churras>"] == 1
    assert dicionario_simbolos["<outro>"] == 2
    assert dicionario_simbolos["id"] == 3
    assert dicionario_simbolos["+"] == 4
    
    # 3. Testa se o vazio () não entrou em lugar nenhum, como esperado
    assert "" not in dicionario_simbolos
    assert () not in dicionario_simbolos


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