def validar_token(token, texto_esperado, categoria_esperada, linha_esperada=None):
    """
    Função auxiliar para validar um token.
    Centraliza o acesso aos atributos para facilitar refatorações futuras.
    """
    assert token.texto == texto_esperado, f"Esperava texto '{texto_esperado}', mas veio '{token.texto}'"
    assert token.categoria == categoria_esperada, f"Esperava categoria '{categoria_esperada}', mas veio '{token.categoria}'"
    if linha_esperada is not None:
        assert token.linha == linha_esperada, f"Esperava linha {linha_esperada}, mas veio {token.linha}"
