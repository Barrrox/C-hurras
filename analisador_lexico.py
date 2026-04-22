# a única biblioteca externa pra receber argumento de linha de comando
import sys

# variaveis globais
reservadas = ["vaca", "frango", "porco", "rodizio", "grelhar", "ta_no_ponto?", "queimou", "ponto_certo", "queimado", "espetar", "servir", "servido"]

# classe para representar token
class token:
    def __init__(self, texto, tipo, linha):
        self.texto = texto  # string do token
        self.tipo = tipo    # tipo do token (se eh operação, delimitador, etc)
        self.linha = linha  # numero da linha (para escrever as mensagens de erro)

    def tkprint(self):
        print("token:", self.texto, "| tipo:", self.tipo, "| linha:", self.linha)


# 1. le o arquivo de código e retorna como um vetor de caracteres
def abrir_codigo(filename):
    with open(filename, "r") as arquivo:
        codigo = arquivo.read()
    return codigo


#
# Analisador léxico
#

# retorna verdadeiro se char é digito
def eh_digito(caractere):
    if caractere >= '0' and caractere <= '9':
        return True
    else:
        return False


# retorna verdadeiro se char é letra maiuscula ou minuscula
def eh_letra(caractere):
    if (caractere >= 'a' and caractere <= 'z') or (caractere >= 'A' and caractere <= 'Z'):
        return True
    else:
        return False


# imprime mensagem de erro e sai do programa
def erro_lexico(msg):
    print(msg)
    exit(0)


# retorna vetor com a relação entre char atual e linha de código
def relacao_linha_char(codigo):
    relacao = []
    for i in range(len(codigo)):
        if codigo[i] == '\n':
            relacao.append(i)
    return relacao


# define em qual linha do código está um char
def linha_char(posicao, relacao):
    linha = 0
    for idx in relacao:
        if idx < posicao:
            linha += 1
        else:
            break
    return linha


# função do analisador léxico, se bem sucedida, retorna lista de tokens
def analisar_lexico(codigo):
    # você não viu nada aqui....
    codigo += "  "

    # representa token sendo lendo atualmente
    char_atual = ''
    token_atual = ""

    # utilidades para identificar em qual linha o programa está
    relacao = relacao_linha_char(codigo)

    # token gerados
    tokens = []

    # ponteiro de código que vai varrer o mesmo
    pc = 0

    # variaveis do automatão
    estado = 1

    # E QUE COMECEM OS JOGOS!
    while pc < len(codigo):
        char_atual = codigo[pc]
        token_atual += char_atual

        linha_atual = linha_char(pc, relacao) + 1

        match estado:
            # estado inicial
            case 1:
                if eh_digito(char_atual):
                    estado = 2
                elif eh_letra(char_atual) or char_atual == '_':
                    estado = 4
                elif char_atual == '-':
                    estado = 6
                elif char_atual == ' ':
                    estado = 11
                elif char_atual == '\t':
                    estado = 11
                elif char_atual == '\n':
                    estado = 11
                elif char_atual == '\'':
                    estado = 12
                elif char_atual == '\"':
                    estado = 16
                elif char_atual == '+' or char_atual == '/' or char_atual == '%' or char_atual == '*':
                    estado = 23
                elif char_atual == '&':
                    estado = 20
                elif char_atual == '|':
                    estado = 21
                elif char_atual == '=' or char_atual == '!' or char_atual == '<' or char_atual == '>':
                    estado = 22
                elif char_atual == ',':
                    estado = 25
                elif char_atual == ';':
                    estado = 26
                elif char_atual == '{':
                    estado = 27
                elif char_atual == '}':
                    estado = 28
                elif char_atual == '(':
                    estado = 29
                elif char_atual == ')':
                    estado = 30
                else:
                    estado = 31

            #
            # Identificação de inteiros
            #
            case 2:
                if not eh_digito(char_atual):
                    estado = 3
            case 3:
                token_atual = token_atual[:-2]
                tokens.append(token(token_atual, "int", linha_atual))

                token_atual = ""
                pc -= 2
                estado = 1

            #
            # Identificação de ID ou reservadas
            #
            case 4:
                # Se é diferente de digito, letra ou _ então passa de estado
                if not (eh_digito(char_atual) or eh_letra(char_atual) or char_atual == "_" or char_atual == "?"):
                    estado = 5

                # falta lidar com erro aqui

            case 5:
                token_atual = token_atual[:-2]  #

                if token_atual in reservadas:
                    tokens.append(token(token_atual, token_atual, linha_atual))
                else:
                    tokens.append(token(token_atual, "id", linha_atual))

                token_atual = ""
                pc -= 2
                estado = 1

            #
            # Comentários
            #
            case 6:
                if not char_atual == "-":
                    estado = 7
                elif char_atual == "-":
                    estado = 8
            #
            # Operador "-"
            #
            case 7:
                token_atual = token_atual[:-2]
                tokens.append(token(token_atual, "op", linha_atual))

                token_atual = ""
                pc -= 2
                estado = 1

            case 8:
                if char_atual == "<":
                    estado = 9
                else:
                    erro_lexico("ERRO:\n\tComentário mal aberto na linha " + str(linha_atual) + ". Você quis dizer:\n\t\t--<")
            case 9:
                if char_atual == ">":
                    estado = 10
            case 10:
                if not char_atual == "-":
                    estado = 9
                else:
                    estado = 11
            case 11:
                token_atual = ""
                pc -= 1
                estado = 1

            # Caractere
            case 12:
                if char_atual == '\'':
                    estado = 13
                elif char_atual == '\n':
                    estado = 13
                else:
                    estado = 14
            case 13:
                erro_lexico("ERRO: caractere vazio na linha " + str(linha_atual))
            case 14:
                if not char_atual == '\'':
                    token_atual = token_atual[:-1]
                    erro_lexico("ERRO: caractere não fechado na linha " + str(linha_atual) + ". Você quis dizer:\n\t" + str(token_atual) + "\'")
                else:
                    estado = 15
            case 15:
                token_atual = token_atual[:-1]
                tokens.append(token(token_atual, "char", linha_atual))
                token_atual = ""
                estado = 1
                pc -= 1

            # String
            case 16:
                if char_atual == '\"':
                    estado = 17
                elif char_atual == '\n':
                    estado = 17
                else:
                    estado = 18
            case 17:
                erro_lexico("ERRO: string vazia ou inválida na linha " + str(linha_atual))
            case 18:
                if char_atual == '\"':
                    estado = 19
                elif char_atual == '\n':
                    estado = 17
            case 19:
                token_atual = token_atual[:-1]
                tokens.append(token(token_atual, "string", linha_atual))
                token_atual = ""
                estado = 1
                pc -= 1

            # Operador "&&"
            case 20:
                if char_atual == '&':
                    estado = 23
                else:
                    erro_lexico("ERRO: Operador AND é: && na linha " + str(linha_atual))
            # Operador "||"
            case 21:
                if char_atual == '|':
                    estado = 23
                else:
                    erro_lexico("ERRO: Operador OR é: || na linha " + str(linha_atual))

            # Operadores "==", "!=", "<", ">", "<=", ">="
            case 22:
                if char_atual == '=':
                    estado = 23
                else:
                    estado = 24
            case 23:
                token_atual = token_atual[:-1]
                tokens.append(token(token_atual, "op", linha_atual))
                token_atual = ""
                estado = 1
                pc -= 1
            case 24:
                token_atual = token_atual[:-2]
                tokens.append(token(token_atual, "op", linha_atual))

                token_atual = ""
                pc -= 2
                estado = 1

            # Separador
            case 25:
                token_atual = token_atual[:-1]
                tokens.append(token(token_atual, ",", linha_atual))
                token_atual = ""
                estado = 1
                pc -= 1

            # Fim de linha
            case 26:
                token_atual = token_atual[:-1]
                tokens.append(token(token_atual, ";", linha_atual))
                token_atual = ""
                estado = 1
                pc -= 1

            # Inicio de bloco
            case 27:
                token_atual = token_atual[:-1]
                tokens.append(token(token_atual, "{", linha_atual))
                token_atual = ""
                estado = 1
                pc -= 1

            # Fim de bloco
            case 28:
                token_atual = token_atual[:-1]
                tokens.append(token(token_atual, "}", linha_atual))
                token_atual = ""
                estado = 1
                pc -= 1

            # (
            case 29:
                token_atual = token_atual[:-1]
                tokens.append(token(token_atual, "(", linha_atual))
                token_atual = ""
                estado = 1
                pc -= 1

            # )
            case 30:
                token_atual = token_atual[:-1]
                tokens.append(token(token_atual, ")", linha_atual))
                token_atual = ""
                estado = 1
                pc -= 1

            # Caractere inválido
            case 31:
                erro_lexico("ERRO: caractere inválido '" + char_atual + "' na linha " + str(linha_atual))

            # Caso padrão
            case _:
                erro_lexico("ERRO: meu amigo, tem alguma coisa de errado aqui")

        # Incrementa o ponteiro
        pc += 1

    # encerrou analise de forma correta, retornar tokens
    return tokens


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERRO: arquivo não informado, use o analisador como:\n\tpython analisador_lexico.py codigo.churras")
    else:
        codigo = abrir_codigo(sys.argv[1])
        tks = analisar_lexico(codigo)
        for tk in tks:
            tk.tkprint()