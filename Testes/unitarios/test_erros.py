import pytest
import analisador_lexico
from testes.utils import executar_lexico, verificar_erro_lexico

def test_ignora_espacos_e_quebras():
    tokens = executar_lexico(" \n \t \n")
    assert len(tokens) == 0

def test_ignora_comentarios():
    tokens = executar_lexico("--< isso é um comentario \n multilinhas >-")
    assert len(tokens) == 0

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
    verificar_erro_lexico(entrada_invalida)
