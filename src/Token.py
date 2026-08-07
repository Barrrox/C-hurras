# classe para representar token
class Token:
    def __init__(self, texto : str, categoria : str, linha : int) -> None:
        self.texto : str = texto  # string do token
        self.categoria : str = categoria    # categoria/tipo do token (se eh operação, delimitador, etc)
        self.linha  : int = linha  # numero da linha (para escrever as mensagens de erro)

    def tkprint(self) -> None:
        print("token:", self.texto, "| categoria:", self.categoria, "| linha:", self.linha)
