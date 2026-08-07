from Token import Token
import os

class Lexer():
    # variaveis globais (agora como atributos de classe)
    RESERVADAS : list[str] = [
        "vaca", "frango", "porco", "rodizio", "grelhar", "ta_no_ponto?",
        "queimou", "ponto_certo", "queimado", "espetar", "servir", "servido"
    ]
    TIPOS_VARIAVEIS : list[str] = ["vaca", "frango", "porco"]

    def __init__(self) -> None:
        """Classe Lexer gerencia o processo de análise léxica.
        """
        self.pc: int = 0 # Ponteiro de char para a leitura do código
        self.tokens : list[Token] = []  # Lista com os tokens

    # imprime mensagem de erro e sai do programa
    def _erro_lexico(self, msg: str) -> None:
        print(msg)
        exit(0)

    # retorna vetor com a relação entre char atual e linha de código
    def _relacao_linha_char(self, codigo: str) -> list[int]:
        relacao = []
        for i in range(len(codigo)):
            if codigo[i] == '\n':
                relacao.append(i)
        return relacao

    # define em qual linha do código está um char
    def _linha_char(self, posicao: int, relacao: list[int]) -> int:
        linha = 0
        for idx in relacao:
            if idx < posicao:
                linha += 1
            else:
                break
        return linha

    def analisar_lexico(self, codigo: str) -> list[Token]:
        """Interface para executar o verdadeiro analisador lexico. Retorna a lista de tokens

        Args:
            codigo (string): string de caracteres 

        Returns:
            list[Token]: Lista com os tokens
        """

        lista_tokens = self.analisar_lexico_aux(codigo)
        self.print_tokens()
        self.salvar_tokens()

        return lista_tokens

    # função do analisador léxico, se bem sucedida, retorna lista de tokens
    def analisar_lexico_aux(self, codigo: str) -> list[Token]:
        """Executa a análise léxica do código fonte utilizando um autômato de estados finito.

        O método percorre o código caractere por caractere, realizando transições entre estados
        nomeados para identificar tokens como identificadores, números, strings e operadores.

        Returns:
            list[Token]: Uma lista de objetos Token.
        """
        codigo += "  "

        # representa token sendo lendo atualmente
        char_atual = ''
        token_atual = ""

        # utilidades para identificar em qual linha o programa está
        relacao = self._relacao_linha_char(codigo)

        # mapeamento de estados
        ESTADO_INICIAL = "ESTADO_INICIAL"
        LENDO_NUMERO = "LENDO_NUMERO"
        ACEITA_NUMERO = "ACEITA_NUMERO"
        LENDO_ID_RESERV = "LENDO_ID_RESERV"
        ACEITA_ID_RESERV = "ACEITA_ID_RESERV"
        LEU_MENOS = "LEU_MENOS"
        ACEITA_OP_MENOS = "ACEITA_OP_MENOS"
        LEU_DOIS_MENOS = "LEU_DOIS_MENOS"
        LENDO_COMENTARIO = "LENDO_COMENTARIO"
        LEU_FECHA_COMENTARIO = "LEU_FECHA_COMENTARIO"
        ACEITA_ESPACO = "ACEITA_ESPACO"
        LEU_ASPAS_SIMPLES = "LEU_ASPAS_SIMPLES"
        ERRO_CARACTERE_VAZIO = "ERRO_CARACTERE_VAZIO"
        LENDO_CARACTERE = "LENDO_CARACTERE"
        ACEITA_CARACTERE = "ACEITA_CARACTERE"
        LEU_ASPAS_DUPLAS = "LEU_ASPAS_DUPLAS"
        ERRO_STRING_VAZIA = "ERRO_STRING_VAZIA"
        LENDO_STRING = "LENDO_STRING"
        ACEITA_STRING = "ACEITA_STRING"
        LEU_E_COMERCIAL = "LEU_E_COMERCIAL"
        LEU_BARRA_VERTICAL = "LEU_BARRA_VERTICAL"
        LEU_OP_SIMPLES = "LEU_OP_SIMPLES"
        ACEITA_OPERADOR = "ACEITA_OPERADOR"
        ACEITA_IGUAL = "ACEITA_IGUAL"
        ACEITA_VIRGULA = "ACEITA_VIRGULA"
        ACEITA_PONTO_VIRGULA = "ACEITA_PONTO_VIRGULA"
        ACEITA_ABRE_CHAVE = "ACEITA_ABRE_CHAVE"
        ACEITA_FECHA_CHAVE = "ACEITA_FECHA_CHAVE"
        ACEITA_ABRE_PAR = "ACEITA_ABRE_PAR"
        ACEITA_FECHA_PAR = "ACEITA_FECHA_PAR"
        ERRO_CARACTERE_INV = "ERRO_CARACTERE_INV"

        # variavel do automatão
        estado = ESTADO_INICIAL

        # E QUE COMECEM OS JOGOS!
        while self.pc < len(codigo):
            char_atual = codigo[self.pc]
            token_atual += char_atual

            linha_atual = self._linha_char(self.pc, relacao) + 1

            match estado:
                # estado inicial
                case "ESTADO_INICIAL":
                    if char_atual.isdigit():
                        estado = LENDO_NUMERO
                    elif char_atual.isalpha() or char_atual == '_':
                        estado = LENDO_ID_RESERV
                    elif char_atual == '-':
                        estado = LEU_MENOS
                    elif char_atual in [' ', '\t', '\n']:
                        estado = ACEITA_ESPACO
                    elif char_atual == '\'':
                        estado = LEU_ASPAS_SIMPLES
                    elif char_atual == '\"':
                        estado = LEU_ASPAS_DUPLAS
                    elif char_atual in ['+', '/', '%', '*']:
                        estado = ACEITA_OPERADOR
                    elif char_atual == '&':
                        estado = LEU_E_COMERCIAL
                    elif char_atual == '|':
                        estado = LEU_BARRA_VERTICAL
                    elif char_atual in ['=', '!', '<', '>']:
                        estado = LEU_OP_SIMPLES
                    elif char_atual == ',':
                        estado = ACEITA_VIRGULA
                    elif char_atual == ';':
                        estado = ACEITA_PONTO_VIRGULA
                    elif char_atual == '{':
                        estado = ACEITA_ABRE_CHAVE
                    elif char_atual == '}':
                        estado = ACEITA_FECHA_CHAVE
                    elif char_atual == '(':
                        estado = ACEITA_ABRE_PAR
                    elif char_atual == ')':
                        estado = ACEITA_FECHA_PAR
                    else:
                        estado = ERRO_CARACTERE_INV

                #
                # Identificação de inteiros
                #
                case "LENDO_NUMERO":
                    if not char_atual.isdigit():
                        estado = ACEITA_NUMERO
                case "ACEITA_NUMERO":
                    token_atual = token_atual[:-2]
                    self.tokens.append(Token(token_atual, "int", linha_atual))

                    token_atual = ""
                    self.pc -= 2
                    estado = ESTADO_INICIAL

                #
                # Identificação de ID ou reservadas
                #
                case "LENDO_ID_RESERV":
                    # Se é diferente de digito, letra ou _ então passa de estado
                    if not (char_atual.isdigit() or char_atual.isalpha() or char_atual == "_" or char_atual == "?"):
                        estado = ACEITA_ID_RESERV

                case "ACEITA_ID_RESERV":
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
                    estado = ESTADO_INICIAL

                #
                # Comentários (--< ... >--)
                #
                case "LEU_MENOS":
                    if not char_atual == "-":
                        estado = ACEITA_OP_MENOS
                    elif char_atual == "-":
                        estado = LEU_DOIS_MENOS

                #
                # Operador "-"
                #
                case "ACEITA_OP_MENOS": 
                    
                    token_atual = token_atual[:-2]
                    self.tokens.append(Token(token_atual, token_atual, linha_atual))

                    token_atual = ""
                    self.pc -= 2
                    estado = ESTADO_INICIAL

                case "LEU_DOIS_MENOS":
                    if char_atual == "<":
                        estado = LENDO_COMENTARIO
                    else:
                        self._erro_lexico("ERRO:\n\tComentário mal aberto na linha " + str(linha_atual) + ". Você quis dizer:\n\t\t--<")
                case "LENDO_COMENTARIO":
                    if char_atual == ">":
                        estado = LEU_FECHA_COMENTARIO
                case "LEU_FECHA_COMENTARIO":
                    if not char_atual == "-":
                        estado = LENDO_COMENTARIO
                    else:
                        estado = ACEITA_ESPACO
                case "ACEITA_ESPACO":
                    token_atual = ""
                    self.pc -= 1
                    estado = ESTADO_INICIAL

                # Caracteres ('a')
                case "LEU_ASPAS_SIMPLES":
                    if char_atual == '\'':
                        estado = ERRO_CARACTERE_VAZIO
                    elif char_atual == '\n':
                        estado = ERRO_CARACTERE_VAZIO
                    else:
                        estado = LENDO_CARACTERE
                case "ERRO_CARACTERE_VAZIO":
                    self._erro_lexico("ERRO: caractere vazio na linha " + str(linha_atual))
                case "LENDO_CARACTERE":
                    if not char_atual == '\'':
                        token_atual = token_atual[:-1]
                        self._erro_lexico("ERRO: caractere não fechado na linha " + str(linha_atual) + ". Você quis dizer:\n\t" + str(token_atual) + "\'")
                    else:
                        estado = ACEITA_CARACTERE
                case "ACEITA_CARACTERE":
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "char", linha_atual))
                    token_atual = ""
                    estado = ESTADO_INICIAL
                    self.pc -= 1

                # Strings ("churrasco")
                case "LEU_ASPAS_DUPLAS":
                    if char_atual == '\"':
                        estado = ERRO_STRING_VAZIA
                    elif char_atual == '\n':
                        estado = ERRO_STRING_VAZIA
                    else:
                        estado = LENDO_STRING
                case "ERRO_STRING_VAZIA":
                    self._erro_lexico("ERRO: string vazia ou inválida na linha " + str(linha_atual))
                case "LENDO_STRING":
                    if char_atual == '\"':
                        estado = ACEITA_STRING
                    elif char_atual == '\n':
                        estado = ERRO_STRING_VAZIA
                case "ACEITA_STRING":
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "string", linha_atual))
                    token_atual = ""
                    estado = ESTADO_INICIAL
                    self.pc -= 1

                # Operador "&&"
                case "LEU_E_COMERCIAL":
                    if char_atual == '&':
                        estado = ACEITA_OPERADOR
                    else:
                        self._erro_lexico("ERRO: Operador AND é: && na linha " + str(linha_atual))
                # Operador "||"
                case "LEU_BARRA_VERTICAL":
                    if char_atual == '|':
                        estado = ACEITA_OPERADOR
                    else:
                        self._erro_lexico("ERRO: Operador OR é: || na linha " + str(linha_atual))

                # Lógica de Atribuição e Operadores Relacionais (==, !=, <, >, <=, >=)
                case "LEU_OP_SIMPLES":
                    if char_atual == '=':
                        estado = ACEITA_OPERADOR
                    else:
                        estado = ACEITA_IGUAL
                case "ACEITA_OPERADOR":
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, token_atual, linha_atual))
                    token_atual = ""
                    estado = ESTADO_INICIAL
                    self.pc -= 1
                case "ACEITA_IGUAL":
                    token_atual = token_atual[:-2]
                    self.tokens.append(Token(token_atual, token_atual, linha_atual))

                    token_atual = ""
                    self.pc -= 2
                    estado = ESTADO_INICIAL

                # Lógica de Delimitadores: Vírgula
                case "ACEITA_VIRGULA":
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, ",", linha_atual))
                    token_atual = ""
                    estado = ESTADO_INICIAL
                    self.pc -= 1

                # Lógica de Delimitadores: Ponto e Vírgula
                case "ACEITA_PONTO_VIRGULA":
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, ";", linha_atual))
                    token_atual = ""
                    estado = ESTADO_INICIAL
                    self.pc -= 1

                # Início de bloco: Abre Chave
                case "ACEITA_ABRE_CHAVE":
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "{", linha_atual))
                    token_atual = ""
                    estado = ESTADO_INICIAL
                    self.pc -= 1

                # Fim de bloco: Fecha Chave
                case "ACEITA_FECHA_CHAVE":
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "}", linha_atual))
                    token_atual = ""
                    estado = ESTADO_INICIAL
                    self.pc -= 1

                # (
                case "ACEITA_ABRE_PAR":
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, "(", linha_atual))
                    token_atual = ""
                    estado = ESTADO_INICIAL
                    self.pc -= 1

                # )
                case "ACEITA_FECHA_PAR":
                    token_atual = token_atual[:-1]
                    self.tokens.append(Token(token_atual, ")", linha_atual))
                    token_atual = ""
                    estado = ESTADO_INICIAL
                    self.pc -= 1

                # Erro: Caractere Inválido
                case "ERRO_CARACTERE_INV":
                    self._erro_lexico("ERRO: caractere inválido '" + char_atual + "' na linha " + str(linha_atual))

                # Estado Desconhecido: se chegou aqui é porque deu muuuuito ruim
                case _:
                    self._erro_lexico("ERRO: meu amigo, tem alguma coisa de errado aqui")

            # Incrementa o ponteiro
            self.pc += 1

        # encerrou analise de forma correta, retornar tokens
        return self.tokens

    def print_tokens(self) -> None:
        for tk in self.tokens:
            tk.tkprint()

    def salvar_tokens(self, caminho_saida: str = "output/tokens_saida.txt") -> None:
        """Salva a lista de tokens formatada em um arquivo."""
        try:
            os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
            with open(caminho_saida, "w") as f:
                for tk in self.tokens:
                    f.write(f"token: {tk.texto} | categoria: {tk.categoria} | linha: {tk.linha}\n")
            print(f"Tokens salvos com sucesso em: {caminho_saida}")
        except Exception as e:
            print(f"ERRO ao salvar tokens: {e}")



