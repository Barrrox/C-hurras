import pytest
from analisador_lexico import analisar_lexico

# ==========================================
# Como os teste funcionam?
# ==========================================

# Função auxiliar para garantir o fechamento de tokens que dependem do lookahead
def analisar(codigo):
    return analisar_lexico(codigo + " ")

# ==========================================
# TESTES DE SUCESSO (Separados por Tipo)
# ==========================================

@pytest.mark.parametrize("entrada", ["123", "0", "9999"])
def test_tipo_inteiro(entrada):
    tokens = analisar(entrada)
    assert len(tokens) == 1
    assert tokens[0].tipo == "int"
    assert tokens[0].texto == entrada

@pytest.mark.parametrize("entrada", ["minha_var", "_var2", "variavel_123"])
def test_tipo_identificador(entrada):
    tokens = analisar(entrada)
    assert len(tokens) == 1
    assert tokens[0].tipo == "id"
    assert tokens[0].texto == entrada

@pytest.mark.parametrize("entrada", [
    "vaca", "frango", "porco", "rodizio", "grelhar", 
    "ta_no_ponto?", "queimou", "ponto_certo", "queimado", 
    "espetar", "servir", "servido"
])
def test_tipo_palavra_reservada(entrada):
    tokens = analisar(entrada)
    assert len(tokens) == 1
    # O tipo da palavra reservada é o próprio texto dela (conforme seu estado 5)
    assert tokens[0].tipo == entrada 
    assert tokens[0].texto == entrada

@pytest.mark.parametrize("entrada", [
    "-", "+", "*", "/", "%",  # Aritméticos
    "&&", "||",               # Lógicos
    "==", "!=", "<=", ">=", "=", "<", ">" # Relacionais e Atribuição
])
def test_tipo_operador(entrada):
    tokens = analisar(entrada)
    assert len(tokens) == 1
    assert tokens[0].tipo == "op"
    assert tokens[0].texto == entrada

@pytest.mark.parametrize("entrada", ["'a'", "' '", "'1'"])
def test_tipo_char(entrada):
    tokens = analisar(entrada)
    assert len(tokens) == 1
    assert tokens[0].tipo == "char"
    assert tokens[0].texto == entrada

@pytest.mark.parametrize("entrada", ['"churrasco"', '"a b c"'])
def test_tipo_string(entrada):
    tokens = analisar(entrada)
    assert len(tokens) == 1
    # Nota: No seu código, no estado 19, você definiu o tipo como "string" (ou "char" na versão original). 
    # Assumindo que você corrigiu para "string" conforme meu exemplo anterior.
    assert tokens[0].tipo == "string" 
    assert tokens[0].texto == entrada

@pytest.mark.parametrize("entrada", [",", ";", "{", "}"])
def test_tipo_delimitador(entrada):
    tokens = analisar(entrada)
    assert len(tokens) == 1
    # O tipo do delimitador é o próprio caractere
    assert tokens[0].tipo == entrada 
    assert tokens[0].texto == entrada

# ==========================================
# TESTES DE IGNORADOS (Espaços e Comentários)
# ==========================================

def test_ignora_espacos_e_quebras():
    tokens = analisar_lexico(" \n \t \n")
    assert len(tokens) == 0

def test_ignora_comentarios():
    tokens = analisar_lexico("--< isso é um comentario \n multilinhas >-")
    assert len(tokens) == 0

# ==========================================
# TESTES DE FALHA (Erros Léxicos)
# ==========================================

@pytest.mark.parametrize("entrada_invalida", [
    "--?",    # Comentário mal aberto
    "''",     # Char vazio
    '""',     # String vazia
    "'\n'",   # Char com quebra de linha
    "'a",     # Char não fechado
    '"\n"',   # String com quebra de linha sem fechar
    "& ",     # AND incompleto
    "| ",     # OR incompleto
    "@",      # Caractere inválido
])
def test_erros_lexicos_encerram_programa(entrada_invalida):
    # Verifica se o programa chama exit(0) ao encontrar erro
    with pytest.raises(SystemExit):
        analisar(entrada_invalida)