# classe para representar token
class Token:
    def __init__(self, texto : str, categoria : str, linha : int):
        self.texto = texto  # string do token
        self.categoria = categoria    # categoria/tipo do token (se eh operação, delimitador, etc)
        self.linha = linha  # numero da linha (para escrever as mensagens de erro)

    def tkprint(self):
        print("token:", self.texto, "| categoria:", self.categoria, "| linha:", self.linha)
