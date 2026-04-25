import pytest
from analisador_lexico import Lexer

def executar_lexico(codigo):
    """
    Centraliza a chamada ao analisador léxico.
    Cria uma instância da classe Lexer para processar o código fornecido como string.
    """
    lexer = Lexer(None) # Passamos None pois o código será injetado diretamente
    lexer.codigo = codigo
    return lexer.analisar_lexico()

def verificar_erro_lexico(codigo):
    """
    Abstrai a verificação de erro léxico (atualmente via SystemExit).
    """
    with pytest.raises(SystemExit):
        executar_lexico(codigo)

def validar_token(token, texto_esperado, categoria_esperada, linha_esperada=None):
    """
    Função auxiliar para validar um token.
    Centraliza o acesso aos atributos para facilitar refatorações futuras.
    """
    assert token.texto == texto_esperado, f"Esperava texto '{texto_esperado}', mas veio '{token.texto}'"
    assert token.categoria == categoria_esperada, f"Esperava categoria '{categoria_esperada}', mas veio '{token.categoria}'"
    if linha_esperada is not None:
        assert token.linha == linha_esperada, f"Esperava linha {linha_esperada}, mas veio {token.linha}"
