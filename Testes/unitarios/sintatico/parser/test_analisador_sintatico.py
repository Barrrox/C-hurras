import pytest
from automato import AutomatoLR0
from construtor_tabelaSLR import ConstrutorTabelaSLR
from analisador_sintatico import ParserSLR
from Token import Token
from gramatica import Gramatica

# Mock para facilitar o teste sem depender de arquivos físicos
class ParserMock(ParserSLR):
    def __init__(self, gramatica: Gramatica, automato: AutomatoLR0):
        self.producoes = gramatica.producoes
        self.simbolos = gramatica.simbolos
        self.gramatica = gramatica
        self.automato = automato
        
    def criar_tabelaSLR(self) -> list[list['SLRcell']]:
        tabelador = ConstrutorTabelaSLR()
        tabelador.construir_tabelaSLR(self.gramatica, self.automato)
        return tabelador.tabelaSLR

def criar_tokens(lista_str):
    tokens = []
    for s in lista_str:
        tokens.append(Token(texto=s, categoria=s, linha=1))
    tokens.append(Token(texto="$", categoria="$", linha=1))
    return tokens

def test_parser_gramatica5_aceita_valido(gramatica5: Gramatica):
    automato = AutomatoLR0(gramatica5)
    automato.gerar_automato(gramatica5)
    parser = ParserMock(gramatica5, automato)
    
    # (id)*id = aceita
    tokens = criar_tokens(["(", "id", ")", "*", "id"])
    resultado = parser.analisar_sintaxe(tokens)
    assert resultado is True

def test_parser_gramatica5_recupera_erro_parentese(gramatica5: Gramatica):
    automato = AutomatoLR0(gramatica5)
    automato.gerar_automato(gramatica5)
    parser = ParserMock(gramatica5, automato)
    
    # (id*id = rejeita mas passa pelo modo pânico (retorna False por ter erros)
    tokens = criar_tokens(["(", "id", "*", "id"])
    resultado = parser.analisar_sintaxe(tokens)
    assert resultado is False

def test_parser_gramatica5_recupera_erro_parentese_fechando(gramatica5: Gramatica):
    automato = AutomatoLR0(gramatica5)
    automato.gerar_automato(gramatica5)
    parser = ParserMock(gramatica5, automato)
    
    # id)**id = rejeita mas passa pelo modo pânico
    tokens = criar_tokens(["id", ")", "*", "*", "id"])
    resultado = parser.analisar_sintaxe(tokens)
    assert resultado is False

def test_parser_gramatica6_aceita_valido(gramatica6: Gramatica):
    automato = AutomatoLR0(gramatica6)
    automato.gerar_automato(gramatica6)
    parser = ParserMock(gramatica6, automato)
    
    # [[a;a]] = aceita
    tokens = criar_tokens(["[", "[", "a", ";", "a", "]", "]"])
    resultado = parser.analisar_sintaxe(tokens)
    assert resultado is True

def test_parser_gramatica6_recupera_erro_incompleto(gramatica6: Gramatica):
    automato = AutomatoLR0(gramatica6)
    automato.gerar_automato(gramatica6)
    parser = ParserMock(gramatica6, automato)
    
    # [a;] = rejeita mas passa pelo modo pânico
    tokens = criar_tokens(["[", "a", ";", "]"])
    resultado = parser.analisar_sintaxe(tokens)
    assert resultado is False
