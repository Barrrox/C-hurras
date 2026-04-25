# a única biblioteca externa pra receber argumento de linha de comando
import sys

# classe para representar token
class Token:
    def __init__(self, texto, categoria, linha):
        self.texto = texto  # string do token
        self.categoria = categoria    # categoria/tipo do token (se eh operação, delimitador, etc)
        self.linha = linha  # numero da linha (para escrever as mensagens de erro)

    def tkprint(self):
        print("token:", self.texto, "| categoria:", self.categoria, "| linha:", self.linha)


class Lexer():
    # variaveis globais (agora como atributos de classe)
    RESERVADAS = [
        "vaca", "frango", "porco", "rodizio", "grelhar", "ta_no_ponto?",
        "queimou", "ponto_certo", "queimado", "espetar", "servir", "servido"
    ]
    TIPOS_VARIAVEIS = ["vaca", "frango", "porco"]

    def __init__(self, caminho_codigo):
        """Classe Lexer gerencia o processo de análise léxica.

        Args:
            caminho_codigo (str): caminho relativo ou absoluto para o arquivo contendo o código .churras
        """
        self.caminho_codigo = caminho_codigo
        self.codigo = "" # Guardará a string do código bruto todo
        self.pc = 0 # Ponteiro de char para a leitura do código
        self.tokens : list[Token] = []  # Lista com os tokens

    # imprime mensagem de erro e sai do programa
    def _erro_lexico(self, msg):
        print(msg)
        exit(0)

    # retorna vetor com a relação entre char atual e linha de código
    def _relacao_linha_char(self):
        relacao = []
        for i in range(len(self.codigo)):
            if self.codigo[i] == '\n':
                relacao.append(i)
        return relacao

    # define em qual linha do código está um char
    def _linha_char(self, posicao, relacao):
        linha = 0
        for idx in relacao:
            if idx < posicao:
                linha += 1
            else:
                break
        return linha

    # 1. le o arquivo de código e retorna como um vetor de caracteres
    def ler_arquivo(self):
        with open(self.caminho_codigo, "r") as arquivo:
            self.codigo = arquivo.read()
        return self.codigo

    # função do analisador léxico, se bem sucedida, retorna lista de tokens
    def analisar_lexico(self):
        self.codigo += "  "

        # representa token sendo lendo atualmente
        char_atual = ''
        token_atual = ""

        # utilidades para identificar em qual linha o programa está
        relacao = self._relacao_linha_char()

        # variaveis do automatão
        estado = 1

        # E QUE COMECEM OS JOGOS!
        while self.pc < len(self.codigo):
            char_atual = self.codigo[self.pc]
            token_atual += char_atual

            linha_atual = self._linha_char(self.pc, relacao) + 1

            match estado:
                # estado inicial
                case 1:
                    if char_atual.isdigit():
                        estado = 2
                    elif char_atual.isalpha() or char_atual == '_':
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
                    if not char_atual.isdigit():
                        estado = 3
                case 3:
                    token_atual = token_atual[:-2]
                    self.tokens.append(Token(token_atual, "int", linha_atual))

                    token_atual = ""
                    self.pc -= 2
                    estado = 1

                #
                # Identificação de ID ou reservadas
                #
                case 4:
                    # Se é diferente de digito, letra ou _ então passa de estado
                    if not (char_atual.isdigit() or char_atual.isalpha() or char_atual == "_" or char_atual == "?"):
                        estado = 5

                case 5:
                    token_atual = token_atual[:-2]

                    if token_atual in self.RESERVADAS:
                        if token_atual in self.TIPOS_VARIAVEIS:
                            self.tokens.append(Token(token_atual, "tipo", linha_atual))
                        else:
                            self.tokens.append(Token(token_atual, token_atual, linha_atual))
                    else:
                        self.tokens.append(Token(token_atual, "id", linha_atual))

                    token_atual = ""
                    self.pc -= 2
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
                    self.tokens.append(Token(token_atual, "op", linha_atual))

                    token_atual = ""
                    self.pc -= 2
                    estado = 1

                case 8:
                    if char_atual == "<":
                        estado = 9
                    else:
                        self._erro_lexico("ERRO:\n\tComentário mal aberto na linha " + str(linha_atual) + ". Você quis dizer:\n\t\t--<")
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
                    self.pc -= 1
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
                    self._erro_lexico("ERRO: caractere vazio na linha " + str(linha_atual))
                case 14:
                    if not char_atual == '\'':
                        token_atual = token_atual[:-1]
                        self._erro_lexico("ERRO: caractere não fechado na linha " + str(linha_atual) + ". Você quis dizer:\n\t" + str(token_atual) + "\'")
                    else:
                        estado = 15
                case 15:
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "char", linha_atual))
                    token_atual = ""
                    estado = 1
                    self.pc -= 1

                # String
                case 16:
                    if char_atual == '\"':
                        estado = 17
                    elif char_atual == '\n':
                        estado = 17
                    else:
                        estado = 18
                case 17:
                    self._erro_lexico("ERRO: string vazia ou inválida na linha " + str(linha_atual))
                case 18:
                    if char_atual == '\"':
                        estado = 19
                    elif char_atual == '\n':
                        estado = 17
                case 19:
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "string", linha_atual))
                    token_atual = ""
                    estado = 1
                    self.pc -= 1

                # Operador "&&"
                case 20:
                    if char_atual == '&':
                        estado = 23
                    else:
                        self._erro_lexico("ERRO: Operador AND é: && na linha " + str(linha_atual))
                # Operador "||"
                case 21:
                    if char_atual == '|':
                        estado = 23
                    else:
                        self._erro_lexico("ERRO: Operador OR é: || na linha " + str(linha_atual))

                # Operadores "==", "!=", "<", ">", "<=", ">="
                case 22:
                    if char_atual == '=':
                        estado = 23
                    else:
                        estado = 24
                case 23:
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "op", linha_atual))
                    token_atual = ""
                    estado = 1
                    self.pc -= 1
                case 24:
                    token_atual = token_atual[:-2]
                    self.tokens.append(Token(token_atual, "op", linha_atual))

                    token_atual = ""
                    self.pc -= 2
                    estado = 1

                # Separador
                case 25:
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, ",", linha_atual))
                    token_atual = ""
                    estado = 1
                    self.pc -= 1

                # Fim de linha
                case 26:
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, ";", linha_atual))
                    token_atual = ""
                    estado = 1
                    self.pc -= 1

                # Inicio de bloco
                case 27:
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "{", linha_atual))
                    token_atual = ""
                    estado = 1
                    self.pc -= 1

                # Fim de bloco
                case 28:
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "}", linha_atual))
                    token_atual = ""
                    estado = 1
                    self.pc -= 1

                # (
                case 29:
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "(", linha_atual))
                    token_atual = ""
                    estado = 1
                    self.pc -= 1

                # )
                case 30:
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, ")", linha_atual))
                    token_atual = ""
                    estado = 1
                    self.pc -= 1

                # Caractere inválido
                case 31:
                    self._erro_lexico("ERRO: caractere inválido '" + char_atual + "' na linha " + str(linha_atual))

                # Caso padrão
                case _:
                    self._erro_lexico("ERRO: meu amigo, tem alguma coisa de errado aqui")

            # Incrementa o ponteiro
            self.pc += 1

        # encerrou analise de forma correta, retornar tokens
        return self.tokens

    def print_tokens(self):
        for tk in self.tokens:
            tk.tkprint()

    def salvar_tokens(self, caminho_saida="tokens_saida.txt"):
        """Salva a lista de tokens formatada em um arquivo."""
        try:
            with open(caminho_saida, "w") as f:
                for tk in self.tokens:
                    f.write(f"token: {tk.texto} | categoria: {tk.categoria} | linha: {tk.linha}\n")
            print(f"Tokens salvos com sucesso em: {caminho_saida}")
        except Exception as e:
            print(f"ERRO ao salvar tokens: {e}")


def main():
    if len(sys.argv) != 2:
        print("ERRO: arquivo não informado, use o analisador como:\n\tpython analisador_lexico.py codigo.churras")
        return
    
    lexer = Lexer(sys.argv[1])
    lexer.ler_arquivo()
    lexer.analisar_lexico()
    lexer.print_tokens()
    lexer.salvar_tokens()

if __name__ == "__main__":
    main()
